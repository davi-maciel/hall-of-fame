# OIAB — Olimpíada Ibero-americana de Biologia

Brazilian students at the OIAB. Part of the hall-of-fame data collection —
one olympiad per folder, shared schema.

Coverage: 2007–2019, 2021–2026 — every edition held (2020 was cancelled).

```
data/raw/oiab.json       canonical records (name, year, medal) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/oiab.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention / null (`medalStatus` marks the 2022 rows whose award is unknown). Source
verification: `python3 scripts/verify_corroboration.py` re-fetches every corroboration URL and
checks its content.
