#!/usr/bin/env python3
"""
Corroboration for Brazil at the Iranian Geometry Olympiad (repo-standard). 2026-09-09 collection pass:
every URL fetched and content-verified. Editions: 2016-2025 (10; correspondence contest, three age levels).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OBM = "https://www.obm.org.br/resultados-olimpiada-iraniana-de-geometria-igo/"


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def obm(needle, coverage="medallists only"):
    return src(OBM, "obm.org.br", "primary", coverage, "national organizer results table (2016-2024, by level): names, city/state, medal", needle)


def xlsx(url, needle):
    return src(url, "igo-official.com", "official", "complete: every Brazilian participant, all levels, per-problem scores, medal (xlsx; content checked locally 2026-09-09, the verifier only tests liveness)",
               "official final-results spreadsheet (one sheet per level)", None)


def post(url, needle, confirms, coverage="medallists only", domain="obm.org.br"):
    return src(url, domain, "primary", coverage, confirms, needle)


SOURCES = {
 2016: [obm("Bigolin")],
 2017: [obm("Hisatsuga"), post("https://impa.br/notices/brasil-conquista-13-medalhas-na-olimpiada-de-geometria/", "Hisatsuga", "IMPA: 13 medals, names by level", domain="impa.br")],
 2018: [obm("Sponchiado"), post("https://impa.br/notices/brasil-ganha-nove-medalhas-em-olimpiada-de-geometria/", "Sponchiado", "IMPA: 9 medals, names by level", domain="impa.br"),
        post("https://noic.com.br/matematica/veja-o-resultado-do-brasil-na-igo-2018/", "Sponchiado", "NOIC results post", domain="noic.com.br")],
 2019: [obm("Lengruber"), post("https://www.obm.org.br/2019/10/18/estudantes-brasileiros-conquistaram-11-medalhas-na-igo-de-2019/", "Lengruber", "OBM news: 11 medals, names by level"),
        post("https://noic.com.br/uncategorized/confira-o-resultado-da-olimpiada-iraniana-de-geometria/", "Dellaroli", "NOIC results post (medallists named)", domain="noic.com.br")],
 2020: [obm("Machado Lage"), post("https://www.obm.org.br/2021/01/12/igo-2020-conheca-o-resultado-do-brasil/", "Domingos Porto", "OBM news: results table by level")],
 2021: [obm("Shimamura"), post("https://www.obm.org.br/2021/12/27/16218/", "Shimamura", "OBM news: 10 medals, results table by level")],
 2022: [obm("Stabenow"), post("https://www.obm.org.br/2023/01/02/brasil-conquista-8-medalhas-na-9a-igo/", "Stabenow", "OBM news: 8 medals, results table by level")],
 2023: [xlsx("https://igo-official.com/wp-content/uploads/2025/02/IGO-2023-Final-Results.xlsx", "Padovan"), obm("Padovan"),
        post("https://www.obm.org.br/2024/04/11/igo-2023-conheca-o-resultado-do-brasil/", "Fontes Silva", "OBM news: results table by level")],
 2024: [xlsx("https://igo-official.com/wp-content/uploads/2025/02/Final-Results-IGO-2024.xlsx", "Gago"), obm("Gago")],
 2025: [xlsx("https://igo-official.com/wp-content/uploads/2025/12/Final-Results-IGO-2025.xlsx", "Acioli"),
        post("https://www.obm.org.br/2026/01/01/igo-2024-conheca-os-resultados/", "Acioli", "OBM news (2026-01-01): 12 medals, results table by level")],
}

NOTES = {
 2016: "Brazil's debut (3rd IGO): six medallists in the Intermediate/Advanced levels - OBM table only (single source). 'Tarcisio' -> Tarcísio (pool form).",
 2019: "First year with an Elementary-level medallist; 11 medals.",
 2023: "From 2023 the official spreadsheets list every Brazilian participant with per-problem scores, so unawarded participants (medal null) are recorded - 18 participants, 7 medals. Official 'Julia de Paula Pessoa Leguiza' etc. match OBM.",
 2024: "18 participants, 15 medals (official + OBM agree on every medal). OBM table 'Castelo Branco' -> Castello; 'Marco Aurélio' -> the IMO/APMO form.",
 2025: "12th IGO: 14 participants, 12 medals (official spreadsheet + OBM news 2026-01-01; OBM's all-years table stops at 2024).",
}

GLOBAL_NOTES = [
 "Correspondence olympiad run from Iran (October/November); Brazilian OBM awardees sit it locally in three age levels (Elementary, Intermediate, Advanced; a fourth 'free' level has had no Brazilians). Brazil takes part since 2016.",
 "Coverage: 2016-2022 medallists only (OBM's table and news list medals, not the full entry list); 2023-2025 complete from the official final-results spreadsheets (medal null = participant without medal). 'level' and, where official, 'score' are recorded.",
 "rawName policy: OBM table forms aligned to the pool (imo/apmo/maio/...); the official spreadsheets use the same Portuguese full forms.",
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
        "olympiadId": "igo",
        "description": "Sources confirming Brazilian IGO participants + results, per edition.",
        "provenanceClasses": {
            "official": "igo-official.com final-results spreadsheets (2023-2025).",
            "primary": "OBM (national organizer) results table and news; IMPA; NOIC.",
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

    md = ("# Per-Year Corroboration — Brazil at the IGO\n\n"
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
