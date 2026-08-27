#!/usr/bin/env python3
"""
Build the canonical merged graph (src/data/graph.json) from the flat record
array data/raw/imo.json.

Pipeline:
  1. Read raw records: {rawName, olympiadId, year, medal, rank?}.
  2. Normalize each name -> display name (NFC), searchKey (no diacritics,
     lowercased), and slug (ASCII kebab-case).
  3. Apply the alias map (data/aliases.json) so name variants of the same real
     person collapse to one canonical slug.
  4. Merge participations per canonical student (dedup by slug).
  5. Generate undirected co-participation edges: for each (olympiad, year),
     one edge per unordered pair of students on that team. Each pair stored once.
  6. Write src/data/graph.json.

Deterministic and idempotent: only metadata.generatedAt is nondeterministic.
Run:  python3 scripts/build_graph.py
"""
import json
import os
import re
import unicodedata
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW_JSON = os.path.join(ROOT, "data", "raw", "imo.json")
ALIASES_JSON = os.path.join(ROOT, "data", "aliases.json")
OUT_JSON = os.path.join(ROOT, "src", "data", "graph.json")

VALID_MEDALS = {"gold", "silver", "bronze", "honorable-mention", None}


def strip_diacritics(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )


def to_display(name: str) -> str:
    """Display name: NFC-normalized, diacritics preserved, whitespace collapsed."""
    return unicodedata.normalize("NFC", re.sub(r"\s+", " ", name).strip())


def to_search_key(name: str) -> str:
    """searchKey: display name lowercased with diacritics stripped."""
    return strip_diacritics(to_display(name)).lower()


def to_slug(name: str) -> str:
    """slug/id: strip diacritics, lowercase, non-alphanumeric runs -> single hyphen, trim."""
    s = strip_diacritics(to_display(name)).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def load_aliases():
    if not os.path.exists(ALIASES_JSON):
        return {}, {}
    data = json.load(open(ALIASES_JSON, encoding="utf-8"))
    return data.get("aliases", {}), data.get("displayNames", {})


def main():
    records = json.load(open(RAW_JSON, encoding="utf-8"))
    alias_map, display_overrides = load_aliases()

    students = {}          # canonical slug -> student dict
    # canonical slug -> {(olympiad, year): bestDisplayName} to pick display deterministically
    display_candidates = {}
    # (olympiad, year) -> set of canonical slugs on that team
    teams = {}

    for rec in records:
        medal = rec.get("medal")
        assert medal in VALID_MEDALS, f"invalid medal: {medal!r}"
        year = rec["year"]
        olympiad = rec["olympiadId"]

        raw_slug = to_slug(rec["rawName"])
        slug = alias_map.get(raw_slug, raw_slug)

        if slug not in students:
            students[slug] = {
                "id": slug,
                "name": None,            # filled after choosing display
                "searchKey": None,
                "participations": [],
            }
            display_candidates[slug] = {}

        # Track the spelling per year so we can pick a deterministic display name.
        display_candidates[slug][year] = to_display(rec["rawName"])

        students[slug]["participations"].append({
            "olympiad": olympiad,
            "year": year,
            "medal": medal,
        })

        teams.setdefault((olympiad, year), set()).add(slug)

    # Choose display names: explicit override, else the most recent year's spelling.
    for slug, student in students.items():
        if slug in display_overrides:
            display = display_overrides[slug]
        else:
            latest_year = max(display_candidates[slug])
            display = display_candidates[slug][latest_year]
        student["name"] = display
        student["searchKey"] = to_search_key(display)
        # Sort participations by year for stable output.
        student["participations"].sort(key=lambda p: (p["year"], p["olympiad"]))

    # Build edges: one undirected edge per unordered pair per (olympiad, year).
    edges = []
    seen = set()
    for (olympiad, year), slugs in teams.items():
        ordered = sorted(slugs)
        for i in range(len(ordered)):
            for j in range(i + 1, len(ordered)):
                a, b = ordered[i], ordered[j]
                key = (a, b, olympiad, year)
                if key in seen:
                    continue
                seen.add(key)
                edges.append({
                    "source": a,
                    "target": b,
                    "olympiad": olympiad,
                    "year": year,
                })

    # Deterministic ordering.
    edges.sort(key=lambda e: (e["year"], e["olympiad"], e["source"], e["target"]))
    students_sorted = {k: students[k] for k in sorted(students)}

    graph = {
        "students": students_sorted,
        "edges": edges,
        "metadata": {
            "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "studentCount": len(students_sorted),
            "edgeCount": len(edges),
        },
    }

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
        f.write("\n")

    validate(graph)
    summary(graph)


def validate(graph):
    students = graph["students"]
    edges = graph["edges"]
    keys = set(students)
    seen = set()
    current_year = datetime.now(timezone.utc).year
    for e in edges:
        assert e["source"] in keys, f"edge source missing: {e['source']}"
        assert e["target"] in keys, f"edge target missing: {e['target']}"
        assert e["source"] != e["target"], f"self-edge: {e['source']}"
        k = (e["source"], e["target"], e["olympiad"], e["year"])
        assert k not in seen, f"duplicate edge: {k}"
        seen.add(k)
        assert e["year"] <= current_year, f"future year: {e['year']}"
    for slug, s in students.items():
        assert s["id"] == slug
        for p in s["participations"]:
            assert p["medal"] in VALID_MEDALS, f"bad medal {p['medal']}"
            assert p["year"] <= current_year
    assert graph["metadata"]["studentCount"] == len(students)
    assert graph["metadata"]["edgeCount"] == len(edges)
    print("Validation: OK")


def summary(graph):
    from collections import Counter
    students = graph["students"]
    parts = [p for s in students.values() for p in s["participations"]]
    medals = Counter(p["medal"] for p in parts)
    years = [p["year"] for p in parts]
    print(f"Students: {len(students)}")
    print(f"Edges:    {len(graph['edges'])}")
    print(f"Participations: {len(parts)}")
    print("Medal distribution:")
    for m in ["gold", "silver", "bronze", "honorable-mention", None]:
        print(f"  {str(m):20s} {medals.get(m, 0)}")
    print(f"Year range: {min(years)}-{max(years)} ({len(set(years))} editions)")


if __name__ == "__main__":
    main()
