#!/usr/bin/env python3
"""
Corroboration for Brazil at the PAGMO (repo-standard). 2026-09-09 collection pass:
every URL fetched and content-verified. Editions: 2021-2025 (5; four contestants each).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OBM = "https://www.obm.org.br/resultados-pagmo/"


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def obm(needle):
    return src(OBM, "obm.org.br", "primary", "full", "national organizer results table (all 5 editions): names, city/state, medal", needle)


def post(url, needle, confirms, coverage="full", domain="obm.org.br"):
    return src(url, domain, "primary", coverage, confirms, needle)


SOURCES = {
 2021: [obm("Quintanilla"), post("https://www.obm.org.br/2021/10/09/com-xxxx-medalhas-brasil-encerra-participacao-na-pagmo-2021/", "Quintanilla", "OBM news: 4 medals by name (virtual 1st edition)"),
        post("https://noic.com.br/matematica/divulgado-o-time-da-pagmo-2021/", "Quintanilla", "NOIC team announcement", "full (pre-event roster)", domain="noic.com.br")],
 2022: [obm("Kochloukova"), post("https://www.obm.org.br/2022/10/31/brasil-conquista-uma-medalha-de-ouro-e-tres-de-prata-na-pagmo-2022/", "Miyashita", "OBM news: gold + 3 silvers by name"),
        post("https://noic.com.br/matematica/divulgado-o-resultado-da-pagmo-2022/", "Miyashita", "NOIC results post", domain="noic.com.br")],
 2023: [obm("Pazó"), post("https://www.obm.org.br/2023/08/13/20594/", "Pazó", "OBM news: G/S/2B by name"),
        post("https://noic.com.br/uncategorized/anunciado-o-time-da-pagmo-2023/", "Schneider", "NOIC team announcement", "full (pre-event roster)", domain="noic.com.br")],
 2024: [obm("Sophia Li Ci Liu"), post("https://www.obm.org.br/2024/11/30/brasil-e-campeao-da-pagmo-2024/", "Sophia", "OBM news: 3 golds + silver by name; team champion")],
 2025: [obm("Passarini"), post("https://www.obm.org.br/2025/10/31/time-brasil-conquista-quatro-medalhas-de-prata-na-5a-pagmo/", "Passarini", "OBM news: 4 silvers by name; Fortaleza hosts"),
        post("https://www.obm.org.br/2025/04/12/equipe-brasileira-para-a-pagmo-2025-e-definida/", "Passarini", "OBM: team announcement", "full (pre-event roster)")],
}

NOTES = {
 2021: "1st edition, virtual (organised by Brazil, Chile, Ecuador, Spain and Mexico).",
 2022: "Alice Ella Schneider (Belo Horizonte) = the EGMO 2025 / Rioplatense 2025 'Alice Schneider' (fuller form adopted everywhere).",
 2023: "'Ana Beatriz Barbosa Pazó Serpa' = EGMO 2025 'Ana Beatriz Pazó' (fuller form adopted in egmo/).",
 2024: "Team champion.",
 2025: "5th edition hosted by Brazil (Fortaleza, October 2025). 6th (2026) team selected; event not yet held on 2026-09-09.",
}

GLOBAL_NOTES = [
 "Pan-American girls' olympiad modelled on the EGMO; teams of four; Brazil in every edition since the 2021 debut. OBM's all-years table is the naming source; OBM news and NOIC corroborate each year. No official PAGMO results site was found online.",
 "All 20 records are medals (no unawarded contestant so far).",
]

YEARS = sorted(SOURCES)


def build_records():
    records = []
    for y in YEARS:
        srcs = SOURCES[y]
        naming = [s for s in srcs if s["cls"] in ("official", "primary", "archive")]
        indep = [s for s in srcs if s["cls"] in ("official", "primary")]
        rec = {"year": y, "namingSourceCount": len(naming), "independentPrimaryCount": len(indep),
               "meetsThreeNaming": len(naming) >= 3, "meetsThreePrimary": len(indep) >= 3, "sources": srcs}
        if y in NOTES:
            rec["note"] = NOTES[y]
        records.append(rec)
    return records


def main():
    records = build_records()
    payload = {
        "olympiadId": "pagmo",
        "description": "Sources confirming Brazilian PAGMO contestants + results, per edition.",
        "provenanceClasses": {"official": "(none online)", "primary": "OBM (national organizer) results table and news; NOIC.", "archive": "(none)"},
        "globalNotes": GLOBAL_NOTES,
        "years": records,
    }
    with open(os.path.join(ROOT, "data", "corroboration.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")

    lines = []
    for r in records:
        doms = ", ".join(dict.fromkeys(s["domain"] for s in r["sources"]))
        flag = "" if r["namingSourceCount"] >= 2 else "  (single-source)"
        note = " *" if "note" in r else ""
        lines.append(f"| {r['year']} | {r['namingSourceCount']} | {doms}{flag}{note} |")

    details = []
    for r in records:
        details.append(f"### {r['year']}")
        for i, s in enumerate(r["sources"], 1):
            details.append(f"{i}. **{s['domain']}** ({s['cls']}, coverage: {s['coverage']}) — {s['url']} — {s['confirms']}")
        if "note" in r:
            details.append("")
            details.append(f"> {r['note']}")
        details.append("")

    md = ("# Per-Year Corroboration — Brazil at the PAGMO\n\n"
          "**Machine-readable:** `data/corroboration.json`. Rebuild: `python3 scripts/build_corroboration.py`; "
          "verify: `python3 scripts/verify_corroboration.py`. 2026-09-09 collection pass.\n\n## Notes\n\n"
          + "\n".join(f"- {n}" for n in GLOBAL_NOTES)
          + "\n\n## Summary\n\n| Year | Sources | Domains |\n|-----:|:--:|---------|\n" + "\n".join(lines)
          + "\n\n## Per-year sources\n\n" + "\n".join(details))
    with open(os.path.join(ROOT, "CORROBORATION.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Editions: {len(records)}")
    print("Wrote data/corroboration.json + CORROBORATION.md")


if __name__ == "__main__":
    main()
