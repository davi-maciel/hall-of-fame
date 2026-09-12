#!/usr/bin/env python3
"""
Corroboration for Brazil at the OMCPLP (repo-standard). 2026-09-09 collection pass:
every URL fetched and content-verified. Editions: 2011-2019, 2022-2025 (13; 2020-2021 cancelled).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OBM = "https://www.obm.org.br/resultados-omcplp/"
OLC = "https://olimpiadascientificas.org/equipes-brasileiras/matematica/lusofonia/"
WB2016 = "https://web.archive.org/web/20161224154153/http://www.obm.org.br/opencms/competicoes/internacionais/lusofonia.html"


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def obm(needle):
    return src(OBM, "obm.org.br", "primary", "full", "national organizer results table (all 13 editions): names, city/state, medal", needle)


def post(url, needle, confirms, coverage="full", domain="obm.org.br"):
    return src(url, domain, "primary", coverage, confirms, needle)


NEEDLE = {2011: "Haddad", 2012: "Zanarella", 2013: "Siaudizionis", 2014: "Kowalczuk", 2015: "Sponchiado", 2016: "Hippólyto", 2017: "Koga",
          2018: "Quirino", 2019: "Lengruber", 2022: "Fontenele", 2023: "Fujibayashi", 2024: "Amiune", 2025: "Basílio"}

POSTS = {
 2011: [src(OLC, "olimpiadascientificas.org", "primary", "full", "olimpiadascientificas.org roster mirror (source: OBM), 2011-2012", "Haddad")],
 2012: [src(OLC, "olimpiadascientificas.org", "primary", "full", "olimpiadascientificas.org roster mirror (source: OBM), 2011-2012", "Zanarella")],
 2013: [post("https://noic.com.br/uncategorized/resultados-da-3a-omcplp/", "Siaudzionis", "NOIC results post: 4 names + medals (Maputo)", domain="noic.com.br"),
        post("https://noic.com.br/matematica/comeca-a-olimpiada-matematica-da-lusofonia/", "Campos Vargas", "NOIC: team at the start (names, cities)", "full (pre-event roster)", domain="noic.com.br")],
 2014: [post("https://noic.com.br/matematica/resultado-brasileira-da-lusofonia-2014/", "Kowalczuk", "NOIC results post (Luanda)", domain="noic.com.br")],
 2015: [post("https://noic.com.br/matematica/brasil-conquista-primeiro-lugar-na-olimpiada-de-matematica-da-cplp/", "Sponchiado", "NOIC results post: 4 names + medals; team champion (Praia)", domain="noic.com.br"),
        post("https://noic.com.br/matematica/divulgada-a-equipe-brasileira-para-a-olimpiada-de-matematica-da-cplp/", "Sponchiado", "NOIC team announcement", "full (pre-event roster)", domain="noic.com.br"),
        src(WB2016, "obm.org.br (Wayback)", "archive", "full", "OBM's former site (2016 snapshot): 2015 table (names, cities, medals)", "Sponchiado")],
 2016: [src(WB2016, "obm.org.br (Wayback)", "archive", "full", "OBM's former site (2016 snapshot): 2016 table (names, cities, medals) + leaders", "Hippólyto"),
        src("https://www.obm.org.br/2016/10/10/o-brasil-conquistou-o-segundo-lugar-na-omcplp/", "obm.org.br", "primary", "team placing only (results linked, no names)", "OBM news: 2nd place (117 pts vs Portugal 121), Fortaleza 5-9 Oct")],
 2017: [post("https://www.obm.org.br/2017/05/16/confira-a-equipe-que-participara-da-7a-omcplp/", "Koga", "OBM: team announcement (Porto, 24-30 Jul)", "full (pre-event roster)"),
        post("https://impa.br/notices/brasil-conquista-quatro-medalhas-na-olimpiada-dos-paises-lusofonos/", "Koga", "IMPA: results (4 names, cities, medals)", domain="impa.br")],
 2018: [post("https://www.obm.org.br/2018/09/11/com-ouro-maximo-equipe-do-brasil-volta-da-omcplp-2018/", "Quirino", "OBM news: 4 names (short forms) + medals; leaders; team champion (São Tomé)"),
        post("https://noic.com.br/matematica/brasil-conquista-4-medalhas-na-cplp-2018/", "Quirino", "NOIC results post: 4 names (short forms) + medals", domain="noic.com.br"),
        post("https://impa.br/notices/com-ouro-perfeito-brasil-conquista-quatro-medalhas-na-omcplp/", "Quirino", "IMPA: results (4 names, cities, medals)", domain="impa.br")],
 2019: [post("https://www.obm.org.br/2019/11/04/9a-olimpiada-de-matematica-dos-paises-da-cplp-comecou-neste-domingo-em-nova-friburgo/", "Lengruber", "OBM: team at the opening (full names, cities), leaders", "full (pre-event roster)"),
        post("https://www.obm.org.br/2019/11/08/12007/", "Ouro", "OBM news: medal table; team champion (Nova Friburgo)", "medal counts"),
        post("https://noic.com.br/matematica/brasil-conquista-dois-ouros-e-duas-pratas-na-omcplp/", "Lengruber", "NOIC results post: 4 names + medals", domain="noic.com.br"),
        post("https://impa.br/notices/brasil-e-ouro-na-olimpiada-de-matematica-de-paises-de-lingua-portuguesa/", "Lengruber", "IMPA: results (4 names, cities, medals); leaders", domain="impa.br"),
        post("https://impa.br/notices/brasil-sedia-9a-omcplp-a-partir-de-domingo-3/", "Lengruber", "IMPA: team at the venue (full names)", "full (pre-event roster)", domain="impa.br")],
 2022: [post("https://www.obm.org.br/2022/11/05/com-tres-ouros-e-uma-prata-brasil-fica-em-primeiro-lugar-na-omcplp/", "Fontenele", "OBM news: 4 names, points, medals; leader; team champion (Maputo)")],
 2023: [post("https://www.obm.org.br/2023/05/28/com-dois-ouros-e-duas-pratas-brasil-fica-em-primeiro-lugar-na-omcplp/", "Fujibayashi", "OBM news: results table; team champion (Fortaleza)"),
        post("https://noic.com.br/uncategorized/times-luso-e-cone-sul-anunciados/", "Lucas Kenji", "NOIC team announcement (first-name short forms)", "full (pre-event roster)", domain="noic.com.br")],
 2024: [post("https://www.obm.org.br/2024/07/27/brasil-e-campeao-da-olimpiada-de-matematica-da-cplp/", "Amiune", "OBM news: 4 names, points, medals; leaders; team champion (Oeiras)")],
 2025: [post("https://www.obm.org.br/2025/11/01/brasil-e-campeao-da-13a-omcplp/", "Basílio", "OBM news: results table; team champion (Fortaleza)")],
}


def sources_for(y):
    return [obm(NEEDLE[y])] + POSTS.get(y, [])


SOURCES = {y: sources_for(y) for y in NEEDLE}

NOTES = {
 2011: "First edition (Coimbra), then called Olimpíada de Matemática da Lusofonia. 'Daniel Nishida Kawai' = APMO 2011-12 / OLC 'Daniel Eiti Nishida Kawai'.",
 2013: "OBM/NOIC spell the silver medallist 'Siaudizionis' / 'Siaudzionis' - the latter (his own byline; ijso/ioi/oii) used.",
 2016: "OBM table 'Bernardo Peruzzo Trevisan' -> Trevizan (IMO/APMO/Cono Sur). Marcelo Hippólyto de Sandes Peixoto = Cono Sur 2017 'Marcelo Hippolyto Peixoto' (fuller form adopted there).",
 2018: "'Luciano Rodrigues de Oliveira Jr.' -> Junior (APMO 2020, Maio 2016). Eduardo Quirino de Oliveira: perfect score.",
 2019: "9th edition, Nova Friburgo (Brazil's 3rd hosting after 2012 Salvador and 2016 Fortaleza).",
 2022: "Resumed after the 2020-2021 cancellations (COVID); Maputo, 2-5 Nov.",
 2025: "13th edition, Fortaleza; team champion. 14th (2026) team selected 2026-04-28, event not yet held on 2026-09-09.",
}

GLOBAL_NOTES = [
 "Lusophone olympiad (Angola, Brazil, Cabo Verde, Guiné-Bissau, Moçambique, Portugal, São Tomé e Príncipe, Timor-Leste); teams of four, under 18. Annual 2011-2019, cancelled 2020-2021, annual again from 2022.",
 "OBM's all-years results table is the naming source for every edition; medals only (Brazil has never had a non-medallist here: 26 gold, 25 silver, 1 bronze through 2025).",
 "rawName policy: OBM table forms, aligned to the pool (imo/apmo/oim/conosur/maio) where the student is already there - three spelling fixes noted per year.",
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
        "olympiadId": "omcplp",
        "description": "Sources confirming Brazilian OMCPLP contestants + results, per edition.",
        "provenanceClasses": {
            "official": "(none online - the olympiad's site omcplp.obmep.org.br publishes no results archive)",
            "primary": "OBM (national organizer) all-years results table and news; olimpiadascientificas.org mirror; NOIC; IMPA.",
            "archive": "Wayback snapshot of OBM's former site (2015-2016 tables).",
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

    md = ("# Per-Year Corroboration — Brazil at the OMCPLP\n\n"
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
