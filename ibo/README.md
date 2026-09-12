# IBO — International Biology Olympiad

Brazilian students at the IBO. Part of the hall-of-fame data collection —
one olympiad per folder, shared schema.

Coverage: 2006, 2008–2019, 2021–2026 — every edition Brazil competed in
(2007 not attended; the 2020 IBO Challenge was non-competitive and is not listed).

```
data/raw/ibo.json        canonical records (name, year, medal) — edit this file
data/corroboration.json  per-edition source URLs (provenance class, coverage, verified needle)
scripts/build_graph.py   data/raw/ibo.json -> src/data/graph.json
src/data/graph.json      students + co-participation edges + metadata
```

Rebuild: `python3 scripts/build_graph.py`. Medal values: gold / silver / bronze /
honorable-mention (Certificate of Merit) / null. Source verification:
`python3 scripts/verify_corroboration.py` re-fetches every corroboration URL and checks its content.
