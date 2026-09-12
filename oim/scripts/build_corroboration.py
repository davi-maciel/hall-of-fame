#!/usr/bin/env python3
"""
Corroboration for Brazil at the OIM (repo-standard). 2026-09-09 collection pass:
every URL fetched and content-verified. Editions: 1985, 1987-2025 (40; no 1986 edition).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OBM = "https://www.obm.org.br/resultados-do-brasil-olimpiada-ibero-americana-de-matematica/"
OLC = "https://olimpiadascientificas.org/equipes-brasileiras/matematica/oim/"
WB = "https://web.archive.org/web/20161110114648/http://www.obm.org.br/opencms/competicoes/internacionais/"


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def obm(needle, coverage="full"):
    return src(OBM, "obm.org.br", "primary", coverage,
               "national organizer results table (all 40 editions): names, city/state, medal", needle)


def olc(needle, coverage="full"):
    return src(OLC, "olimpiadascientificas.org", "primary", coverage,
               "olimpiadascientificas.org roster mirror (source: OBM), 1985-2013", needle)


def wb(page, needle, confirms, coverage="full"):
    return src(WB + page, "obm.org.br (Wayback)", "archive", coverage, confirms, needle)


def post(url, needle, confirms="OBM news: full team result", coverage="full", domain="obm.org.br"):
    return src(url, domain, "primary", coverage, confirms, needle)


# OBM-table needle per year (table spelling), OLC needle where it differs, archive page
NEEDLE = {
 1985: "Teixeira", 1987: "Fritz Braga", 1988: "Adami", 1989: "Carvalho Torres", 1990: "Meggiolaro", 1991: "Laber",
 1992: "Tengan", 1993: "Penharrubia", 1994: "Cancherini", 1995: "Cordeiro de Melo", 1996: "Arroyo", 1997: "Vajapeyam",
 1998: "Catae", 1999: "Iveson", 2000: "Nobuo Uno", 2001: "Sobreira", 2002: "Naves", 2003: "Feitosa", 2004: "Hirama",
 2005: "Hoshina", 2006: "Linhares Rodrigues", 2007: "Pondé", 2008: "Finder", 2009: "Lopes Pedroso", 2010: "Empinotti",
 2011: "Camelo", 2012: "Miyazaki", 2013: "Oliveira Reis", 2014: "Zanarella", 2015: "Vercelli", 2016: "Jhen Shan",
 2017: "Hisatsuga", 2018: "Sponchiado", 2019: "Prieto", 2020: "Zeus", 2021: "Machado Lage", 2022: "Torkomian",
 2023: "Giglio", 2024: "Bandeira Lemos", 2025: "Feltran",
}
PARTIAL = {1985: "medalists only (2 named; delegation size undetermined)", 1989: "medalists only (2 named)",
           1991: "medalists only (2 named)", 1992: "medalists only (3 named)"}

POSTS = {
 2014: [post("https://www.obm.org.br/2014/09/26/estudante-brasileiro-fica-com-a-primeira-colocacao-na-olimpiada-ibero-americana-de-matematica/", "Zanarella", "OBM news: 4 names, cities, points, medals; leaders"),
        post("https://noic.com.br/uncategorized/brasil-em-primeiro-na-ibero-americana-de-matematica/", "Zanarella", "NOIC results post: 4 names, points, medals", domain="noic.com.br")],
 2015: [post("https://noic.com.br/matematica/ouro-e-mais-tres-medalhas-para-o-brasil-na-olimpiada-iberoamericana-de-matematica/", "Sacramento", "NOIC results post: 4 names + medals", domain="noic.com.br")],
 2016: [post("https://noic.com.br/uncategorized/brasil-conquista-tres-ouros-na-olimpiada-iberoamericana-de-matematica/", "Campos Vargas", "NOIC results post: 4 names + medals (two 'ouro 42')", domain="noic.com.br")],
 2017: [post("https://www.obm.org.br/2017/09/26/com-quatro-medalhas-brasil-fica-em-2o-na-ibero-americana/", "Meinhart", "OBM news: 4 names, cities, medals; 2nd place"),
        post("https://noic.com.br/uncategorized/dois-ouros-e-dois-pratas-para-o-brasil-na-ibero-americana-de-matematica/", "Tarcísio Teixeira", "NOIC results post: 4 names (short forms) + medals", domain="noic.com.br"),
        post("https://impa.br/notices/com-quatro-medalhas-brasil-fica-em-segundo-na-ibero-americana/", "Meinhart", "IMPA: results (4 names, cities, medals)", domain="impa.br")],
 2018: [post("https://www.obm.org.br/2018/09/28/duas-medalhas-de-ouro-e-duas-de-prata-para-brasil-na-olimpiada-ibero-americana-de-matematica/", "Sponchiado", "OBM news: 4 names, points, medals; leaders"),
        post("https://noic.com.br/matematica/saiu-o-resultado-da-ibero-americana-de-matematica/", "Sponchiado", "NOIC results post: 4 names + medals", domain="noic.com.br")],
 2019: [post("https://www.obm.org.br/2019/09/19/equipe-brasileira-traz-tres-ouros-e-uma-prata-da-ibero-americana-realizada-no-mexico/", "Prieto", "OBM news: 4 names, cities, points, medals; leaders"),
        post("https://noic.com.br/uncategorized/o-brasil-conquista-2o-lugar-geral-na-ibero-americana-de-matematica/", "Trevizan", "NOIC results post: 4 names + medals", domain="noic.com.br"),
        post("https://impa.br/notices/brasil-conquista-tres-ouros-e-uma-prata-na-ibero-americana/", "Prieto", "IMPA: results (4 names, cities, points)", domain="impa.br")],
 2020: [src("https://www.obm.org.br/2020/11/30/brasil-conquista-quatro-medalhas-na-olimpiada-ibero-americana-de-matematica/", "obm.org.br", "primary", "results published as an image (no names in text)", "OBM news: 1G/2S/1B, virtual edition (Peru host)"),
        post("https://noic.com.br/uncategorized/confira-os-resultados-do-brasil-na-iberoamericana-de-matematica/", "Carvalho Barros", "NOIC results post: 4 names + medals", domain="noic.com.br")],
 2021: [post("https://www.obm.org.br/2021/10/23/brasil-conquista-tres-ouros-e-uma-prata-na-36a-olimpiada-ibero-americana-de-matematica/", "Machado Lage", "OBM news: 4 names, cities, points, medals; leaders")],
 2022: [post("https://www.obm.org.br/2022/10/01/ibero-2022-brasil-conquista-uma-medalha-de-ouro-e-tres-de-prata/", "Torkomian", "OBM news: results table; 2nd place")],
 2023: [post("https://www.obm.org.br/2023/09/12/brasil-e-campeao-na-38a-olimpiada-ibero-americana-de-matematica/", "Giglio", "OBM news: 4 names, points, medals; leaders; team champion"),
        post("https://noic.com.br/uncategorized/confira-o-resultado-da-olimpiada-ibero-americana-de-matematica/", "Giglio", "NOIC results post: 4 names + medals", domain="noic.com.br")],
 2024: [post("https://www.obm.org.br/2024/09/25/brasil-brilha-na-39a-olimpiada-ibero-americana-de-matematica/", "Bandeira Lemos", "OBM news: 4 names + medals")],
 2025: [post("https://www.obm.org.br/2025/09/28/brasil-e-campeao-na-olimpiada-ibero-americana-de-matematica-no-chile/", "Feltran", "OBM news: 4 names, points, medals; leaders; team champion")],
}


def sources_for(y):
    s = [obm(NEEDLE[y], PARTIAL.get(y, "full"))]
    if y <= 2013:
        s.append(olc(NEEDLE[y], PARTIAL.get(y, "full")))
    if y <= 1995:
        s.append(wb("ibero_85_95.html", NEEDLE[y], "OBM's former site (2016 snapshot): 1985-1995 teams + medals", PARTIAL.get(y, "full")))
    elif y <= 2015:
        s.append(wb("ibero_96_07.html", NEEDLE[y], "OBM's former site (2016 snapshot): 1996-2015 teams + medals"))
    elif y == 2016:
        s.append(wb("olimp_iberoamericana.html", "Jhen Shan", "OBM's former site (2016 snapshot): 2016 team, cities, medals, leaders"))
    s += POSTS.get(y, [])
    return s


SOURCES = {y: sources_for(y) for y in NEEDLE}

NOTES = {
 1985: "Debut. Only two names survive (gold + silver); whether Brazil sent fewer than four students or the others were never recorded is undetermined - same for 1989, 1991, 1992. No official per-name OIM database exists online (OEI's historical site is gone; Wayback only).",
 1988: "OBM table 'Jun Takamura' / 'Song San Woei' vs archived OBM + OLC 'Jun Takakura' / 'Sog San Woei'; the IMO 1988 official roster has Takakura and Song -> Takakura, Song.",
 1990: "Current OBM table gives Carlos Gustavo T. de A. Moreira 'Ouro' and omits the fourth student; the archived OBM page and OLC (older 4-row version) have him as '1o. Prêmio (Hors Concours)' and Luciano Guimarães de Castro gold. Archived version used: medalStatus hors-concours, Luciano written as the IMO 1990 form 'Luciano Guimarães Monteiro de Castro'. Gugu's full name from OBM's 2014/2018 posts (team leader).",
 1991: "'Eduardo Laber' = IMO 1991 'Eduardo Sany Laber'.",
 1992: "'Renato Caldas Madeira' (table) / 'Renato Caldas' (archived) = IMO 1992 'Renato de O. Caldas Madeira' (site alias).",
 1993: "'Reynaldo' (table) vs 'Reinaldo' Penharrubia Fagundes (archived, OLC, IMO 1993-94) -> Reinaldo; 'Paulo José B.' = Bonfim (IMO).",
 1995: "'André Luiz' (OBM) vs 'André Luís' de Souza Neves (IMO) - IMO form kept; 'Fernando A.' = Antonio (archived).",
 1997: "'Vajapeyam' (OBM 1997, Cono Sur table, archived) / 'Vajapejam' (OBM 1998) / 'Vajapeyan' (IMO DB) -> Vajapeyam (site alias for the IMO form). 'Emanuel Carneiro' = Emanuel Augusto de Souza Carneiro (Cono Sur 1996 table).",
 2011: "'Henrique G.' = Gasparini (IMO/APMO).",
 2013: "'Franco M. de Alencar Severo' / 2012 'Franco Matheus Alencar Severo' -> Franco Matheus de Alencar Severo (IMO form).",
 2014: "Ana Karoline Borges Carneiro (silver) later led the EGMO 2017 and 2020 teams. Zanarella = individual winner (42/42).",
 2016: "'Pedro H.' = Henrique. Two 'ouro 42' (perfect scores): Campos Vargas, Sacramento de Oliveira.",
 2022: "'Gabriel Cruz Vitale Torkomian' = IMO-DB 'Gabriel Torkomian' (OBM IMO 2022 team post) - site alias.",
 2024: "OBM table 'Marco Aurélio Nogueira D’ Emidio' -> D'Emidio; OBM post 'Castelo Branco' -> Castello (IMO/APMO).",
 2025: "40th edition, Temuco; Brazil champion (3G+1S). Bruno Machado Feltran = the ipho/eupho/ijso/apmo contestant (São Paulo, OBM awardee).",
}

GLOBAL_NOTES = [
 "Teams of up to four (under 18, at most two participations). OBM's all-years results table is the naming source for every edition; it lists medals only (no honourable mentions or certificates), and for 1985/1989/1991/1992 fewer than four names - rosters for those years may be partial.",
 "rawName policy: OBM table forms with initials expanded from the archived OBM page, OLC and the IMO dataset (most-complete documented form); spellings aligned to the IMO dataset where the student is already there (~70 of 113 also appear in imo/).",
 "medal null occurs once: Carlos Gustavo Tamm de Araújo Moreira 1990, hors concours (medalStatus).",
 "Not added: 41st OIM 2026 (Buenos Aires) - team announced 2026-08-14, event not yet held on 2026-09-09.",
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
        "olympiadId": "oim",
        "description": "Sources confirming Brazilian OIM contestants + results, per edition.",
        "provenanceClasses": {
            "official": "(none online - OEI's historical OIM site is offline)",
            "primary": "OBM (national organizer) all-years results table and news; olimpiadascientificas.org mirror; NOIC; IMPA.",
            "archive": "Wayback snapshots of OBM's former site (1985-2016 team pages).",
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

    md = ("# Per-Year Corroboration — Brazil at the OIM\n\n"
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
