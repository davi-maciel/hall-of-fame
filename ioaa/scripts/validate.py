#!/usr/bin/env python3
"""Validate src/data/graph.json: referential integrity, year ranges, no dup edges."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPH = ROOT / "src" / "data" / "graph.json"

VALID_MEDALS = {"gold", "silver", "bronze", "honorable-mention", None}
# 2020 had no IOAA: it was replaced by the GeCAA (a distinct online event),
# which the IOAA board states "did not count as an IOAA". 2021 WAS a real
# IOAA (the 14th, held online from Bogotá). First edition: 2007.
CANCELLED_YEARS = {2020}
MIN_YEAR, MAX_YEAR = 2007, 2026


def main():
    g = json.loads(GRAPH.read_text(encoding="utf-8"))
    students, edges = g["students"], g["edges"]
    errors, warnings = [], []

    for slug, s in students.items():
        if s["id"] != slug:
            errors.append(f"student key {slug} != id {s['id']}")
        if not s["participations"]:
            warnings.append(f"{slug} has no participations")
        seen_part = set()
        for p in s["participations"]:
            if p["medal"] not in VALID_MEDALS:
                errors.append(f"{slug}: bad medal {p['medal']!r}")
            if not (MIN_YEAR <= p["year"] <= MAX_YEAR):
                errors.append(f"{slug}: year {p['year']} out of range")
            if p["year"] in CANCELLED_YEARS:
                errors.append(f"{slug}: participation in cancelled year {p['year']}")
            k = (p["olympiad"], p["year"])
            if k in seen_part:
                errors.append(f"{slug}: duplicate participation {k}")
            seen_part.add(k)

    seen_edge = set()
    for e in edges:
        for end in ("source", "target"):
            if e[end] not in students:
                errors.append(f"edge {end} {e[end]} not in students")
        if e["source"] == e["target"]:
            errors.append(f"self-edge on {e['source']}")
        key = tuple(sorted((e["source"], e["target"]))) + (e["olympiad"], e["year"])
        if key in seen_edge:
            errors.append(f"duplicate edge {key}")
        seen_edge.add(key)
        # both endpoints must actually have that participation
        for end in ("source", "target"):
            st = students.get(e[end])
            if st and not any(
                p["olympiad"] == e["olympiad"] and p["year"] == e["year"]
                for p in st["participations"]
            ):
                errors.append(
                    f"edge {key}: {e[end]} lacks participation {e['olympiad']} {e['year']}"
                )

    if g["metadata"]["studentCount"] != len(students):
        errors.append("metadata.studentCount mismatch")
    if g["metadata"]["edgeCount"] != len(edges):
        errors.append("metadata.edgeCount mismatch")

    for w in warnings:
        print(f"WARN: {w}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        sys.exit(f"\nVALIDATION FAILED: {len(errors)} error(s)")
    print(f"OK: {len(students)} students, {len(edges)} edges, no errors.")


if __name__ == "__main__":
    main()
