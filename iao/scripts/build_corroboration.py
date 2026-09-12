#!/usr/bin/env python3
"""
Corroboration for Brazil at the IAO (repo-standard). 2026-09-10 collection pass: every URL fetched and
content-verified. Editions attended: 1998, 1999, 2000, 2002-2007 (9). 2001: applied, did not travel. 2008+: absent.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
R = "http://www.issp.ac.ru/iao/"
OLC = "https://olimpiadascientificas.org/equipes-brasileiras/astronomia/iao/"
WIKI = "https://pt.wikipedia.org/wiki/Olimp%C3%ADada_Internacional_de_Astronomia"


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def official(path, needle, confirms, coverage="medallists + team list"):
    return src(R + path, "issp.ac.ru", "official", coverage, confirms, needle)


def olc(needle, sub="", coverage="full"):
    return src(OLC + sub, "olimpiadascientificas.org", "primary", coverage, "olimpiadascientificas.org roster (source: OBA site) incl. non-medallists and states", needle)


def wiki(needle="Brasil participa da IAO"):
    return src(WIKI, "pt.wikipedia.org", "primary", "team size + medal counts", "pt.wikipedia 'A Participação do Brasil' table (participants and medals per year)", needle)


SOURCES = {
 1998: [official("1998/iao98_e.html", "Brazil", "III IAO report: Brazil among the five teams; diploma table Brazil 0/0/1 (winner names never posted)", "medal count + team list"), olc("Iguchi"), wiki()],
 1999: [official("1999/iao99_e.html", "Shridhar Jayanthi", "IV IAO report: Shridhar Jayanthi (São José dos Campos) II prize; diploma table 0/1/0"), olc("Della Lastra", "iao-1999/"), wiki()],
 2000: [official("2000/iao00_e.html", "Jayanthi Shridhar", "V IAO report: Jayanthi Shridhar III prize; diploma table 0/0/1"), olc("Quachio", "iao-2000/"), wiki()],
 2002: [official("2002/iao02_er.html", "Bortoluci", "VII IAO results: Bortoluci José III, Pereira Felipe III; team table"), official("2002/iao02_e.html", "Brazil", "VII IAO report: Brazil applied and arrived", "team list"), olc("Slepetys", "iao-2002/"), wiki()],
 2003: [official("2003/iao03_e.html", "Celistrino", "VIII IAO report: Celistrino Teixeira II, Silva Michel III (55 participants, 14 teams)"), olc("Cosentino", "iao-2003/"), wiki()],
 2004: [official("2004/iao04_e.html", "Echelmeier", "IX IAO report: Villar Coelho II (junior), Echelmeier III and de Araujo e Silva III (senior)"), olc("Echelmeier"), wiki()],
 2005: [official("2005/iao05_pw.html", "Villar Coelho", "X IAO prizewinners: Villar Coelho Felipe Ferreira I Diploma"), official("2005/index.html", "Villar Coelho", "X IAO front page: Brazil among teams; Felipe Ferreira Villar Coelho gold", "team list + gold"), olc("Donadia"), wiki()],
 2006: [official("2006/iao06_pw.html", "Fonseca", "XI IAO prizewinners: Assis Felipe Goncalves II (senior), Araujo Hugo Fonseca III (junior)"), olc("Palmeira"), wiki()],
 2007: [official("2007/iao07_pw.html", "Parpinel", "XII IAO prizewinners: Fonseca Araujo Hugo II, Parpinel Cavina Rafael III"), olc("Mippo"), wiki()],
}

NOTES = {
 1998: "Debut (OBA's founding year). The official page says 'names of the winners to be on the Web page' and never posted them; Shridhar Jayanthi's bronze rests on OLC/OBA plus the official Brazil 0/0/1 diploma count. 1998 rows carry schools rather than states on OLC.",
 2000: "Six names on OLC (IAO teams are five: 3 alpha + 2 beta); the sixth is presumably a guest/observer - kept as listed.",
 2002: "2001 (Crimea): the official 'information before' page lists Brazil among applicants but not among the nine teams that arrived - no edition row.",
 2003: "Raul Celistrino Teixeira = silver; Michel Aquena Silva = bronze (official writes 'Silva Michel').",
 2005: "Only Brazilian IAO gold (Felipe Ferreira Villar Coelho, junior group, Beijing). OLC lists six names vs Wikipedia's five.",
 2006: "OLC 'Felipe Gonçalves Assis' = the IBO 2006 contestant 'Felipe Gonçalves de Assis' (Campina Grande-PB); pool form kept. Six names on OLC.",
 2007: "Last edition attended: Brazil switched to the new IOAA from 2007 on. Cindy Yuchi Tsai and Rafael Parpinel Cavina went on to IOAA 2008.",
}

GLOBAL_NOTES = [
 "Editions attended: 1998, 1999, 2000, 2002, 2003, 2004, 2005, 2006, 2007 (9). 2001: applied, did not travel (official page). 2008-2015: no Brazil in the official winners/results lists (checked 2008, 2009, 2013 lists directly). pt.wikipedia's table shows one Brazilian silver in 2009 and 2013 - contradicted by the official prizewinner lists, presumably an IOAA conflation; not used.",
 "Diplomas I/II/III are recorded as gold/silver/bronze: 1 gold, 5 silver, 9 bronze (15). Non-medallist rows come from OLC's OBA-sourced rosters (official pages list only prizewinners and team names).",
 "Names: OLC/OBA Portuguese forms; official pages write surname-first ASCII (e.g. 'Villar Coelho Felipe Ferreira'). Five students also appear in ioaa/ijso/ipho/ibo/maio/oii/ioi datasets (see aliases notes).",
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
        "olympiadId": "iao",
        "description": "Sources confirming Brazilian IAO contestants + results, per edition.",
        "provenanceClasses": {
            "official": "issp.ac.ru per-year IAO reports and prizewinner pages.",
            "primary": "olimpiadascientificas.org rosters (OBA-sourced); pt.wikipedia participation table.",
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

    md = ("# Per-Year Corroboration — Brazil at the IAO\n\n"
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
