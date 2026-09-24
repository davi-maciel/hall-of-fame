#!/usr/bin/env python3
"""
Aggregate each olympiad folder's data/corroboration.json into site/data/sources.json:
  { "<olympiad>": { "<year>": [ {"u": url, "d": domain, "c": confirms, "chk": status, "p": [personId, ...]}, ... ] } }
so the person page can offer fact-check links per (olympiad, year).

"chk" / "p" come from data/source_names.json (scripts/check_source_names.py):
chk = text | status-only | error is how the page was checked, p = the people of
that edition whose name the page actually contains (omitted when empty). When
source_names.json is missing the fields are simply absent and the person page
shows every link the old way.

Folders without a corroboration trail (the physics datasets imported from
small-world) get a curated dataset-level fallback where a genuine covering
source exists; otherwise the year simply has no links (never fabricate).

Run:  python3 site/scripts/build_sources.py
"""
import json
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
ROOT = SITE.parent
OUT = SITE / "data" / "sources.json"
NAMES = SITE / "data" / "source_names.json"
sys.path.insert(0, str(SITE / "scripts"))
from build_people import HIDDEN_DATASETS  # noqa: E402  (single source of truth)

WITH_TRAILS = ["imo", "icho", "ioi", "ioaa", "ijso", "oibf", "eupho", "nbpho", "ipho", "oii", "egoi", "imcho", "oiaq", "apmo", "egmo", "oim", "conosur", "omcplp", "rioplatense", "rmm", "pagmo", "igo", "ibo", "oiab", "iao", "olaa", "iypt", "iol", "ieso", "igeo", "wopho", "ieo"]

# Dataset-level fallbacks: one URL that genuinely lets a reader verify any year
# of that dataset. (yearsNote kept human-readable in "c".)
FALLBACKS = {
    # oibf: no single live covering source; per-year PDFs are archived in the repo
}


def main():
    names = json.loads(NAMES.read_text(encoding="utf-8")).get("byOlympiad", {}) if NAMES.exists() else None
    unchecked = 0
    out = {}
    for ds in WITH_TRAILS:
        if ds in HIDDEN_DATASETS:  # not on the site, so no source links either
            continue
        corr = json.loads((ROOT / ds / "data" / "corroboration.json").read_text(encoding="utf-8"))
        by_year = {}
        for yrec in corr["years"]:
            entries = []
            for s in yrec["sources"]:
                e = {"u": s["url"], "d": s["domain"].split(" (")[0], "c": s.get("confirms", "")}
                if names is not None:
                    chk = names.get(ds, {}).get(str(yrec["year"]), {}).get(s["url"])
                    if chk:
                        e["chk"] = chk["status"]
                        if chk.get("found"):
                            e["p"] = sorted(chk["found"])
                    else:
                        unchecked += 1
                entries.append(e)
            by_year[str(yrec["year"])] = entries
        out[ds] = by_year

    for ds, entries in FALLBACKS.items():
        if ds in HIDDEN_DATASETS:
            continue
        out[ds] = {"*": entries}

    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    n = sum(len(v) for ds in out.values() for v in ds.values())
    print(f"sources.json: {len(out)} olympiads, {n} source entries")
    if names is None:
        print("  source_names.json not found: no chk/p fields (run scripts/check_source_names.py)")
    elif unchecked:
        print(f"  WARNING: {unchecked} URL refs missing from source_names.json — rerun scripts/check_source_names.py")
    else:
        named = sum(1 for ds in out.values() for v in ds.values() for e in v if e.get("p"))
        print(f"  name-checked: {named} entries name at least one person of their edition")


if __name__ == "__main__":
    main()
