#!/usr/bin/env python3
"""
Corroboration for Brazil at the Cono Sur / Cone Sul Mathematical Olympiad (repo-standard).
2026-09-09 collection pass: every URL fetched and content-verified.
Editions: 1988, 1991-2026 (37; none held in 1989-1990).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OBM = "https://www.obm.org.br/resultados-olimpiada-de-matematica-do-cone-sul/"
OLC = "https://olimpiadascientificas.org/equipes-brasileiras/matematica/cone-sul/"
WB = "https://web.archive.org/web/20171226121934/http://www.obm.org.br/opencms/competicoes/internacionais/"


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def obm(needle, coverage="full"):
    return src(OBM, "obm.org.br", "primary", coverage,
               "national organizer results table (all 37 editions): names, city/state, medal/certificate", needle)


def olc(needle, coverage="full"):
    return src(OLC, "olimpiadascientificas.org", "primary", coverage,
               "olimpiadascientificas.org roster mirror (source: OBM), 1988-2013", needle)


def wb(page, needle, confirms, coverage="full"):
    return src(WB + page, "obm.org.br (Wayback)", "archive", coverage, confirms, needle)


def post(url, needle, confirms="OBM news: full team result", coverage="full", domain="obm.org.br"):
    return src(url, domain, "primary", coverage, confirms, needle)


NEEDLE = {
 1988: "Bazkhaus", 1991: "Palmeira", 1992: "Pompeu", 1993: "Esteves", 1994: "Balreira", 1995: "Aroldo", 1996: "Vajapeyam",
 1997: "Iveson", 1998: "Simoni Gouveia", 1999: "Sobreira", 2000: "Naves de Brito", 2001: "Einstein", 2002: "Carrah",
 2003: "Hsu", 2004: "Telmo", 2005: "Tupynambá", 2006: "Pondé", 2007: "Grazielly", 2008: "Marins", 2009: "Militão",
 2010: "Camelo", 2011: "Canto Costa", 2012: "Belfort", 2013: "Santana Rocha", 2014: "Vercelli", 2015: "Kowalczuk",
 2016: "Sponchiado", 2017: "Hippolyto", 2018: "Gomes Cabral", 2019: "Neves da Cruz", 2020: "Yvens", 2021: "Dellaroli",
 2022: "Bastos", 2023: "Linhares", 2024: "Feltran", 2025: "Amiune", 2026: "Benício",
}
PARTIAL = {1988: "1 name (bronze); delegation size undetermined"}

POSTS = {
 2013: [post("https://noic.com.br/uncategorized/brasileiros-vencem-cone-sul-2013/", "Zanarella", "NOIC: 4 names, ages, cities, medals; leaders (photo caption)", domain="noic.com.br")],
 2014: [post("https://noic.com.br/matematica/quatro-medalhas-brasileiras-na-olimpiada-cone-sul/", "Vercelli", "NOIC results post: 4 names + medals", domain="noic.com.br")],
 2015: [post("https://www.obm.org.br/2015/05/18/brasil-conquista-o-primeiro-lugar-geral-por-paises-na-26a-olimpiada-de-matematica-do-cone-sul/", "Kowalczuk", "OBM news: 4 names, cities, medals; leaders; team champion (Temuco)"),
        post("https://noic.com.br/matematica/quatro-medalhas-para-o-brasil-na-cone-sul-de-matematica/", "Carneiro Porto", "NOIC results post: 4 names + medals", domain="noic.com.br")],
 2016: [post("https://www.obm.org.br/2016/05/11/brasil-conquista-quatro-medalhas-na-olimpiada-de-matematica-do-cone-sul/", "Kowalczuk", "OBM news: 4 names, cities, points, medals; leaders"),
        post("https://noic.com.br/matematica/quatro-medalhas-para-o-brasil-na-olimpiada-matematica-do-cone-sul/", "Sponchiado", "NOIC results post: 4 names + medals", domain="noic.com.br"),
        wb("olimp_conesul.html", "Kowalczuk", "OBM's former site (2017 snapshot): 2016 team, cities, medals")],
 2017: [post("https://www.obm.org.br/2017/08/21/ouro-perfeito-coroa-participacao-do-brasil-na-olimpiada-cone-sul/", "Trevizan", "OBM news: results (Guayaquil)"),
        post("https://noic.com.br/matematica/dois-ouros-para-o-brasil-na-olimpiada-de-matematica-cone-sul/", "Marcelo Hippolyto", "NOIC results post: 4 names (short forms) + medals", domain="noic.com.br"),
        post("https://impa.br/notices/ouro-perfeito-coroa-participacao-do-brasil-na-olimpiada-cone-sul/", "Hippolyto", "IMPA: results (4 names + medals), Guayaquil 15-21 Aug", domain="impa.br"),
        post("https://impa.br/notices/com-presenca-feminina-brasil-quer-o-topo-na-cone-sul/", "Bigolin", "IMPA: team feature (first girl on a Brazilian Cono Sur team)", "partial (pre-event)", domain="impa.br")],
 2018: [post("https://www.obm.org.br/2018/08/28/brasil-conquista-quatro-medalhas-na-olimpiada-do-cone-sul-em-maceio/", "Gomes Cabral", "OBM news: 4 names + medals; leaders; Maceió"),
        post("https://noic.com.br/matematica/brasil-leva-ouro-perfeito-na-cone-sul-2018-veja-o-resultado/", "Gabriel Ribeiro Paiva", "NOIC results post: 4 names (short forms) + medals", domain="noic.com.br"),
        post("https://impa.br/notices/brasil-conquista-quatro-medalhas-na-cone-sul/", "Gomes Cabral", "IMPA: results (4 names + medals)", domain="impa.br"),
        post("https://impa.br/notices/definidas-as-equipes-para-as-disputas-da-cone-sul-e-cplp/", "Gomes Cabral", "IMPA: team announcement (full names, cities, leader)", "full (pre-event roster)", domain="impa.br")],
 2019: [post("https://www.obm.org.br/2019/09/02/11538/", "Neves da Cruz", "OBM news: results table; leaders; Sucre; team champion"),
        post("https://noic.com.br/matematica/cone-sul/2-ouros-e-2-pratas-para-o-brasil-na-olimpiada-de-matematica-do-cone-sul/", "Longo", "NOIC results post: 4 names + medals", domain="noic.com.br"),
        post("https://impa.br/notices/brasil-e-campeao-da-30a-olimpiada-de-matematica-do-cone-sul/", "Neves da Cruz", "IMPA: results (4 names, cities, points); leaders", domain="impa.br"),
        post("https://impa.br/notices/equipe-brasileira-esta-na-bolivia-para-disputar-a-cone-sul/", "Neves da Cruz", "IMPA: team at the venue (full names, cities)", "full (pre-event roster)", domain="impa.br")],
 2020: [src("https://www.obm.org.br/2020/12/07/brasil-encerra-participacao-na-cone-sul-com-quatro-medalhas/", "obm.org.br", "primary", "results published as an image (no names in text)", "OBM news: 1G/3S, 2nd place, virtual edition"),
        post("https://noic.com.br/matematica/cone-sul/saiu-o-resultado-da-olimpiada-de-matematica-do-cone-sul-2020/", "Domingos Porto", "NOIC results post: 4 names + medals", domain="noic.com.br")],
 2021: [post("https://www.obm.org.br/2021/12/03/brasil-conquista-quatro-medalhas-na-32a-olimpiada-do-cone-sul/", "Dellaroli", "OBM news: results table (virtual edition)")],
 2022: [post("https://www.obm.org.br/2022/08/08/brasil-e-campeao-na-33a-olimpiada-de-matematica-do-cone-sul/", "Bastos", "OBM news: results table; Mehuín; team champion")],
 2023: [post("https://www.obm.org.br/2023/08/10/brasil-vence-olimpiada-de-matematica-do-cone-sul-e-fica-em-1o-lugar-no-ranking-de-paises/", "Fontenele", "OBM news: 4 names, points, medals; Buenos Aires; team champion")],
 2024: [post("https://www.obm.org.br/2024/09/30/brasil-e-campeao-da-35a-olimpiada-de-matematica-do-cone-sul/", "Feltran", "OBM news: 4 names, points, medals; Fortaleza; team champion")],
 2025: [post("https://www.obm.org.br/2025/06/08/brasil-conquista-tres-pratas-e-um-bronze-na-36a-olimpiada-de-matematica-do-cone-sul-e-garante-segundo-lugar-por-paises/", "Amiune", "OBM news: 4 names, points, medals; Uruguay; 2nd place")],
 2026: [post("https://www.obm.org.br/2026/08/09/brasil-conquista-segundo-lugar-na-37a-olimpiada-de-matematica-do-cone-sul/", "Benício", "OBM news: 4 names, points, medals; leaders; Peru; 2nd place")],
}


def sources_for(y):
    s = [obm(NEEDLE[y], PARTIAL.get(y, "full"))]
    if y <= 2013:
        s.append(olc(NEEDLE[y], PARTIAL.get(y, "full")))
    if y <= 2009:
        s.append(wb("conesul_88_07.html", NEEDLE[y], "OBM's former site (2017 snapshot): 1988-2009 teams + medals", PARTIAL.get(y, "full")))
    s += POSTS.get(y, [])
    return s


SOURCES = {y: sources_for(y) for y in NEEDLE}

NOTES = {
 1988: "Debut (1st edition, Montevideo): a single name survives, Raul Bazkhaus (bronze); delegation size undetermined. No 1989-1990 editions.",
 1991: "OBM table 'Mauricio Palmeira' vs archived OBM/OLC 'Márcio Palmeira' - table kept. 'Renato Madeira' (Rio) = OIM 1992 'Renato Caldas Madeira' = IMO 1992 'Renato de O. Caldas Madeira' (site alias). Rodrigo Onias: certificate (no medal).",
 1992: "Table 'Breno de Alencar Araripe Falcão' (= IMO 1995) vs archived 'João Carlos Alencar Araripe Falcão' - table kept (matches the IMO roster). Two certificates (Marcondes França Júnior = IMO 1994; Breno).",
 1993: "Table 'Guilherme Aguiar Allery' vs archived OBM/OLC 'Guilherme Ellery' - table kept, unverified.",
 1994: "Table 'Davi Araújo Lima' / archived 'Davi Araújo' written as IMO 1995 'Davi Ponciano Araújo Lima' - ASSUMED same person (Fortaleza junior team -> IMO the following year); not independently documented.",
 1996: "'Emanuel A. de Souza Carneiro' expanded per the archived OBM page (Emanuel Augusto de Souza Carneiro = IMO 'Emanuel Carneiro'). 'Vajapeyam' as in the OIM dataset.",
 1998: "'Jônathas D.' = Diógenes (archived OBM, OLC).",
 2001: "Einstein do Nascimento Jr.: certificate (no medal).",
 2005: "Edson Augusto Bezerra Lopes = IMO 2005 'Edson Bezerra Lopes' (site alias).",
 2009: "Matheus Barros de Paula (São Paulo) merges by exact name with the IJSO 2007-08 / OIbF 2010 contestant - junior science -> under-16 math -> physics progression, same city.",
 2012: "'Tadeu P. de Matos Belfort Neto' = Tadeu Pires (OBM award lists 2012-15). 'Henrique G. Fiuza' = Gasparini Fiúza.",
 2013: "Sacramento de Oliveira at 13 (NOIC) - first of three Cono Sur medals (2013-15).",
 2015: "Vitor Augusto CARNEIRO Porto - OBM's award lists 2013-16 and this table agree; the 'Cariveiro' of the APMO sources is a typo (see apmo/ 2016 note).",
 2016: "'Mateus Siqueira Thimóteo' (OBM post: 'Timóteo'). Vicente López, Argentina.",
 2017: "Mariana Bigolin Groff (EGMO 2017-19) - first girl on a Brazilian Cono Sur team (IMPA). Bruno Barros de Sousa (Xambioá - TO). Guayaquil.",
 2020: "Virtual edition (Brazil host); 2021 also virtual (Paraguay host).",
 2022: "Short forms 'Leonardo Maldonado' / 'Gabriel Bastos Duarte' expanded per APMO/OBM (Leonardo Henrique Fakhreddine Maldonado, Gabriel Bastos Vasconcelos Duarte). Mehuín, Chile.",
 2023: "Table 'Fontenelle' vs OBM post + APMO official/OBM 'Fontenele' -> Rodrigo Fontenele de Oliveira Linhares. Buenos Aires.",
 2025: "36th edition, Uruguay. Maria Clara Fontes Silva = the EGOI/IOI/OII/EGMO/APMO contestant (Aracaju).",
 2026: "37th edition, Peru, held August 2026 (OBM post 2026-08-09). Two sources, one organization (OBM table + OBM news) - THIRD SOURCE PENDING (searched NOIC, IMPA, Google News 2026-09-09).",
}

GLOBAL_NOTES = [
 "Under-16 olympiad of the southern-cone countries; teams of four. OBM's all-years table is the only Brazilian all-years source (OLC mirrors it to 2013); it records non-medalists as 'Certificado' where known (1991, 1992, 2001) but the 1988 debut keeps a single name.",
 "rawName policy: OBM table forms with initials expanded from the archived OBM page, OLC, OBM award lists and the IMO/APMO datasets (most-complete documented form). medal null = certificate (confirmed no medal).",
 "Many contestants reappear in imo/, apmo/ and oim/ (the Cono Sur is the under-16 feeder of the IMO team) - identities were aligned against that pool before building.",
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
        "olympiadId": "conosur",
        "description": "Sources confirming Brazilian Cono Sur contestants + results, per edition.",
        "provenanceClasses": {
            "official": "(none online - the olympiad has no permanent results site)",
            "primary": "OBM (national organizer) all-years results table and news; olimpiadascientificas.org mirror; NOIC; IMPA.",
            "archive": "Wayback snapshots of OBM's former site (1988-2009 and 2016 team pages).",
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

    md = ("# Per-Year Corroboration — Brazil at the Cono Sur Mathematical Olympiad\n\n"
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
