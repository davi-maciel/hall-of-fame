# RMM — Romanian Master of Mathematics (Brazil as invited team)

Brazilian students at the Romanian Master of Mathematics, the invitational
olympiad held in Bucharest. Part of the hall-of-fame data collection — one
olympiad per folder, shared schema.

Coverage: 2010–2013, 2015–2021 and 2026 — every edition Brazil attended
(no editions in 2014 and 2022; Brazil absent 2023–2025).

```
data/raw/rmm.json        canonical records (name, year, medal) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/rmm.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention / null. Source verification: `python3 scripts/verify_corroboration.py`
re-fetches every corroboration URL and checks its content.
