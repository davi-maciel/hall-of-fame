# OLAA — Olimpíada Latino-Americana de Astronomia e Astronáutica

Brazilian students at the OLAA. Part of the hall-of-fame data collection —
one olympiad per folder, shared schema.

Coverage: 2009–2025, every edition (2020 virtual, 2021 hybrid; Brazil hosted 2009, 2011,
2015 and 2025).

```
data/raw/olaa.json       canonical records (name, year, medal) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/olaa.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention / null. Source verification: `python3 scripts/verify_corroboration.py`
re-fetches every corroboration URL and checks its content.
