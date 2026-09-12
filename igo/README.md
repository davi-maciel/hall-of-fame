# IGO — Iranian Geometry Olympiad (Brazil)

Brazilian participants in the Iranian Geometry Olympiad, a correspondence
contest sat locally in three age levels (elementary, intermediate, advanced).
Part of the hall-of-fame data collection — one olympiad per folder, shared schema.

Coverage: 2016–2025, every edition Brazil entered. 2016–2022 list medallists
only; 2023–2025 list every Brazilian participant (official spreadsheets).

```
data/raw/igo.json        canonical records (name, year, level, medal, score) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/igo.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention / null. `level` is elementar, intermediario or avancado; `score`
is the official total where published. Source verification:
`python3 scripts/verify_corroboration.py` re-fetches every corroboration URL and
checks its content.
