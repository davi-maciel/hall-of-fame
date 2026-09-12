#!/usr/bin/env python3
"""
Corroboration for Brazil at the IOL (repo-standard). 2026-09-10 collection pass: every URL fetched and
content-verified. Editions attended: 2011-2014, 2016-2019, 2022-2026 (13). Not attended: 2015; 2020 cancelled;
2021 (Brazil could not join the remote edition).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PART = "https://ioling.org/participants/BRA"
BRA = "https://ioling.org/results/BRA/"
OBL = "https://obling.org/"
OLC = "https://olimpiadascientificas.org/equipes-brasileiras/linguistica/iol/"


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def part(needle):
    return src(PART, "ioling.org", "official", "full", "ioling.org 'Delegations' for Brazil: every team, member and leader per year (medal emoji on winners)", needle)


def res(year, needle):
    return src(f"https://ioling.org/results/{year}/", "ioling.org", "official", "awards + scores", "ioling.org per-year results: individual contest awards (medals, HM) and team contest results", needle)


def bra(needle):
    return src(BRA, "ioling.org", "official", "medallists + HM", "ioling.org country page: all Brazilian medallists, honourable mentions and team trophies", needle)


def obl(slug, needle):
    return src(OBL + slug, "obling.org", "official", "full", "OBL (national organizer) edition page: IOL team with full names, schools and cities, awards", needle)


def olc(needle, sub=""):
    return src(OLC + sub, "olimpiadascientificas.org", "primary", "full", "olimpiadascientificas.org roster (2011-2012) with cities and awards", needle)


def noic(url, needle, confirms, coverage="full"):
    return src(url, "noic.com.br", "primary", coverage, confirms, needle)


def press(url, domain, needle, confirms, coverage="full"):
    return src(url, domain, "primary", coverage, confirms, needle)


SOURCES = {
 2011: [part("Miquelin"), src("https://ioling.org/results/2011/", "ioling.org", "official", "awards + scores (no Brazilian award)", "ioling.org 2011 results: no Brazilian award that year", None), obl("kyta", "Miquelin"), olc("Miquelin", "iol-2011/")],
 2012: [part("Miyazaki"), res(2012, "Miyazaki"), bra("Miyazaki"), obl("noke-vana", "Miyazaki"), olc("Miyazaki", "iol-2012/")],
 2013: [part("Navarro Barros"), res(2013, "Navarro Barros"), bra("Navarro Barros"), obl("paraplu", "Navarro Barros")],
 2014: [part("Cavalcanti Silva"), res(2014, "Diniz"), bra("Diniz"), obl("vina", "Cavalcanti"), noic("https://noic.com.br/linguistica/resultado-brasileiro-na-iol-2014/", "DINIZ", "NOIC: the single 2014 award (HM)", "awards")],
 2016: [part("Kumruian"), res(2016, "Ozaki"), bra("Ozaki"), obl("okun", "Kumruian")],
 2017: [part("Herkenhoff"), res(2017, "Palote"), bra("Palote"), obl("nanduti", "Herkenhoff")],
 2018: [part("Steinmetz"), res(2018, "Palote"), bra("Palote"), obl("margele", "Steinmetz"),
        noic("https://noic.com.br/uncategorized/confira-o-resultado-do-brasil-na-olimpiada-internacional-de-linguistica/", "Steinmetz", "NOIC: both teams, S + B + HM, team bronze")],
 2019: [part("Nh"), res(2019, "Palote"), bra("Palote"), obl("yora", "Azevedo"),
        noic("https://noic.com.br/uncategorized/brasileiros-conquistam-duas-pratas-na-olimpiada-internacional-de-linguistica/", "Palote", "NOIC: two silvers, both teams"),
        noic("https://noic.com.br/linguistica/confira-as-equipes-da-iol/", "Palote", "NOIC team announcement", "full (pre-event roster)")],
 2022: [part("Naigeborin"), res(2022, "Naigeborin"), bra("Naigeborin"), obl("mascate", "Naigeborin")],
 2023: [part("Oikawa"), res(2023, "Oikawa"), bra("Oikawa"), obl("khipu", "Oikawa"),
        noic("https://noic.com.br/uncategorized/o-brasil-obteve-resultado-historico-na-iol/", "Luiz Satoshi", "NOIC: 2G + 5B + HM (record)"),
        noic("https://noic.com.br/uncategorized/saiu-o-time-da-iol/", "Luiz Satoshi", "NOIC team announcement", "full (pre-event roster)")],
 2024: [part("Ramscheid"), res(2024, "Moraes Barros"), bra("Moraes Barros"), obl("abya-yala", "Ramscheid")],
 2025: [part("Pigini"), res(2025, "Pigini"), bra("Pigini")],
 2026: [part("Lonel"), res(2026, "Lonel"), bra("Lonel")],
}

NOTES = {
 2011: "Debut (Pittsburgh) with two teams, Itararé (4) and Suassuna (3); no awards. ioling/OBL spell the Etapa student 'André Amaral de Souza/Sousa' - the pool form (Rioplatense 2008, IOI 2012) 'Sousa' is used.",
 2012: "First medals: Ivan Tadeu Ferreira Antunes Filho silver, Pedro Neves Lopes bronze; Rafael Kazuhiro Miyazaki HM + best-solution prize (problem 2).",
 2013: "Only gold before 2023: Gabriel Alves da Silva Diniz (+ best-solution prize).",
 2016: "Registered as 'Brazil 1' (single team).",
 2018: "Two teams (Pães, Pões); Pões won the team-contest bronze trophy (not recorded as an individual medal). Artur Corrêa Souza: best-solution prize only.",
 2019: "Gustavo Palote da Silva Martins and João Henrique Oliveira Fontes entered the IOL Hall of Fame (repeat medallists).",
 2022: "Return after the 2020 cancellation and the 2021 remote edition Brazil could not join. Full names per OBL (ioling has 'Fernando César', 'Wesley Andrade'...).",
 2023: "Record year (Bansko): 2G + 5B + HM; Quero-quero took the team-contest HM.",
 2024: "Brazil hosted (Brasília). OBL/ioling short forms 'Paulo Portela' (Farias Brito, Fortaleza) and 'Pedro Rocha' (Colégio Núcleo, Recife) kept as the fullest documented forms; Fêsãw 2025 team-contest bronze trophy not recorded as individual medals.",
 2025: "Team Fêsãw: team-contest bronze trophy; individual: Pigini bronze + four HMs. Names as registered on ioling (no OBL page for the Ojidu cycle yet).",
 2026: "Bucharest: Felipe Araújo Moraes Barros's second silver (Hall of Fame), Levi O. Matias bronze, two HMs. Names as registered on ioling.",
}

GLOBAL_NOTES = [
 "Editions attended: 2011-2014, 2016-2019, 2022-2026 (13; 21 teams, 83 participants per ioling.org). Not attended: 2015 (no team), 2020 (cancelled), 2021 (Brazil could not join the remote edition - OBL).",
 "Every row rests on ioling.org (official: delegations page + per-year results + country page); the national organizer's OBL edition pages (2011-2024) give full names, schools and cities; NOIC/OLC corroborate 2011-2014 and 2018-2023.",
 "Awards: individual-contest gold/silver/bronze and honourable mention (= honorable-mention). Team-contest trophies/HMs and best-solution prizes are noted, not stored as medals. `team` = the delegation's nickname when Brazil sent two teams.",
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
        "olympiadId": "iol",
        "description": "Sources confirming Brazilian IOL contestants + results, per edition.",
        "provenanceClasses": {
            "official": "ioling.org (IOL) delegations, results and country pages; obling.org (OBL, national organizer) edition pages.",
            "primary": "NOIC; olimpiadascientificas.org.",
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

    md = ("# Per-Year Corroboration — Brazil at the IOL\n\n"
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
