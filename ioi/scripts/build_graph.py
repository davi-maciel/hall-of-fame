#!/usr/bin/env python3
"""Build src/data/graph.json from data/raw/ioi.json.

Reads the flat per-competitor raw records, normalizes names into stable
ASCII slugs, dedupes people by slug (via an alias map), and emits the
co-participation graph. Idempotent: the only nondeterministic field is
metadata.generatedAt.
"""
import json
import re
import unicodedata
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "ioi.json"
OUT = ROOT / "src" / "data" / "graph.json"

# Alias map: variant slug -> {"canonical": <slug>, "name": <preferred display>}.
# The authoritative source (stats.ioinformatics.org) keys every contestant to a
# numeric person ID and uses one consistent spelling per person across all years,
# so no within-source aliases exist. This map is the seam for reconciling
# alternate spellings should a second source introduce them.
ALIASES: dict[str, dict[str, str]] = {}


def strip_diacritics(s: str) -> str:
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def make_slug(name: str) -> str:
    ascii_name = strip_diacritics(name).lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_name).strip("-")
    return slug


def search_key(name: str) -> str:
    return strip_diacritics(name).lower().strip()


def resolve(slug: str) -> str:
    """Follow the alias map to the canonical slug (single hop expected)."""
    seen = set()
    while slug in ALIASES and slug not in seen:
        seen.add(slug)
        slug = ALIASES[slug]["canonical"]
    return slug


def main() -> None:
    records = json.loads(RAW.read_text(encoding="utf-8"))

    students: dict[str, dict] = {}
    # year -> set of canonical slugs that competed that year
    by_year: dict[int, set] = {}

    for rec in records:
        raw_name = rec["rawName"]
        variant = make_slug(raw_name)
        slug = resolve(variant)

        display = ALIASES.get(variant, {}).get(
            "name", unicodedata.normalize("NFC", raw_name)
        )

        st = students.setdefault(
            slug,
            {
                "id": slug,
                "name": display,
                "searchKey": search_key(display),
                "participations": [],
            },
        )
        # one participation per (person, olympiad, year)
        key = (rec["olympiadId"], rec["year"])
        if not any(
            (p["olympiad"], p["year"]) == key for p in st["participations"]
        ):
            st["participations"].append(
                {
                    "olympiad": rec["olympiadId"],
                    "year": rec["year"],
                    "medal": rec["medal"],
                }
            )

        by_year.setdefault(rec["year"], set()).add(slug)

    # sort participations for deterministic output
    for st in students.values():
        st["participations"].sort(key=lambda p: (p["olympiad"], p["year"]))

    # Edges: one undirected edge per teammate pair per (olympiad, year).
    # IOI is the only olympiad here; partition by year.
    edges = []
    seen_edges = set()
    for year, slugs in by_year.items():
        for a, b in combinations(sorted(slugs), 2):
            if a == b:
                continue
            ekey = (a, b, "ioi", year)
            if ekey in seen_edges:
                continue
            seen_edges.add(ekey)
            edges.append(
                {"source": a, "target": b, "olympiad": "ioi", "year": year}
            )

    edges.sort(key=lambda e: (e["year"], e["source"], e["target"]))

    graph = {
        "students": dict(sorted(students.items())),
        "edges": edges,
        "metadata": {
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "studentCount": len(students),
            "edgeCount": len(edges),
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote {OUT}")
    print(f"  students: {len(students)}")
    print(f"  edges:    {len(edges)}")


if __name__ == "__main__":
    main()
