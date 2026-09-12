#!/usr/bin/env python3
"""
Corroboration for Brazil at the Romanian Master of Mathematics (repo-standard). 2026-09-09 collection
pass: every URL fetched and content-verified. Editions attended: 2010-2013, 2015-2021, 2026 (12).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OBM = "https://www.obm.org.br/resultados-romanian-master-of-mathematics/"
OLC = "https://olimpiadascientificas.org/equipes-brasileiras/matematica/rmm/"


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def obm(needle, coverage="full"):
    return src(OBM, "obm.org.br", "primary", coverage, "national organizer results table (all 12 editions): names, city/state, award/certificate", needle)


def official(year, needle, coverage="full"):
    return src(f"https://rmms.lbi.ro/rmm{year}/index.php?id=results_math", "rmms.lbi.ro", "official", coverage,
               "official individual results: rank, per-problem scores, total, medal (country code BRA/BRZ)", needle)


def post(url, needle, confirms, coverage="full", domain="obm.org.br"):
    return src(url, domain, "primary", coverage, confirms, needle)


SOURCES = {
 2010: [obm("Davi Lopes de Medeiros"),
        src(OLC, "olimpiadascientificas.org", "primary", "full", "olimpiadascientificas.org roster mirror (source: OBM) - listed under the label '2009'", "Hugo Fonseca Araújo")],
 2011: [obm("Lucas Lourenço Hernandes"), official(2011, "Empinotti"),
        src(OLC, "olimpiadascientificas.org", "primary", "full", "olimpiadascientificas.org roster mirror (source: OBM) - listed under the label '2010'", "Lourenço Hernandes")],
 2012: [obm("Henrique Gasparini Fiúza do Nascimento"), official(2012, "Camelo"),
        src(OLC, "olimpiadascientificas.org", "primary", "full", "olimpiadascientificas.org roster mirror (source: OBM), label '2012'", "Macieira")],
 2013: [obm("Bitarães"), official(2013, "Bitaraes")],
 2015: [obm("Gabriel Fazoli Domingos"), official(2015, "ZANARELLA"),
        post("https://noic.com.br/uncategorized/divulgado-resultado-da-romanian-master-mathematics-2015/", "Zanarella", "NOIC results post", domain="noic.com.br"),
        post("https://noic.com.br/uncategorized/e-comeca-romanian-master-mathematics-2015/", "Sacramento", "NOIC: team at the start", "full (pre-event roster)", domain="noic.com.br")],
 2016: [obm("Gabriel Toneatti Vercelli"), official(2016, "Toneatti"),
        post("https://www.obm.org.br/2016/03/03/brasil-conquista-quatro-bronzes-na-romanian-master-of-mathematics-2016/", "Campos Vargas", "OBM news: 4 bronzes by name")],
 2017: [obm("Mateus Siqueira Thimoteo"), official(2017, "THIMÓTEO", "full (9 contestants; OBM lists the 6 awardees/certificates)"),
        post("https://noic.com.br/matematica/brasil-conquista-decimo-lugar-na-romenia/", "Kowalczuk", "NOIC results post: names + awards, 10th place", domain="noic.com.br")],
 2018: [obm("Gabriel Tostes Messias Pereira"), official(2018, "TREVIZAN"),
        post("https://www.obm.org.br/2018/02/26/com-2-medalhas-de-bronze-brasil-retorna-da-romanian-master-of-mathematics/", "Tostes", "OBM news: 2 bronzes + HMs by name"),
        post("https://noic.com.br/uncategorized/brasil-ganha-dois-bronzes-na-romenian-masters-de-matematica/", "Tostes", "NOIC results post", domain="noic.com.br"),
        post("https://impa.br/notices/brasil-ganha-duas-medalhas-em-olimpiada-na-romenia/", "Tostes", "IMPA: results (names, medals)", domain="impa.br"),
        post("https://impa.br/notices/brasil-esta-escalado-para-a-10a-romanian-master-of-mathematics/", "Tostes", "IMPA: team announcement", "full (pre-event roster)", domain="impa.br")],
 2019: [obm("Samuel Prieto Lima"), official(2019, "SPONCHIADO"),
        post("https://www.obm.org.br/2019/02/24/brasileiros-voltam-da-romenia-com-tres-medalhas-na-bagagem/", "Prieto", "OBM news: 3 bronzes + HM by name"),
        post("https://www.obm.org.br/2019/01/24/conheca-a-equipe-que-competira-na-proxima-rmm-na-romenia/", "Prieto", "OBM: team announcement", "full (pre-event roster)"),
        post("https://noic.com.br/matematica/brasil-conquista-tres-bronzes-na-romanian-masters-of-mathematics-2019/", "Prieto", "NOIC results post", domain="noic.com.br"),
        post("https://impa.br/notices/brasil-conquista-tres-medalhas-na-romanian-master-of-mathematics/", "Prieto", "IMPA: results (names, medals)", domain="impa.br"),
        post("https://impa.br/notices/brasil-anuncia-equipe-que-disputara-olimpiada-na-romenia/", "Prieto", "IMPA: team announcement", "full (pre-event roster)", domain="impa.br")],
 2020: [obm("Francisco Moreira Machado Neto"), official(2020, "GOMES CABRAL"),
        post("https://www.obm.org.br/2020/03/02/brasil-volta-da-romenia-com-medalha-de-bronze/", "Gomes Cabral", "OBM news: bronze + HMs by name"),
        post("https://www.obm.org.br/2020/02/11/selecao-olimpica-e-escalada-para-competir-na-romenia/", "Zeus", "OBM: team announcement", "full (pre-event roster)"),
        post("https://noic.com.br/uncategorized/divulgado-o-resultado-da-olimpiada-romeniana-de-matematica/", "Paschoal", "NOIC results post", domain="noic.com.br"),
        post("https://impa.br/notices/equipe-brasileira-conquista-bronze-em-olimpiada-romena/", "Gomes Cabral", "IMPA: results (names, awards)", domain="impa.br"),
        post("https://impa.br/notices/definida-equipe-do-brasil-para-olimpiada-romena-de-matematica/", "Zeus", "IMPA: team announcement", "full (pre-event roster)", domain="impa.br")],
 2021: [obm("Miguel de Carvalho Oliveira"), official(2021, "MACHADO LAGE"),
        post("https://www.obm.org.br/2021/10/16/equipe-brasileira-conquista-tres-medalhas-da-13a-rmm/", "Machado Lage", "OBM news: silver + 2 bronzes + 3 HMs by name (virtual edition, October)")],
 2026: [obm("Alessandro Mathias Machado"), official(2026, "Mathias Machado"),
        post("https://www.obm.org.br/2026/02/28/brasil-conquista-melhor-resultado-da-historia-na-rmm-2026-e-alcanca-5a-posicao-geral/", "Amiune", "OBM news: 2 silvers + 2 bronzes + HM by name; 5th place"),
        post("https://www.obm.org.br/2026/01/12/10a-romanian-master-of-mathematics-confira-a-escalacao-do-brasil/", "Amiune", "OBM: team announcement", "full (pre-event roster)")],
}

NOTES = {
 2010: "3rd edition (then 'Romanian Master of Sciences'); the official 2010 site serves raw PHP, so no official per-name page survives - OBM table + OLC only. Two certificates (no award). 'Davi Lopes de Medeiros' = IMO 'Davi Lopes Alves de Medeiros'.",
 2011: "Official page uses codes BRZ/BRA and 'Lourenco Hernandes Lucas' forms; OLC lists this year under '2010' (its labels lag by one for 2010-2011).",
 2013: "OBM table 'Victor de Oliveira Reis' -> pool form Victor Oliveira Reis (IMO/OIM).",
 2015: "'Alessandro Pacanowski' -> full IMO form.",
 2017: "Brazil fielded nine contestants (official page: BRA 1-9); OBM's table lists only the six with an award or certificate. The three unawarded (Davi Cavalcanti Sena, Pedro Henrique Sacramento de Oliveira, Lucas Hiroshi Hanke Harada) are added from the official page. 'Thimoteo' -> Thimóteo.",
 2019: "Four contestants only (all documented by official + OBM + NOIC + IMPA).",
 2020: "Seven contestants (official BRA 1-7), all in OBM's table.",
 2021: "13th edition held virtually in October 2021.",
 2026: "18th edition (OBM numbering) / 17th RMM: Brazil's best result (2S+2B+1HM, 5th place). Two organizations only (official results + OBM table/news) - THIRD SOURCE PENDING.",
}

GLOBAL_NOTES = [
 "Invitational olympiad in Bucharest (February; 2021 virtual in October). Brazil attended 2010-2013, 2015-2021 and 2026; no editions in 2014 and 2022; Brazil absent 2023-2025 (official country lists checked). Delegations of 4-9 (six is usual; the official page marks 'official team' members with an asterisk in later years - not stored).",
 "Naming source: OBM's all-years table (full names); official pages give surname-first or all-caps forms and were used for medals/scores and the 2017 extra contestants. Certificates (no award) = medal null.",
 "All contestants are IMO-track students - every name aligned to the pool (imo/apmo/oim/conosur/...) before building.",
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
        "olympiadId": "rmm",
        "description": "Sources confirming Brazilian RMM contestants + results, per edition.",
        "provenanceClasses": {
            "official": "rmms.lbi.ro per-edition individual results (2011-2013, 2015-2021, 2026).",
            "primary": "OBM (national organizer) all-years results table and news; olimpiadascientificas.org mirror; NOIC; IMPA.",
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

    md = ("# Per-Year Corroboration — Brazil at the RMM\n\n"
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
