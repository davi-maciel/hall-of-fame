# OIAQ — Olimpíada Ibero-americana de Química

Brazilian students at the OIAQ. Part of the hall-of-fame data collection —
one olympiad per folder, shared schema.

Coverage: 1995–2025 (29 editions — Brazil attended every edition held; none in
2001 or 2020; Brazil hosted 1997, 2007, 2011, 2015 and the 2021 remote edition).

```
data/raw/oiaq.json       canonical records (name, year, medal) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/oiaq.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention / null. Source verification: `python3 scripts/verify_corroboration.py`.
