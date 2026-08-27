#!/usr/bin/env python3
"""
Assemble data/corroboration.json and CORROBORATION.md for Brazil at the NBPhO,
repo-standard format. Verified by the 2026-08-22 research pass; official PDFs
content-verified.
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


SOURCES = {
 2020: [src("https://nbpho.ee/wp-content/uploads/2020/05/NB_final_results_publish.pdf", "nbpho.ee", "official", "full",
            "17th NBPhO (online) final results — G Antonio Italo, S Felipe Farias + Lucas Shoji, B Lucas Takayasu + 'Maria Freitas'", "Lucas Takayasu"),
        src("https://blog.etapa.com.br/noticias/olimpiada-de-fisica-dos-paises-balticos", "blog.etapa.com.br", "primary", "2/5",
            "Etapa (04/06/2020): prata+bronze, 17ª NBPhO online, 'primeira participação do Brasil'", "Lucas Shoji")],
 2025: [src("https://nbpho.ee/wp-content/uploads/2025/04/NBPhO-2025-grading-Final-for-web.pdf", "nbpho.ee", "official", "full",
            "grading/results PDF (short-form names; medals match dataset)", "Mateus Sussia"),
        src("https://www1.fisica.org.br/olimpiada/2025/index.php/15-soif/367-desempenho-de-destaque-na-nbpho-2025",
            "fisica.org.br", "primary", "full", "SBF: full names + schools + medals, Tallinn 25–27 Apr", "Tobias Gabriel Utz")],
 2026: [src("https://nbpho.ee/wp-content/uploads/2026/04/NBPhO-2026-results.pdf", "nbpho.ee", "official", "full",
            "results PDF (surname column truncated: 'Carneiro Bitten', 'Ulisses Fonsec')", "Benny Pereira"),
        src("https://mais.opovo.com.br/jornal/cidades/2026/05/03/aluno-cearense-se-destaca-em-olimpiada-internacional-de-fisica-na-estonia.html",
            "opovo.com.br", "primary", "1/5", "O Povo (03/05/2026): prata, Tallinn, best Brazilian", "Matheus Facó"),
        src("https://ne9.com.br/conheca-o-aluno-cearense-vice-campeao-da-olimpiada-de-fisica-na-europa/",
            "ne9.com.br", "primary", "1/5", "NE9 (30/04/2026): prata, Colégio 7 de Setembro", "Matheus Facó")],
}

NOTES = {
 2020: "nbpho.ee/nbpho-2020/ is 404 — the real page is nbpho.ee/nbpho2020/ (no hyphen). NOIC's NBPhO info page wrongly claims Brazil debuted in 2021; the official 2020 PDF + Etapa post prove 2020.",
 2026: "PDF spells 'Leonardo Facó' vs dataset 'Faco' — accent variant, same person (Matheus Leonardo Faco).",
}

GLOBAL_NOTES = [
 "All three official nbpho.ee PDFs verified live 2026-08-22.",
 "Official PDFs use short/truncated name forms; SBF's 2025 article is the full-name authority for that year.",
 "Brazil's absences 2021–2024 are documented — no participation to source.",
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
        "olympiadId": "nbpho",
        "description": "Independent web sources confirming Brazilian NBPhO participants + results, per edition.",
        "provenanceClasses": {
            "official": "nbpho.ee official results PDFs.",
            "primary": "SBF articles, schools (Etapa), Brazilian press (O Povo, NE9).",
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
        flag = "" if r["namingSourceCount"] >= 3 else "  ⚠️ **<3**"
        note = " 📝" if "note" in r else ""
        lines.append(f"| {r['year']} | {r['namingSourceCount']} | {r['independentPrimaryCount']} | {doms}{flag}{note} |")
    n3 = sum(1 for r in records if r["meetsThreeNaming"])
    p3 = sum(1 for r in records if r["meetsThreePrimary"])

    details = []
    for r in records:
        details.append(f"### {r['year']}")
        for i, s in enumerate(r["sources"], 1):
            details.append(f"{i}. **{s['domain']}** ({s['cls']}, coverage: {s['coverage']}) — {s['url']} — {s['confirms']}")
        if "note" in r:
            details.append(f"\n> {r['note']}")
        details.append("")

    md = f"""# Per-Year Corroboration — Independent Sources for Brazil at the NBPhO

**Machine-readable version:** `data/corroboration.json`. Rebuild with
`python3 scripts/build_corroboration.py`; re-verify URLs with
`python3 scripts/verify_corroboration.py`. Built from the 2026-08-22 research pass.

## Headline

- **{n3} of {len(records)} editions** have ≥3 participant-naming source domains.
- Every edition anchored by its official nbpho.ee results PDF (verified live).

## Notes

{chr(10).join(f"- {n}" for n in GLOBAL_NOTES)}

## Summary table

| Year | Naming domains | Indep-primary | Domains |
|-----:|:--:|:--:|---------|
{chr(10).join(lines)}

📝 = per-year note below.

## Per-year sources

{chr(10).join(details)}"""

    with open(os.path.join(ROOT, "CORROBORATION.md"), "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Editions: {len(records)}")
    print(f">=3 naming: {n3}/{len(records)}; >=3 independent-primary: {p3}/{len(records)}")
    print("Wrote data/corroboration.json + CORROBORATION.md")


if __name__ == "__main__":
    main()
