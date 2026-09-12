#!/usr/bin/env python3
"""
Corroboration for Brazil at the IBO (repo-standard). 2026-09-09 collection pass: every URL fetched and
content-verified. Editions attended: 2006, 2008-2019, 2021-2026 (19). 2007 not attended; 2020 = non-competitive
IBO Challenge (excluded, see notes).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
R = "https://www.ibo-info.org/files/downloads/results-reports/results/"
OLC = "https://olimpiadascientificas.org/equipes-brasileiras/biologia/ibo/"
WB = "https://web.archive.org/web/"
SEL = "/https://olimpiadasbiologiasistema.butantan.gov.br/ResultadoSeletivaInternacional"


def obb(ts, needle, year):
    return src(WB + ts + SEL, "web.archive.org", "archive", "full (pre-event roster)",
               f"OBB 'Resultado definitivo da Seletiva Internacional' {year} (archived copy; live host gone): IBO + OIAB teams with school and city", needle)


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def official(path, needle, confirms="official final results PDF: full ranking with names, scores and medals", coverage="full"):
    return src(R + path, "ibo-info.org", "official", coverage, confirms, needle)


def olc(needle, coverage="full"):
    return src(OLC, "olimpiadascientificas.org", "primary", coverage, "olimpiadascientificas.org roster (sources: OBB site, past IBO sites, NOIC), 2005-2017", needle)


def noic(url, needle, confirms, coverage="full"):
    return src(url, "noic.com.br", "primary", coverage, confirms, needle)


SOURCES = {
 2006: [official("IBO2006.pdf", "TAVARES Bruno"), olc("Saharoff")],
 2008: [official("IBO2008.pdf", "NEGREIROS BESSA"), olc("Negreiros Bessa")],
 2009: [src("https://www.ibo-info.org/files/downloads/results-reports/final-reports/IBO-2009%20report.pdf", "ibo-info.org", "official", "full",
            "official final report (the results PDF is a scan): team list + full ranking with medals", "Patrocinio Zen"), olc("Rainne")],
 2010: [official("IBO2010_Final_Results.pdf", "BENEVIDES"), olc("Benevides")],
 2011: [official("IBO2011_Ranking_total_final.pdf", "Medeiros Fernandes"), olc("Medeiros Fernandes")],
 2012: [official("IBO2012_Detailed_Results.pdf", "Lubiana", "official detailed results: names, scores, rank (no medal column)", "full (scores; medals from OLC)"), olc("Lubiana")],
 2013: [official("IBO2013_final_ranking.pdf", "Lavor Lira"), olc("Lavor Lira"),
        noic("https://noic.com.br/biologia/quadro-de-medalhas-brasileiras-ibo-2013/", "Lavor", "NOIC: Brazilian medal table")],
 2014: [official("IBO2014_FINAL_scores.pdf", "PERTOT", "official final scores (text extraction garbles rows; BRA01-04 identified by code)", "full"), olc("Allan"),
        noic("https://noic.com.br/uncategorized/resultado-brasileiro-na-ibo-2014/", "Allan", "NOIC results post"),
        noic("https://noic.com.br/biologia/divulgadas-equipes-brasileiras-da-ibo-e-oiab/", "Allan", "NOIC team announcement", "full (pre-event roster)")],
 2015: [official("IBO2015-official-ranking.pdf", "Voltani"), olc("Voltani"),
        noic("https://noic.com.br/biologia/tres-medalhas-para-o-brasil-na-olimpiada-internacional-de-biologia-ibo/", "Voltani", "NOIC results post: 3 bronzes"),
        noic("https://noic.com.br/biologia/divulgada-a-equipe-brasileira-da-ibo-e-da-oiab-2015/", "Voltani", "NOIC team announcement", "full (pre-event roster)")],
 2016: [official("IBO2016.pdf", "KAWAKAMI"), olc("Kawakami"),
        noic("https://noic.com.br/uncategorized/divulgadas-as-equipes-brasileiras-nas-internacionais-de-biologia/", "Kawakami", "NOIC team announcement (IBO + OIAB)", "full (pre-event roster)")],
 2017: [official("IBO2017Full.pdf", "Parada"), olc("Parada"),
        noic("https://noic.com.br/biologia/divulgados-os-representantes-do-brasil-nas-internacionais-de-biologia/", "Coca Parada", "NOIC team announcement with full names (IBO + OIAB)", "full (pre-event roster)")],
 2018: [official("IBO2018-IBO-Ranking_web.pdf", "Galiza Soares"), noic("https://noic.com.br/uncategorized/confira-resultado-da-ibo/", "Galiza", "NOIC results post")],
 2019: [official("IBO2019-IBO-Ranking_web.pdf", "Jaziel"), noic("https://noic.com.br/uncategorized/duas-medalhas-para-o-brasil-na-ibo/", "Jaziel", "NOIC results post: 2 bronzes")],
 2021: [official("IBO%202021%20-%20IBO%20Challenge%20II%20-%20results.pdf", "Sicupira", "official IBO Challenge II results (remote edition): names + awards"), obb("20210723210710", "SICUPIRA", 2021)],
 2022: [official("IBO2022.pdf", "Pascalichio"), obb("20220705114103", "PASCALICHIO", 2022)],
 2023: [official("IBO2023.pdf", "Gabilondo"), obb("20231201053656", "GABILONDO", 2023)],
 2024: [official("IBO2024%20results%20-%20amended%20version%20January%202025.pdf", "Vitarelli", "official results (amended version, Jan 2025)"), obb("20240721061254", "VITARELLI", 2024)],
 2025: [official("IBO2025%20Ranking.pdf", "Pongelupp")],
 2026: [official("IBO_2026_Individual_Results_Final.pdf", "Tsuchie", "official final updated individual results (302 competitors)")],
}

NOTES = {
 2006: "Brazil's first IBO team (Rio Cuarto): four contestants, none medalled (cc-ranks 123-164; bronze cut at rank 121). Full names from OLC (official gives surname + first name only). OLC also lists four 'Beijing 2005' names, but the official 2005 results contain no Brazilian - not competitors.",
 2008: "2007 (Saskatoon) not attended (OLC: financial reasons; official 2007 results have no Brazil).",
 2009: "The results PDF is a scanned image; the official final report carries the same ranking as text.",
 2012: "The official detailed-results sheet has no medal column: Lubiana bronze and Andressa Gomes Sales merit per OLC/NOIC.",
 2014: "Certificate of Participation (CoP) = no award.",
 2017: "Official PDF abbreviates (Bruno Gomes, Laís Parada, Emanuel Bezerra); full forms from NOIC's team post (Bruno Teixeira Gomes = OIAB 2016 gold).",
 2018: "Pedro Henrique Silva de Oliveira = the IJSO 2015-16 contestant (Fortaleza; exact name).",
 2019: "Official MED column: B bronze, M merit (honorable-mention), X none.",
 2021: "IBO Challenge II (remote): medals awarded - kept as a normal edition.",
 2024: "Alexandre Andrade de Almeida = the IJSO/OIbF/EuPhO contestant (exact name).",
}

GLOBAL_NOTES = [
 "Teams of four. Editions attended: 2006 (debut), 2008-2019, 2021-2026. Not attended: 2007. 2020 was the non-competitive 'IBO Challenge' (team projects, no exam/medals; one Brazilian, João Victor Silva Ribeiro, appears in the yearbook) - excluded from the dataset, mirroring the GeCAA-2020 treatment in ioaa/.",
 "Every edition rests on the official IBO results PDF (ibo-info.org); OLC's roster page (2005-2017) and NOIC posts corroborate 2006-2019. The OBB (national organizer) site was unreachable during collection.",
 "Awards: gold/silver/bronze + Certificate of Merit (= honorable-mention); Certificate of Participation / 'Pass' = medal null.",
 "rawName policy: official spellings with accents restored from OLC/NOIC where the PDF strips them; nine students also appear in ijso/ioaa/icho/oibf datasets (exact-name merges, see aliases notes).",
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
        "olympiadId": "ibo",
        "description": "Sources confirming Brazilian IBO contestants + results, per edition.",
        "provenanceClasses": {
            "official": "ibo-info.org results PDFs / final reports.",
            "primary": "olimpiadascientificas.org roster; NOIC.",
            "archive": "Wayback Machine copies of the OBB 'Seletiva Internacional' results page (2021-2024).",
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

    md = ("# Per-Year Corroboration — Brazil at the IBO\n\n"
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
