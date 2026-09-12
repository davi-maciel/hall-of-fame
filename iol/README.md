# IOL — International Linguistics Olympiad

Brazilian students at the IOL. Part of the hall-of-fame data collection —
one olympiad per folder, shared schema.

Coverage: 2011–2014, 2016–2019, 2022–2026 — every edition Brazil entered (no team in
2015, 2020 cancelled, 2021 remote edition not joined).

```
data/raw/iol.json        canonical records (name, year, medal, team) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/iol.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention / null (individual contest); `team` is the delegation's nickname in the
years Brazil sent two teams. Source verification: `python3 scripts/verify_corroboration.py`
re-fetches every corroboration URL and checks its content.
