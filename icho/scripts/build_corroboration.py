#!/usr/bin/env python3
"""
Assemble data/corroboration.json and CORROBORATION.md for Brazil at the IChO.
Assembled from the research pass ("three corroborating URLs per year", all fetched and
read at research time) into the repo-standard structured format (same schema as imo/).
Re-verify liveness+content with scripts/verify_corroboration.py.

Provenance classes:
  - "official": the IChO results database (icho-official.org), compiled for the IChO
                Steering Committee — the dataset's primary source (S1).
  - "primary" : fully independent record families — the Brazilian national body's own
                records (ABQ RQI table S4, OBQ/UFC PDFs S5, OBQ PDFs S6), host-country
                result pages (S9), Brazilian press/institutions (S7).
  - "archive" : third-party aggregators that likely derive from official data
                (scoreboard.bc-pf.org, S8).

Optional per-source "needle": string verify_corroboration.py must find in the page.
Sources with coverage=="full" are auto-checked against the year's roster surnames.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ABQ_PDF = "https://www.abq.org.br/rqi/2014/777/RQI-777-pagina16-56-Edicao-Olimpiada-Intenacional-de-Quimica.pdf"


def s1(edition_id, year):
    return {"url": f"http://www.icho-official.org/results/results.php?id={edition_id}&year={year}",
            "domain": "icho-official.org", "cls": "official", "coverage": "full",
            "confirms": "official per-edition result table — full 4-person team, ranks + awards"}


def s4(confirms="nominal year-by-year table 1999–2024: name + rank + medal for every Brazilian competitor"):
    return {"url": ABQ_PDF, "domain": "abq.org.br (RQI)", "cls": "primary", "coverage": "full", "confirms": confirms}


def s5(url, coverage, confirms, needle=None):
    d = {"url": url, "domain": "obq.ufc.br", "cls": "primary", "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def s6(url, confirms="OBQ result PDF — all 4 with medals"):
    return {"url": url, "domain": "obquimica.org", "cls": "primary", "coverage": "full", "confirms": confirms}


def s8(year, confirms="independent aggregator — all 4 Brazilians with score + medal"):
    return {"url": f"https://scoreboard.bc-pf.org/en/results/chemistry/international-chemistry-olympiad/{year}",
            "domain": "scoreboard.bc-pf.org", "cls": "archive", "coverage": "full", "confirms": confirms}


def abqsp(coverage, confirms, needle=None):
    d = {"url": "https://abqsp.org.br/oqsp/historico/", "domain": "abqsp.org.br", "cls": "primary",
         "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


SOURCES = {
 1999: [s1(31, 1999), s4("all 4, 'Participante' — independently reproduces the hardest year"),
        src("http://web.archive.org/web/20001208072100/http://scicsws01.sci.ku.ac.th:80/~icho31/mainpage/winner3.html",
            "web.archive.org (Thai host)", "primary", "full",
            "original 31st-IChO host winners page (archived) — all 4 with full names, scores, ranks (150/161/180/170), 'Participant'")],
 2000: [s1(32, 2000), s4("all 4; Sergio X. B. Araujo = Menção honrosa"),
        s5("http://www.obq.ufc.br/Resultado32IChO.pdf", "1/4", "confirms Sergio Xavier Barbosa Araujo's honorable mention", needle="Sergio")],
 2001: [s1(33, 2001), s4(),
        s5("http://www.obq.ufc.br/Resultado33IChO.pdf", "full",
           "all 4 verbatim (Carlos Henrique, Luiz Bruno Pereira Lima, Marcus Paulo F. Amarante, Michelle M. T. Figueiredo)")],
 2002: [s1(34, 2002), s4("all 4; 2 bronze, 2 HM"),
        s5("http://www.obq.ufc.br/Resultado%20IChO34.pdf", "2/4", "confirms the medalists (Fonteles, Yuri)", needle="Fonteles")],
 2003: [s1(35, 2003), s4(),
        src("http://www.35icho.uoa.gr/ichol_eng/chemistry_eng/results/results.pdf", "35icho.uoa.gr (Greek host)",
            "primary", "partial", "original host results PDF — lists Brazil incl. Studart", needle="Studart"),
        s5("http://www.obq.ufc.br/35th%20IChOResultado.pdf", "full", "full roster")],
 2004: [s1(36, 2004), s4("all 4; R. V. Ferreira Alves = HM"),
        s5("http://www.obq.ufc.br/36th%20IChOResultado.pdf", "full", "full roster")],
 2005: [s1(37, 2005), s4("all 4; Juliana V. Mota = bronze"),
        s5("http://www.obq.ufc.br/Resultado37thIChO.pdf", "full", "full 4-person roster")],
 2006: [s1(38, 2006), s4("all 4; 3 bronze"),
        s5("http://www.obq.ufc.br/38th%20IChOResultado.pdf", "full", "full roster (Cesaris, Meneses, Apolônio, Thais)")],
 2007: [s1(39, 2007), s4("all 4; Thais = silver"),
        s5("http://www.obq.ufc.br/Resultados%20IChO39.pdf", "full", "full roster (Thais, Cesaris, Jorio, Ernando)")],
 2008: [s1(40, 2008), s4("all 4; Thais = silver, 3 bronze"), s8(2008),
        s5("http://www.obq.ufc.br/40thIChO_resultado.pdf", "full", "full roster")],
 2009: [s1(41, 2009), s4("all 4; Levindo = silver"), s8(2009),
        s5("http://www.obq.ufc.br/ResultadoIChO2009.pdf", "full", "full roster"),
        src("https://www.quimica.com.br/41st-international-chemistry-olimpiad-delegacao-brasileira-ganha-destaque-em-evento-na-inglaterra/",
            "quimica.com.br", "primary", "partial", "press — delegation coverage", needle="Levindo")],
 2010: [s1(42, 2010), s4("all 4; Levindo = silver, 3 bronze"), s8(2010),
        abqsp("2/4", "Okuma + Franco = bronze (SP medalists, prose history)", needle="Okuma")],
 2011: [s1(43, 2011), s4("all 4; Davi R. Chaves = silver"),
        abqsp("2/4", '"2011 IChO … Tábata C. A. de Pontes (bronze) … + 1 silver + 1 bronze"', needle="Pontes"),
        s8(2011)],
 2012: [s1(44, 2012), s4("all 4; Daniel Hara = silver, 3 bronze"),
        abqsp("2/4", '"2012 IChO … Daniel Arjona de Andrade Hara (prata) … outros três brasileiros … bronze"', needle="Arjona"),
        s8(2012)],
 2013: [s1(45, 2013), s4("all 4, all bronze"),
        s6("https://obquimica.org/storage/olympiads/result-files/ResultadoIChO2013%E2%80%93Russia.pdf"),
        s8(2013)],
 2014: [s1(46, 2014), s4("all 4; 3 bronze, 1 none"),
        abqsp("2/4", '"2014 IChO … Chan Song Moon e Kevin Eiji Iwashita (bronze)"', needle="Iwashita"),
        s8(2014)],
 2015: [s1(47, 2015), s4("all 4; Vitor Gomes Pires = silver"),
        s6("https://obquimica.org/storage/olympiads/result-files/Resultado%20IChO%202015.pdf"),
        s8(2015)],
 2016: [s1(48, 2016), s4("all 4; 2 silver, 2 bronze"),
        abqsp("full", '"Vitor Gomes Pires e Pedro Seber e Silva (prata); Amgarten e Davi O. Aragão (bronze)"'),
        s6("https://obquimica.org/storage/olympiads/result-files/Resultado%20IChO%202016.pdf"), s8(2016)],
 2017: [s1(49, 2017), s4("all 4; 3 silver, 1 bronze"), s8(2017),
        s6("https://obquimica.org/storage/olympiads/result-files/Resultado%20IChO%202017.pdf")],
 2018: [s1(50, 2018), s4("all 4; 2 gold"),
        src("https://agenciabrasil.ebc.com.br/educacao/noticia/2018-08/brasil-ganha-2-medalhas-de-ouro-na-olimpiada-internacional-de-quimica",
            "agenciabrasil.ebc.com.br", "primary", "2/4", "2 golds (Armelin + Ivna)", needle="Armelin"),
        s6("https://obquimica.org/storage/olympiads/result-files/Resultado%20IChO%202018.pdf"),
        src("https://agencia.fapesp.br/dois-estudantes-brasileiros-conquistam-ouro-na-olimpiada-internacional-de-quimica/28398",
            "agencia.fapesp.br", "primary", "2/4", "2 golds", needle="Armelin"),
        s8(2018)],
 2019: [s1(51, 2019), s4("all 4; 2 silver, 2 bronze"),
        src("https://www.ufpi.br/ultimas-noticias-ufpi/32315-alunos-brasileiros-conquistam-medalhas-na-51-edicao-da-olimpiada-internacional-de-quimica-icho",
            "ufpi.br", "primary", "3/4", "Ygor/Joaquim silver, Lucas bronze", needle="Ygor"),
        s6("https://obquimica.org/storage/olympiads/result-files/Resultado%20IChO%202019.pdf"), s8(2019)],
 2020: [s1(52, 2020), s4("all 4; Ygor = silver, 3 bronze"),
        s6("https://obquimica.org/storage/olympiads/result-files/Resultado%20IChO%202020.pdf"), s8(2020)],
 2021: [s1(53, 2021), s4("all 4; Vinicius Avelar = silver"),
        src("https://cfq.org.br/noticia/brasil-conquista-quatro-medalhas-na-olimpiada-internacional-de-quimica/",
            "cfq.org.br", "primary", "full", "all 4"),
        s6("https://obquimica.org/storage/olympiads/result-files/Resultado%20IChO%202021.pdf"), s8(2021)],
 2022: [s1(54, 2022), s4("all 4; 3 bronze, 1 HM"),
        s8(2022, "all 4 (Rafael/Moises/Diego bronze, João Pedro diploma)"),
        src("https://www.correiobraziliense.com.br/euestudante/educacao-basica/2022/08/5026143-aluno-do-ceara-e-o-1-brasileiro-a-vencer-olimpiadas-internacionais.html",
            "correiobraziliense.com.br", "primary", "1/4", "Rafael Moreno Ribeiro bronze", needle="Moreno")],
 2023: [s1(55, 2023), s4("all 4; 3 silver, 1 bronze — resolves the CFQ medal swap"), s8(2023),
        src("https://cfq.org.br/noticia/brasil-participa-da-55a-olimpiada-internacional-de-quimica-na-suica-e-obtem-melhor-resultado-das-ultimas-cinco-olimpiadas/",
            "cfq.org.br", "primary", "full — but SWAPS the Nailton/João Vitor medals (press error; resolved by the ABQ table + rank ordering)",
            "names all 4; medal attribution for 2 of them is wrong", needle="Nailton")],
 2024: [s1(56, 2024), s4("all 4; Lucas Loes = gold, rank 6"),
        src("https://www.qui.ufmg.br/equipe-brasileira-das-olimpiadas-de-quimica/", "qui.ufmg.br", "primary", "full",
            "Lucas ouro, Artur + Gabriel Paz prata, Fernando bronze"),
        s8(2024)],
 2025: [s1(57, 2025),
        s8(2025, "all 4 (Lucas silver; Daniel, Ian, Cristian bronze)"),
        src("https://www.colegioetapa.com.br/portal/resultados/olimpiadas-cientificas", "colegioetapa.com.br",
            "primary", "2/4", "Lucas Kenji = prata, Daniel Suda = bronze", needle="Kenji")],
 2026: [s1(58, 2026),
        src("https://www.icho2026.uz/results/rankings.pdf", "icho2026.uz (Tashkent host)", "primary", "full",
            "host rankings PDF — all 4 with scores + ranks (138/156/175/278), exact match")],
}

NOTES = {
 2023: "CFQ swapped the Nailton/João Vitor medals; the national-body table (S4) and rank ordering (S1) resolve it in favour of the dataset.",
 2025: "S4 predates 2025, so all three sources are independent of one another. ⚠️ Beware conflation: several 2025 'olimpíada de química' articles are about the Mendeleev IMChO (Belo Horizonte, May 2025) — a different competition with overlapping students.",
 2026: "⚠️ 2 OF 3 SOURCES — THIRD PENDING. Searched 2026-08-01 (13 days post-event): bc-pf 2026 page empty, obquimica results stop at 2021, no ABQ/CFQ/NOIC/press article on the Tashkent team yet (July-2026 Brazilian coverage is the Mendeleev IMChO-60 in Moscow — do not conflate). Re-check: bc-pf 2026, NOIC IChO page, obquimica PDFs, CFQ news, next ABQ RQI table (which will also supersede S4 through 2026).",
}

GLOBAL_NOTES = [
 "The ABQ RQI table (S4) was machine-compared record-by-record against the dataset: 104/104 records 1999–2024 match — zero medal, rank, or roster conflicts.",
 "The icho-official.org Brazil COUNTRY page silently drops the top Brazilian in several years (2019/2022/2023/2024) — per-edition tables are used instead; the country page is deliberately NOT cited here.",
 "scoreboard.bc-pf.org covers 2008+ only (pre-2008 returns 404); cphof-style aggregators derive from official data — classed 'archive'.",
 "Every URL was fetched live and its Brazilian rows read at research time; re-verify anytime with scripts/verify_corroboration.py.",
 "Liveness check 2026-08-01: 95/107 URLs PASS with content verified. Failures are link-rot/bot-walls, not data problems: the obq.ufc.br server (S5, 10 URLs, 2000-2009) is unreachable — use web.archive.org copies; quimica.com.br 403s scripted fetches; the ufpi.br 2019 article now 404s (Wayback has it).",
]

YEARS = sorted(SOURCES)


def build_records():
    records = []
    for y in YEARS:
        srcs = SOURCES[y]
        naming = [s for s in srcs if s["cls"] in ("official", "primary", "archive")]
        indep = [s for s in srcs if s["cls"] in ("official", "primary")]
        rec = {
            "year": y,
            "namingSourceCount": len(naming),
            "independentPrimaryCount": len(indep),
            "meetsThreeNaming": len(naming) >= 3,
            "meetsThreePrimary": len(indep) >= 3,
            "sources": srcs,
        }
        if y in NOTES:
            rec["note"] = NOTES[y]
        records.append(rec)
    return records


def main():
    records = build_records()
    payload = {
        "olympiadId": "icho",
        "description": "Independent web sources confirming Brazilian IChO participants + results, per edition.",
        "provenanceClasses": {
            "official": "icho-official.org — the IChO Steering Committee results database (primary source of the dataset).",
            "primary": "Fully independent record families: Brazilian national-body records (ABQ RQI, OBQ/UFC, OBQ), host-country result pages, Brazilian press/institutions.",
            "archive": "Third-party aggregators likely derived from official data (scoreboard.bc-pf.org).",
        },
        "globalNotes": GLOBAL_NOTES,
        "years": records,
    }
    with open(os.path.join(ROOT, "data", "corroboration.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")

    lines = []
    for r in records:
        doms = ", ".join(dict.fromkeys(s["domain"] for s in r["sources"] if s["cls"] != "counts"))
        flag = "" if r["namingSourceCount"] >= 3 else "  ⚠️ **<3**"
        note = " 📝" if "note" in r else ""
        lines.append(f"| {r['year']} | {r['namingSourceCount']} | {r['independentPrimaryCount']} | {doms}{flag}{note} |")
    table = "\n".join(lines)

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
    detail_md = "\n".join(details)

    global_md = "\n".join(f"- {n}" for n in GLOBAL_NOTES)

    md = f"""# Per-Year Corroboration — Independent Sources for Brazil at the IChO

**Machine-readable version:** `data/corroboration.json`. Rebuild with
`python3 scripts/build_corroboration.py`; re-verify URLs (liveness + content) with
`python3 scripts/verify_corroboration.py` (writes `data/corroboration_check.json`).

Built from the migration pass (every URL fetched and its Brazilian rows read at
research time) into the repo-standard structured format. Source families: official DB (S1), Brazilian national-body records (S4-S6), press (S7), aggregator (S8), host pages (S9).

## Headline

- **{n3} of {len(records)} editions** have ≥3 participant-naming source domains.
- **{p3} of {len(records)} editions** have ≥3 genuinely-independent primaries (official +
  national body + press/host; aggregators excluded).
- **2026 is the open item: 2 sources, third pending** (see the 2026 note below).

## Notes

{global_md}

## Summary table

| Year | Naming domains | Indep-primary | Domains |
|-----:|:--:|:--:|---------|
{table}

📝 = per-year note below.

## Per-year sources

{detail_md}"""

    with open(os.path.join(ROOT, "CORROBORATION.md"), "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Editions: {len(records)}")
    print(f">=3 naming: {n3}/{len(records)}; >=3 independent-primary: {p3}/{len(records)}")
    print("Shortfall (<3 naming):", [r["year"] for r in records if not r["meetsThreeNaming"]])
    print("Wrote data/corroboration.json + CORROBORATION.md")


if __name__ == "__main__":
    main()
