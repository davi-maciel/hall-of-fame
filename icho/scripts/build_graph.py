#!/usr/bin/env python3
"""Build src/data/graph.json from data/raw/icho.json.

Reads the flat array of Brazilian IChO participation records, normalizes names
into stable slugs (applying an alias map so each real person is a single
student), builds co-participation edges, and writes the graph.

Idempotent: running it repeatedly yields byte-identical output except for the
`generatedAt` timestamp (the only nondeterministic field).

Usage: python3 scripts/build_graph.py
"""
from __future__ import annotations

import json
import re
import unicodedata
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "icho.json"
OUT = ROOT / "src" / "data" / "graph.json"

OLYMPIAD = "icho"

# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------

def strip_diacritics(text: str) -> str:
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


def slugify(name: str) -> str:
    """ASCII kebab-case: strip diacritics, lowercase, non-alphanumeric runs -> '-'."""
    ascii_name = strip_diacritics(name).lower()
    return re.sub(r"[^a-z0-9]+", "-", ascii_name).strip("-")


def search_key(name: str) -> str:
    """Lowercased, diacritics stripped, single-spaced."""
    return re.sub(r"\s+", " ", strip_diacritics(name).lower()).strip()


def display_name(name: str) -> str:
    """NFC form, diacritics preserved."""
    return unicodedata.normalize("NFC", re.sub(r"\s+", " ", name).strip())

# ---------------------------------------------------------------------------
# Alias map: variant slug -> canonical slug.
#
# Each entry is a real person who appears across editions under spelling
# variants that do NOT slugify to the same value. Pairs whose names already
# slugify identically (e.g. Thais Macedo Bezerra Terceiro Jorge 2006/2007/2008,
# Rafael de Cesaris Araujo Tavares 2006/2007, Raul Bruno Machado da Silva
# 2010/2011, Vitoria Nunes Medeiros 2012/2013, Ygor de Santana Moura 2019/2020,
# Gabriel Paz Sampaio Aguiar 2023/2024, Artur Galiza Magalhaes 2023/2024) merge
# automatically and need no entry here.
# ---------------------------------------------------------------------------
ALIASES = {
    # Levindo (Jose) Garcia Quarto - 2009 short form, 2010 with middle name.
    "levindo-garcia-quarto": "levindo-jose-garcia-quarto",
    # Vitor Gomes Pires - 2016 source truncates to "Vitor Pires".
    "vitor-pires": "vitor-gomes-pires",
    # Gabriel Ferreira Gomes Amgarten - 2015 romanized as "Amgartem"; 2016
    # truncated to "Gabriel Amgarten". Official original-script spelling: Amgarten.
    "gabriel-ferreira-gomes-amgartem": "gabriel-ferreira-gomes-amgarten",
    "gabriel-amgarten": "gabriel-ferreira-gomes-amgarten",
    # Ivna de Lima F. Gomes - 2017 short form "Ivna de Gomes".
    "ivna-de-gomes": "ivna-de-lima-f-gomes",
    # Joao Victor Moreira Pimentel - 2017 short form. (Distinct from the 2009
    # contestant Joao Victor Magalhaes Caminha, who is kept separate.)
    "joao-victor-pimentel": "joao-victor-moreira-pimentel",
}

# Preferred display name per canonical slug. Used when a person has multiple
# source spellings; picks the fullest, correctly-accented, correctly-cased form.
DISPLAY_OVERRIDE = {
    "levindo-jose-garcia-quarto": "Levindo José Garcia Quarto",
    "vitor-gomes-pires": "Vitor Gomes Pires",
    "gabriel-ferreira-gomes-amgarten": "Gabriel Ferreira Gomes Amgarten",
    "ivna-de-lima-f-gomes": "Ivna de Lima F. Gomes",
    "joao-victor-moreira-pimentel": "João Victor Moreira Pimentel",
    "raul-bruno-machado-da-silva": "Raul Bruno Machado da Silva",
    "vitoria-nunes-medeiros": "Vitória Nunes Medeiros",
    "ygor-de-santana-moura": "Ygor de Santana Moura",
    "artur-galiza-magalhaes": "Artur Galiza Magalhães",
    "gabriel-paz-sampaio-aguiar": "Gabriel Paz Sampaio Aguiar",
}

VALID_MEDALS = {"gold", "silver", "bronze", "honorable-mention", None}


def canonical_slug(raw_name: str) -> str:
    s = slugify(raw_name)
    return ALIASES.get(s, s)


def best_display(raw_names: list[str]) -> str:
    """Richest raw name: most tokens, then most diacritics, then longest."""
    def key(n: str):
        nonascii = sum(1 for ch in n if ord(ch) > 127)
        return (len(n.split()), nonascii, len(n))
    return display_name(max(raw_names, key=key))


def build(records: list[dict]) -> dict:
    students: dict[str, dict] = {}
    raw_names_by_slug: dict[str, list[str]] = {}

    for rec in records:
        assert rec["olympiadId"] == OLYMPIAD, rec
        assert rec["medal"] in VALID_MEDALS, f"bad medal: {rec}"
        slug = canonical_slug(rec["rawName"])
        raw_names_by_slug.setdefault(slug, []).append(rec["rawName"])
        student = students.setdefault(slug, {"id": slug, "name": "", "searchKey": "", "participations": []})
        student["participations"].append({
            "olympiad": rec["olympiadId"],
            "year": rec["year"],
            "medal": rec["medal"],
        })

    # Resolve display name / searchKey and sort participations.
    for slug, student in students.items():
        name = DISPLAY_OVERRIDE.get(slug) or best_display(raw_names_by_slug[slug])
        student["name"] = name
        student["searchKey"] = search_key(name)
        student["participations"].sort(key=lambda p: p["year"])

    # Co-participation edges: one undirected edge per teammate pair per edition.
    teams: dict[int, set[str]] = {}
    for rec in records:
        teams.setdefault(rec["year"], set()).add(canonical_slug(rec["rawName"]))

    edge_seen: set[tuple[str, str, int]] = set()
    edges: list[dict] = []
    for year, members in sorted(teams.items()):
        for a, b in combinations(sorted(members), 2):
            if a == b:
                continue  # no self-edges
            key = (a, b, year)
            if key in edge_seen:
                continue  # no duplicate edge within an edition
            edge_seen.add(key)
            edges.append({"source": a, "target": b, "olympiad": OLYMPIAD, "year": year})

    # Deterministic ordering.
    ordered_students = {slug: students[slug] for slug in sorted(students)}
    edges.sort(key=lambda e: (e["year"], e["source"], e["target"]))

    return {
        "students": ordered_students,
        "edges": edges,
        "metadata": {
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "studentCount": len(ordered_students),
            "edgeCount": len(edges),
        },
    }


def main() -> None:
    records = json.loads(RAW.read_text(encoding="utf-8"))
    graph = build(records)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    print(f"  students: {graph['metadata']['studentCount']}")
    print(f"  edges:    {graph['metadata']['edgeCount']}")


if __name__ == "__main__":
    main()
