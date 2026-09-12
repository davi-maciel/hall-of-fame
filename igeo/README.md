# iGeo — International Geography Olympiad

Brazilian students at the iGeo. Part of the hall-of-fame data collection —
one olympiad per folder, shared schema.

Coverage: 2018, 2022, 2024–2026 rows only: the official iGeo results name gold medallists alone, so Brazilian rosters depend on OBG posts and press (2016, 2019 and 2023 have no usable names yet).

```
data/raw/igeo.json        canonical records (name, year, medal) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/igeo.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention / null (`medalStatus` marks rows whose result is not yet published).
Source verification: `python3 scripts/verify_corroboration.py` re-fetches every corroboration
URL and checks its content.
