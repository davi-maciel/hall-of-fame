# Rioplatense — Olimpíada Rioplatense de Matemática (Brazil)

Brazilian medallists at the Olimpíada Matemática Rioplatense (OMA, Argentina), a
four-level regional olympiad (Nivel A, 1, 2, 3) in which Brazil enters two teams
(Fortaleza and São Paulo). Part of the hall-of-fame data collection — one olympiad
per folder, shared schema.

Coverage: 1996–2025, every edition held (none in 2020–2021). Medallists and
honourable mentions only — OMA publishes medal tables, not full rosters.

```
data/raw/rioplatense.json  canonical records (name, year, level, team, medal) — edit this file
data/corroboration.json    per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py     data/raw/rioplatense.json -> src/data/graph.json
src/data/graph.json        students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention. `level` is A, 1, 2 or 3; `team` is Fortaleza, São Paulo or Brasil.
Source verification: `python3 scripts/verify_corroboration.py` re-fetches every
corroboration URL and checks its content.
