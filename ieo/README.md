# IEO — International Economics Olympiad

Brazilian students at the IEO. Part of the hall-of-fame data collection —
one olympiad per folder, shared schema.

Coverage: complete — all nine editions (2018–2026), five contestants each (45 records).
Brazil has attended since the inaugural IEO in Moscow and won the team Gold trophy in 2019,
2020, 2021 and 2023. Names follow the fullest documented form (official spreadsheets, the
Banco Central attendance list for 2025, press and team photos for 2026); three 2026 rows keep
the organiser's short form.

```
data/raw/ieo.json         canonical records (name, year, medal) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/ieo.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze / null (the IEO
awards no honourable mentions; "Best in Economics/Finance" distinctions are not recorded).
Source verification: `python3 scripts/verify_corroboration.py` re-fetches every corroboration
URL and checks its content (the ieo-official.org results page is a Livewire app whose default
view shows the latest edition; the yearly sites carry the per-edition rankings).
