# OIM — Olimpíada Ibero-americana de Matemática (Brazil)

Brazilian students at the OIM. Part of the hall-of-fame data collection —
one olympiad per folder, shared schema.

Coverage: 1985–2025, every edition (no edition in 1986). Teams of up to 4.

```
data/raw/oim.json        canonical records (name, year, medal) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/oim.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention / null; `medalStatus: "hors-concours"` marks a contestant who
competed outside the classification. Source verification:
`python3 scripts/verify_corroboration.py` re-fetches every corroboration URL and
checks its content.
