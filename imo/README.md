# IMO — International Mathematical Olympiad

Brazilian students at the IMO. Part of the hall-of-fame data collection —
one olympiad per folder, shared schema.

Coverage: 1979–2026 (47 editions; no 1980 IMO was held).

```
data/raw/imo.json       canonical records (name, year, medal) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/imo.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention / null. Source verification: `python3 scripts/verify_corroboration.py`
re-fetches every corroboration URL and checks its content.
