# IPhO — International Physics Olympiad

Brazilian students at the IPhO. Part of the hall-of-fame data collection —
one olympiad per folder, shared schema.

Coverage: 2000–2026 (2020 = IdPhO substitute; Brazil absent 2024).

```
data/raw/ipho.json       canonical records (name, year, medal) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/ipho.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention / null. Source verification: `python3 scripts/verify_corroboration.py`
re-fetches every corroboration URL and checks its content.
