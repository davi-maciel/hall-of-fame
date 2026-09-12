# IESO — International Earth Science Olympiad

Brazilian students at the IESO. Part of the hall-of-fame data collection —
one olympiad per folder, shared schema.

Coverage: 2012–2019 and 2026 (Brazil skipped 2021–2025; 2020 cancelled). Rosters are partial for 2013–2015 and 2017.

```
data/raw/ieso.json        canonical records (name, year, medal) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/ieso.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention / null (`medalStatus` marks rows whose result is not yet published).
Source verification: `python3 scripts/verify_corroboration.py` re-fetches every corroboration
URL and checks its content.
