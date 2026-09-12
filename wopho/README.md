# WoPhO — World Physics Olympiad

Brazilian students at the WoPhO (Indonesia, 2011/12 and 2012/13 — the only two finals ever
held; the 2013 final was cancelled and the competition folded). Part of the hall-of-fame data
collection — one olympiad per folder, shared schema.

Coverage: complete. One record — Ivan Tadeu Ferreira Antunes Filho, silver at the 2nd WoPhO
(Tangerang, 28 Dec 2012 – 3 Jan 2013), the only Brazilian ever awarded. The year field uses the
organiser's edition label (`2012`). The 2011/12 final had no Brazilian awardee.

```
data/raw/wopho.json       canonical records (name, year, medal) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/wopho.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention / null. Source verification: `python3 scripts/verify_corroboration.py`
re-fetches every corroboration URL and checks its content (wopho.org is defunct, so the
official pages are cited through Wayback Machine captures).
