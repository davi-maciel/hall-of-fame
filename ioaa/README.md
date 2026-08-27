# IOAA — International Olympiad on Astronomy and Astrophysics

Brazilian students at the IOAA. Part of the hall-of-fame data collection —
one olympiad per folder, shared schema.

Coverage: 2007–2025 (19 editions; no 2020 IOAA was held).

```
data/raw/ioaa.json       canonical records (name, year, medal) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/ioaa.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention / null. Source verification: `python3 scripts/verify_corroboration.py`
re-fetches every corroboration URL and checks its content.
