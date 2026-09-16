# IMChO — Mendeleev International Chemistry Olympiad

Brazilian students at the Mendeleev olympiad. Part of the hall-of-fame data
collection — one olympiad per folder, shared schema.

Coverage: 2023–2026 (Brazil's first participation was the 57th edition, 2023;
Brazil hosted the 59th, Belo Horizonte 2025). Rosters are complete for all four editions (signed jury protocols for 2023, 2025 and 2026; the bc-pf scoreboard's full protocol for 2024).

```
data/raw/imcho.json      canonical records (name, year, medal) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/imcho.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention / null. Source verification: `python3 scripts/verify_corroboration.py`.
