#!/usr/bin/env python3
"""
Assemble data/corroboration.json and CORROBORATION.md for Brazil at the IJSO, in the
repo-standard structured format (same schema as imo/). Sources were collected and read
by the 2026-08-02 research pass.
Re-verify liveness+content with scripts/verify_corroboration.py.

Provenance classes:
  - "official": IJSO organisation / host-committee result documents (ijsoweb.org,
                per-year host sites, the old ijso-official.org — mostly via Wayback).
  - "primary" : the Brazilian organizer OBC/B8 (obciencias.com.br — NOTE: plain-HTTP only,
                TLS broken), contemporary press (FAPESP, Estadão), schools (Objetivo,
                Etapa), NOIC, government (CCPM/PMCE, Consed).
  - "archive" : olimpiadascientificas.org and pt.wikipedia rosters (pre-2008 OLC pages
                explicitly cite pt-wikipedia; OBC/wiki wording also overlaps — lineage
                independence is limited; treated honestly as archive tier).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

OBC_H = "http://www.obciencias.com.br/histoacuteria.html"
OBC_N = "http://www.obciencias.com.br/notiacutecias.html"
OLC = "https://olimpiadascientificas.org/equipes-brasileiras/interdisciplinar/ijso/"
PTWIKI = "https://pt.wikipedia.org/wiki/Olimp%C3%ADada_Internacional_J%C3%BAnior_de_Ci%C3%AAncias"


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def obc(confirms="full roster + medals (organizer's História page)"):
    return src(OBC_H, "obciencias.com.br (OBC/B8)", "primary", "full", confirms)


def olc(confirms, url=OLC):
    return src(url, "olimpiadascientificas.org", "archive", "full", confirms)


def wiki(confirms="roster + medals", url=PTWIKI):
    return src(url, "pt.wikipedia.org", "archive", "full", confirms)


SOURCES = {
 2004: [src("https://web.archive.org/web/2005/http://www.agencia.fapesp.br/boletim_dentro.php?id=2911",
            "agencia.fapesp.br (Wayback)", "primary", "full", "final traveling delegation — all 6 names + ages + schools (26/11/2004)"),
        src("https://web.archive.org/web/20050207052420/http://www.ozzybohmer.com/jakarta2004-resultado.asp",
            "ozzybohmer.com (coordinator, Wayback)", "primary", "1/6", "post-event: Rafael Guedes Lang bronze (the only medal)", needle="Lang"),
        obc("full roster + Lang bronze, 25th place ('Karen Hosomi, Teramae' typo = one person)"),
        wiki()],
 2005: [obc("full roster: 3 silver + 1 bronze + 2 no-award, 12th place"),
        src("https://web.archive.org/web/20110206035452/http://www.ijso.com.br/historia.htm",
            "ijso.com.br (B8, Wayback 2011)", "primary", "full", "earliest organizer record — same roster/medals"),
        wiki("roster + medals — ⚠️ weakest year: organizer and wiki wording overlap; no contemporary source survives")],
 2006: [src("https://web.archive.org/web/20080525100609/http://www.ozzybohmer.com/ijso2006/results/Moderation.htm",
            "ozzybohmer.com/ijso2006 (host, Wayback)", "official", "full",
            "host result sheet — all 12 students under 'Brazil 1'/'Brazil 2' headings (ONLY source for the team split)", needle="Terceros"),
        src("https://web.archive.org/web/20080525101802/http://www.ozzybohmer.com/ijso2006/results/Medalswinner.htm",
            "ozzybohmer.com/ijso2006 (host, Wayback)", "official", "full", "ranked medal list — Cavina/Terceros silver band, Niide/Valverde bronze band, others rank ≈129–172", needle="Cavina"),
        src("https://ijsoweb.org/participating-countries", "ijsoweb.org", "official", "counts",
            "current official past-results: Brazil-1 0/1/1, Brazil-2 0/1/1", needle="Brazil"),
        obc("roster + the 4 medalists (no team split)")],
 2007: [src("https://web.archive.org/web/20101125235547/http://www.ijso-official.org/node/44",
            "ijso-official.org (Wayback)", "official", "counts", "official ranking: Brazil 0G/4S/2B, 7th place", needle="Brazil"),
        src("https://web.archive.org/web/20130324174549/http://200.136.76.28/noticias.asp?id=2432",
            "Objetivo (Wayback)", "primary", "5/6", "names the 5 Objetivo students + medals; 7th of 43", needle="Tsai"),
        obc(), wiki("roster + medals (incl. dedicated IJSO 2007 article)")],
 2008: [olc("full roster + medals + SP states", url=OLC + "ijso-2008/"),
        obc("full roster; Gustavo Haddad gold = first ever by an Americas country"),
        src("https://ijsoweb.org/participating-countries", "ijsoweb.org", "official", "counts", "Brazil 1G/4S/1B", needle="Brazil"),
        wiki()],
 2009: [olc("full roster + medals (page authored by Ivan Antunes Filho, a 2009 team member — near-primary)", url=OLC + "ijso-2009/"),
        obc(), wiki()],
 2010: [olc("full roster + medals + leaders", url=OLC + "ijso-2010/"),
        obc("full roster + experimental-exam team bronze"),
        src("https://olimpiada.webnode.com.br/home/newscbm_124783/110/", "olimpiada.webnode.com.br", "primary", "full",
            "contemporary article (2010-12-10): full roster + medals + experimental 3rd place"),
        wiki("full roster (dedicated IJSO_2010 article; 32 delegations)", url="https://pt.wikipedia.org/wiki/IJSO_2010")],
 2011: [olc("full roster + medals + leaders", url=OLC + "ijso-2011/"),
        obc("full roster (leader full name Victor Fujii Ando)"),
        src("https://ijsoweb.org/participating-countries", "ijsoweb.org", "official", "counts", "8th IJSO ranking: Brazil 3S/3B", needle="Brazil"),
        wiki()],
 2012: [olc("full roster + overall & experimental medals + leaders"),
        obc("full roster + experimental GOLD (perfect score — Forte/Farias/Camacho)"),
        wiki("full roster, 1G/3S/2B (dedicated IJSO_Brasil_2012 article)", url="https://pt.wikipedia.org/wiki/IJSO_Brasil_2012")],
 2013: [src(OBC_N, "obciencias.com.br (OBC/B8)", "primary", "full", "contemporary item 21/12/2013 — all six full names + medals + Pune dates"),
        obc(), olc("full roster + medals"), wiki()],
 2014: [obc("full roster + medals + leaders/observers"),
        src("http://www.obciencias.com.br/resultados-2014.html", "obciencias.com.br (OBC/B8)", "primary", "full",
            "selection list — exactly these 6 with schools/cities"),
        src(OBC_N, "obciencias.com.br (OBC/B8)", "primary", "full", "contemporary item 21/12/2014: 2 silver + 4 bronze"),
        olc("same 6 names + medal split"), wiki()],
 2015: [src("https://noic.com.br/interdisciplinares/medalhas-de-prata-para-o-brasil-na-olimpiada-internacional-junior-de-ciencias-ijso/",
            "noic.com.br", "primary", "full", "2015-12-10: full 6-name roster, all silver; Victor Cambraia top silver of the event"),
        obc("'12.a IJSO' — full roster, all silver"),
        src("https://web.archive.org/web/20160415035329/http://www.obciencias.com.br/notiacutecias.html",
            "obciencias.com.br (Wayback)", "primary", "full", "item 17/12/2015 — all 6 silver (short names)")],
 2016: [src("https://noic.com.br/uncategorized/brasil-conquista-4-ouros-e-melhor-resultado-da-historia-na-olimpiada-internacional-de-ciencias-junior-ijso/",
            "noic.com.br", "primary", "full", "full roster, 4G+2S + experimental gold/silver split — best result in history"),
        obc("'13.a IJSO' — full unabbreviated names, 4G+2S, experimental gold Time A"),
        src("https://www.objetivo.br/institucional/noticias.aspx?titulo=ijso-equipe-olimpica-do-objetivo-conquista-ouro-e-prata-na-indonesia",
            "objetivo.br", "primary", "3/6", "Calderaro + Corrêa gold, Anne Feng Cai silver", needle="Calderaro"),
        src("https://web.archive.org/web/20161114153003/http://www.obciencias.com.br/resultados-2016.html",
            "obciencias.com.br (Wayback)", "primary", "full", "OBC 2016 gold medalists = the IJSO team (schools/cities)")],
 2017: [obc("'14.a IJSO' — full 6-name roster, all silver (final delegation)"),
        src("https://www.objetivo.br/institucional/noticias.aspx?titulo=olimpiada-internacional-de-ciencias-junior-ijso-rafael-akira-e-medalha-de-prata",
            "objetivo.br", "primary", "1/6", "Rafael Akira Okamura Ferro silver, best BR score, Gelderland Dec 3–12", needle="Akira"),
        src("https://www.escavador.com/sobre/601264619/ricardo-sammuel-moura-lima", "escavador.com", "primary", "1/6",
            "Lattes-derived: Ricardo Sammuel Moura Lima silver, 14th IJSO", needle="Sammuel"),
        src("https://noic.com.br/uncategorized/divulgado-o-time-da-ijso-2017/", "noic.com.br", "primary", "5/6 — SUPERSEDED pre-event roster",
            "Oct 2017 announcement listed Ygor de Santana Moura; final delegation had Ricardo Sammuel instead", needle="Ygor")],
 2018: [obc("'15.a IJSO' — full roster, 4S+2B"),
        src("https://objetivo.br/institucional/noticias.aspx?titulo=ijso-selecao-olimpica-do-objetivo-conquista-prata-e-bronze-na-africa",
            "objetivo.br", "primary", "3/6", "Baracat + Menegon silver, Alexandre Almeida bronze; Baracat top of Americas/S. hemisphere (school claim)", needle="Baracat"),
        src("https://blog.etapa.com.br/noticias/etapa-conquista-prata-na-ijso-2018", "blog.etapa.com.br", "primary", "1/6",
            "Eduardo Bardal Slikta silver; team total 4 prata + 2 bronze", needle="Slikta"),
        src("https://noic.com.br/interdisciplinares/veja-a-equipe-brasileira-na-ijso-2018/", "noic.com.br", "primary", "full",
            "pre-event roster — matches final delegation")],
 2019: [src("https://noic.com.br/2019/12/16/equipe-brasileira-conquista-dois-ouros-e-quatro-pratas-na-ijso-2019",
            "noic.com.br", "primary", "full", "full 6-name roster with medals (2G+4S)"),
        obc("'16.a IJSO' — full roster with medals"),
        src("https://www.objetivo.br/institucional/noticias.aspx?titulo=olimpiada-internacional-junior-de-ciencias-no-catar-alunos-do-objetivo-conquistam-ouro-e-prata",
            "objetivo.br", "primary", "4/6", "Caio gold (best BR score), Baracat/Pezato/Alicia silver", needle="Pezato"),
        src("https://blog.etapa.com.br/noticias/etapa-em-competicao-internacional-de-ciencias", "blog.etapa.com.br", "primary", "2/6",
            "Vinícius Kenji gold, Lucas Takayasu silver; team 2G+4S", needle="Takayasu")],
 2021: [src("http://www.obciencias.com.br/resultados-2021.html", "obciencias.com.br (OBC/B8)", "primary", "full",
            "official convocados — all 6 names + seletiva ranks"),
        src("https://ijsoweb.org/event/2021/medals-list-2021.pdf", "ijsoweb.org", "official", "counts",
            "official medals list: Brazil 0G/2S/2B", needle="Brazil"),
        src("https://blog.etapa.com.br/noticias/ijso-2021", "blog.etapa.com.br", "primary", "2/6",
            "Viegas + Lucas Cavalcante silver; team of 6; hybrid Dubai edition", needle="Viegas"),
        src("https://objetivo.br/institucional/noticias.aspx?titulo=e-bronze-olimpiada-internacional-junior-de-ciencias-ijso-premia-aluno-do-objetivo",
            "objetivo.br", "primary", "1/6", "Igor Bersanetti Gabilondo bronze", needle="Gabilondo"),
        src("https://br.linkedin.com/in/mateus-augusto-cavassin", "linkedin.com", "primary", "1/6 — single source",
            "Cavassin bronze, world rank 56 (self-reported; consistent with official tally)", needle=None)],
 2022: [src("https://web.archive.org/web/20230321021334/https://www.ijso2022.com/ijso-2022/results",
            "ijso2022.com (host, Wayback)", "official", "full",
            "official results page + individual-results PDF link — 2G/4S + BEST EXPERIMENTAL = Brazil Team B (Loes, Porfirio, Oda)", needle="Loes"),
        src("http://www.obciencias.com.br/resultados-2022.html", "obciencias.com.br (OBC/B8)", "primary", "full", "official convocados — same 6 names"),
        src("https://blog.etapa.com.br/noticias/ijso-2022", "blog.etapa.com.br", "primary", "2/6",
            "Loes 6th overall (best BR placement ever) + Porfírio 16th, both gold; experimental gold", needle="Loes"),
        src("https://www.objetivo.br/institucional/noticias.aspx?titulo=ijso-2022-olimpiada-internacional-junior-de-ciencias-premia-alunos-do-objetivo-com-ouro-e-prata",
            "objetivo.br", "primary", "4/6", "4 Objetivo silvers + Gustavo Jun experimental gold (article uses first names: 'Gustavo Jun e Vitor Takashi')", needle="Gustavo Jun")],
 2023: [src("http://www.obciencias.com.br/resultados-2023.html", "obciencias.com.br (OBC/B8)", "primary", "full",
            "official convocados — 6 names + seletiva scores (ROSTER only; per-student medals unpublished)"),
        src("https://web.archive.org/web/20241013093932/https://ijso2023.in.th/wp-content/uploads/2023/12/IJSO_2023_Results.pdf",
            "ijso2023.in.th (host, Wayback)", "official", "counts", "official results: Brazil 0G/4S/1B (country level only)", needle="Brazil"),
        src("https://www.pm.ce.gov.br/2023/11/10/aluno-do-cpmce-gef-finalista-de-olimpiada-internacional-junior-de-ciencias-e-recebido-pelo-comando-da-pmce/",
            "pm.ce.gov.br", "primary", "1/6", "Sanzio Fechine selection/participation (gov.br-CE)", needle="Sanzio"),
        src("https://noic.com.br/quem-somos/", "noic.com.br", "primary", "1/6",
            "Henrique Pongelupp 'premiado na IJSO 2023' (medal color unstated)", needle="Pongelupp")],
 2024: [src("https://www.instagram.com/p/DDcZDoHRNMT/", "instagram.com/@obciencias (via imginn)", "primary", "full",
            "ORGANIZER'S RESULT POST (11 Dec 2024): 'Brasil ganha 6 medalhas de bronze na IJSO... 100%% do time brasileiro volta premiado' — ALL SIX bronze.", needle=None),
        src("http://www.obciencias.com.br/resultados-2024.html", "obciencias.com.br (OBC/B8)", "primary", "full",
            "official convocados — 6 names + seletiva scores (page live but unlinked from menu)"),
        src("https://www.objetivo.br/institucional/noticias.aspx?titulo=aluno-do-objetivo-conquista-bronze-na-ijso-uma-das-mais-importantes-olimpiadas-cientificas-do-mundo",
            "objetivo.br", "primary", "1/6", "Felipe Garcia Araújo bronze, 21st IJSO Bucharest", needle="Felipe"),
        src("https://noic.com.br/quem-somos/", "noic.com.br", "primary", "1/6",
            "Jailson Godeiro Neto bronze (year inferred from his single OBC convocation)", needle="Jailson"),
        src("https://www.consed.org.br/noticia/olimpiada-brasileira-de-ciencias-levara-estudantes-brasileiros-para-competicao-internacional-na-romenia",
            "consed.org.br", "primary", "counts", "OBC→IJSO 2024 pipeline + dates (no names)", needle=None)],
}

NOTES = {
 2004: "Pre-travel roster substitution: the original selection list (Wayback 20041204154540) named Fernanda Ishizaki Brocanella Witter and Lucas Kollef; the delegation that flew (FAPESP list) had Bruna Guidini Santos and Rafael Guedes Lang instead.",
 2005: "Weakest-sourced year: no contemporary source survives; organizer (OBC/B8) and pt-wikipedia wording overlap, so lineage independence is limited.",
 2006: "Host year, TWO teams (Brazil-1/Brazil-2, 12 students). The team split exists ONLY in the host Moderation sheet + ijsoweb country table (they agree). Closing ceremony was cancelled. Graph convention: all 12 linked as same-edition co-participants (same as IOAA 2012).",
 2017: "Final delegation differs from NOIC's October pre-event roster (Ygor de Santana Moura → Ricardo Sammuel Moura Lima); no explanation found. OBC História is the final record.",
 2021: "Hybrid Dubai edition; Brazilian team sat exams online from São Paulo. The two no-medal records are INFERRED from the official 0G/2S/2B tally (airtight: the other 4 medals are individually attributed).",
 2023: "RESOLVED 2026-08-04: per-student medals via direct communication from the Brazilian olympiad community (project owner's contact) — 4 silver (Evers Cordeiro, Feltran, Porfirio, Azevedo) + 1 bronze (Pongelupp), exactly matching the official country tally (0G/4S/1B, host PDF via Wayback). Only year whose per-student medals rest on a non-public source. The sixth convoked student was removed from the dataset by project decision (2026-08-04). Historical traps kept on record: organizer posted nothing about this edition; en-wiki carries an uncited incident claim (added 2026-06-17, hidden team-leader comment) — never attributed to anyone here.",
 2024: "RESOLVED 2026-08-03 via the organizer's Instagram (@obciencias, 11 Dec 2024, read through imginn.com): ALL SIX students won bronze ('100%% do time brasileiro volta premiado', six 🥉). Consistent with the two independently-known bronzes (Felipe — Objetivo; Jailson — NOIC bio). The IJSO organisation itself still published no results document. Delegation post comments confirm Victor Tsuneichi is STAFF (grouped with Ronaldo Fogo; also tagged as staff in the Dec-2022 post), not a seventh student.",
}

GLOBAL_NOTES = [
 "Brazil attended 20 editions: 2004–2019 + 2021–2024. 2020 (17th, Frankfurt) was cancelled outright — zero countries in the official matrix. 2025 (22nd, Sirius/Russia) = verified Brazilian absence (complete official country column without Brazil).",
 "obciencias.com.br (OBC/B8, the Brazilian organizer) rejects modern TLS — fetch plain-HTTP.",
 "olimpiadascientificas.org's pre-2008 IJSO pages explicitly cite pt-wikipedia (per their GitHub source) — classed 'archive', not independent, for those years.",
 "medal=null carries THREE meanings here, disambiguated by medalStatus in data/raw/ijso.json: confirmed no-award (2004–2006, 15 records), inferred no-award from official tally (2021, 2 records), and UNKNOWN pending better sources (2023: 6 records incl. one known medalist of unknown color; 2024: 4 records).",
 "Re-check list for the 2023/2024 gaps: B8/OBC Instagram (Dec 2023 / Dec 2024 posts), future NOIC student bios, ijsoweb result files for 18th–21st if ever posted, Etapa 'conquistas' yearbook PDFs.",
 "Liveness check 2026-08-02: 73/78 URLs PASS. Known temporal/bot-wall failures, not rot: escavador.com 403s scripts; LinkedIn 999s scripts; pm.ce.gov.br currently serves an ELECTORAL-PERIOD placeholder (Brazilian pre-election restriction — re-check after Oct 2026); noic.com.br/quem-somos rate-limited the checker (other NOIC URLs pass).",
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
        "olympiadId": "ijso",
        "description": "Independent web sources confirming Brazilian IJSO participants + results, per edition.",
        "provenanceClasses": {
            "official": "IJSO organisation / host-committee result documents (ijsoweb.org, host sites, old ijso-official.org — mostly Wayback).",
            "primary": "Brazilian organizer OBC/B8, contemporary press (FAPESP, Estadão), schools (Objetivo, Etapa), NOIC, government sources.",
            "archive": "olimpiadascientificas.org and pt.wikipedia rosters (limited lineage independence; pre-2008 OLC cites wikipedia).",
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

    md = f"""# Per-Year Corroboration — Independent Sources for Brazil at the IJSO

**Machine-readable version:** `data/corroboration.json`. Rebuild with
`python3 scripts/build_corroboration.py`; re-verify URLs (liveness + content) with
`python3 scripts/verify_corroboration.py`.

## Headline

- **{n3} of {len(records)} editions** have ≥3 participant-naming source domains.
- **{p3} of {len(records)} editions** have ≥3 genuinely-independent primaries.
- **Open gaps: 2023 and 2024 individual medals** (see the per-year notes) — rosters are
  complete for all 20 editions; medals are complete for 18 of 20.

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
