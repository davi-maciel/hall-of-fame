# APMO — Asian Pacific Mathematics Olympiad (Brazil)

Brazilian students at the APMO, a correspondence olympiad (papers are sat in
Brazil and marked centrally). Part of the hall-of-fame data collection — one
olympiad per folder, shared schema.

Coverage: 2010–2026, every edition (10 contestants per year).

```
data/raw/apmo.json       canonical records (name, year, medal, score) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/apmo.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention / null. Source verification: `python3 scripts/verify_corroboration.py`
re-fetches every corroboration URL and checks its content.
