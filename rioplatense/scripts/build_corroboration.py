#!/usr/bin/env python3
"""
Corroboration for Brazil at the Olimpíada Rioplatense de Matemática (repo-standard). 2026-09-09
collection pass: every URL fetched and content-verified. Editions: V (1996) - 32 (2025), none in 2020-2021.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


EDITION = {1996: 5, 1997: 6, 1998: 7, 1999: 8, 2000: 9, 2001: 10, 2002: 11, 2003: 12, 2004: 13, 2005: 14, 2006: 15, 2007: 16,
           2008: 17, 2009: 18, 2010: 19, 2011: 20, 2012: 21, 2013: 22, 2014: 23, 2015: 24, 2016: 25, 2017: 26, 2018: 27,
           2019: 28, 2022: 29, 2023: 30, 2024: 31, 2025: 32}
NEEDLE = {1996: "Catae", 1997: "Nascimento", 1998: "Honda Saito", 1999: "Alinson", 2000: "Gukovas", 2001: "Braun Vieira", 2002: "Luty",
          2003: "Carrah", 2004: "Regitano", 2005: "Sorensen", 2006: "Gleycianne", 2007: "Camelo", 2008: "Guinsberg", 2009: "Achjian",
          2010: "Tsuzuki", 2011: "Fazoli", 2012: "Hisatsuga", 2013: "Nishimoto", 2014: "Degelo", 2015: "Dominguez", 2016: "Ticianelli",
          2017: "Saneshima", 2018: "Maziviero", 2019: "Vichinsky", 2022: "Busetti", 2023: "Stabenow", 2024: "Koshimizu", 2025: "Gastao"}


def oma(year):
    n = EDITION[year]
    if n == 32:
        url = "https://oma.org.ar/contents/paginas/contents/32_rio_resultados.html"
    elif n >= 21 or n == 11:
        url = f"https://oma.org.ar/old_oma/internacional/resultados-omr{n}.html"
    else:
        url = f"https://oma.org.ar/old_oma/internacional/resultados-omr{n}.htm"
    return src(url, "oma.org.ar", "official", "medallists and honourable mentions only",
               f"OMA medal table of the {n}th Rioplatense: name, team (Fortaleza / San Pablo / Brasil), level, medal", NEEDLE[year])


SOURCES = {y: [oma(y)] for y in EDITION}
SOURCES[1996].append(src("https://noic.com.br/olimpiadas/matematica/rioplatense/", "noic.com.br", "primary", "format description only (no names)",
                         "NOIC: Brazil = the only country with two teams (Fortaleza via OCM, São Paulo via OPM); four levels A/1/2/3", None))

NOTES = {
 1996: "Debut (V edition, Mendoza): two Brazilians under the single label 'Brasil' (Catae silver, Arroyo Ruiz gold). Editions I-IV (1992-95) have no published participant data.",
 1997: "From 1997 OMA labels the two Brazilian teams 'Fortaleza' and 'SAO' / 'Sao Paulo' / 'San Pablo' / 'São Pablo' (label drift, all normalised to São Paulo). 1997-1999 tables are surname-first ('Abe, Eduardo') and were reordered.",
 1998: "'Thiago Costa' (Fortaleza, Nivel 1) written as Thiago Barros Rodrigues Costa - ASSUMED (Fortaleza, OIM/IMO 2001).",
 2000: "'Ulises Albuquerque' (Nivel 3) = Maio 1998 'Ulisses Medeiros de Albuquerque' (Fortaleza) - assumed. 'Adriano Vieira' (Nivel A) = 2001 'Adriano Jorge Braun Vieira Neto'.",
 2001: "OMA's page has mojibake spaces inside accented words ('Andr é', 'Per ú') - repaired before parsing.",
 2002: "OMA's page repeats the Nivel 1 silver trio (Katz, Luty Rodrigues Ribeiro, Kozynski) verbatim under 'Medallas de Bronce / Nivel A' - the duplicated bronze row is dropped (a student sits one level).",
 2003: "'Israel Franklin Dourado Carrah' - fullest form, adopted in conosur/ too.",
 2009: "Only São Paulo medallists appear (18th edition); Fortaleza's attendance that year is undetermined (medal-only table).",
 2010: "Rows carry the medal and team on one line ('Medalla de Oro Fortaleza') - parsed accordingly.",
 2012: "Short forms in OMA's table (Bruno Meinhart, Daniel Lima, Pedro Costa, Tadeu Belfort, Lucca Siaudzionis, Rafael Rodrigues) expanded against the pool (all Fortaleza/São Paulo juniors of the Maio/Cono Sur pipeline).",
 2013: "'Matheus Carioca' (Fortaleza, Nivel 2) written as Matheus Carioca Sampaio (OIbF) - assumed.",
 2018: "Honourable mentions first appear in OMA's tables (2018, 2019, 2023-2025).",
 2025: "32nd edition (new OMA CMS page): surnames in capitals ('Davi LIMA MAIA'), title-cased here; fuller forms adopted for Alice Ella Schneider and Heloísa Guedes de Azevedo O. Mysczak (EGMO short forms).",
}

GLOBAL_NOTES = [
 "OMA (Argentina) publishes one medal table per edition - medallists and, since 2018, honourable mentions - so the dataset is medallists-only: non-medalling Brazilians are unknown and delegation sizes (normally 3 per level per team) cannot be reconstructed from it.",
 "Two Brazilian teams compete (Fortaleza and São Paulo); the 'team' field keeps OMA's label. Levels: A (grades 6-7), 1 (8-9), 2 (10-11), 3 (12).",
 "OMA's pages are the only per-name source online (no OBM page exists - the teams are selected by the Ceará and São Paulo state olympiads); NOIC describes the format only. Every edition is therefore single-source, official.",
 "rawName policy: OMA forms normalised (surname-first reordered, capitals title-cased, mojibake repaired) and short forms expanded against the pool; assumed identities are flagged per year.",
]

YEARS = sorted(SOURCES)


def build_records():
    records = []
    for y in YEARS:
        srcs = SOURCES[y]
        naming = [s for s in srcs if s["cls"] in ("official", "primary", "archive")]
        indep = [s for s in srcs if s["cls"] in ("official", "primary")]
        rec = {"year": y, "namingSourceCount": len(naming), "independentPrimaryCount": len(indep),
               "meetsThreeNaming": len(naming) >= 3, "meetsThreePrimary": len(indep) >= 3, "sources": srcs}
        if y in NOTES:
            rec["note"] = NOTES[y]
        records.append(rec)
    return records


def main():
    records = build_records()
    payload = {
        "olympiadId": "rioplatense",
        "description": "Sources confirming Brazilian Rioplatense medallists, per edition.",
        "provenanceClasses": {
            "official": "oma.org.ar per-edition medal tables (old site .htm/.html pages and the new-CMS 32nd-edition page).",
            "primary": "NOIC format page (no names).",
            "archive": "(none)",
        },
        "globalNotes": GLOBAL_NOTES,
        "years": records,
    }
    with open(os.path.join(ROOT, "data", "corroboration.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")

    lines = []
    for r in records:
        doms = ", ".join(dict.fromkeys(s["domain"] for s in r["sources"]))
        flag = "" if r["namingSourceCount"] >= 2 else "  (single-source)"
        note = " *" if "note" in r else ""
        lines.append(f"| {r['year']} | {r['namingSourceCount']} | {doms}{flag}{note} |")

    details = []
    for r in records:
        details.append(f"### {r['year']}")
        for i, s in enumerate(r["sources"], 1):
            details.append(f"{i}. **{s['domain']}** ({s['cls']}, coverage: {s['coverage']}) — {s['url']} — {s['confirms']}")
        if "note" in r:
            details.append("")
            details.append(f"> {r['note']}")
        details.append("")

    md = ("# Per-Year Corroboration — Brazil at the Olimpíada Rioplatense de Matemática\n\n"
          "**Machine-readable:** `data/corroboration.json`. Rebuild: `python3 scripts/build_corroboration.py`; "
          "verify: `python3 scripts/verify_corroboration.py`. 2026-09-09 collection pass.\n\n## Notes\n\n"
          + "\n".join(f"- {n}" for n in GLOBAL_NOTES)
          + "\n\n## Summary\n\n| Year | Sources | Domains |\n|-----:|:--:|---------|\n" + "\n".join(lines)
          + "\n\n## Per-year sources\n\n" + "\n".join(details))
    with open(os.path.join(ROOT, "CORROBORATION.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Editions: {len(records)}")
    print("Wrote data/corroboration.json + CORROBORATION.md")


if __name__ == "__main__":
    main()
