# IYPT — International Young Physicists' Tournament

Brazilian team members at the IYPT. Part of the hall-of-fame data collection —
one olympiad per folder, shared schema.

Coverage: 2004–2007, 2011–2019, 2022–2026 — every edition Brazil entered (absent 2008–2010
and 2021; 2020 not held).

```
data/raw/iypt.json       canonical records (name, year, medal) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/iypt.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

The IYPT is a team tournament: the medal on each record is the team's medal (gold = finalists,
then silver and bronze bands), or null when the team finished below the bronze band.
Rebuild: `python3 scripts/build_graph.py`. Source verification:
`python3 scripts/verify_corroboration.py` re-fetches every corroboration URL and checks its content.
