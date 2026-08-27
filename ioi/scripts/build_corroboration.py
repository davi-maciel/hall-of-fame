#!/usr/bin/env python3
"""
Assemble data/corroboration.json and CORROBORATION.md for Brazil at the IOI, in the
repo-standard structured format (same schema as imo/).

Source of truth: data/raw/sources_by_year.json — the curated per-year URL list whose
every entry passed scripts/verify_sources.py (HTTP 200 + Brazilian name present; the
PASS log is data/raw/sources_verified.json). This script only reshapes it: label ->
provenance class, plus coverage defaults. Re-verify anytime with
scripts/verify_corroboration.py.

Provenance classes:
  - "official": stats.ioinformatics.org — the IOI's own statistics database.
  - "primary" : genuinely independent naming sources (OBI/Unicamp national body, press,
                host-year result pages, personal CVs, schools).
  - "archive" : aggregators/mirrors that derive from the IOI database (cphof, clist,
                ioi.te.lv). cphof has known medal-color errors — participation evidence
                only, not medal evidence.
"""
import json
import os
import re
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "data", "raw", "sources_by_year.json")

ARCHIVE_PAT = re.compile(r"aggregator|mirror", re.I)


def classify(label, url):
    if label.startswith("IOI-DB"):
        return "official"
    if ARCHIVE_PAT.search(label):
        return "archive"
    return "primary"


def coverage_for(label, cls):
    # Full-roster sources: the IOI DB, the OBI/Unicamp per-year team lists, and
    # full-standings aggregators. Press/CV/school sources typically name a subset.
    if cls in ("official", "archive") or label.startswith("OBI/Unicamp") or "host results" in label:
        return "full"
    return "partial"


GLOBAL_NOTES = [
 "Every URL passed scripts/verify_sources.py at research time: HTTP 200 + a known Brazilian name for that year present in the fetched content (PASS log: data/raw/sources_verified.json).",
 "cphof medal colors are unreliable (known errors) — cphof entries corroborate participation and roster, not medals.",
 "The OBI/Unicamp page (olimpiada.ic.unicamp.br) is one URL covering every year; it counts once per year as the independent national-body source.",
 "All 27 years were additionally reconciled official-vs-OBI by count, medal multiset, and name: 0 discrepancies.",
 "Liveness check 2026-08-01: 84 PASS + 23 status-only, 1 content miss: ioi2013.org/competition/results is alive (AMT-hosted) but serves its results table via JS/subpages, so the roster is absent from server HTML — checker artifact, not rot.",
]


def main():
    data = json.loads(open(SRC, encoding="utf-8").read())
    years = data["years"]

    records = []
    for y in sorted(years, key=int):
        srcs = []
        for e in years[y]:
            cls = classify(e["source"], e["url"])
            cov = coverage_for(e["source"], cls)
            entry = {
                "url": e["url"],
                "domain": urlparse(e["url"]).netloc.replace("www.", "") or e["url"],
                "cls": cls,
                "coverage": cov,
                "confirms": e["source"],
            }
            if cls == "archive" and "cphof" in e["url"]:
                entry["confirms"] += " — participation/roster only (medal colors unreliable)"
            srcs.append(entry)
        naming = [s for s in srcs if s["cls"] in ("official", "primary", "archive")]
        indep = [s for s in srcs if s["cls"] in ("official", "primary")]
        records.append({
            "year": int(y),
            "namingSourceCount": len(naming),
            "independentPrimaryCount": len(indep),
            "meetsThreeNaming": len(naming) >= 3,
            "meetsThreePrimary": len(indep) >= 3,
            "sources": srcs,
        })

    payload = {
        "olympiadId": "ioi",
        "description": "Independent web sources confirming Brazilian IOI participants + results, per edition.",
        "provenanceClasses": {
            "official": "stats.ioinformatics.org — the IOI's own statistics database.",
            "primary": "Genuinely independent naming sources (OBI/Unicamp national body, press, host results, CVs, schools).",
            "archive": "Aggregators/mirrors deriving from the IOI DB (cphof, clist, ioi.te.lv); cphof = participation evidence only.",
        },
        "globalNotes": GLOBAL_NOTES,
        "years": records,
    }
    with open(os.path.join(ROOT, "data", "corroboration.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")

    lines = []
    for r in records:
        doms = ", ".join(dict.fromkeys(s["domain"] for s in r["sources"]))
        flag = "" if r["namingSourceCount"] >= 3 else "  ⚠️ **<3**"
        lines.append(f"| {r['year']} | {r['namingSourceCount']} | {r['independentPrimaryCount']} | {doms}{flag} |")
    table = "\n".join(lines)

    n3 = sum(1 for r in records if r["meetsThreeNaming"])
    p3 = sum(1 for r in records if r["meetsThreePrimary"])

    details = []
    for r in records:
        details.append(f"### {r['year']}")
        for i, s in enumerate(r["sources"], 1):
            details.append(f"{i}. **{s['domain']}** ({s['cls']}, coverage: {s['coverage']}) — {s['url']} — {s['confirms']}")
        details.append("")
    detail_md = "\n".join(details)

    global_md = "\n".join(f"- {n}" for n in GLOBAL_NOTES)

    md = f"""# Per-Year Corroboration — Independent Sources for Brazil at the IOI

**Machine-readable version:** `data/corroboration.json`. Rebuild with
`python3 scripts/build_corroboration.py` (reshapes the curated
`data/raw/sources_by_year.json`); re-verify URLs with
`python3 scripts/verify_corroboration.py`.

## Headline

- **{n3} of {len(records)} editions** have ≥3 participant-naming source domains.
- **{p3} of {len(records)} editions** have ≥3 counting only genuinely-independent primaries
  (official + OBI/Unicamp + press/host/CV; aggregators excluded).
- Beyond URLs: all 27 years are reconciled official-vs-OBI with 0 discrepancies
  (count, medal multiset, every name).

## Notes

{global_md}

## Summary table

| Year | Naming domains | Indep-primary | Domains |
|-----:|:--:|:--:|---------|
{table}

## Per-year sources

{detail_md}"""

    with open(os.path.join(ROOT, "CORROBORATION.md"), "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Editions: {len(records)}")
    print(f">=3 naming: {n3}/{len(records)}; >=3 independent-primary: {p3}/{len(records)}")
    print("Shortfall (<3 naming):", [r["year"] for r in records if not r["meetsThreeNaming"]])
    print("Wrote data/corroboration.json + CORROBORATION.md")


if __name__ == "__main__":
    main()
