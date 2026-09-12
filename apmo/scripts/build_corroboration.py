#!/usr/bin/env python3
"""
Corroboration for Brazil at the APMO (repo-standard). 2026-09-08 collection pass:
every URL fetched and content-verified. Editions: 2010-2026 (17, all attended, 10 per year).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OBM = "https://www.obm.org.br/resultados-apmo/"


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def official(year, needle):
    return src(f"https://www.apmo-official.org/country_report/BRA/{year}", "apmo-official.org", "official", "full",
               "official per-name results: in-country rank, total score, award", needle)


def pdf(year, needle, coverage="awardees only (10/10)"):
    return src(f"https://www.apmo-official.org/static/results/apmo{year}_res.pdf", "apmo-official.org", "official", coverage,
               "official results PDF: country table (rank, score, G/S/B/HM counts) + award lists by name", needle)


def obm(needle):
    return src(OBM, "obm.org.br", "primary", "full",
               "national organizer results table (all years): full names, city/state, points, award", needle)


def post(url, needle, confirms="OBM news: full results table"):
    return src(url, "obm.org.br", "primary", "full", confirms, needle)


SOURCES = {
 2010: [official(2010, "Camelo Sá"), pdf(2010, "Empinotti", "awardees only (7/10 — no HMs)"), obm("Marcelo Tadeu de Sá Oliveira Sales")],
 2011: [official(2011, "Braga Costa"), pdf(2011, "Macieira"), obm("Hanon Guy Lima Rossi")],
 2012: [official(2012, "Miyazaki"), pdf(2012, "Rodrigo Sanches"), obm("Rafael Kazuhiro Miyazaki")],
 2013: [official(2013, "Zanarella"), pdf(2013, "Zanarella"), obm("Murilo Corato Zanarella"),
        src("https://noic.com.br/uncategorized/resultados-apmo/", "noic.com.br", "primary", "medal counts only",
            "1G/2S/4B/3HM and 9th place; links the official PDF", None)],
 2014: [official(2014, "Santana Rocha"), pdf(2014, "Santana Rocha"), obm("Daniel Santana Rocha")],
 2015: [official(2015, "Sichinel"), pdf(2015, "Sacramento"), obm("Valentino Amadeus Sichinel"),
        src("https://noic.com.br/matematica/saiu-o-resultado-da-apmo-2015/", "noic.com.br", "primary", "full",
            "NOIC results post: 10 names + awards", "Valentino Amadeus Sichinel"),
        src("https://web.archive.org/web/20161224154153/http://www.obm.org.br/opencms/competicoes/internacionais/apmo.html",
            "obm.org.br (Wayback)", "archive", "full", "OBM's former site (2016 snapshot): 2015 table with city/state, points, award", "Sichinel")],
 2016: [official(2016, "Kowalczuk"), obm("Diemison Vargas de Cerqueira"),
        src("https://noic.com.br/matematica/divulgado-o-resultado-da-asian-pacific-mathematics-olympiad/", "noic.com.br", "primary", "full",
            "NOIC results post: 10 names, points, awards", "Diemison Vargas de Cerqueira")],
 2017: [official(2017, "Thimoteo"), obm("Mateus Siqueira Thimoteo"),
        post("https://www.obm.org.br/2017/05/22/resultado-da-asian-pacific-mathematics-olympiad-apmo/", "Mateus Siqueira Thimoteo")],
 2018: [official(2018, "Meinhart"), obm("Bruno Brasil Meinhart")],
 2019: [official(2019, "Ishiyi"), obm("Othon Daiki Ishiyi"),
        post("https://www.obm.org.br/2019/06/12/divulgado-o-resultado-da-asian-pacific-mathematics-olympiad-apmo-2019/", "Othon Daiki Ishiyi")],
 2020: [official(2020, "Saraiva de Moraes"), obm("Luciano Rodrigues de Oliveira Junior")],
 2021: [official(2021, "Prado Porto"), obm("Yvens Ian Prado Porto"),
        post("https://www.obm.org.br/2021/06/09/15161/", "Yvens Ian Prado Porto")],
 2022: [official(2022, "Lengruber"), obm("Fabrícia Cardoso Marques"),
        post("https://www.obm.org.br/2022/06/02/17226/", "Fabrícia Cardoso Marques", "OBM news: full results table; 15th of 35 countries")],
 2023: [official(2023, "Constancio"), obm("Caio Harley Constancio Neves"),
        post("https://www.obm.org.br/2023/07/24/20395/", "Caio Harley Constancio Neves", "OBM news: full results table; 11th of 38")],
 2024: [official(2024, "Ursino"), obm("Gabriel Bastos Vasconcelos Duarte"),
        post("https://www.obm.org.br/2024/08/15/divulgados-os-resultados-internacionais-da-apmo-2024/", "Gabriel Bastos Vasconcelos Duarte", "OBM news: full results table; 12th of 39")],
 2025: [official(2025, "Portella"), obm("Alessandro Mathias Machado"),
        post("https://www.obm.org.br/2025/08/08/brasil-fica-na-8a-posicao-na-apmo-2025/", "Alessandro Mathias Machado", "OBM news: full results table; 8th of 37")],
 2026: [official(2026, "Ivamoto"), obm("Enzo Ivamoto Hirota"),
        post("https://www.obm.org.br/2026/06/04/24708/", "Enzo Ivamoto Hirota")],
}

NOTES = {
 2010: "AWARD CONFLICT: the official per-year page marks ranks 8-10 (9, 8, 8 pts) as Hon. Men., but the official 2010 results PDF (Brazil: 0 G / 3 S / 4 B / 0 HM, and none of the three in its award lists), the official all-years summary (0 HM) and OBM ('Certificado') all say no award -> medal null. Root cause (site repo leomtz/apmowebsite, commit 'Brazil names 2010 and 2011', 2020-06-09): the 2010-11 Brazil rows were keyed in by the site maintainer without per-problem scores (all '-') and the awards follow the generic 1/2/4/3 template, so ranks 8-10 got 'Hon. Men.' by pattern, not from a source. Official page typo 'Basbosa Alves' = Deborah Barbosa Alves.",
 2011: "Official page typo 'Medes Silva' = Maria Clara Mendes Silva; 'Henrique G.' expanded to Henrique Gasparini (2012 official page, IMO dataset).",
 2012: "Official 'Alessandro A. P. de Oliveira Pacahowski' / OBM 'Pacanowsky' = Alessandro Augusto Pinto de Oliveira Pacanowski (IMO 2013-14 form). The PDF award list misprints 'Angels Rodrigo Sanches'.",
 2013: "Official 'de Silva Reis, Lucas' = Lucas da Silva Reis (OBM). OBM's 2013 row drops the 'de' of Franco Matheus de Alencar Severo (2012 row, official page, IMO) - full form used so the slug does not split.",
 2014: "OBM 'Arthur do Nascimento' (São Paulo - SP, HM) = Arthur Ferreira do Nascimento: an OBM 2013 honourable mention from São Paulo (which is what makes a student APMO-eligible) and the IOI/OII 2014 contestant.",
 2015: "Official typos 'Toeatti Vercelli' and 'Galvão de Barrons'; OBM, NOIC and the archived OBM page agree on Toneatti Vercelli / Galvão de Barros.",
 2016: "'Cariveiro Porto' (official page AND OBM's APMO table) is a shared typo: OBM's own award lists 2013-2016, its Cono Sur 2015 table/news and NOIC all say Vitor Augusto CARNEIRO Porto (Fortaleza) -> Carneiro retained (corrected 2026-09-09). NOIC typo 'Saramento'. Davi Cavalcanti Sena listed as Recife - PE here and Fortaleza - CE in 2017.",
 2017: "OBM writes 'Thimoteo' here; its award lists 2013-15 and the Cono Sur table say Thimóteo (accented form used).",
 2018: "Two-source year (no OBM news post found). OBM table typo 'Samuel Pietro Lima' (official + OBM 2019: Prieto).",
 2020: "Two-source year. OBM drops the 'Neto' of Francisco Moreira Machado Neto (official has it in 2019 and 2020).",
 2021: "'Domingues' (official page AND OBM, 2021 only) is a one-year variant of Rodrigo Salgado Domingos Porto (2020/22/23 + IMO). Score conflict at rank 4: official 16 vs OBM 15 — official retained.",
 2022: "Two non-awardees (11 and 8 pts) rank above the honourable mention (8 pts): APMO HMs require a complete solution to one problem.",
 2023: "OBM 'Castelo Branco' -> Castello Branco (official, OBM 2025, IMO). The official page splits 'Luís Felipe Pestana Giglio' and 'Leonardo Henrique Fakhreddine Maldonado' at the wrong token.",
 2025: "OBM table 'Davi Li Chiun Liu' vs official 'David': the OBM 2024 awards list (São Paulo - SP) also says David -> David retained.",
 2026: "Two independent organizations only (official DB + OBM table + OBM news); no third-party coverage found (searched 2026-09-08) — THIRD SOURCE PENDING. Rank 8 (14 pts, no complete solution) is a non-awardee below two HMs with the same total.",
}

GLOBAL_NOTES = [
 "Correspondence olympiad: sat in Brazil (March) by OBM awardees; the ten best papers are sent to the Japan-based committee. The official page's 'rank' is the in-country rank 1-10, not a global rank. Awards per country are capped at 1G/2S/4B/3HM, so year-to-year medal counts are near-constant.",
 "rawName policy: OBM full forms (with diacritics) instead of the official site's Last/First split; where the person is already in the IMO dataset the IMO spelling is used (most-complete documented form). Score = official total (5 problems x 7).",
 "Pre-2016 per-contestant pages exist only for Australia, Brazil and the Philippines (the three countries whose historical data reached the site maintainer); every other country/year before 2016 returns HTTP 500. Brazil's 2012-15 rows come from OBM PDFs archived in the site repo, 2010-11 were keyed in by hand.",
 "The official site (a volunteer-built DB) carries several name typos (Basbosa, Medes, Toeatti, Barrons, Pacahowski, mis-split given names); OBM's table has its own (Pietro, Castelo, Domingues, Davi, Pacanowsky). Every deviation is resolved in the per-year notes.",
 "medal null = confirmed no-award (official award column empty; OBM 'Certificado'). 2010 is the one year where the official per-year page and the official PDF disagree — the PDF wins (see note).",
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
        "olympiadId": "apmo",
        "description": "Sources confirming Brazilian APMO contestants + results, per edition.",
        "provenanceClasses": {
            "official": "apmo-official.org per-country/per-year results DB and the official results PDFs (2010-2015).",
            "primary": "OBM (national organizer) all-years results table and per-year news posts; NOIC.",
            "archive": "Wayback snapshot of OBM's former site (2015 table).",
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

    md = ("# Per-Year Corroboration — Brazil at the APMO\n\n"
          "**Machine-readable:** `data/corroboration.json`. Rebuild: `python3 scripts/build_corroboration.py`; "
          "verify: `python3 scripts/verify_corroboration.py`. 2026-09-08 collection pass.\n\n## Notes\n\n"
          + "\n".join(f"- {n}" for n in GLOBAL_NOTES)
          + "\n\n## Summary\n\n| Year | Sources | Domains |\n|-----:|:--:|---------|\n" + "\n".join(lines)
          + "\n\n## Per-year sources\n\n" + "\n".join(details))
    with open(os.path.join(ROOT, "CORROBORATION.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Editions: {len(records)}")
    print("Wrote data/corroboration.json + CORROBORATION.md")


if __name__ == "__main__":
    main()
