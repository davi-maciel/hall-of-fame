# APhO — Asian Physics Olympiad

Brazilian students at the APhO (Asian Physics Olympiad, held annually since 2000). Part of the
hall-of-fame data collection — one olympiad per folder, shared schema.

Coverage: complete. Brazil took part in one edition, the 22nd APhO (hosted by India in Dehradun and
held online, 23–31 May 2022), with the statutory eight-student delegation: two bronze medals, three
honourable mentions and three students who finished below the award cut. The APhO ranks all
contestants on one international list and awards medals by percentage of the field, so there is no
per-country quota.

```
data/raw/apho.json       canonical records (name, year, medal, rank, score) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/apho.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention / null. Source verification: `python3 scripts/verify_corroboration.py` re-fetches
every corroboration URL and checks its content (the 2022 host site is gone, so the official results
table is cited through a Web Archive capture).
