#!/usr/bin/env python3
"""Build src/data/graph.json from data/raw/conosur.json.

Mirrors the small-world pipeline:
- display name: NFC (preserves diacritics); title-cased only if the source was ALL-CAPS
- searchKey:   diacritics stripped, lowercased, single-spaced
- slug (id):   ASCII kebab-case  (e.g. "João Victor" -> "joao-victor")
- edges:       for each (olympiad, year), one undirected edge per pair of
               participants, stored once (source slug < target slug)

Raw record shape (data/raw/conosur.json), a JSON list of:
  {"rawName": str, "olympiadId": "conosur", "year": int,
   "medal": "gold"|"silver"|"bronze"|"honorable-mention"|null,
   "medalStatus": str (optional, e.g. "hors-concours")}
"""
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "conosur.json"
ALIASES = ROOT / "scripts" / "aliases.json"
OUT = ROOT / "src" / "data" / "graph.json"

VALID_MEDALS = {"gold", "silver", "bronze", "honorable-mention", None}


def strip_diacritics(s: str) -> str:
    nfd = unicodedata.normalize("NFD", s)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn")


def make_slug(name: str) -> str:
    base = strip_diacritics(name).lower()
    base = base.replace("'", "").replace("\u2019", "")
    base = base.replace("&", " and ")
    base = re.sub(r"[^a-z0-9]+", "-", base)
    return base.strip("-")


def make_search_key(name: str) -> str:
    key = strip_diacritics(name).lower()
    return re.sub(r"\s+", " ", key).strip()


def display_name(raw: str) -> str:
    name = unicodedata.normalize("NFC", raw).strip()
    name = re.sub(r"\s+", " ", name)
    # Title-case only if the source had no lowercase letters (ALL CAPS input)
    if name and not any(c.islower() for c in name if c.isalpha()):
        name = " ".join(w.capitalize() for w in name.split(" "))
    return name


def load_aliases():
    """Optional alias maps to merge variant spellings.

    aliases.json: {"slugAliases": {variantSlug: canonicalSlug},
                   "preferredNames": {canonicalSlug: "Preferred Display Name"}}
    """
    if ALIASES.exists():
        a = json.loads(ALIASES.read_text(encoding="utf-8"))
        return a.get("slugAliases", {}), a.get("preferredNames", {})
    return {}, {}


def main():
    if not RAW.exists():
        sys.exit(f"missing {RAW}; create data/raw/conosur.json first")

    records = json.loads(RAW.read_text(encoding="utf-8"))
    slug_aliases, preferred = load_aliases()

    students = {}  # slug -> student dict
    # (olympiad, year) -> set of participant slugs
    rosters = {}

    for r in records:
        raw = r["rawName"]
        year = int(r["year"])
        olympiad = r.get("olympiadId", "conosur")
        medal = r.get("medal")
        if medal not in VALID_MEDALS:
            sys.exit(f"invalid medal {medal!r} for {raw} {year}")

        slug = make_slug(raw)
        slug = slug_aliases.get(slug, slug)
        if not slug:
            sys.exit(f"empty slug for rawName {raw!r}")

        if slug not in students:
            students[slug] = {
                "id": slug,
                "name": preferred.get(slug, display_name(raw)),
                "searchKey": make_search_key(preferred.get(slug, raw)),
                "participations": [],
            }
        elif slug in preferred:
            students[slug]["name"] = preferred[slug]
            students[slug]["searchKey"] = make_search_key(preferred[slug])

        # de-dup identical (olympiad, year) participations for the same student
        existing = students[slug]["participations"]
        dup = next(
            (p for p in existing if p["olympiad"] == olympiad and p["year"] == year),
            None,
        )
        if dup is None:
            students[slug]["participations"].append(
                {"olympiad": olympiad, "year": year, "medal": medal}
            )
        elif dup["medal"] is None and medal is not None:
            dup["medal"] = medal  # upgrade null -> known medal

        rosters.setdefault((olympiad, year), set()).add(slug)

    # sort participations chronologically for stable output
    for s in students.values():
        s["participations"].sort(key=lambda p: (p["year"], p["olympiad"]))

    # build edges: one per unordered pair per (olympiad, year)
    edges = []
    seen = set()
    for (olympiad, year), slugs in rosters.items():
        for a, b in combinations(sorted(slugs), 2):
            key = (a, b, olympiad, year)
            if key in seen:
                continue
            seen.add(key)
            edges.append(
                {"source": a, "target": b, "olympiad": olympiad, "year": year}
            )

    edges.sort(key=lambda e: (e["year"], e["olympiad"], e["source"], e["target"]))

    # students map ordered by most recent participation first (like small-world)
    def last_year(s):
        return max((p["year"] for p in s["participations"]), default=0)

    ordered = dict(
        sorted(
            students.items(),
            key=lambda kv: (-last_year(kv[1]), kv[1]["name"]),
        )
    )

    graph = {
        "students": ordered,
        "edges": edges,
        "metadata": {
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "studentCount": len(ordered),
            "edgeCount": len(edges),
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"students={len(ordered)} edges={len(edges)} -> {OUT}")


if __name__ == "__main__":
    main()
