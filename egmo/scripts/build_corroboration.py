#!/usr/bin/env python3
"""
Corroboration for Brazil at the EGMO (repo-standard). 2026-09-08 collection pass:
every URL fetched and content-verified. Editions: 2017-2026 (10, all attended, 4 per year).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
COUNTRY = "https://www.egmo.org/countries/country51/"
OBM = "https://www.obm.org.br/resultados-european-girls-mathematical-olympiad/"


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def country(needle):
    return src(COUNTRY, "egmo.org", "official", "full",
               "official country page: roster, per-problem scores, awards, leaders, stable person ids", needle)


def board(n, needle):
    return src(f"https://www.egmo.org/egmos/egmo{n}/scoreboard/", "egmo.org", "official", "full",
               "official edition scoreboard: rank, per-problem scores, award", needle)


def obm(needle):
    return src(OBM, "obm.org.br", "primary", "full",
               "national organizer results table (all years): full names, city/state, award", needle)


def post(url, needle, confirms="OBM news: full team result", coverage="full", domain="obm.org.br"):
    return src(url, domain, "primary", coverage, confirms, needle)


def impa(url, needle, confirms, coverage="full"):
    return src(url, "impa.br", "primary", coverage, confirms, needle)


def noic(url, needle, confirms, coverage="full"):
    return src(url, "noic.com.br", "primary", coverage, confirms, needle)


SOURCES = {
 2017: [country("Jamille Rebouças"), board(6, "Saltiel"), obm("Juliana Carvalho de Souza"),
        post("https://www.obm.org.br/2017/04/06/equipe-feminina-embarca-para-a-suica/", "Juliana Carvalho de Souza",
             "OBM news: 2 bronzes + HM by name, fourth member named, 26th place")],
 2018: [country("Débora Yamato"), board(7, "Yamato"), obm("Débora Tami Yamato"),
        post("https://www.obm.org.br/2018/04/14/brasil-encerra-participacao-na-egmo-2018-com-2-pratas-e-2-bronzes/", "Mariana Quirino de Oliveira",
             "OBM news: 4 medals by full name + points, leaders, 13th place"),
        impa("https://impa.br/notices/sbm-e-impa-anunciam-equipe-feminina-que-disputara-a-egmo/", "Mariana Quirino de Oliveira",
             "IMPA: team announcement (full names, cities, leaders)", "full (pre-event roster)"),
        noic("https://noic.com.br/matematica/egmo/brasil-conquista-2-bronzes-e-2-pratas-na-egmo/", "Mariana Quirino",
             "NOIC results post: 4 names (short forms), points, medals, 13th place"),
        noic("https://noic.com.br/uncategorized/divulgado-o-time-brasileiro-da-egmo/", "Débora Tami Yamato",
             "NOIC team announcement", "full (pre-event roster)")],
 2019: [country("Bruna Shoji Nakamura"), board(8, "Bigolin"), obm("Mariana Bigolin Groff"),
        post("https://www.obm.org.br/2019/04/11/egmo-2019-ouro-inedito-para-o-brasil-na-ucrania/", "Bruna Arisa Shoji Nakamura",
             "OBM news: gold + 2 bronzes by full name, fourth member named, 20th place"),
        impa("https://impa.br/notices/equipe-feminina-escalada-para-a-disputa-de-olimpiada-na-ucrania/", "Bruna Arisa Shoji Nakamura",
             "IMPA: team announcement (full names, ages, cities)", "full (pre-event roster)"),
        noic("https://noic.com.br/matematica/brasil-ganha-ouro-inedito-na-egmo/", "Mariana Groff",
             "NOIC results post: 4 names (short forms), points, medals, 20th place")],
 2020: [country("Carolina Moura Valle Costa"), board(9, "Stroeh"), obm("Carolina Moura Valle Costa"),
        post("https://www.obm.org.br/2020/04/21/prata-e-bronze-veja-o-resultado-do-brasil-na-egmo-2020/", "Letícia Barbieri Stroeh",
             "OBM news: 4 medals by full name, points, ranks, 15th place"),
        impa("https://impa.br/notices/equipe-brasileira-conquista-quatro-medalhas-na-egmo-2020/", "Carolina Moura Valle Costa",
             "IMPA: results (full names, cities, medals)"),
        impa("https://impa.br/notices/conheca-as-competidoras-que-vao-representar-o-brasil-na-egmo/", "Letícia Barbieri Stroeh",
             "IMPA: team announcement (full names, cities)", "full (pre-event roster)"),
        noic("https://noic.com.br/matematica/brasil-conquista-15-lugar-na-egmo/", "Carolina Costa",
             "NOIC results post: 4 names (short forms) + medals, 15th place"),
        noic("https://noic.com.br/matematica/confira-a-equipe-que-representara-o-brasil-na-egmo-2020/", "Carolina Moura Valle Costa",
             "NOIC team announcement with selection scores", "full (pre-event roster)")],
 2021: [country("Laís Nuto Rossman"), board(10, "Rossman"), obm("Laís Nuto Rossman"),
        post("https://www.obm.org.br/2021/04/15/com-tres-medalhas-de-bronze-brasil-encerra-participacao-na-egmo-2021/", "Gabriella Santana Morgado",
             "OBM news: 3 bronzes by full name, fourth member named, leaders, 23rd place")],
 2022: [country("Larissa Lemos Afonso"), board(11, "Mileski"), obm("Larissa Lemos Afonso"),
        post("https://www.obm.org.br/2022/04/11/equipe-brasileira-conquista-tres-bronzes-na-egmo-2022/", "Larissa Lemos Afonso",
             "OBM news: 3 bronzes by full name, fourth member (certificate), leaders, 24th place")],
 2023: [country("Isabela Ruthner Dorn"), board(12, "Kochloukova"), obm("Cecília Mileski de Paula"),
        post("https://www.obm.org.br/2023/04/18/equipe-brasileira-conquista-duas-medalhas-de-bronze-e-uma-mencao-honrosa-na-egmo-2023/", "Endy Lumy Okamura Miyashita",
             "OBM news: 2 bronzes + HM by name, fourth member named, 27th place"),
        impa("https://impa.br/notices/equipe-brasileira-conquista-2-medalhas-de-bronze-na-12a-egmo/", "Endy Lumy Okamura Miyashita",
             "IMPA: results (all four named)"),
        noic("https://noic.com.br/matematica/resultado-egmo/", "Cecilia Mileski",
             "NOIC results post: 3 awardees (short forms), 27th place", "partial (3/4)"),
        noic("https://noic.com.br/uncategorized/time-da-egmo-2023/", "Bilhana Kochloukova",
             "NOIC team announcement (short forms) + leaders", "full (pre-event roster)")],
 2024: [country("Luiza Akemi Bidoia de Freitas"), board(13, "Bidoia"), obm("Luiza Akemi Bidoia de Freitas"),
        post("https://www.obm.org.br/2024/04/15/brasil-brilha-na-egmo-2024-uma-medalha-de-prata-e-tres-de-bronze-conquistadas-na-georgia/", "Luiza Akemi Bidoia de Freitas",
             "OBM news: silver + 3 bronzes by full name with points, leaders, 22nd place"),
        impa("https://impa.br/notices/brasil-conquista-uma-medalha-de-prata-e-tres-de-bronze-na-egmo-2024/", "Luiza Akemi Bidoia de Freitas",
             "IMPA: results (all four named, states)"),
        impa("https://impa.br/notices/egmo-2024-comeca-nesta-quinta-feira-11-na-georgia/", "Luiza Akemi Bidoia de Freitas",
             "IMPA: team at the opening (full names, leaders)", "full (pre-event roster)")],
 2025: [country("Ana Beatriz Pazó"), board(14, "Mysczak"), obm("Alice Schneider"),
        post("https://www.obm.org.br/2025/04/16/brasil-brilha-na-14a-european-girls-mathematical-olympiad-egmo-2025/", "Alice Schneider",
             "OBM news: 2 silvers + bronze + HM by name, leaders, 20th place")],
 2026: [country("Maria Cecília Ribeiro Pereira de Melo"), board(15, "Leguiza"), obm("Julia de Paula Pessoa Leguiza"),
        post("https://www.obm.org.br/2026/04/13/brasil-faz-historia-na-15a-european-girls-mathematical-olympiad-egmo-2026-em-bordeaux/", "Maria Cecília Ribeiro Pereira de Melo",
             "OBM news: G/S/B/HM by full name, leaders, 15th place"),
        impa("https://impa.br/notices/medalhistas-da-obmep-sao-laureadas-em-olimpiada-feminina-internacional/", "Heloísa Mysczak",
             "IMPA: results (all four named, short forms for two), 15th place")],
}

NOTES = {
 2017: "Debut year, two organizations only (egmo.org, OBM). Names: OBM 'Jamile Falcão Rebouças' (also her own NOIC byline) vs egmo.org 'Jamille'; 'Julia' (egmo.org + OBM news) vs 'Júlia' (OBM table) — majority forms kept.",
 2018: "egmo.org short forms expanded per OBM/IMPA (Ana Beatriz Cavalcante Pires de Castro Studart, Mariana Quirino de Oliveira, Débora Tami Yamato).",
 2019: "egmo.org 'Bruna Shoji Nakamura' (2019) / 'Bruna Arisa Shoji Nakamura' (2021) share person1378; 'Mariana Groff' (2017-18) / 'Mariana Bigolin Groff' (2019) share person911.",
 2020: "Virtual edition. Carolina Moura Valle Costa (Itu/Etapa SP) and Letícia Barbieri Stroeh (Campinas/Etapa Valinhos) are the same people as in the egoi/ioi/oii datasets (OBI rosters) — merged at site level by exact name.",
 2021: "Virtual edition. OBM news typo 'Laís Nuno Rossman' (OBM table + egmo.org: Nuto).",
 2022: "Endy Lumy Okamura Miyashita (Fortaleza, Farias Brito) = the EGOI 2022-23 contestant in egoi/ (OBI roster).",
 2023: "OBM/IMPA 'Koshloukova' vs egmo.org 'Kochloukova' (also the OBM 2026 post, as deputy leader) — Kochloukova retained. OBM/IMPA typo 'Isabela Ruthner Dom'.",
 2024: "Maria Clara Fontes Silva (Aracaju - SE, Coesi) = the EGOI/IOI/OII contestant — same school and city in OBI's roster; OBM 2024 awards list (Nível 2 gold, Aracaju - SE). Also APMO 2026.",
 2026: "Held 12-18 April 2026, Bordeaux. Three independent organizations (egmo.org, OBM, IMPA). 'Julia' (OBM table, egmo.org) vs 'Júlia' (OBM news, IMPA) — table form kept. Brazil's 2nd gold ever; 15th place = 2nd-best team result.",
}

GLOBAL_NOTES = [
 "Guest (non-European) team since the 2017 debut; four contestants per year; egmo.org publishes full per-name results with stable person ids, which confirm every multi-year identity used here.",
 "rawName policy: fullest documented form (OBM table / OBM news / IMPA) where egmo.org abbreviates; medal null = confirmed no-award (empty award cell on the official scoreboard; OBM 'Certificado'). Score = official total (6 problems x 7).",
 "OBM's all-years table is the naming source for every edition; egmo.org is the award source (the two never disagree on awards).",
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
        "olympiadId": "egmo",
        "description": "Sources confirming Brazilian EGMO contestants + results, per edition.",
        "provenanceClasses": {
            "official": "egmo.org country page (BRA) and per-edition scoreboards.",
            "primary": "OBM (national organizer) all-years results table and per-year news; IMPA news; NOIC.",
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

    md = ("# Per-Year Corroboration — Brazil at the EGMO\n\n"
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
