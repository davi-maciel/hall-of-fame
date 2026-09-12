#!/usr/bin/env python3
"""
Corroboration for Brazil at the iGeo (repo-standard). 2026-09-10 collection pass. Editions attended: 2016, 2018, 2019,
2022-2026 (8). Rosters are partial: the official iGeo results list gold medallists only, so Brazilian names come from
OBG (national organizer) posts, schools and press. No names found for 2016 (first names only), 2019 and 2023.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = "https://geoolympiad.org/wp-content/uploads/2025/04/"


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def official(year, fname=None, confirms="iGeo official results: gold medallists and team rankings only (no Brazilian entry)"):
    url = RES + (fname or f"{year}-iGeo-Results.pdf")
    return src(url, "geoolympiad.org", "official", "gold medallists + team ranking", confirms, None)


def press(url, domain, needle, confirms, coverage="full"):
    return src(url, domain, "primary", coverage, confirms, needle)


SOURCES = {
 2018: [official(2018), press("https://www.facebook.com/colegionucleo/photos/temos-mais-um-aluno-n%C3%BAcleo-provando-seu-conhecimento-para-o-mundo-marina-hutzler/1763515040405071", "facebook.com", None, "Colégio Núcleo (Recife): Marina Hutzler, 1st in Brazil, went to iGeo 2018 (Quebec) - text via search snippet", "one student")],
 2022: [official(2022), press("https://www.facebook.com/obgeografia/videos/616207526523982", "facebook.com", "Lauren", "OBG video post: Lucas Lang, Lauren Schuantes, Manuela Teixeira and Karen Gomes represented Brazil at the online iGeo 2022 (Paris)")],
 2024: [official(2024), press("https://tribunaonline.com.br/atribunanasescolas/feras-da-geografia-se-destacam-na-irlanda-198302", "tribunaonline.com.br", "Azurza", "A Tribuna (ES): Pablo Fernando de Azurza Nogueira Gomez bronze (first Brazilian/South American iGeo medal), Gabriel Volpato Lima on the team; two more (CE, BH) unnamed", "2 of 4"),
        press("https://noic.com.br/uncategorized/entrevista-com-pablo-primeiro-brasileiro-medalhista-na-igeo/", "noic.com.br", "primeiro brasileiro medalhista", "NOIC interview with the 2024 bronze medallist ('Pablo Alvarez')", "one student")],
 2025: [src("https://geoolympiad.org/wp-content/uploads/2025/10/2025-iGeo-Results-and-Report.pdf", "geoolympiad.org", "official", "gold medallists + team ranking", "iGeo 2025 official results and report: gold medallists and team rankings only", None), press("https://www.instagram.com/p/DLYyq35MAsg/", "instagram.com", None, "OBG (national organizer) Instagram: the four selected for iGeo 2025 - Isabela Granado Santos, João Lucas Dantas Barbosa, Bárbara Pinheiro Puget Cruz, Clara Gonzalez Ferreira Pinto Sampaio", "full (pre-event roster)"),
        press("https://regionalnorte.com.br/estudantes-paraenses-sao-selecionadas-para-olimpiada-internacional-de-geografia-na-tailandia", "regionalnorte.com.br", "Granado", "Regional Norte: Isabela Granado and Bárbara Puget (Colégio Santa Rosa, Belém) selected; team of four from N/NE", "2 of 4 (pre-event)")],
 2026: [press("https://www.instagram.com/p/DcLny4cjo-R/", "instagram.com", None, "Colégio Militar de Fortaleza Instagram: Tiago Sales bronze at iGeo 2026 (Istanbul, 10-17 Aug), Brazil's only 2026 medal and third ever", "one student + medal"),
        press("https://www.instagram.com/p/DcEdsF_EbMH/", "instagram.com", None, "OBG Instagram: Brazilian team at the 2026 opening ceremony", "event"),
        press("https://wscom.com.br/noticias/noticias-locais/2026/03/05/estudante-paraibana-representa-o-brasil-na-olimpiada-internacional-de-geografia-em-istambul/", "wscom.com.br", "Bianca Ribas", "WSCOM: Bianca Ribas (Colégio Motiva, João Pessoa) selected for iGeo 2026", "one student (pre-event)"),
        press("https://agoralaguna.com.br/2026/04/theodora-flor-estudante-de-laguna-representara-estado-em-olimpiada-de-geografia-na-turquia/", "agoralaguna.com.br", "Theodora", "Agora Laguna: Theodora Flor (Laguna-SC) selected for iGeo 2026", "one student (pre-event)")],
}

NOTES = {
 2018: "Only Marina Hutzler documented (Colégio Núcleo post); the other three unknown.",
 2022: "Online edition (Paris). Four short-form names from OBG's video post.",
 2024: "Dublin. First Brazilian iGeo medal (bronze, Pablo Fernando de Azurza Nogueira Gomez); Gabriel Volpato Lima also from Colégio FAESA (Vitória); the CE and BH members are unnamed in the sources found.",
 2025: "Bangkok. Isabela Granado Santos bronze (second Brazilian medal) per the 2026-08 DATA_STATUS verification; here corroborated only indirectly (the CMF 2026 post counts three Brazilian medals) - re-check OBG's results post. Roster from the OBG announcement.",
 2026: "Istanbul (10-17 Aug 2026). Tiago Sales (Colégio Militar de Fortaleza) bronze - Brazil's third medal; Bianca Ribas and Theodora Flor documented pre-event; the fourth member unnamed. OBG's results post not yet found.",
}

GLOBAL_NOTES = [
 "Editions attended: 2016, 2018, 2019, 2022-2026 (8; 2017 skipped, 2020 cancelled, 2021 online edition not entered). Brazilian medals: bronze 2024, 2025, 2026.",
 "COVERAGE IS PARTIAL: iGeo's official results list only gold medallists, so Brazilian rosters depend on OBG (Olimpíada Brasileira de Geografia) posts and press. 2016 (three EEEP Salaberga Torquato students known by first name only), 2019 and 2023 have no usable names; 2018 has 1 of 4, 2024 2 of 4, 2026 3 of 4. OBG's old site (unifal-mg.edu.br/obgeografia) is gone and its Instagram is only partly indexed.",
 "Selection via the OBG national final (UNIFAL-MG, later Unicamp): a written round, a paper and simulated tests in English.",
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
        "olympiadId": "igeo",
        "description": "Sources confirming Brazilian iGeo contestants + results, per edition (partial coverage).",
        "provenanceClasses": {
            "official": "geoolympiad.org results PDFs (gold medallists + team rankings).",
            "primary": "OBG Instagram/Facebook posts; school and press news; NOIC.",
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
    md = ("# Per-Year Corroboration — Brazil at the iGeo\n\n"
          "**Machine-readable:** `data/corroboration.json`. Rebuild: `python3 scripts/build_corroboration.py`; "
          "verify: `python3 scripts/verify_corroboration.py`. 2026-09-10 collection pass.\n\n## Notes\n\n"
          + "\n".join(f"- {n}" for n in GLOBAL_NOTES)
          + "\n\n## Summary\n\n| Year | Sources | Domains |\n|-----:|:--:|---------|\n" + "\n".join(lines)
          + "\n\n## Per-year sources\n\n" + "\n".join(details))
    with open(os.path.join(ROOT, "CORROBORATION.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Editions: {len(records)}")


if __name__ == "__main__":
    main()
