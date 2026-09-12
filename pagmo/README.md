# PAGMO — Pan-American Girls' Mathematical Olympiad (Brazil)

Brazilian students at the PAGMO, the Pan-American girls' olympiad created in
2021 on the EGMO model. Part of the hall-of-fame data collection — one olympiad
per folder, shared schema.

Coverage: 2021–2025, every edition (4 contestants per year).

```
data/raw/pagmo.json      canonical records (name, year, medal) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/pagmo.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention / null. Source verification: `python3 scripts/verify_corroboration.py`
re-fetches every corroboration URL and checks its content.
