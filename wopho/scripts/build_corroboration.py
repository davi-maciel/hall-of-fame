#!/usr/bin/env python3
"""
Corroboration for Brazil at the WoPhO (World Physics Olympiad, Indonesia; repo-standard). 2026-09-11 collection
pass. Only two finals were ever held (Lombok 2011/12, Tangerang 2012/13); Brazil has one awarded participation,
Ivan Tadeu Ferreira Antunes Filho (silver, 2012/13). The official site wopho.org is defunct: its pages are cited
through Wayback Machine captures.
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


IVAN = "Ivan Tadeu Ferreira Antunes Filho"

SOURCES = {
 2012: [src("https://web.archive.org/web/20140907141700/http://www.wopho.org:80/about-detail.php?id=903", "web.archive.org", "official", "full",
            "Archived wopho.org 'Final - Tangerang, Banten' page: official award table of the 2nd WoPhO (10 gold, 10 silver, 13 bronze) - Ivan Tadeu Ferreira Antunes Filho, Brazil, Silver; 72 participants from 16 countries", IVAN),
        src("https://web.archive.org/web/20130127044018/http://www.wopho.org:80/news-news.php?id=29", "web.archive.org", "official", "full",
            "Archived wopho.org news 'Here Is The New World Physics Olympiad Champion' (3 Jan 2013): the same award table", IVAN),
        src("http://olimpiadascientificas.org/equipes-brasileiras/fisica/wopho/", "olimpiadascientificas.org", "primary", "full",
            "OLC WoPhO page: 2012/2013 Tangerang - Ivan Tadeu Ferreira Antunes Filho, Medalha de Prata", IVAN),
        src("https://www.objetivo.br/institucional/noticias.aspx?titulo=ivan-tadeu-recebe-medalha-inedita-e-destacase-entre-os-melhores-estudantes-do-mundo", "objetivo.br", "primary", "one student",
            "Colegio Objetivo news: Ivan Tadeu silver at the 2nd WoPhO, the only medallist from the Americas and the first Brazilian recognised at the tournament", IVAN),
        src("https://www.objetivo.br/institucional/noticias.aspx?titulo=mit-harvard-e-caltech-das-salas-de-aula-do-objetivo-para-as-principais-universidades-do-exterior", "objetivo.br", "primary", "one student",
            "Colegio Objetivo feature on alumni abroad: recalls Ivan Tadeu's WoPhO silver in Indonesia", "Ivan Tadeu")],
}

NOTES = {
 2012: "Held 28 Dec 2012 - 3 Jan 2013 in Tangerang (Banten), Indonesia; the organiser labels the edition 'WoPhO 2012' (OLC: 2012/2013). Ivan Tadeu was invited automatically as an IPhO 2012 gold medallist. Medal bands: at least 90% of the top score gold, 78% silver, 65% bronze; no honourable mentions.",
}

GLOBAL_NOTES = [
 "Only two finals were ever held: Lombok (28 Dec 2011 - 3 Jan 2012) and Tangerang (28 Dec 2012 - 3 Jan 2013). The 3rd final (Yogyakarta, Dec 2013) was cancelled for lack of funding - archived announcement of 18 Oct 2013: https://web.archive.org/web/20180315212806/http://www.wopho.org:80/final.php?id=11 - and the competition folded.",
 "2011/12 (Lombok) has no Brazilian row: the official award table (https://web.archive.org/web/20140907141634/http://www.wopho.org:80/about-detail.php?id=704 ; 11 gold, 12 silver, 12 bronze) lists no Brazilian. The pre-event registration list (https://web.archive.org/web/20111024135707/http://wopho.org:80/final-list-participant.php?id=6) carries two Brazilians in the fee-paying 'Guest' group (USD 1,500 under the 2011 rules: https://web.archive.org/web/20111024134147/http://wopho.org:80/final-detail.php?id=1); neither was awarded.",
 "Eligibility (2011 rules and FAQ): gold and silver medallists of that year's IPhO/APhO were invited automatically; others could qualify through an online selection round (ten problems, Feb-Jun) or enter as guests for a fee. WoPhO is an individual competition with no country quota.",
 "Third-party report: Kwee & Surya, Physics Competitions 14(2) 2012 (https://www.wfphc.eu/wp-content/uploads/2024/11/PhysicsCompetitions_Vol_14_No_2_2012_01.pdf) - 122 students from 13 countries at the 1st final; top-10 tables only, no Brazilian.",
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
        "olympiadId": "wopho",
        "description": "Sources confirming Brazilian WoPhO contestants + results, per edition.",
        "provenanceClasses": {
            "official": "wopho.org pages (site defunct; Wayback Machine captures of the official award tables).",
            "primary": "olimpiadascientificas.org (OLC) team page; Colégio Objetivo (the medallist's school) news.",
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
    md = ("# Per-Year Corroboration — Brazil at the WoPhO\n\n"
          "**Machine-readable:** `data/corroboration.json`. Rebuild: `python3 scripts/build_corroboration.py`; "
          "verify: `python3 scripts/verify_corroboration.py`. 2026-09-11 collection pass.\n\n## Notes\n\n"
          + "\n".join(f"- {n}" for n in GLOBAL_NOTES)
          + "\n\n## Summary\n\n| Year | Sources | Domains |\n|-----:|:--:|---------|\n" + "\n".join(lines)
          + "\n\n## Per-year sources\n\n" + "\n".join(details))
    with open(os.path.join(ROOT, "CORROBORATION.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Editions: {len(records)}")


if __name__ == "__main__":
    main()
