# Hall da Fama — site (v1: a Tabela)

Static, no build step, no dependencies. Vanilla HTML/CSS/JS.

## Run

```bash
python3 site/scripts/build_people.py   # regenerate data/people.json from the olympiad folders
python3 site/scripts/build_sources.py  # regenerate data/sources.json from corroboration trails
cd site && python3 -m http.server 8741 # then open http://localhost:8741/
```

## What v1 does

- **Pessoas view** (default): one row per person — participations, distinct olympiads,
  olympiad codes, year span, medal counts. Click a row → the student's page. Click
  headers to sort.
- **Participações view**: one row per participation (long format).
- **Person pages** (`person.html?id=<slug>`): name (+ source spellings), summary line,
  chronological trajectory with full olympiad names and per-year teammates (linked),
  and a **Fontes** section at the bottom — per-edition fact-check links
  (`scripts/build_sources.py` → `data/sources.json`).
  Teammates are computed client-side from shared (olympiad, year).
- **Filters**: name search (diacritic-insensitive), olympiad, field, scope, medal,
  year range — one visual register, no chips. All state lives in the URL → every
  view is shareable.
- **Export**: Copy TSV (pastes into Sheets), CSV, JSON — always of the current
  filtered view.
- Medal nuance: `—` = confirmed no-award; "pendente" = event not yet held. UI is monochrome — text codes, no colors/emoji.
- Light/dark via `prefers-color-scheme`.

## Files

```
scripts/build_people.py   entity resolution: all */src/data/graph.json -> data/people.json
                          (unified slugifier; prints every multi-variant merge for review)
scripts/aliases.json      cross-dataset identity fixes (e.g. Cindy Yushi/Yuchi Tsai)
data/people.json          GENERATED — canonical people + participations (1464 / 2979)
data/olympiads.json       olympiad metadata: code, name, field, scope, palette colors
index.html / style.css / app.js
```

## Adding a new olympiad dataset

1. Build the `<olympiad>/` folder per repo convention (graph.json etc.).
2. Add the id to `DATASETS` in `scripts/build_people.py`.
3. Add its entry (code/field/scope) to `data/olympiads.json`.
4. Re-run `build_people.py` — it ends with the **identity gate**: `find_duplicates.py`
   flags plausible same-person pairs (token-subset, initial-expansion, suffix, typo,
   first+last classes; blocked by surname; hard negatives: same-team co-occurrence and
   career span > 10 years). The build FAILS until every candidate is resolved into
   `scripts/aliases.json` (merge) or `scripts/distinct.json` (distinct, with reason).
   Never auto-merge; record every decision.

## Next (agreed direction, not yet built)

Stats page (participation histogram that filters the table, coverage matrix) ·
whole-dataset download links.
