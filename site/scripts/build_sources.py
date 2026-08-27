#!/usr/bin/env python3
"""
Aggregate each olympiad folder's data/corroboration.json into site/data/sources.json:
  { "<olympiad>": { "<year>": [ {"u": url, "d": domain, "c": confirms}, ... ] } }
so the person page can offer fact-check links per (olympiad, year).

Folders without a corroboration trail (the physics datasets imported from
small-world) get a curated dataset-level fallback where a genuine covering
source exists; otherwise the year simply has no links (never fabricate).

Run:  python3 site/scripts/build_sources.py
"""
import json
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
ROOT = SITE.parent
OUT = SITE / "data" / "sources.json"

WITH_TRAILS = ["imo", "icho", "ioi", "ioaa", "ijso", "oibf", "eupho", "nbpho", "ipho", "oii", "egoi"]

# Dataset-level fallbacks: one URL that genuinely lets a reader verify any year
# of that dataset. (yearsNote kept human-readable in "c".)
FALLBACKS = {
    # oibf: no single live covering source; per-year PDFs are archived in the repo
}


def main():
    out = {}
    for ds in WITH_TRAILS:
        corr = json.loads((ROOT / ds / "data" / "corroboration.json").read_text(encoding="utf-8"))
        by_year = {}
        for yrec in corr["years"]:
            by_year[str(yrec["year"])] = [
                {"u": s["url"], "d": s["domain"].split(" (")[0], "c": s.get("confirms", "")}
                for s in yrec["sources"]
            ]
        out[ds] = by_year

    for ds, entries in FALLBACKS.items():
        out[ds] = {"*": entries}

    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    n = sum(len(v) for ds in out.values() for v in ds.values())
    print(f"sources.json: {len(out)} olympiads, {n} source entries")


if __name__ == "__main__":
    main()
