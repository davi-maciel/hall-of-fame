#!/usr/bin/env python3
"""Stage 1 of the pipeline: parse the official IChO result HTML into raw JSON.

Reads every `data/raw/icho_<year>.html` (the per-edition result tables downloaded
from the official IChO database), extracts the Brazilian competitor rows, and writes:

  1. data/raw/brazil_by_year_extracted.json — intermediate: every Brazil row exactly
     as parsed (display name, original-script name, country, rank, award), keyed by year.
  2. data/raw/icho.json — OUTPUT 1: one flat record per (competitor, year) with the
     chosen rawName, medal enum, and rank.

Stage 2 (scripts/build_graph.py) then turns icho.json into src/data/graph.json.

Deterministic and idempotent: same HTML in -> byte-identical JSON out. No network.

Why a per-edition page and not the country page: the official Brazil *country* page
silently drops the top-ranked student in several editions (drops the top-ranked student in several editions). The
per-edition tables consistently list complete 4-person teams, so they are the source.

rawName selection: each edition lists two name columns — a romanized "Contestant" and an
"Original script" column. Neither is uniformly more complete (e.g. 2012 favours the
script column "Daniel Arjona de Andrade Hara"; 2019 favours the display column
"Lucas Yutaka Kuroishi" over the truncated script "Lucas Yutaka"). rawName keeps the
*richer* of the two, decided by: more word-tokens, then more diacritics, then longer
string, then the display column. Name reconciliation across editions happens later, in
build_graph.py's alias map — not here.

Usage: python3 scripts/extract_raw.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
INTERMEDIATE = RAW_DIR / "brazil_by_year_extracted.json"
OUT = RAW_DIR / "icho.json"

OLYMPIAD = "icho"

# Official award label -> medal enum. "Participant" is a *known* no-medal result
# (competed, placed below the bronze/HM cut-off), represented as null — never a guess.
AWARD_TO_MEDAL = {
    "Gold medal": "gold",
    "Silver medal": "silver",
    "Bronze medal": "bronze",
    "Honorable mention": "honorable-mention",
    "Participant": None,
}


def parse_brazil_rows(html: str) -> list[list[str]]:
    """Return each Brazil <tr> as a list of stripped cell strings.

    Columns in the official table: [Contestant, Original script, Country, Rank, Award].
    """
    text = re.sub(r"<script.*?</script>", "", html, flags=re.DOTALL)
    rows = re.findall(r"<tr>(.*?)</tr>", text, flags=re.DOTALL)
    out = []
    for row in rows:
        cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, flags=re.DOTALL)
        cells = [re.sub(r"<[^>]+>", "", c).strip() for c in cells]
        if any(c == "Brazil" for c in cells):
            out.append(cells)
    return out


def tokens(name: str) -> list[str]:
    return [t for t in re.split(r"\s+", name.strip()) if t]


def richest(display: str, script: str) -> str:
    """The more complete of the two official name columns."""
    candidates = [c for c in (display.strip(), script.strip()) if c]
    if len(candidates) == 1:
        return candidates[0]

    def key(c: str):
        nonascii = sum(1 for ch in c if ord(ch) > 127)
        return (len(tokens(c)), nonascii, len(c))

    a, b = display.strip(), script.strip()
    return a if key(a) >= key(b) else b


def year_of(path: Path) -> int:
    m = re.search(r"icho_(\d{4})\.html$", path.name)
    if not m:
        raise ValueError(f"unexpected filename: {path.name}")
    return int(m.group(1))


def main() -> None:
    edition_files = sorted(RAW_DIR.glob("icho_[12][0-9][0-9][0-9].html"), key=year_of)
    if not edition_files:
        raise SystemExit(f"No icho_<year>.html files found in {RAW_DIR}")

    by_year: dict[str, list[list[str]]] = {}
    for path in edition_files:
        rows = parse_brazil_rows(path.read_text(encoding="utf-8"))
        by_year[str(year_of(path))] = rows

    # Intermediate: verbatim parsed rows.
    INTERMEDIATE.write_text(
        json.dumps(by_year, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    # OUTPUT 1: one record per (competitor, year).
    records = []
    for year in sorted(by_year, key=int):
        for cells in by_year[year]:
            display, script, _country, rank, award = (cells + [""] * 5)[:5]
            if award not in AWARD_TO_MEDAL:
                raise ValueError(f"{year}: unknown award label {award!r}")
            rec = {
                "rawName": richest(display, script),
                "olympiadId": OLYMPIAD,
                "year": int(year),
                "medal": AWARD_TO_MEDAL[award],
            }
            if rank.strip():
                rec["rank"] = int(rank)
            records.append(rec)

    OUT.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

    editions = len(by_year)
    print(f"Parsed {editions} editions ({min(by_year, key=int)}–{max(by_year, key=int)})")
    print(f"Wrote {INTERMEDIATE.relative_to(ROOT)} and {OUT.relative_to(ROOT)} ({len(records)} records)")


if __name__ == "__main__":
    main()
