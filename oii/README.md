# OII/CIIC — Olimpíada Ibero-americana de Informática

Brazilian students at the OII/CIIC. Part of the hall-of-fame data collection —
one olympiad per folder, shared schema.

Coverage: 2004, 2007, 2012–2026 (2011 attended, roster not publicly recorded).

```
data/raw/oii.json       canonical records (name, year, medal) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/oii.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention / null. Source verification: `python3 scripts/verify_corroboration.py`
re-fetches every corroboration URL and checks its content.
