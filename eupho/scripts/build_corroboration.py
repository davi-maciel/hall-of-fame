#!/usr/bin/env python3
"""
Assemble data/corroboration.json and CORROBORATION.md for Brazil at the EuPhO,
repo-standard format. Verified by the 2026-08-22 research pass: every URL fetched
live and content-checked against graph.json rosters.
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


def pdf(url, confirms, needle):
    return src(url, "eupho.ee", "official", "full", f"official results PDF — {confirms}", needle)


SOURCES = {
 2017: [pdf("https://eupho.ee/wp-content/uploads/2020/07/1stEuPhO_results.pdf", "1st EuPhO (Tallinn), results+medals; Diogo listed as 'Diogo Netto'", "Gabriel Golfetti"),
        src("https://noic.com.br/fisica/ipho/brasil-conquista-medalhas-de-ouro-prata-e-bronze-na-eupho/", "noic.com.br", "primary", "full",
            "per-student medals, 1ª edição/Estônia (2017-05-24)", "Golfetti")],
 2018: [pdf("https://eupho.ee/wp-content/uploads/2020/07/eupho18-results.pdf", "full ranked table w/ scores ('Gabriel Trigo', no 'Guerra')", "Rafael Timbó"),
        src("https://noic.com.br/uncategorized/tres-pratas-e-dois-bronzes-para-o-brasil-na-eupho/", "noic.com.br", "primary", "full",
            "3 pratas + 2 bronzes, Moscou (2018-06-01)", "GABRIEL GUERRA TRIGO"),
        src("https://blog.etapa.com.br/noticias/aluno-etapa-conquista-bronze-na-2a-eupho", "blog.etapa.com.br", "primary", "1/5",
            "Etapa student bronze, 2ª EuPhO", "Gabriel Guerra Trigo")],
 2019: [pdf("https://eupho.ee/wp-content/uploads/2020/07/EuPhO2019_results.pdf", "full results table", "Gabriel Capelo Domingues"),
        src("https://noic.com.br/fisica/resultado-historico-para-o-brasil-na-eupho-2019/", "noic.com.br", "primary", "full",
            "Riga/Letônia results (2019-06-04)", "Santana Moura"),
        src("https://blog.etapa.com.br/noticias/bronze-na-olimpiada-europeia-de-fisica", "blog.etapa.com.br", "primary", "1/5",
            "bronze at 3ª edição, Riga (07/06/2019)", "Miguel Vieira Pereira")],
 2020: [pdf("https://eupho.ee/wp-content/uploads/2020/07/EuPhO-2020-results.pdf", "online edition, 4-student team w/ scores+awards", "Menegon"),
        src("https://noic.com.br/uncategorized/sai-o-resultado-da-seletiva-de-fisica-descubra-quem-respresentara-o-brasil-nas-internacionais/",
            "noic.com.br", "primary", "3/4 — pre-event announcement (roster later changed, see note)",
            "NOIC seletiva announcement (2020-03-15)", "Wanderson Faustino Patricio")],
 2021: [pdf("https://eupho.ee/wp-content/uploads/2021/06/EuPhO2021-results.pdf", "full results table", "Ian Seo Takose"),
        src("https://www.sbfisica.org.br/v1/olimpiada/2021/index.php/soif/15-soif/269-brasil-conquista-cinco-medalhas-na-eupho-2021.html",
            "sbfisica.org.br", "primary", "full", "SBF/OBF: 5 medals", "Takose"),
        src("https://blog.etapa.com.br/noticias/eupho-2021", "blog.etapa.com.br", "primary", "2/5", "Etapa students at EuPhO 2021", "Makoto")],
 2022: [pdf("https://eupho.ee/wp-content/uploads/2022/05/EuPhO2022-awards.pdf", "awards list", "Pepato"),
        src("https://www.sbfisica.org.br/v1/olimpiada/2022/index.php/soif/15-soif/304-olimpiada-europeia-de-fisica-eupho-2022.html",
            "sbfisica.org.br", "primary", "full", "SBF article incl. Alícia HM", "Everton Albuquerque"),
        src("https://noic.com.br/olimpiadas/fisica/hall-da-fisica/", "noic.com.br", "archive", "partial",
            "NOIC hall compilation w/ testimonials (2018/2021/2022/2023)", "João Pepato")],
 2023: [pdf("https://eupho.ee/wp-content/uploads/2023/06/EuPhO23-results.pdf", "full results", "Albernaz"),
        src("https://noic.com.br/uncategorized/resultados-da-eupho/", "noic.com.br", "primary", "full",
            "ouro + 3 pratas + bronze, Alemanha (2023-07-10)", "Alberto Akira Ito Albernaz"),
        src("https://www1.fisica.org.br/olimpiada/2024/index.php/15-soif/329-desempenho-historico-na-eupho-2023",
            "fisica.org.br", "primary", "full", "SBF article", "Mazili")],
 2024: [pdf("https://eupho.ee/wp-content/uploads/2024/07/EuPhO-2024-results-resultsforweb.pdf", "full results, 256 participants", "Bruno Machado Feltran"),
        src("https://www1.fisica.org.br/olimpiada/2024/index.php/soif/15-soif/356-brasil-conquista-2-pratas-e-3-bronzes-na-eupho-2024",
            "fisica.org.br", "primary", "full", "SBF: 2 pratas + 3 bronzes", "Gurjão")],
 2025: [pdf("https://eupho.ee/wp-content/uploads/2025/06/EuPhO_2025_results-3.pdf",
            "results (Sofia) — 4/5: Hideshima (no award) absent from PDF; two-column text layer, token matching needed", "Avelar"),
        src("https://www1.fisica.org.br/olimpiada/2025/index.php/15-soif/373-conquistas-na-eupho-2025",
            "fisica.org.br", "primary", "full", "SBF article — all 5 incl. Hideshima (photo caption) + schools", "Vitor Takashi Hideshima"),
        src("https://www.agazeta.com.br/colunas/leonel-ximenes/einstein-capixaba-faz-bonito-na-olimpiada-de-fisica-na-europa-0625",
            "agazeta.com.br", "primary", "1/5", "column 26/06/2025: prata, IFES, Bulgária", "Patrick Avelar")],
 2026: [pdf("https://eupho.ee/wp-content/uploads/2026/06/EuPhO_2026_Results-1.pdf", "all 5 Brazilians bronze (ranks 73–96), Sweden", "Yamashita Risseto"),
        src("https://g1.globo.com/pa/para/noticia/2026/06/19/estudante-do-pa-conquista-bronze-inedito-na-olimpiada-europeia-de-fisica.ghtml",
            "g1.globo.com", "primary", "1/5", "bronze, EuPhO 2026 na Suécia (19/06/2026)", "Eyke Cardoso"),
        src("https://www.oliberal.com/para/aluno-paraense-e-selecionado-para-representar-o-brasil-na-olimpiada-europeia-de-fisica-1.1095992",
            "oliberal.com", "primary", "1/5 — pre-event selection (Mar 2026)", "O Liberal selection story", "Eyke")],
}

NOTES = {
 2018: "Official PDF has 'Gabriel Trigo'; NOIC + Etapa corroborate the full 'Gabriel Guerra Trigo' (dataset form).",
 2020: "Online edition, 4-student team. NOIC's March seletiva announced Takose and Rafael Prado Basto for EuPhO; the actual team (official PDF) was 4 students incl. Alexandre S. B. de Almeida, without Takose/Basto. No post-event Brazilian article exists — results are official-only.",
 2025: "Vitor Takashi Hideshima (5th team member, no award) is absent from the official PDF; SBF's article confirms his membership — dataset's null medal is consistent.",
}

GLOBAL_NOTES = [
 "All official eupho.ee results PDFs verified live 2026-08-22.",
 "SBF hosting split: pre-2023 articles live on sbfisica.org.br/v1/olimpiada/<year> (HTTrack mirrors, still live); 2023+ on www1.fisica.org.br/olimpiada/<year>.",
 "Name-spelling watch vs dataset: 2017 PDF 'Diogo Netto' / NOIC 'Neto' vs dataset 'Diogo Correia Netto' (kept); 2021 PDF extraction glitch 'MakotoTanabe'.",
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
        "olympiadId": "eupho",
        "description": "Independent web sources confirming Brazilian EuPhO participants + results, per edition.",
        "provenanceClasses": {
            "official": "eupho.ee official results PDFs (one per edition).",
            "primary": "SBF/OBF articles, NOIC, schools (Etapa), press (G1, A Gazeta, O Liberal).",
            "archive": "compilations (NOIC hall page).",
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

    md = f"""# Per-Year Corroboration — Independent Sources for Brazil at the EuPhO

**Machine-readable version:** `data/corroboration.json`. Rebuild with
`python3 scripts/build_corroboration.py`; re-verify URLs with
`python3 scripts/verify_corroboration.py`. Built from the 2026-08-22 research pass.

## Headline

- **{n3} of {len(records)} editions** have ≥3 participant-naming source domains.
- **{p3} of {len(records)} editions** have ≥3 genuinely-independent primaries.
- Every edition anchored by its official eupho.ee results PDF (all verified live).

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
    print("Shortfall (<3 naming):", [r["year"] for r in records if not r["meetsThreeNaming"]])
    print("Wrote data/corroboration.json + CORROBORATION.md")


if __name__ == "__main__":
    main()
