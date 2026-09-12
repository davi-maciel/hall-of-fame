# OMCPLP — Olimpíada de Matemática da Comunidade dos Países de Língua Portuguesa (Brazil)

Brazilian students at the OMCPLP (the Lusophone mathematical olympiad). Part of
the hall-of-fame data collection — one olympiad per folder, shared schema.

Coverage: 2011–2019 and 2022–2025, every edition held (no editions in 2020–2021).
Teams of 4.

```
data/raw/omcplp.json     canonical records (name, year, medal) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/omcplp.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention / null. Source verification: `python3 scripts/verify_corroboration.py`
re-fetches every corroboration URL and checks its content.
