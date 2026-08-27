#!/usr/bin/env python3
"""
Corroboration for Brazil at the OII/CIIC (repo-standard). 2026-08-22 collection pass:
every URL fetched and content-verified. Editions: 2004, 2007, 2011, 2012-2026.
2011 = participation confirmed, roster unknown (no records in dataset).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OBI = "https://olimpiada.ic.unicamp.br/competicoes/oii_ciic/"


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


SOURCES = {
 2004: [src("https://web.archive.org/web/20050216131717/http://oia.org.ar/ciic/result2004.html",
        "oia.org.ar (Wayback)", "official", "full",
        "VI CIIC results: Brasil 1G/2S/4B/3 meritos, per-problem scores (meritos mapped to honorable-mention)", "Slepetys")],
 2007: [src("https://www.objetivo.br/institucional/noticias.aspx?titulo=irmaos-amigos-e-companheiros-de-estudo",
        "objetivo.br", "primary", "1/? — only documented member",
        "Ricardo Hahn Pereira silver; article says he was the only high-schooler in the delegation", "Ricardo"),
        src("https://www.iberoinformatica.org/results/2007/all", "iberoinformatica.org", "official", "stub",
        "official DB 2007 page exists but is empty (0 contestants) — no official roster published", None)],
 2011: [src("http://programanacionaldeolimpiadas.blogspot.com/2011/09/resultados-de-la-iberoamericana-de.html",
        "programanacionaldeolimpiadas.blogspot.com", "primary", "participation only",
        "XII CIIC: Brazil among participating countries; no Brazilian names — ROSTER UNKNOWN, no dataset records", "Brasil")],
 2012: [src("https://www.iberoinformatica.org/results/2012/all", "iberoinformatica.org", "official", "full",
        "official per-name results", "Renato Ferreira Pinto Junior"),
        src(OBI, "olimpiada.ic.unicamp.br", "primary", "full", "national organizer roster w/ schools", None),],
 2013: [src("https://www.iberoinformatica.org/results/2013/all", "iberoinformatica.org", "official", "full",
        "official per-name results", "Mateus Carvalho Dantas"),
        src(OBI, "olimpiada.ic.unicamp.br", "primary", "full", "national organizer roster w/ schools", None),],
 2014: [src("https://www.iberoinformatica.org/results/2014/all", "iberoinformatica.org", "official", "full",
        "official per-name results; Brazilian champion: Zelazny", "Michel Rozenberg Zelazny"),
        src(OBI, "olimpiada.ic.unicamp.br", "primary", "full", "national organizer roster w/ schools", None),],
 2015: [src("https://www.iberoinformatica.org/results/2015/all", "iberoinformatica.org", "official", "full",
        "official per-name results; Brazilian champion: Bezrutchka", "Mateus Bezrutchka"),
        src(OBI, "olimpiada.ic.unicamp.br", "primary", "full", "national organizer roster w/ schools", None),],
 2016: [src("https://www.iberoinformatica.org/results/2016/all", "iberoinformatica.org", "official", "full",
        "official per-name results", "Victor Agnez Lima"),
        src(OBI, "olimpiada.ic.unicamp.br", "primary", "full", "national organizer roster w/ schools", None),],
 2017: [src("https://www.iberoinformatica.org/results/2017/all", "iberoinformatica.org", "official", "full",
        "official per-name results", "Gabriel Silva Simões"),
        src(OBI, "olimpiada.ic.unicamp.br", "primary", "full", "national organizer roster w/ schools", None),],
 2018: [src("https://www.iberoinformatica.org/results/2018/all", "iberoinformatica.org", "official", "full",
        "official per-name results; Brazilian champion: Bulhões + Ivan Carvalho (co)", "Frederico Bulhões de Sousa Ribeiro"),
        src(OBI, "olimpiada.ic.unicamp.br", "primary", "full", "national organizer roster w/ schools", None),],
 2019: [src("https://www.iberoinformatica.org/results/2019/all", "iberoinformatica.org", "official", "full — 10 incl. 3 non-medalists (OBI lists only 7)",
        "official per-name results", "Thiago Mota Martins"),
        src(OBI, "olimpiada.ic.unicamp.br", "primary", "full", "national organizer roster w/ schools", None),],
 2020: [src("https://www.iberoinformatica.org/results/2020/all", "iberoinformatica.org", "official", "full",
        "official per-name results; Brazilian champion: Yan Matheus", "Yan Matheus Tavares e Silva"),
        src(OBI, "olimpiada.ic.unicamp.br", "primary", "full", "national organizer roster w/ schools", None),],
 2021: [src("https://www.iberoinformatica.org/results/2021/all", "iberoinformatica.org", "official", "full",
        "official per-name results; Brazilian champion: Oda", "Luiz Henrique Yuji Delgado Oda"),
        src(OBI, "olimpiada.ic.unicamp.br", "primary", "full", "national organizer roster w/ schools", None),],
 2022: [src("https://www.iberoinformatica.org/results/2022/all", "iberoinformatica.org", "official", "full",
        "official per-name results; Brazilian champion: Carolina + Luca + Pedro Chen (co, shared w/ ESP/CUB)", "Pedro Shinzato Chen"),
        src(OBI, "olimpiada.ic.unicamp.br", "primary", "full", "national organizer roster w/ schools", None),],
 2023: [src("https://www.iberoinformatica.org/results/2023/all", "iberoinformatica.org", "official", "full",
        "official per-name results; Brazilian champion: Arthur Lobo + Leonardo Valente (co)", "Vladimir Arauzo Huisa"),
        src(OBI, "olimpiada.ic.unicamp.br", "primary", "full", "national organizer roster w/ schools", None),],
 2024: [src("https://www.iberoinformatica.org/results/2024/all", "iberoinformatica.org", "official", "full",
        "official per-name results; Brazilian champion: Arthur Lobo", "Arthur Lobo Leite Lopes"),
        src(OBI, "olimpiada.ic.unicamp.br", "primary", "full", "national organizer roster w/ schools", None),],
 2025: [src("https://www.iberoinformatica.org/results/2025/all", "iberoinformatica.org", "official", "full",
        "official per-name results; Brazilian champion: Graminholi", "Fernando Graminholi Gonçalves"),
        src(OBI, "olimpiada.ic.unicamp.br", "primary", "full", "national organizer roster w/ schools", None),],
 2026: [src("https://www.iberoinformatica.org/results/2026/all", "iberoinformatica.org", "official", "full",
        "official per-name results; Brazilian champion: Maria Clara Fontes Silva", "Maria Clara Fontes Silva"),]
}

NOTES = {
 2004: "Correspondence-era format with a 4th tier MERITO below bronze — mapped to honorable-mention. Gold/silver tie at 217,5 points reported verbatim by the source.",
 2007: "Roster partially documented: only Ricardo Hahn Pereira (silver) is recoverable; delegation size unknown.",
 2011: "Participation confirmed, roster unknown — official DB returns HTTP 500 for 2011; OBI page starts at 2012.",
 2016: "Three Brazilians at rank 1 (350.0) tied with 4 Mexicans; OBI marks no 2016 champion.",
 2019: "Official page lists 10 incl. 3 non-medalists; OBI lists only the 7 medalists — official is the more complete source.",
 2026: "Single-source year so far: OBI page has no OII 2026 section yet. Re-check for the second source.",
}

GLOBAL_NOTES = [
 "Renamed CIIC -> OII after 2022. Official DB (iberoinformatica.org) is per-name for 2012-2026; pre-2012 rests on archived national-federation pages.",
 "Remote/correspondence contest awarded at the IOI — hence 9-10 person delegations (unlike travel olympiads).",
 "rawName policy: official-DB forms upgraded to the fullest documented variant (OBI fuller middles, accents) per the most-complete-name display rule.",
 "Undocumentable era: 1999, 2006, 2008-2010 have no surviving results anywhere (some likely non-edition years); Brazil positively absent 1998, 2001-2003, 2005.",
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
        "olympiadId": "oii",
        "description": "Sources confirming Brazilian OII/CIIC participants + results, per edition.",
        "provenanceClasses": {
            "official": "iberoinformatica.org per-name results DB; archived OIA-Argentina CIIC pages.",
            "primary": "OBI/Unicamp national organizer rosters; Objetivo; Argentine ministry blog.",
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

    md = ("# Per-Year Corroboration — Brazil at the OII/CIIC\n\n"
          "**Machine-readable:** `data/corroboration.json`. Rebuild: `python3 scripts/build_corroboration.py`; "
          "verify: `python3 scripts/verify_corroboration.py`. 2026-08-22 collection pass.\n\n## Notes\n\n"
          + "\n".join(f"- {n}" for n in GLOBAL_NOTES)
          + "\n\n## Summary\n\n| Year | Sources | Domains |\n|-----:|:--:|---------|\n" + "\n".join(lines)
          + "\n\n## Per-year sources\n\n" + "\n".join(details))
    with open(os.path.join(ROOT, "CORROBORATION.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Editions: {len(records)}")
    print("Wrote data/corroboration.json + CORROBORATION.md")


if __name__ == "__main__":
    main()
