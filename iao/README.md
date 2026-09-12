# IAO — International Astronomy Olympiad

Brazilian students at the IAO. Part of the hall-of-fame data collection —
one olympiad per folder, shared schema.

Coverage: 1998–2000 and 2002–2007 — every edition Brazil attended (Brazil moved to the
IOAA from 2007 on).

```
data/raw/iao.json        canonical records (name, year, medal) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/iao.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze (IAO
Diplomas I / II / III) / null. Source verification: `python3 scripts/verify_corroboration.py`
re-fetches every corroboration URL and checks its content.
