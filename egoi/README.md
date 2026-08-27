# EGOI — European Girls' Olympiad in Informatics (Brazil as guest)

Brazilian students at the EGOI. Part of the hall-of-fame data collection —
one olympiad per folder, shared schema.

Coverage: 2021–2026, every edition.

```
data/raw/egoi.json       canonical records (name, year, medal) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/egoi.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention / null. Source verification: `python3 scripts/verify_corroboration.py`
re-fetches every corroboration URL and checks its content.
