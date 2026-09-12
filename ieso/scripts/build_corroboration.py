#!/usr/bin/env python3
"""
Corroboration for Brazil at the IESO (repo-standard). 2026-09-10 collection pass. Editions attended: 2012-2019 and 2026
(9). 2020 cancelled; 2021-2025 not attended. Rosters are partial for 2013-2015 and 2017 (see notes).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WB = "https://web.archive.org/web/20251213153335/https://www.igeoscied.org/wp-content/uploads/"
INDEX = "https://web.archive.org/web/20251213153335/https://www.igeoscied.org/activities/ieso-2/list-of-medal-and-team-award-winners/"
OLC = "https://olimpiadascientificas.org/equipes-brasileiras/interdisciplinar/ieso/"


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def medals(path, needle, confirms="IGEO official medal list (archived copy of igeoscied.org): individual medals and team awards", coverage="medallists + team-award members"):
    return src(WB + path, "web.archive.org", "official", coverage, confirms, needle)


def olc(needle):
    return src(OLC, "olimpiadascientificas.org", "primary", "team list (2012-2013)", "olimpiadascientificas.org IESO teams page (sources: IF Sul de Minas, OBAP)", needle)


def wb(url, needle, confirms, coverage="full"):
    return src(url, "web.archive.org", "archive", coverage, confirms, needle)


def press(url, domain, needle, confirms, coverage="full"):
    return src(url, domain, "primary", coverage, confirms, needle)


SOURCES = {
 2012: [medals("2022/11/2012-IESO-2012-Argentina-Medals-List.pdf", "Fernandez"), olc("Mayara")],
 2013: [medals("2022/11/2013-IESO-2013-India-Medals-List.pdf", "Lovo", "IGEO medal list: Igor Felix Pio (ESP gold team award), Mario Lovo (ITFI gold team) - no individual medal"),
        press("https://www.ifes.edu.br/noticias/14290-estudantes-do-ifes-conquistam-medalhas-em-competicao-internacional-de-ciencias-da-terra", "ifes.edu.br", None, "IFES news (page now 404; text via search snippet): Eliton Mathias Morais, Igor Felix Pio and Mario Lovo of Campus Itapina + one more student represented Brazil", "team (snippet)")],
 2014: [medals("2022/11/2014-IESO-2014-Spain-Medals-List-.pdf", "Colossi")],
 2015: [medals("2022/11/2015-IESO-2015-Brazil-Medals-List.pdf", "Dehet")],
 2016: [medals("2022/11/2016-10th-IESO.pdf", "Ribeiro"),
        wb("https://web.archive.org/web/20160412210656/http://www.ifes.edu.br/noticias/16330-alunos-de-itapina-sao-selecionados-para-a-olimpiada-internacional-de-ciencias-da-terra", "Bullergahn", "IFES news (archived): Vilian Borchardt Bullergahn, Gustavo Rocha Alves and Ronaldo Rodrigues Ribeiro selected for IESO 2016", "3 of 4 (pre-event)"),
        wb("https://web.archive.org/web/20191015234617/https://portal.ifsuldeminas.edu.br/index.php/ultimas-noticias-ifsuldeminas/80-noticias-da-pppi/597-ieso-no-japao", "Lissandra", "IFSULDEMINAS news (archived): the four (3 IFES + Lissandra Souza, IFMG Bambuí); Ronaldo Rodrigues bronze")],
 2017: [medals("2022/11/2017-IESO2017-France-Medals-List.pdf", "PANCOTTO"),
        wb("https://web.archive.org/web/20251017002809/https://fapes.es.gov.br/Not%C3%ADcia/bolsistas-da-fapes-ganham-premiacoes-em-olimpiada-internacional-na-franca", "Pancotto", "FAPES news (archived): Bruno Pancotto bronze + ITFI 2nd, Guilherme Pratissoli ITFI 1st, Bruna de Oliveira also on the team", "3 of 4")],
 2018: [src("https://www.dropbox.com/s/zg4hkk9d6bdhq7g/2018%20Results.pdf?raw=1", "dropbox.com", "official", "medallists + team-award members", "IESO 2018 official results PDF (linked from igeoscied.org): Giancarlo Nappi bronze + ITFI 1st, Giovanna Klauck ESP 3rd", "Nappi"),
        wb("https://web.archive.org/web/20190819093342/https://portal.ifsuldeminas.edu.br/index.php/ultimas-noticias-ifsuldeminas/80-noticias-da-pppi/2286-finalistas-na-ieso", "Klauck", "IFSULDEMINAS news (archived): all four names, mentors, awards")],
 2019: [medals("2023/09/IESO-2019_Medalist.pdf", "De Sousa", "IGEO 2019 medallist deck: Ednaldo de Sousa bronze + ITFI bronze"),
        wb("https://web.archive.org/web/20190923193711/https://portal.ifsuldeminas.edu.br/index.php/institucional-geral/3062-ieso-2019", "Vilas Boas", "IFSULDEMINAS news (archived): the four names, mentors, bronze"),
        press("https://cidadesemfoco.com/aluno-do-ifpi-de-paulistana-vai-representar-o-brasil-na-13a-olimpiada-internacional-de-ciencias-da-terra/", "cidadesemfoco.com", "Ednaldo", "IFPI news: pre-event team (Mauro Aparecido Ambrósio Filho later replaced by João Augusto Vilas Boas dos Santos Gonçalves)", "pre-event roster")],
 2026: [press("https://drd.com.br/estudantes-do-ifmg-de-sao-joao-evangelista-vao-representar-o-brasil-em-olimpiada-internacional-na-italia/", "drd.com.br", "Washington", "Diário do Rio Doce (IFMG release): four IFMG São João Evangelista students named for IESO 2026 (Turin, 20-27 Aug)", "full (pre-event roster, short names)")],
}

NOTES = {
 2012: "IFTM (Uberaba) team; Rafael Franco Fernandez bronze (OLC spells 'Fernandes'), Mayara Cardoso Oliveira Best Presentation. 'Fabrício da Silva' and 'Renato Silva' are OLC short forms.",
 2013: "Roster 3 of 4: the IFES article naming the fourth student is offline; OLC's trio (Bruno Xavier Rodrigues, Rodrigo Altoe, Sávio Fabres Boldrini) is the OBAP 2012 winning team, not necessarily the IESO team - not used. Team awards only (ESP gold, ITFI gold); no individual medal.",
 2014: "Roster 1 of 4 (medal list only).",
 2015: "Hosted (Poços de Caldas). Roster 3 of 4 (medal list: bronze + team-award members).",
 2016: "Four names confirmed by IFSULDEMINAS; 'Lissandra Souza' is a short form.",
 2017: "Roster 3 of 4; 'Bruna de Oliveira' short form.",
 2019: "Pre-event roster listed Mauro Aparecido Ambrósio Filho; the post-event IFSULDEMINAS report names João Augusto Vilas Boas dos Santos Gonçalves instead - report followed.",
 2026: "Return after six years (IFMG São João Evangelista team, Turin 20-27 Aug 2026). Results not yet published for Brazil - medals null with medalStatus; names are short forms from the IFMG release. Re-check IFMG/IGEO.",
}

GLOBAL_NOTES = [
 "Editions attended: 2012-2019 (8) and 2026 (1). 2020 cancelled; 2021-2025 not attended (per DATA_STATUS verification against full participant lists). A bronze every year 2012-2019 except 2013.",
 "Backbone: the IGEO medal lists archived from igeoscied.org (live host unreachable during collection) give medallists and team-award members; Brazilian IF news (IFES, IFSULDEMINAS, FAPES, IFPI) complete the rosters for 2016, 2018, 2019. Rosters remain partial for 2013 (3), 2014 (1), 2015 (3), 2017 (3) - listed as coverage gaps.",
 "Team awards (ITFI, ESP) are international mixed-team prizes and are not stored as medals. Selection: OBAP (Olimpíada Brasileira de Agropecuária) winners from federal institutes.",
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
        "olympiadId": "ieso",
        "description": "Sources confirming Brazilian IESO contestants + results, per edition.",
        "provenanceClasses": {
            "official": "IGEO medal lists (archived igeoscied.org files; 2018 via the linked Dropbox PDF).",
            "primary": "olimpiadascientificas.org; IF and press news.",
            "archive": "Wayback Machine copies of IFES / IFSULDEMINAS / FAPES news.",
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
    md = ("# Per-Year Corroboration — Brazil at the IESO\n\n"
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
