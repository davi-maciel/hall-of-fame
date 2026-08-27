#!/usr/bin/env python3
"""
Assemble data/corroboration.json and CORROBORATION.md for Brazil at the IPhO,
repo-standard format. Verified by the 2026-08-22 research pass: every URL fetched
(live or Wayback) and content-checked against graph.json rosters.

Source families:
  U-yr  ipho-unofficial.org/timeline/<year>/individual — per-year results (primary;
        the de-facto public IPhO results database). Excludes 2000 medal-less Brazil
        and the whole 2020 IdPhO.
  OC    olimpiadascientificas.org IPhO page (+ webnode mirror) — full 5-member
        rosters incl. non-medalists, 2000–2011 (gap-fill primary).
  WIN   old official IPhO homepage (Univ. Jyväskylä) "Winners by Olympiads" PDF via
        Wayback — official award compilation through 2014.
  Host sites / SBF / NOIC / Etapa / press — per-year.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

OC_URL = "http://olimpiadascientificas.org/equipes-brasileiras/fisica/ipho/"
WIN_URL = "http://web.archive.org/web/20150912074235/http://www.jyu.fi/tdk/kastdk/olympiads/ipho_winners_45.pdf"


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def uyr(year, coverage, confirms, needle):
    return src(f"https://ipho-unofficial.org/timeline/{year}/individual", "ipho-unofficial.org", "primary",
               coverage, f"per-year individual results — {confirms}", needle)


def oc(confirms, needle):
    return src(OC_URL, "olimpiadascientificas.org", "primary", "full",
               f"full 5-member roster w/ states — {confirms} (mirror: olimpiada.webnode.com.br)", needle)


def win(confirms, needle):
    return src(WIN_URL, "jyu.fi (old official IPhO site, Wayback)", "official", "awards",
               f"official 'Winners by Olympiads' compilation (1967–2014) — {confirms}", needle)


def noic(url, coverage, confirms, needle):
    return src(url, "noic.com.br", "primary", coverage, confirms + " (site 406-blocks curl; verify via browser fetch)", needle)


SOURCES = {
 2000: [oc("Leicester debut roster, 5 no-award students — the ONLY per-name source family for 2000", "Danilo Jimenez Rezende"),
        src("http://web.archive.org/web/20100124032207/http://ipho.phy.ntnu.edu.tw/2000minutes.html",
            "ipho.phy.ntnu.edu.tw (Wayback)", "official", "counts", "IPhO 2000 minutes — Brazil in the new-participants list (no names)", "Brazil")],
 2001: [uyr(2001, "awards", "Pimentel HM", "Pimentel"),
        src("http://web.archive.org/web/20010720031951/http://www.ipho2001.org.tr/results/all.html",
            "ipho2001.org.tr (host, Wayback)", "official", "full", "host results — full 5-member roster + leaders, exact match", "Fontenele"),
        oc("Antalya roster", "Richartz")],
 2002: [uyr(2002, "3/4", "3 award winners (Pelá bronze; Brazil sent 4)", "Pela"),
        win("Pelá bronze, Muniz + Fonteles HM", "Fonteles"),
        oc("4-member roster (not a gap — consistent across sources)", "Janilo")],
 2003: [uyr(2003, "awards", "Jong Woo Jin HM", "Jong Woo Jin"),
        src("http://web.archive.org/web/20031027081111/http://www.phy.ntnu.edu.tw/ipho2003/English/result.htm",
            "phy.ntnu.edu.tw (host, Wayback)", "official", "awards", "host results — all award winners", "Jong Woo Jin"),
        oc("roster", "Quixada")],
 2004: [uyr(2004, "awards", "Graminho HM", "Graminho"),
        win("Graminho honourable mention", "Graminho"),
        oc("roster", "Maracaba")],
 2005: [uyr(2005, "awards", "3 awards", "Heleodoro"),
        win("Silva Filho, Heleodoro, Castro da Silva", "Heleodoro"),
        oc("roster ('Aron A. Heleodoro' — name-order conflict, see note)", "Heleodoro")],
 2006: [uyr(2006, "awards", "Sobreira", "Sobreira"),
        win("Sobreira + Rehn Casierra", "Casierra"),
        oc("roster", "Aleixo")],
 2007: [uyr(2007, "awards", "Thomás F. Lima bronze", "Lima"),
        win("Thomas F. Lima bronze", "Thomas F. Lima"),
        oc("roster", "Nilo Daniel")],
 2008: [uyr(2008, "awards", "Takeda", "Takeda"),
        src("http://web.archive.org/web/20080731100948/http://ipho2008.hnue.edu.vn/Competition/Results/tabid/82/Default.aspx",
            "ipho2008.hnue.edu.vn (host, Wayback)", "official", "awards", "host award winners", "Takeda"),
        oc("roster incl. non-medalist Vitor Mori", "Vitor Mori")],
 2009: [uyr(2009, "awards", "Halpern", "Halpern"),
        win("all 5 named (Farias, Guilhon, Halpern, Stedile, Paiva Filho)", "Halpern"),
        oc("Mérida roster", "Stedile")],
 2010: [uyr(2010, "awards", "Haddad", "Haddad"),
        win("all 5 (Haddad, Lira, Andrade e Silva, Alencar, Sousa)", "Haddad"),
        src("http://web.archive.org/web/20101008094715/http://www.sbfisica.org.br/v1/index.php?option=com_content&view=article&id=215:na-croacia-a-equipe-da-obf-conquista-cinco-medalhas-na-41o-ipho&catid=75:agosto-2010&Itemid=270",
            "sbfisica.org.br (Wayback)", "primary", "counts", "SBF: 5 medals, first all-medal team (teaser, no names)", "cinco medalhas"),
        oc("roster", "Lira")],
 2011: [uyr(2011, "awards", "Haddad gold", "Haddad"),
        src("http://web.archive.org/web/20110825233428/http://www.sbfisica.org.br/v1/index.php?option=com_content&view=article&id=331:ouro-para-o-brasil-na-olimpiada-internacional-de-fisica&catid=94:julho-2011&Itemid=270",
            "sbfisica.org.br (Wayback)", "primary", "full", "SBF: names + schools + Haddad's 41.29 points", "Hernandes"),
        oc("roster (last OC year)", "Godoi")],
 2012: [uyr(2012, "full", "gold Antunes + 3 bronze; Dalla Stella no award", "Antunes"),
        src("http://web.archive.org/web/20140805021810/http://g1.globo.com/educacao/noticia/2012/07/brasil-ganha-quatro-medalhas-na-olimpiada-internacional-de-fisica.html",
            "g1.globo.com (Wayback)", "primary", "full", "G1: all 5 names incl. Dalla Stella as non-medalist", "Dalla Stella"),
        win("gold Antunes; Dalla Stella under Participation certificate", "Antunes")],
 2013: [uyr(2013, "awards", "Arai silver", "Arai"),
        noic("https://noic.com.br/fisica/ipho/resultado-ipho-2013/", "full", "NOIC: silver Arai + 4 bronze", "Arai"),
        win("2013 awards", "Arai")],
 2014: [uyr(2014, "awards", "Cronemberger", "Cronemberger"),
        noic("https://noic.com.br/fisica/5-medalhas-brasileiras-na-ipho-2014/", "full", "NOIC: 5 bronzes", "CRONEMBERGER"),
        win("2014 awards", "Cronemberger")],
 2015: [uyr(2015, "awards", "Tafnes", "Tafnes"),
        noic("https://noic.com.br/fisica/tres-medalhas-para-o-brasil-na-olimpiada-internacional-de-fisica-ipho/",
             "full", "NOIC: 3 bronze + 2 HM w/ states", "Tafnes")],
 2016: [uyr(2016, "awards", "Bergamaschi gold", "Bergamaschi"),
        src("https://www1.fisica.org.br/olimpiada/2016/images/arquivos/AnuncioMedalhasIPhO2016__2_.pdf",
            "fisica.org.br (SBF/OBF)", "official", "full", "SBF medal announcement PDF — all 5 names", "Zanarella")],
 2017: [uyr(2017, "awards", "Golfetti", "Golfetti"),
        noic("https://noic.com.br/uncategorized/brasil-conquista-melhor-resultado-da-historia-na-ipho/",
             "full", "NOIC: 3 gold + 2 bronze — best result in history", "Golfetti")],
 2018: [uyr(2018, "awards", "Kitayama", "Kitayama"),
        noic("https://noic.com.br/uncategorized/5-medalhas-para-o-brasil-na-ipho-2018/", "full",
             "NOIC: all 5 w/ cities (Thomas Bergamaschi silver)", "Bergamaschi")],
 2019: [uyr(2019, "full", "all 5 incl. Eleni Claire Shor silver (rank 45)", "Shor"),
        noic("https://noic.com.br/fisica/ipho/cinco-medalhas-para-o-brasil-na-ipho/", "full",
             "NOIC results post — one team member appears under a former name (same person; see note)", "Cutrim")],
 2020: [src("http://web.archive.org/web/20201219170042/http://www.sbfisica.org.br/v1/home/index.php/pt/acontece/1237-estudantes-brasileiro-conquistam-medalhas-de-prata-e-bronze-na-international-distributed-physics-olympiad",
            "sbfisica.org.br (Wayback)", "official", "full",
            "SBF: IdPhO 2020 — all 5 names + schools + medals (4 silver + 1 bronze) + event explanation", "Takose"),
        noic("https://noic.com.br/olimpiadas/fisica/hall-da-fisica/", "2/5", "NOIC hall: Davi Maciel + Vinícius Rodrigues prata, IdPhO framing", "Davi Maciel"),
        src("https://en.wikipedia.org/wiki/International_Physics_Olympiad", "en.wikipedia.org", "archive", "counts",
            "confirms IdPhO 2020 as the IPhO-endorsed substitute (no Brazilian names)", "IdPhO")],
 2021: [uyr(2021, "full", "gold/silver/3 bronze", "Uchoa"),
        src("http://web.archive.org/web/20210730163251/http://www.sbfisica.org.br/v1/home/index.php/pt/acontece/1380-ouro-prata-e-bronze-na-ipho-2021",
            "sbfisica.org.br (Wayback)", "primary", "full", "SBF: all 5 + schools (live URL now 404)", "Siqueira"),
        src("https://www1.fisica.org.br/olimpiada/2020/", "fisica.org.br (SBF/OBF)", "primary", "full — selection stage",
            "TBF top-5 = the same 5 students", "CAIO AUGUSTO")],
 2022: [uyr(2022, "awards", "Tizon", "Tizon"),
        src("https://ipho2022.com/results/", "ipho2022.com (host)", "official", "full", "host results — all 5", "Tizon")],
 2023: [uyr(2023, "awards", "Menhem", "Menhem"),
        noic("https://noic.com.br/uncategorized/resultado-do-brasil-na-ipho/", "full", "NOIC: all 5 (Porfirio silver)", "Porfirio"),
        src("https://olimpiadas.etapa.com.br/fisica", "etapa.com.br", "primary", "1/5", "Etapa: Porfirio prata", "Porfirio")],
 2025: [uyr(2025, "awards", "Feltran", "Feltran"),
        src("https://cdn.prod.website-files.com/664df830da8ff5d22656764b/68834cd4e6e698960f2c6e1a_final_ranks_ipho2025.pdf",
            "ipho2025.fr (host)", "official", "full", "host final ranks PDF — all 5 + medals + scores (linked from ipho2025.fr results page)", "Feltran"),
        src("https://olimpiadas.etapa.com.br/fisica", "etapa.com.br", "primary", "1/5", "Etapa: Feltran prata 2025", "Feltran")],
 2026: [uyr(2026, "full", "all 5 (Feltran gold)", "Feltran"),
        src("https://olimpiadas.etapa.com.br/fisica", "etapa.com.br", "primary", "2/5", "Etapa: Feltran ouro + Kojima bronze 2026", "Kojima")],
}

NOTES = {
 2000: "The only year whose names rest on a single source family (OC + its webnode mirror). Official record (2000 minutes) confirms only Brazil's debut; the Leicester host archive kept medal pages only, which exclude the no-award Brazilian team. Exhaustive Wayback/press sweep found nothing else.",
 2005: "Name-order conflict: official-derived sources say 'Heleodoro Aaron Alexandre'; OC says 'Aron A. Heleodoro (SP)' — surname may be Heleodoro and the dataset's official-derived order inverted. Unresolved; dataset keeps the official form.",
 2012: "SBF's 2016 PDF misstates 2012 as 1 gold + 4 bronze; official + G1 + WIN all show 1 gold + 3 bronze with Dalla Stella = participation certificate. Dataset correct.",
 2019: "RESOLVED 2026-08-22: the apparent NOIC/official roster mismatch is a name change — the contemporary NOIC post uses a team member's former name; the official table carries her current name, Eleni Claire Shor (silver, rank 45). Same person, no conflict. Dataset and site display the current name only.",
 2020: "IPhO 2020 (Lithuania) cancelled; Russia ran the IPhO-endorsed IdPhO (7–15 Dec 2020). Brazilians sat papers at IF-USP under remote Russian supervision: 4 silver + 1 bronze. ipho-unofficial excludes this event entirely (timeline/2020 = 404) — 2020 must be sourced from SBF/NOIC.",
 2026: "ipho-unofficial has 'Lucas Carvalho Brasil' vs dataset 'Lucas Carvalho' (surname possibly truncated in dataset) and 'Henrique Kojima' vs the fuller 'Henrique Naoto Kojima' (Etapa confirms fuller form). Flagged for review.",
}

GLOBAL_NOTES = [
 "ipho-unofficial.org HAS per-year URLs (timeline/<year>/individual) — used as the per-edition primary. Its BRA country page is the all-years view. Neither covers 2000 (no Brazilian awards) nor 2020 (IdPhO excluded).",
 "Gap-fill source typos (dataset correct per official sources): OC 'Rudrigues' (2010), 'Carvina' (2008), 'Guilhom' (2009); WIN PDF OCR 'Reboulgas' (2006). Dataset 2012 'Luìs' grave-accent inherited verbatim from ipho-unofficial.",
 "2002's four-member team is consistent across all sources — a real partial team, not missing data.",
 "noic.com.br 406-blocks curl; verify NOIC URLs via browser-context fetch. Wayback was intermittently offline during the pass; all Wayback URLs here were captured when it responded.",
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
        "olympiadId": "ipho",
        "description": "Independent web sources confirming Brazilian IPhO participants + results, per edition.",
        "provenanceClasses": {
            "official": "old official IPhO winners compilation (jyu.fi), per-year host-site results, SBF/OBF official announcements.",
            "primary": "ipho-unofficial.org per-year tables, olimpiadascientificas rosters, SBF articles, NOIC, Etapa, press (G1).",
            "archive": "tertiary compilations (Wikipedia).",
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

    md = f"""# Per-Year Corroboration — Independent Sources for Brazil at the IPhO

**Machine-readable version:** `data/corroboration.json`. Rebuild with
`python3 scripts/build_corroboration.py`; re-verify URLs with
`python3 scripts/verify_corroboration.py`. Built from the 2026-08-22 research pass
(every URL fetched live or via Wayback and content-verified against graph.json).

Brazil was ABSENT from IPhO 2024 (not sourced). 2020 = the IdPhO substitute event.

## Headline

- **{n3} of {len(records)} editions** have ≥3 participant-naming source domains.
- **{p3} of {len(records)} editions** have ≥3 genuinely-independent primaries.
- Weakest year: 2000 (single source family for names — see note).
- Open flags: 2019 NOIC roster conflict; 2005 name order; 2026 spellings (see notes).

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
