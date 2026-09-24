#!/usr/bin/env python3
"""
Corroboration for Brazil at the APhO (Asian Physics Olympiad; repo-standard). 2026-09-24 collection
pass. Brazil entered the APhO exactly once, the 22nd edition (India/Dehradun, held online 23-31 May
2022), with the statutory eight-student delegation; every other edition 2000-2026 is documented as
not entered (see GLOBAL_NOTES). The 2022 host site apho2022.in is gone (the domain was re-registered
by an unrelated publisher), so the official results table is cited through a Wayback capture.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def src(url, domain, cls, coverage, confirms, needle=None, timing="post", names=None):
    # timing = when the source was produced relative to the edition:
    # "post" (after it, reporting results/participation), "event" (during it),
    # "pre" (before it: selection/team announcements), "ref" (no edition-specific roster).
    # names: person ids (site/data/people.json slugs) a source names although its text cannot be
    # fetched or parsed here - curator attestation, read by site/scripts/check_source_names.py.
    d = {"url": url, "domain": domain, "cls": cls, "timing": timing,
         "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    if names:
        d["names"] = list(names)
    return d


RESULTS_PDF = ("https://web.archive.org/web/2022id_/https://apho2022.in/wp-content/uploads/"
               "2022/06/Results-for-website.pdf")

SOURCES = {
 2022: [src(RESULTS_PDF, "web.archive.org", "official", "5/8 (the awarded students)",
            "Official APhO 2022 results table of the host site apho2022.in (single international ranking, "
            "121 awards over 24 delegations; cutoffs Gold 42 / Silver 36 / Bronze 30 / Honorable mention 23): "
            "Gabriel Morais Barros BRZ_03 rank 32, 34.1 (bronze); Matheus Felipe Ramos Borges BRZ_05 rank 48, "
            "31.6 (bronze); Rafael Moreno Ribeiro BRZ_07 rank 61, 29.7 (HM); Paulo Henrique dos Santos Silva "
            "BRZ_02 rank 78, 27.4 (HM); Gabriel Verissimo Girao BRZ_08 rank 106, 24.7 (HM)",
            "Gabriel Morais Barros"),
        src("https://www.sbfisica.org.br/v1/olimpiada/2021/index.php/15-soif/"
            "302-equipes-brasileiras-para-as-olimpiadas-internacionais-de-2022.html",
            "sbfisica.org.br", "primary", "full (8/8) - team announcement",
            "SBF/OBF 'Equipes Brasileiras para as Olimpiadas Internacionais de 2022': the APhO team of eight "
            "with schools and states, alongside the IPhO five, EuPhO five and OIbF four",
            "APhO (Olimpíada Asiática de Física)", timing="pre"),
        src("https://www.objetivo.br/institucional/noticias.aspx?titulo=parabens-paulo-henrique-dos-santos-"
            "mencao-honrosa-na-olimpiada-asiatica-de-fisica-apho", "objetivo.br", "primary", "1/8",
            "Colegio Objetivo news + interview: Paulo Henrique dos Santos Silva, honourable mention at the 22nd "
            "APhO, hosted by India and held online 23-31 May 2022, 216 contestants from 27 countries, Brazil's "
            "first entry; the Brazilian team sat the papers together in one room in Campina Grande (PB) under "
            "camera invigilation; he qualified as 12th at the TBF",
            "Paulo Henrique dos Santos Silva"),
        src("https://noic.com.br/quem-somos/ex-colaboradores/", "noic.com.br", "primary", "2/8",
            "NOIC contributor biographies: Paulo Henrique 'mencao honrosa na APhO 2022'; Matheus Felipe "
            "classified for both IPhO and APhO in 2022, silver and bronze respectively, and 'um dos dois "
            "primeiros brasileiros a medalhar na APhO' - i.e. exactly two Brazilian medals, matching the "
            "official table's two bronzes",
            "menção honrosa na APhO 2022"),
        src("https://g1.globo.com/educacao/noticia/2022/07/20/em-feito-inedito-estudante-brasileiro-conquista-"
            "medalhas-de-bronze-em-olimpiadas-internacionais-de-fisica-e-quimica.ghtml",
            "g1.globo.com", "primary", "1/8",
            "G1 profile of Rafael Moreno Ribeiro (20 Jul 2022): his medal list includes 'Mencao Honrosa na "
            "APhO (2022)'",
            "Menção Honrosa na APhO (2022)"),
        src("https://www.sbfisica.org.br/v1/olimpiada/2021/index.php/15-soif/301-tbf-2022-premiados.html",
            "sbfisica.org.br", "primary", "full (8/8) - selection ranking",
            "SBF/OBF 'TBF/2022 - Premiados', the ranked final selection round: the APhO eight are ranks 1-5 "
            "(gold, also the IPhO team) plus ranks 11-13 (silver: Gabriel Verissimo Girao, Paulo Henrique dos "
            "Santos Silva, Arthur Ferreira Domont Sobreira)",
            "GABRIEL VERISSIMO GIRAO", timing="pre")],
}

NOTES = {
 2022: "22nd APhO, hosted by India (Dehradun, Graphic Era Hill University / IAPT) and held entirely online, "
       "23-31 May 2022; the Brazilian eight wrote the papers together in one invigilated room in Campina "
       "Grande (PB). Awards follow the single international ranking, never a country quota (statutes # 9: "
       "gold to 12% of official contestants, gold+silver 29%, gold+silver+bronze 51%, +honourable mention "
       "75%) - in 2022 that gave cutoffs 42/36/30/23 and 121 awards (11 gold, 13 silver, 34 bronze, 63 HM). "
       "The official table lists awardees only and uses per-contestant codes BRZ_01-BRZ_08; the three roster "
       "members it omits (BRZ_01, BRZ_04, BRZ_06 in an order the document does not disclose) therefore "
       "finished below the honourable-mention cut - Arthur Ferreira Domont Sobreira, Gustavo Esteche Araujo "
       "and Jose Alberto Feijao Tizon, recorded with a null medal.",
}

# Post-event evidence that is not a fetchable URL: person id -> short reason. Read by
# site/scripts/check_attendance.py, which counts it as a post-event naming source.
ATTESTED = {
 2022: {
  "arthur-ferreira-domont-sobreira": "competed without an award - the official post-event results table runs "
                                     "contestant codes BRZ_01-BRZ_08 and names only five of them, so the "
                                     "three roster members it omits sat the papers and scored below the "
                                     "honourable-mention cut (see the year note)",
  "gustavo-esteche-araujo": "competed without an award - same BRZ_01-BRZ_08 code evidence as above (see the "
                            "year note)",
  "jose-alberto-feijao-tizon": "competed without an award - same BRZ_01-BRZ_08 code evidence as above (see "
                               "the year note)",
 },
}

GLOBAL_NOTES = [
 "Brazil's APhO history is a single edition: the 22nd (2022). Team size is the statutory maximum - APhO "
 "statutes # 4, 'Each participating country shall send a delegation, normally comprising of eight students "
 "(contestants) and at most two accompanying persons (delegation leaders)': https://apho2026.kr/en/sub1_4.html",
 "Selection is the ordinary OBF pipeline (SOIF seletivas -> Torneio Brasileiro de Fisica): the APhO eight are "
 "TBF/2022 ranks 1-5 and 11-13. The EuPhO five (ranks 6-10) are absent - the 6th EuPhO ran 20-24 May 2022 in "
 "Ljubljana (https://eupho.ee/archive/), inside the APhO exam window of 23-31 May.",
 "Not entered, 1st-17th editions (2000-2016): the official APhO participant matrix lists 37 countries with "
 "their status per edition (H host, # present, G guest team, O observers only, - none) and Brazil appears in "
 "none of them: http://asianphysicsolympiad.org/Statistic_Participant_Countries.pdf",
 "Not entered, 18th-21st editions (2017-2021): the 20th APhO host's participating-countries page lists 22 "
 "countries and regions without Brazil (https://apho2019.asi.edu.au/about/participating-countries-2/); the "
 "21st (2021, Taipei, online) medal table reproduced by the next host covers 17 delegations without Brazil; "
 "and on the Brazilian side the OBF only raised APhO membership at a schools meeting of 11 Mar 2021, as a "
 "'equipe convidada em carater nao competitivo', concluding for that year that 'isso nao se mostrou factivel' "
 "while announcing negotiations for 2022: "
 "https://www.sbfisica.org.br/v1/olimpiada/2021/index.php/15-soif/260-participacao-na-apho.html . Colegio "
 "Objetivo's 2022 report calls the 22nd edition Brazil's 'primeira participacao'.",
 "No 2020 edition: 'Not held due to the COVID-19 pandemic' in the official host history, which also fixes the "
 "edition numbering and cities: https://apho2026.kr/en/sub1_2.html",
 "Not entered, 23rd-24th editions (2023-2024): the OBF formed no APhO team - the EQUIPE column of 'Premiados "
 "TBF 2023' assigns every awardee to IPhO, EuPhO or OIbF only "
 "(https://www.sbfisica.org.br/v1/olimpiada/2022/index.php/15-soif/323-premiados-tbf-2023.html), and an OBF "
 "notice of 22 Aug 2024 still reports the international committee 'buscando a participacao em outra Olimpiada "
 "Internacional de Fisica. No momento, estamos considerando a APhO e NBPhO' "
 "(https://app.graxaim.org/soif/2025/open_page/noticias_anteriores); the olympiad that materialised was the "
 "NBPhO in 2025.",
 "Not entered, 25th-26th editions (2025-2026): the 2025 host's participants page lists its delegations "
 "without Brazil (https://www.apho2025.sa/participants/), and the 2026 official ranking PDF (161 awarded "
 "students) carries no Brazilian country code (https://apho2026.kr/en/APhO_2026_ranking.pdf). The 2026 file "
 "covers awarded students only, i.e. the top 75%.",
 "Name spellings: the OBF team page and the TBF ranking print all eight in unaccented capitals; the official "
 "APhO table prints 'Gabriel Verissimo Girao' and 'Paulo Henrique Dos Santos Silva'. The dataset keeps the "
 "fullest documented forms, which for the five students shared with ipho/oibf/ioaa/olaa are those folders' "
 "accented spellings.",
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
        if y in ATTESTED:
            rec["attested"] = ATTESTED[y]
        records.append(rec)
    return records


def main():
    records = build_records()
    payload = {
        "olympiadId": "apho",
        "description": "Sources confirming Brazilian APhO contestants + results, per edition.",
        "provenanceClasses": {
            "official": "apho2022.in host-site results table (domain lost; cited through a Wayback capture).",
            "primary": "SBF/OBF team and selection pages, NOIC, Colégio Objetivo, press (G1).",
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
            attests = f" — attests: {', '.join(s['names'])}" if s.get("names") else ""
            details.append(f"{i}. **{s['domain']}** ({s['cls']}, {s['timing']}, coverage: {s['coverage']}) — {s['url']} — {s['confirms']}{attests}")
        if "attested" in r:
            details.append("")
            for pid, why in r["attested"].items():
                details.append(f"- *attested* `{pid}` — {why}")
        if "note" in r:
            details.append("")
            details.append(f"> {r['note']}")
        details.append("")
    md = ("# Per-Year Corroboration — Brazil at the APhO\n\n"
          "**Machine-readable:** `data/corroboration.json`. Rebuild: `python3 scripts/build_corroboration.py`; "
          "verify: `python3 scripts/verify_corroboration.py`. 2026-09-24 collection pass.\n\n## Notes\n\n"
          + "\n".join(f"- {n}" for n in GLOBAL_NOTES)
          + "\n\n## Summary\n\n| Year | Sources | Domains |\n|-----:|:--:|---------|\n" + "\n".join(lines)
          + "\n\n## Per-year sources\n\n" + "\n".join(details))
    with open(os.path.join(ROOT, "CORROBORATION.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Editions: {len(records)}")


if __name__ == "__main__":
    main()
