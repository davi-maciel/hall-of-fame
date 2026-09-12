#!/usr/bin/env python3
"""
Corroboration for Brazil at the IYPT (repo-standard). 2026-09-10 collection pass: every URL fetched and
content-verified. Editions attended: 2004-2007, 2011-2019, 2022-2026 (18). Team tournament: the medal is the
team's medal (gold = finalists, then silver and bronze bands).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HIST = "https://www.iyptbrasil.com/historia"
ARC_P = "https://archive.iypt.org/people/"
ARC_F = "https://archive.iypt.org/factsheets/"
WIKI = "https://pt.wikipedia.org/wiki/Torneio_Internacional_de_Jovens_F%C3%ADsicos"
OLC = "https://olimpiadascientificas.org/equipes-brasileiras/fisica/iypt/"


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def hist(needle):
    return src(HIST, "iyptbrasil.com", "official", "full", "IYPT Brasil (national organizer) 'História' page: every Brazilian delegation 2004-2026 + results narrative", needle)


def arc_people(needle):
    return src(ARC_P, "archive.iypt.org", "official", "full (with captain and leaders)", "IYPT Archive 'People': team rosters per IYPT", needle)


def arc_facts(needle):
    return src(ARC_F, "archive.iypt.org", "official", "team rank + medal", "IYPT Archive factsheets: per-year ranking tables (scores, diploma/medal)", needle)


def past(year, needle, confirms="iypt.org past-tournament page: final ranking", slug=None):
    slug = slug or f"past-tournaments/iypt-{year}/"
    return src("https://iypt.org/" + slug, "iypt.org", "official", "team rank" if "medal" not in confirms else "team rank + medal", confirms, needle)


def cc(year, needle):
    return src(f"https://cc.iypt.org/iypt{year}/team/brazil/", "cc.iypt.org", "official", "fight line-ups (initial + surname)", "IYPT competition-control team page: Brazil's fight results and speakers", needle)


def wiki(needle):
    return src(WIKI, "pt.wikipedia.org", "primary", "full", "pt.wikipedia: 'Delegações brasileiras' (2004-2019) and results table", needle)


def olc(needle, sub=""):
    return src(OLC + sub, "olimpiadascientificas.org", "primary", "full", "olimpiadascientificas.org roster (2004-07, 2011-13) with rank and medal", needle)


def noic(url, needle, confirms):
    return src(url, "noic.com.br", "primary", "full", confirms, needle)


def press(url, domain, needle, confirms, coverage="full"):
    return src(url, domain, "primary", coverage, confirms, needle)


SOURCES = {
 2004: [hist("Lazarte"), arc_people("Lazarte"), arc_facts("Brazil"), past(2004, "Brazil"), wiki("Lazarte"), olc("Lazarte")],
 2005: [hist("Ogassavara"), arc_people("Ogassavara"), arc_facts("Brazil"), past(2005, "Brazil"), wiki("Ogassavara"), olc("Ogassavara", "iypt-2005/")],
 2006: [hist("Vignon"), arc_people("Vignon"), arc_facts("Brazil"), past(2006, "Brazil"), wiki("Vignon"), olc("Vignon", "iypt-2006/")],
 2007: [hist("Velani"), arc_people("Velani"), arc_facts("Brazil"), past(2007, "Brazil"), wiki("Velani"), olc("Velani")],
 2011: [hist("Frassei"), arc_people("Frassei"), arc_facts("Brazil"), past(2011, "Brazil"), wiki("Frassei"), olc("Frassei", "iypt-2011/")],
 2012: [hist("Guinsberg"), arc_people("Guinsberg"), arc_facts("Brazil"), past(2012, "Brazil"), wiki("Guinsberg"), olc("Guinsberg", "iypt-2012/")],
 2013: [hist("Christovam"), arc_people("Christovam"), arc_facts("Brazil"), past(2013, "Brazil"), wiki("Christovam"), olc("Christovam"),
        noic("https://noic.com.br/uncategorized/resultado-historico-na-iypt-2013/", "Christovam", "NOIC: silver, 7th, team"),
        press("https://g1.globo.com/educacao/noticia/2013/05/estudantes-brasileiros-vao-disputar-torneio-de-fisica-em-taiwan.html", "g1.globo.com", "Christovam", "G1: team announced with cities", "full (pre-event roster)")],
 2014: [hist("Ceotto"), arc_people("Ceotto"), arc_facts("Brazil"), past(2014, "Brazil"), wiki("Ceotto"), noic("https://noic.com.br/fisica/iypt/divulgado-o-resultado-da-iypt-2014/", "Ceotto", "NOIC: 18th, team")],
 2015: [hist("Kalife"), arc_people("Kalife"), arc_facts("Brazil"), past(2015, "Brazil"), wiki("Kalife"), noic("https://noic.com.br/fisica/resultado-inedito-para-o-brasil-na-copa-do-mundo-de-fisica/", "Kalife", "NOIC: silver, 5th, team")],
 2016: [hist("Tamae"), arc_people("Tamae"), arc_facts("Brazil"), past(2016, "Brazil"), wiki("Tamae"), noic("https://noic.com.br/uncategorized/brasil-conquista-bronze-na-copa-do-mundo-de-fisica/", "Tamae", "NOIC: bronze, 14th, team")],
 2017: [hist("Mambrim"), past(2017, "Brazil"), cc(2017, "M. Barbosa"), wiki("Mambrim"),
        press("https://g1.globo.com/educacao/noticia/estudantes-brasileiros-conquistam-medalha-de-prata-no-torneio-internacional-de-jovens-fisicos.ghtml", "g1.globo.com", "Mambrim", "G1: silver, 8th, five names, medal bands explained")],
 2018: [hist("Crocia"), past(2018, "Brazil", slug="past-tournaments/iypt-2018-2/"), cc(2018, "Cutrim Costa"), wiki("Crocia"),
        press("https://revistagalileu.globo.com/Ciencia/noticia/2018/08/brasil-ganha-4-medalha-de-prata-dos-ultimos-5-anos-em-torneio-de-fisica.html", "revistagalileu.globo.com", "Crocia", "Galileu: silver, 5th, five names"),
        press("https://g1.globo.com/go/goias/noticia/2018/07/28/goiano-e-quatro-estudantes-brasileiros-conquistam-o-5o-lugar-em-torneio-internacional-de-fisica-na-china.ghtml", "g1.globo.com", "Cutrim Costa", "G1: 5th, silver band = ranks 5-8")],
 2019: [hist("Slikta"), past(2019, "Brazil"), cc(2019, "Ventura Andreossi"), wiki("Slikta"),
        noic("https://noic.com.br/uncategorized/equipe-brasileira-conquista-medalha-de-prata-na-iypt-2019/", "Slikta", "NOIC: silver, 6th, team with states"),
        press("https://revistagalileu.globo.com/Ciencia/noticia/2019/07/brasileiros-ganham-prata-em-torneio-internacional-de-fisica-na-polonia.html", "revistagalileu.globo.com", "Slikta", "Galileu: silver, 6th, names and schools")],
 2022: [hist("Frascati"), past(2022, "Brazil"), cc(2022, "Seino")],
 2023: [hist("Hinsching"), past(2023, "Silver", "iypt.org past-tournament page: final ranking with medal bands"), cc(2023, "Monforte"),
        press("https://diariodonordeste.verdesmares.com.br/ceara/aluno-do-ifce-ganha-medalha-de-prata-em-torneio-internacional-de-jovens-fisicos-no-paquistao-1.3397702", "diariodonordeste.verdesmares.com.br", "Eleutério", "Diário do Nordeste: José Eleutério silver (Murree)", "one student"),
        press("https://www.correiobraziliense.com.br/euestudante/educacao-basica/2023/08/5113960-escola-publica-brasileiro-e-medalhista-em-torneio-de-fisica-no-paquistao.html", "correiobraziliense.com.br", "Eleutério", "Correio Braziliense: José Eleutério silver", "one student")],
 2024: [hist("Aleixo"), past(2024, "Bronze", "iypt.org past-tournament page: final ranking with medal bands"), cc(2024, "Bandeira Martins"),
        press("https://www1.folha.uol.com.br/ciencia/2025/08/em-4-anos-adolescente-de-goias-coleciona-20-medalhas-em-competicoes-cientificas.shtml", "folha.uol.com.br", "Bassi", "Folha: Gabriel Bassi bronze 2024, silver 2025 (captain)", "one student")],
 2025: [hist("Scarabelli"), past(2025, "Silver", "iypt.org tournament page: final ranking with medal bands", slug="iypt-2025/"), cc(2025, "Dochi Scarabelli"),
        press("https://g1.globo.com/go/goias/noticia/2025/08/21/estudante-goiano-de-17-anos-coleciona-20-medalhas-de-competicoes-cientificas-nacionais-e-internacionais.ghtml", "g1.globo.com", "Bassi", "G1: Gabriel Bassi, IYPT silver 2025", "one student")],
 2026: [hist("Manzoli Gorni"), past(2026, "Bronze", "iypt.org tournament page: final ranking with medal bands (Zurich)", slug="iypt-2026/")],
}

NOTES = {
 2004: "Debut (Brisbane): 15th of 24, no medal. The iypt.org 2004 page lists Brazil in a 12th-row position of an unsorted table; the archive factsheet and every Brazilian source give 15th.",
 2006: "'Pedro Lisbão' per the IYPT archive and IYPT Brasil (OLC: 'Pedro Lisboa').",
 2007: "Last edition before the 2008-2010 gap (no national tournament 2008-09).",
 2011: "Return: 15th of 21, no medal. Lucas Henrique Morais = the OLAA 2011 silver medallist (assumed).",
 2012: "10th of 28, bronze. The archive roster adds a sixth name (Sebastião Bethoven Brandão Filho) - a leader/observer, not a contestant.",
 2013: "7th, first silver; Liara Guinsberg's second IYPT.",
 2016: "14th of 29, bronze (official iypt.org page and archive III).",
 2017: "Medal bands (G1): gold ranks 1-4, silver 5-9, bronze 9-15.",
 2018: "5th of 32, silver (best rank, shared with 2015).",
 2022: "Return after the pandemic: 15th of 27, below the bronze band. Brazil sat the online OYPT in 2021 and 2023 instead of/besides the IYPT - the OYPT is a different tournament and is not recorded here.",
 2023: "8th, silver (Murree). José Antônio Eleutério = first public-school student on the team.",
 2026: "17th, bronze (Zurich). Names from the national organizer's page only; cc.iypt.org has not published the 2026 fight data yet - re-check.",
}

GLOBAL_NOTES = [
 "Editions attended: 2004-2007, 2011-2019, 2022-2026 (18). Absent 2008-2010 and 2021 (Brazil chose the online OYPT); 2020 not held. Team of five each year (90 records). Medals are team medals: silver 2013/2015/2017/2018/2019/2023/2025, bronze 2005/2006/2012/2016/2024/2026, none 2004/2007/2011/2014/2022.",
 "Backbone: the national organizer's roster page (iyptbrasil.com/historia, all 18 delegations) cross-checked against the IYPT Archive (rosters 2004-2016, rankings), iypt.org past-tournament rankings, cc.iypt.org fight line-ups (2017-2025), Wikipedia, OLC, NOIC and press.",
 "Names: fullest documented forms (archive/IYPT Brasil over Wikipedia short forms). Twelve students also appear in ijso/ipho/eupho/ioaa/olaa/iao/oibf/maio/rioplatense datasets (see aliases notes).",
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
        "olympiadId": "iypt",
        "description": "Sources confirming Brazilian IYPT team members + team results, per edition.",
        "provenanceClasses": {
            "official": "iyptbrasil.com (national organizer), archive.iypt.org, iypt.org, cc.iypt.org.",
            "primary": "pt.wikipedia; olimpiadascientificas.org; NOIC; press.",
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

    md = ("# Per-Year Corroboration — Brazil at the IYPT\n\n"
          "**Machine-readable:** `data/corroboration.json`. Rebuild: `python3 scripts/build_corroboration.py`; "
          "verify: `python3 scripts/verify_corroboration.py`. 2026-09-10 collection pass.\n\n## Notes\n\n"
          + "\n".join(f"- {n}" for n in GLOBAL_NOTES)
          + "\n\n## Summary\n\n| Year | Sources | Domains |\n|-----:|:--:|---------|\n" + "\n".join(lines)
          + "\n\n## Per-year sources\n\n" + "\n".join(details))
    with open(os.path.join(ROOT, "CORROBORATION.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Editions: {len(records)}")
    print("Wrote data/corroboration.json + CORROBORATION.md")


if __name__ == "__main__":
    main()
