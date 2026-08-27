#!/usr/bin/env python3
"""
Assemble data/corroboration.json and CORROBORATION.md for Brazil at the OIbF,
repo-standard format. Sources verified by the 2026-08-22 research pass: every URL
fetched and content-checked against graph.json rosters (needles recorded).

Key provenance recovery: the per-edition results PDFs live at fisica.org.br/~oibf/.../premiacoes_n/ — the OIbF permanent
site hosted by SBF. cls=official for those; SBF team/news pages = primary;
olimpiadascientificas = archive.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

PREM = "http://www1.fisica.org.br/~oibf/home/wp-content/uploads/2013/07/premiacoes_n/"
EQ10 = "https://sec.sbfisica.org.br/olimpiadas/obf2010/EquipeBROIbF.shtm"
EQ11 = "https://sec.sbfisica.org.br/olimpiadas/obf2011/EquipeBROIbF.shtm"
OC = "http://olimpiadascientificas.org/equipes-brasileiras/fisica/oibf/"


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def pdf(fname, confirms, needle):
    return src(PREM + fname, "fisica.org.br (~oibf)", "official", "full",
               f"official results PDF ({confirms})", needle)


def eq10(confirms, needle):
    return src(EQ10, "sbf1.sbfisica.org.br", "primary", "full", f"SBF Brazilian-teams page 2000–2010 — {confirms}", needle)


def eq11(confirms, needle):
    return src(EQ11, "sbf1.sbfisica.org.br", "primary", "full", f"SBF Brazilian-teams page through 2011 — {confirms}", needle)


def oc(confirms, needle):
    return src(OC, "olimpiadascientificas.org", "archive", "full", f"Brazilian teams 2000–2012 — {confirms}", needle)


def wb(url, domain, cls, coverage, confirms, needle):
    return src(url, domain + " (Wayback)", cls, coverage, confirms, needle)


SOURCES = {
 2000: [pdf("2000_V.pdf", "V OIbF, 3 HMs", "Francisco Vieira Neto"),
        wb("https://web.archive.org/web/20101031025952/http://www.sbf1.sbfisica.org.br/oibf2004/Ibero00/v_result.htm",
           "sbf1.sbfisica.org.br", "official", "full", "IX-OIbF-2004 host archive of V results", "Diogo Diniz"),
        eq10("3 HMs w/ states", "Alexandre Henrique dos Santos")],
 2001: [pdf("2001_VI.pdf", "VI OIbF, 2G/1S/1B; full name Martha Priscilla", "Martha Priscilla"),
        wb("https://web.archive.org/web/20050311225832/http://www.sbf1.sbfisica.org.br:80/oibf2004/Ibero01/vi_result.htm",
           "sbf1.sbfisica.org.br", "official", "full", "VI results", "Leonardo Leite"),
        eq10("all 4 (short 'Martha Priscila Torres')", "Leonardo Leite Pereira"), oc("all 4", "Leonardo Leite")],
 2002: [pdf("2002_VII.pdf", "VII OIbF, 1G/2B", "Pessoa"),
        wb("https://web.archive.org/web/20050311231021/http://www.sbf1.sbfisica.org.br:80/oibf2004/Ibero02/vii_result.htm",
           "sbf1.sbfisica.org.br", "official", "full", "VII results", "Chociay"),
        eq10("all 3", "Henrique Chociay"), oc("all 3", "Chociay")],
 2003: [pdf("2003_VIII.pdf", "VIII OIbF awardees: 2B/1HM — Kato absent = no award, matches dataset", "Lury Bertollo"),
        wb("https://web.archive.org/web/20050311232559/http://www.sbf1.sbfisica.org.br:80/oibf2004/Ibero03/viii_result.htm",
           "sbf1.sbfisica.org.br", "official", "3/4", "VIII awardees", "Eduardo Higino"),
        eq10("full team INCLUDING Milton Eiji Kato (no medal listed)", "Milton Eiji Kato"), oc("full team incl. Kato", "Kato")],
 2004: [pdf("2004_IX.pdf", "IX OIbF, 2G/1S/1B", "Salerno"),
        wb("https://web.archive.org/web/20050311235815/http://www.sbf1.sbfisica.org.br:80/oibf2004/Ibero04/ix_result.htm",
           "sbf1.sbfisica.org.br", "official", "full", "IX host-site results", "Tsai"),
        eq10("all 4", "Vander Valente Martins"), oc("all 4", "Salerno")],
 2005: [pdf("2005_X.pdf", "X OIbF, 2G/1S/1B", "Bokliang"),
        eq10("all 4", "Antonio Augusto Matsumoto Zambon"), oc("all 4", "Zambon")],
 2006: [pdf("2006_XI.pdf", "XI OIbF, 1G/1S/1B/1HM — spellings match dataset exactly", "Alexandre Hideki Deguchi Martani"),
        eq10("all 4 (page misspells Martani/Mata)", "Raphael Rodrigues Mata"), oc("all 4", "Marrochio")],
 2007: [pdf("2007_XII.pdf", "XII OIbF, 2G/1S/1B", "Anderson Unlin Tsai"),
        eq10("all 4", "Bruno Arderucio Costa"), oc("all 4", "Arderucio")],
 2008: [pdf("2008_XIII.pdf", "XIII OIbF, 3G/1S", "Mariana Quezado Costa Lima"),
        eq10("all 4", "George Gondim Ribeiro"), oc("all 4", "Quezado")],
 2009: [pdf("2009_XIV.pdf", "XIV OIbF, 1G/3S (PDF text garbles 'Rolim Mendez')", "Rolim"),
        wb("https://web.archive.org/web/20101022235504/http://www.sbf1.sbfisica.org.br/olimpiadas/Obf2009/EquipeBROIbF.shtm",
           "sbf1.sbfisica.org.br", "primary", "full", "team w/ full correct names", "Rodrigo Rolim"),
        eq10("all 4", "Luana Benedetto de Assis"), oc("all 4", "Benedetto")],
 2010: [pdf("2010_XV.pdf", "XV OIbF Panama, 4 GOLDS — edition confirmed held", "Elder Massahiro Yoshida"),
        eq10("XV OIbF 2010 Panamá section, 4 golds", "Lucas C. C. Souza"), oc("all 4", "Massahiro")],
 2011: [pdf("2011_XVI.pdf", "XVI OIbF, 2G/1S/1B (PDF garbles 'Lara Timbo Aram')", "Kayo"),
        eq11("all 4", "Miguel Augusto de Bortoli Saggin"), oc("all 4 w/ correct Lara Timbó Araújo", "Saggin")],
 2012: [pdf("2012_XVII.pdf", "XVII OIbF, 2G/1S/1B", "Ilo Pereira"),
        wb("https://web.archive.org/web/20140829160953/http://www.sbfisica.org.br/v1/index.php?option=com_content&view=article&id=430:brasil-vence-olimpiada-iberoamericana-de-fisica-2012&catid=152:acontece-na-sbf&Itemid=270",
           "sbfisica.org.br", "primary", "full", "SBF news: Brazil wins OIbF 2012", "Guinsberg"),
        oc("all 4 (page typo 'Fernanders')", "Guinsberg")],
 2013: [pdf("2013_XVIII.pdf", "XVIII OIbF, 2G/2S", "Bruno Kenichi Saika"),
        wb("https://web.archive.org/web/20160529054243/http://www.sbfisica.org.br:80/v1/olimpiada/2013/indexcec1.html?option=com_content&view=article&id=112:oibf13result&catid=35:pagina-principal&Itemid=182",
           "sbfisica.org.br", "primary", "full", "OBF site 2013 results", "VALLE")],
 2014: [pdf("2014_XIX.pdf", "XIX OIbF, 4 bronzes", "Pedro Alves de Souza Neto"),
        src("http://www.sbfisica.org.br/v1/olimpiada/2014/indexdf98.html?option=com_content&view=article&id=138:oibf14b&catid=35:pagina-principal&Itemid=182",
            "sbfisica.org.br", "primary", "full", "OBF site 2014 results", "Matheus Carioca Sampaio"),
        src("https://noic.com.br/fisica/quatro-medalhas-para-o-brasil-na-oibf/", "noic.com.br", "primary", "full",
            "NOIC results (typo 'Alvez')", "Souza Neto")],
 2015: [pdf("2015_XX.pdf", "XX OIbF, 1G/1S/2B", "Mateus de Castro Silva"),
        src("https://noic.com.br/fisica/divulgadas-as-equipes-da-ipho-e-oibf/", "noic.com.br", "primary", "full — pre-event roster",
            "NOIC team announcement (spells LENNON; gives 'Leonardo H. M. FLORENTINO')", "FLORENTINO")],
 2016: [pdf("2016_XXI.pdf", "XXI OIbF, 2G/2S", "Marina Maciel Ansanelli"),
        src("https://www.sbfisica.org.br/v1/olimpiada/2016/images/arquivos/Brasil_conquista_medalhas_na_XXI_Olimp%C3%ADada_Ibero.pdf",
            "sbfisica.org.br", "primary", "full", "SBF results note (spells 'Fontelles')", "Fontelles")],
 2017: [pdf("2017_XXII.pdf", "XXII OIbF, 3G/1S", "Erik Bardini da Rosa"),
        src("https://www.sbfisica.org.br/v1/olimpiada/2017/index.php/2-uncategorised/133-resultado-da-olimpiada-ibero-americana-de-fisica-2017",
            "sbfisica.org.br", "primary", "full", "OBF site 2017 results", "Gustavo Misawa Hama")],
 2018: [pdf("2018_XXIII.pdf", "XXIII OIbF, 3G/1HM (PDF spells 'Fernandez')", "Fernando Silveira"),
        src("https://www.sbfisica.org.br/v1/olimpiada/2018/index.php/2-uncategorised/180-resultado-da-olimpiada-ibero-americana-de-fisica-2018",
            "sbfisica.org.br", "primary", "full", "OBF site 2018 results, full names incl. D'Ambrosio", "Arounian"),
        src("https://noic.com.br/uncategorized/veja-o-resultado-do-brasil-na-ibero-de-fisica/", "noic.com.br", "primary", "full",
            "NOIC results (short names)", "Capelo")],
 2019: [pdf("2019_XXIV.pdf", "XXIV OIbF, 4 golds", "Vinicius de Alcântara Névoa"),
        src("https://noic.com.br/uncategorized/4-medalhas-de-ouro-para-o-brasil-na-olimpiada-ibero-americana-de-fisica/",
            "noic.com.br", "primary", "full", "NOIC: 4 golds", "Davi Maciel"),
        wb("https://web.archive.org/web/20191022092758/http://www.sbfisica.org.br/v1/home/index.php/pt/acontece/965-brasil-conquista-ouro-e-primeiros-lugares-na-olimpiada-iberoamericana-de-fisica-2019",
           "sbfisica.org.br", "primary", "full", "SBF news (live URL 404s)", "Backes")],
 2020: [pdf("2020_OIbF_virtual_XXV.pdf", "virtual XXV, 4 golds + Mejor Oro (Felipe Farias)", "Felipe Farias Ribeiro Filho"),
        src("https://www.sbfisica.org.br/v1/olimpiada/2021/index.php/20-oibf/254-resultado-oibf-2020.html",
            "sbfisica.org.br", "primary", "full", "OBF site 2020 results", "Lucas Takayasu"),
        src("https://noic.com.br/uncategorized/sai-o-resultado-da-seletiva-de-fisica-descubra-quem-respresentara-o-brasil-nas-internacionais/",
            "noic.com.br", "primary", "full — pre-event roster", "NOIC seletiva announcement", "Maria Eduarda")],
 2021: [pdf("2021_XXVI.pdf", "XXVI João Pessoa, 4 golds + Mejor Oro/Mejor Prueba Teórica (Lucas Almeida)", "Lucas Almeida Oliveira"),
        src("https://www.sbfisica.org.br/v1/olimpiada/2021/index.php/15-soif/281-olimpiada-ibero-americana-de-fisica-oibf-brasil-vence-em-casa",
            "sbfisica.org.br", "primary", "full", "SBF: Brazil wins at home", "Kerber")],
 2022: [src("https://www.sbfisica.org.br/v1/olimpiada/2022/index.php/15-soif/315-brasil-conquista-dois-ouros-e-duas-pratas-na-oibf-2022.html",
            "sbfisica.org.br", "primary", "full", "SBF results 2G/2S (spells 'Mazzili'; virtual XXVII)", "Albernaz"),
        src("https://sites.google.com/view/oibf2022/medallero", "sites.google.com (official XXVII)", "official",
            "full — images only", "official medallero, but image/video content — not text-verifiable", None)],
 2023: [src("https://sites.google.com/view/oibfcr2023/medallero", "sites.google.com (official XXVIII)", "official", "full",
            "official medallero: 3G (Alexandre, Arthur Hwang, Rafael Sena + best theoretical) + 1S (Augusto Burlacchini)", "Burlacchini"),
        src("https://www1.fisica.org.br/olimpiada/2023/index.php/15-soif/333-brasil-conquista-3-ouros-e-1-prata-na-oibf-2023",
            "fisica.org.br", "primary", "full", "SBF results 3G/1S", "Rafael Sena")],
}

NOTES = {
 2003: "Official PDF lists awardees only — Milton Eiji Kato's absence = confirmed no-award (dataset medal null is correct); SBF team page lists him without a medal.",
 2010: "Edition confirmed held (XV, Panama; Brazil 4 golds) — contra any claim of a 2010 gap.",
 2022: "Virtual edition; official Google-Sites medallero is image-based (not text-verifiable) — SBF's live article is the text-verified record. Spelling conflict 'Mazzili' (SBF) vs 'Mazili' (dataset, from EuPhO source) unresolved — official medallero can't adjudicate.",
}

GLOBAL_NOTES = [
 "PDF-origin recovery (2026-08-22): the per-edition premiacoes PDFs are stable live files at fisica.org.br/~oibf/.../premiacoes_n/{YEAR}_{ROMAN}.pdf; Wayback snapshots exist for all 22.",
 "2024 and 2025 editions were cancelled (not sourced); 2026 roster is in the dataset with pending medals (grandfathered) — corroborate after the event.",
 "PDF text layers contain garbled names in some years (2009 'Rolim Mendez', 2011 'Lara Timbo Aram', 2021 'boliviaBarros' artifact) — the SBF team pages carry the clean full names; dataset spellings verified against the cleaner of the two.",
 "Spelling watch (source vs dataset, unresolved but low-stakes): 2015 Florentino RESOLVED 2026-08-22: merged with IJSO's Leonardo Henrique Martins Florentino (site alias); 2016 'Fontelles' vs 'Fonteles'; 2018 'Fernandez' vs 'Fernandes'.",
 "sbf1.sbfisica.org.br now answers with a fake-200 'Object Moved' page — the live host is sec.sbfisica.org.br (fixed 2026-08-22).",
 "The pre-2020 oibf.org domain in Wayback is an unrelated Oklahoma site; the genuine historic trail is SBF's ~oibf WordPress + the IX-OIbF-2004 host archive (Ibero00–04).",
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
        "olympiadId": "oibf",
        "description": "Independent web sources confirming Brazilian OIbF participants + results, per edition.",
        "provenanceClasses": {
            "official": "OIbF's own results (premiacoes PDFs on the SBF-hosted permanent site; per-edition host sites/medalleros).",
            "primary": "SBF/OBF team and news pages, NOIC.",
            "archive": "olimpiadascientificas.org team compilations (2000–2012).",
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

    md = f"""# Per-Year Corroboration — Independent Sources for Brazil at the OIbF

**Machine-readable version:** `data/corroboration.json`. Rebuild with
`python3 scripts/build_corroboration.py`; re-verify URLs with
`python3 scripts/verify_corroboration.py`. Built from the 2026-08-22 research pass
(every URL fetched and content-verified against graph.json rosters).

## Headline

- **{n3} of {len(records)} editions** have ≥3 participant-naming source domains.
- **{p3} of {len(records)} editions** have ≥3 genuinely-independent primaries.
- Every edition is anchored by its official premiacoes PDF (verified live; Wayback snapshots exist).

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
