# Cone Sul — Olimpíada de Matemática do Cone Sul (Brazil)

Brazilian students at the Cono Sur (Cone Sul) Mathematical Olympiad, the
under-16 regional olympiad of southern South America. Part of the hall-of-fame
data collection — one olympiad per folder, shared schema.

Coverage: 1988, 1991–2026, every edition (none held in 1989–1990). Teams of 4.

```
data/raw/conosur.json    canonical records (name, year, medal) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/conosur.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention / null. Source verification: `python3 scripts/verify_corroboration.py`
re-fetches every corroboration URL and checks its content.
