#!/usr/bin/env python3
"""
Assemble data/corroboration.json and CORROBORATION.md: for each IOAA edition Brazil
entered, the web sources that confirm the Brazilian participants and their results.
Migrated from the handwritten SOURCES.md (verified 2026-05-30) into the repo-standard
structured format (same schema as imo/). Re-verify liveness+content with
scripts/verify_corroboration.py.

Provenance classes:
  - "primary" : genuinely independent reporting that NAMES Brazilian competitors with
                results (gov.br agencies, OBA's own blog, ABC, FAPESP, Agência Brasil,
                press, schools).
  - "archive" : result compilations that name the roster but likely derive from
                official/organizer data (olimpiadascientificas.org, pt.wikipedia,
                mirrored official result tables).
  - "counts"  : corroborates medal counts only, no individual names.
(No "official" class: the IOAA has no permanent official results database; host-year
sites go offline. That absence is exactly why this trail matters.)

Optional per-source "needle": string that verify_corroboration.py must find in the
page (diacritics-insensitive). Sources with coverage=="full" are auto-checked against
the year's roster surnames instead.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

OLC = "https://olimpiadascientificas.org/equipes-brasileiras/astronomia/ioaa/"
PTWIKI = "https://pt.wikipedia.org/wiki/Olimp%C3%ADada_Internacional_de_Astronomia_e_Astrof%C3%ADsica"


def olc(confirms, url=OLC):
    return {"url": url, "domain": "olimpiadascientificas.org", "cls": "archive", "coverage": "full", "confirms": confirms}


def wiki(confirms, coverage="full", needle=None):
    d = {"url": PTWIKI, "domain": "pt.wikipedia.org", "cls": "archive", "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


SOURCES = {
 2007: [olc('both names + medals ("Thomas Ferreira de Lima (CE) - Prata / Júlio César Neves Campagnolo (PR) - Bronze")'),
        wiki("both names + medals, inaugural edition"),
        src("https://claffisica.org.br/news-item/brasil-sedia-olimpiada-internacional-de-astronomia-pela-primeira-vez",
            "claffisica.org.br", "primary", "1/2",
            'Julio Campagnolo bronze, "first Brazilian at IOAA 2007" — does not name Thomas', needle="Campagnolo")],
 2008: [olc("all four + medals incl. Katague = participation-only"),
        src("http://astrophysicsblogs.blogspot.com/2008/08/2nd-international-olympiad-on-astronomy.html",
            "astrophysicsblogs.blogspot.com", "archive", "full",
            'official results table with delegation codes ("BR-ST01 Rafael Parpinel Cavina Silver … BR-ST02 Gustavo Perez Katague Certificate")',
            needle="Katague"),
        wiki("all four incl. Katague = Certificado de participação")],
 2009: [olc("all five + medals"),
        src("https://clubedeastronomiacmpa.blogspot.com/2009/", "clubedeastronomiacmpa.blogspot.com", "primary", "full",
            'all five ("prata: Hugo Fonseca, Daniel de Barros Soares e Leonardo Stedile; bronze: Thiago Hallak; menção honrosa: Otavio Menezes")'),
        wiki("all five + medals")],
 2010: [olc("all five + medals"),
        src("http://ccd-oba.blogspot.com/2010/10/ioaa-e-olaa-resultados.html", "ccd-oba.blogspot.com", "primary", "full",
            "OBA's own blog — all five + medals (Thiago Hallak prata; Luiz Felipe, Tábata, Gustavo Haddad bronze; Tiago Gimenes MH)"),
        wiki("all five + medals")],
 2011: [olc("all five + medals incl. Bordoni = no award"),
        src("https://objetivo.br/institucional/noticias.aspx?titulo=polonia-gustavo-haddad-e-ivan-tadeu-no-podio-da-olimpiada-internacional-de-astronomia-e-astrofisica",
            "objetivo.br", "primary", "2/5", "Gustavo Haddad + Ivan Tadeu bronze", needle="Haddad"),
        wiki("full roster + medals")],
 2012: [olc("full 10-name roster + medals (host-year double team)",
            url="http://olimpiadascientificas.org/equipes-brasileiras/astronomia/ioaa/ioaa-2012/"),
        src("https://www.abc.org.br/2012/08/17/olimpiada-internacional-de-astronomia-termina-com-prata-e-bronze-para-o-brasil/",
            "abc.org.br", "primary", "9/10", "Academia Brasileira de Ciências — 2 silver + 1 bronze + six HM named", needle="Trianon"),
        wiki("2012 table")],
 2013: [src("https://agencia.fapesp.br/brasil-ganha-cinco-medalhas-em-olimpiada-internacional-de-astronomia/17703",
            "agencia.fapesp.br", "primary", "full", "all five + medals"),
        olc('all five (gives fuller "Luis Fernando Machado Poletti Valle")'),
        wiki("2013 table")],
 2014: [src("https://www.correiobraziliense.com.br/app/noticia/eu-estudante/ensino_educacaobasica/2014/08/18/ensino_educacaobasica_interna,442913/em-olimpiada-de-astronomia-brasileiros-conquistam-medalha-de-prata.shtml",
            "correiobraziliense.com.br", "primary", "full", "names the 5-student delegation + results (confirms the *Heringer* surname)"),
        olc("all five individual medals"),
        wiki("2014 table")],
 2015: [src("https://agenciabrasil.ebc.com.br/pesquisa-e-inovacao/noticia/2015-08/estudantes-brasileiros-sao-premiados-em-olimpiada-internacional",
            "agenciabrasil.ebc.com.br", "primary", "full",
            'four HM + Pedro Henrique Dias in delegation (spells "Barscevicius", "João Paulo Paiva")', needle="Khalil"),
        src("https://www.eso.org/public/portugal/announcements/annlocal15001-pt-br/", "eso.org", "primary", "1/5",
            "Carolina Lima Guimarães HM", needle="Guimar"),
        wiki("full roster + medals")],
 2016: [wiki("full roster + medals — the ONLY live source for 2016")],
 2017: [src("https://agenciabrasil.ebc.com.br/pesquisa-e-inovacao/noticia/2017-11/brasil-ganha-5-medalhas-na-olimpiada-internacional-de-astronomia",
            "agenciabrasil.ebc.com.br", "primary", "full", "silver + 2 bronze + 2 HM (corrected spellings)"),
        src("https://catracalivre.com.br/quem-inova/olimpiada-internacional-de-astronomia-e-astrofisica-premia-brasil/",
            "catracalivre.com.br", "primary", "full", 'all five (confirms "Gorresen" and "Pompeu Carneiro" spellings)'),
        wiki('2017 table (uses older "Görressen"/"de Sousa" forms)', needle="Martins")],
 2018: [src("https://www.correiobraziliense.com.br/app/noticia/eu-estudante/ensino_ensinosuperior/2018/11/12/ensino_ensinosuperior_interna,719102/brasil-conquista-quatro-medalhas-em-olimpiada-astrofisica-na-china.shtml",
            "correiobraziliense.com.br", "primary", "full", "full delegation + results"),
        src("https://blog.etapa.com.br/noticias/aluno-etapa-conquista-medalha-na-12a-ioaa", "blog.etapa.com.br",
            "primary", "1/5", "Bruno Caixeta Piazza silver + team tally", needle="Piazza"),
        wiki("2018 table")],
 2019: [src("https://agenciabrasil.ebc.com.br/educacao/noticia/2019-08/brasileiros-sao-destaque-em-olimpiada-internacional-de-astronomia",
            "agenciabrasil.ebc.com.br", "primary", "full", '3 bronze + 2 HM (confirms "Raul Basilides Gomes")'),
        src("https://coolmagazine.com.br/com-a-maior-participacao-feminina-da-historia-brasil-conquista-tres-medalhas-em-olimpiada-internacional-de-astronomia-e-astrofisica-na-hungria/",
            "coolmagazine.com.br", "primary", "full", "all five + results"),
        src("https://blog.etapa.com.br/noticias/etapa-na-maior-competicao-de-astronomia", "blog.etapa.com.br",
            "primary", "3/5", "Girotto, Bruna Lopes, Lucas Shoji + team tally", needle="Girotto")],
 2021: [wiki("2 golds (Bruno + Otávio), 4 silver, 4 bronze — matches the dataset"),
        src("https://www.gov.br/observatorio/pt-br/assuntos/noticias/brasil-conquista-cinco-medalhas-na-olimpiada-internacional-de-astronomia-e-astrofisica-2013-ioaa-2022",
            "gov.br (Observatório Nacional)", "primary", "counts",
            'official page referring to 2021\'s "dois ouros inéditos" (two golds)', needle="ouros"),
        src("https://spacewatchafrica.com/brazil-wins-gold-at-the-international-astronomy-and-astrophysics-olympiad-for-the-first-time/",
            "spacewatchafrica.com", "primary", "partial — MINORITY ACCOUNT",
            "reports 1 gold (Otávio), Bruno among silvers, Ualype among bronzes — disputed, see note", needle="Ferrari")],
 2022: [src("https://www.gov.br/observatorio/pt-br/assuntos/noticias/brasil-conquista-cinco-medalhas-na-olimpiada-internacional-de-astronomia-e-astrofisica-2013-ioaa-2022",
            "gov.br (Observatório Nacional)", "primary", "full", "official, all five + medals"),
        src("https://www.bandab.com.br/curitiba/estudante-de-curitiba-medalha-de-prata-olimpiada-astronomia-astrofisica/",
            "bandab.com.br", "primary", "1/5", "Jan Bojan Ratier silver + team tally", needle="Ratier"),
        wiki("2022 table")],
 2023: [src("https://www.gov.br/cnpq/pt-br/assuntos/noticias/cnpq-em-acao/brasil-conquista-ouro-prata-e-mencao-honrosa-na-16a-olimpiada-internacional-de-astronomia-e-astrofisica-1",
            "gov.br (CNPq)", "primary", "full", "official, all five (confirms Gabriel Hemétrio = silver)"),
        src("https://www.terra.com.br/byte/brasileiro-ouro-em-olimpiada-de-astronomia-quer-melhorar-energia-renovavel,a35ac98da9411118383d2499c0ffe0d1fq5thlyy.html",
            "terra.com.br", "primary", "full", "full roster + medals"),
        src("https://blog.etapa.com.br/noticias/ioaa-2023", "blog.etapa.com.br", "primary", "1/5",
            "Murilo de Andrade Porfírio gold", needle="Porf")],
 2024: [src("https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/noticias/2024/08/brasil-conquista-cinco-medalhas-na-17a-olimpiada-internacional-de-astronomia-e-astrofisica",
            "gov.br (MCTI)", "primary", "full", "official, all five + medals"),
        src("https://revistaeducacao.com.br/2024/08/27/olimpiada-internacional-de-astronomia-e-astrofisica/",
            "revistaeducacao.com.br", "primary", "full", "all five + home states"),
        src("https://jornalpequeno.com.br/2024/08/27/maranhense-de-17-anos-brilha-na-olimpiada-internacional-de-astronomia-e-astrofisica-2024/",
            "jornalpequeno.com.br", "primary", "full", "all five + results")],
 2025: [src("https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/noticias/2025/08/jovens-brasileiros-ganham-quatro-medalhas-na-18o-olimpiada-internacional-de-astronomia-e-astrofisica",
            "gov.br (MCTI)", "primary", "full", "official, all five + medals"),
        src("https://www.gov.br/cnpq/pt-br/assuntos/noticias/premios/estudantes-brasileiros-conquistam-14-medalhas-em-olimpiadas-internacionais-de-astronomia-e-astronautica",
            "gov.br (CNPq)", "primary", "full", "all five + medals (same gov.br domain as MCTI but a different agency)"),
        src("https://jtv.com.br/luca-pieroni-pimenta-ouro-olimpiada-internacional-astronomia-2025/",
            "jtv.com.br", "primary", "full", "Luca Pieroni Pimenta gold + full roster")],
}

NOTES = {
 2007: "Shortfall: only two sources corroborate *both* students; the third names one. Stronger both-name sources (OBA, an INPE PDF) were offline at verification time (2026-05-30).",
 2016: "Weakest-sourced year: only PT-Wikipedia lists the roster live. OBA page (idconteudo=714) 404s, olimpiadascientificas stops at 2014, host/international sites name no Brazilians. The earlier \"Sciacca\" spelling (OBA-only) is therefore unverifiable and was reverted.",
 2021: "Medal-split dispute: dataset follows ON + OBA + PT-Wikipedia = 2 golds (Bruno=gold, Ualype=silver). Minority account (spacewatchafrica + Colégio Etapa, https://blog.etapa.com.br/noticias/ioaa-2021) = 1 gold, Bruno=silver, Ualype=bronze. Team of 10 undisputed. Definitive ioaa2021.com results PDF is offline (404).",
}

GLOBAL_NOTES = [
 "No IOAA in 2020 (GeCAA substitute — deliberately excluded; roster kept in data/raw/gecaa-2020.json).",
 "Sources deliberately NOT cited because offline/restricted at verification time (2026-05-30): several OBA pages (404/refused), gov.br/aeb 2021 gold article (\"Conteúdo Restrito\"), various Agência Brasil / Agência Gov mirrors (temporarily deactivated under Brazilian electoral law).",
 "Every URL was fetched live and read at migration time; re-verify anytime with scripts/verify_corroboration.py (results land in data/corroboration_check.json).",
 "Liveness check 2026-08-01: 48/52 URLs PASS with content verified. The 4 content-check misses are checker artifacts, NOT dead links: bandab.com.br and the two gov.br/MCTI pages (2024, 2025) render the article body via JavaScript (names absent from server HTML; articles alive in a browser), and abc.org.br serves a WAF/bot wall (406) to scripted fetches.",
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
        "olympiadId": "ioaa",
        "description": "Independent web sources confirming Brazilian IOAA participants + results, per edition.",
        "provenanceClasses": {
            "primary": "Genuinely independent reporting naming Brazilian competitors + results (gov.br agencies, OBA blog, ABC, FAPESP, Agência Brasil, press, schools).",
            "archive": "Result compilations naming the roster but likely derived from organizer data (olimpiadascientificas.org, pt.wikipedia, mirrored result tables).",
            "counts": "Corroborates medal counts only, no individual names.",
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

    md = f"""# Per-Year Corroboration — Independent Sources for Brazil at the IOAA

**Machine-readable version:** `data/corroboration.json`. Rebuild with
`python3 scripts/build_corroboration.py`; re-verify URLs (liveness + content) with
`python3 scripts/verify_corroboration.py` (writes `data/corroboration_check.json`).

Migrated from the handwritten `SOURCES.md` (research pass verified 2026-05-30) into the
repo-standard structured format. Every URL was fetched and its Brazilian rows read at
research time — not cited from search snippets.

## Headline

- **{n3} of {len(records)} editions** have ≥3 participant-naming source domains.
- **{p3} of {len(records)} editions** have ≥3 counting only genuinely-independent primaries
  (archives excluded). The IOAA has **no permanent official results database** — host-year
  sites rot — so the archive tier (olimpiadascientificas, PT-Wikipedia) carries real weight here.
- Flagged shortfalls: **2007** (third source names only 1 of 2) and **2016** (PT-Wikipedia only).
- **2021** carries a medal-split dispute note (dataset follows the official 2-gold account).

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
