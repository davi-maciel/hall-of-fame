#!/usr/bin/env python3
"""
Corroboration for Brazil at the IEO (International Economics Olympiad; repo-standard). 2026-09-11 collection pass.
Brazil has attended all nine editions (2018-2026), five contestants each year. Official per-edition results live on
the yearly sites (<year>.ieo-official.org/results, with spreadsheets under files.ecolymp.org / files.ieo-official.org)
and on the Livewire results page of ieo-official.org (year selector; the default view shows the latest edition).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MAIN = "https://ieo-official.org/results"


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def yearly(year, needle, path="results"):
    return src(f"https://{year}.ieo-official.org/{path}", f"{year}.ieo-official.org", "official", "full",
               f"Official IEO {year} site: individual results (medal lists + full ranking by score) with the five Brazilians", needle)


def xlsx(url, year):
    return src(url, url.split('/')[2], "official", "full (spreadsheet; not text-checked)",
               f"Official IEO {year} results spreadsheet: surname/first name, country, scores, medal", None)


def main_page(needle=None):
    return src(MAIN, "ieo-official.org", "official",
               "full (Livewire year selector; the fetched default view shows the latest edition only)",
               "ieo-official.org annual results: name, country, final total, medal, special awards for every year 2018-2026", needle)


def press(url, domain, needle, confirms, coverage="full"):
    return src(url, domain, "primary", coverage, confirms, needle)


SOURCES = {
 2018: [yearly(2018, "Rafael Carlini", "results/"), src("https://2018.ieo-official.org/the-final-results/", "2018.ieo-official.org", "official", "medallists", "IEO 2018 news 'The final results': team ranking (Brazil joint 3rd) and gold/silver/bronze lists", "Marcio Akira Imanishi de Moraes"), main_page(),
        press("https://liberdadenews.com.br/educacao/25947-brasil-ficou-com-as-medalhas-de-ouro-e-prata-na-olimpiada-internacional-de-economia", "liberdadenews.com.br", "Lasevicius", "Press (Oct 2018): two golds (Rafael Carlini - Etapa; Marcio Akira Imanishi - Objetivo Integrado), two silvers (Tomas Aguirre Lessa Vaz - EE Manuel Ciridiao Buarque; Henrique Lasevicius - Objetivo Integrado); Adriano Kenzo Bonara the fifth member; team 3rd"),
        press("https://www.obecon.org.br/a-obecon-e-sua-marca-na-trajetoria-de-rafael-carlini/", "obecon.org.br", "Rafael Carlini", "OBECON profile: Rafael Carlini gold and 6th overall at IEO 2018; Brazil two golds and two silvers", "one student")],
 2019: [yearly(2019, "Guilhermo Cutrim Costa"), xlsx("https://files.ecolymp.org/2019/IEO_Results_2019.xlsx", 2019), main_page(),
        press("https://gauchazh.clicrbs.com.br/educacao/noticia/2019/08/comandado-por-tecnicos-gauchos-grupo-do-brasil-leva-1o-lugar-em-olimpiada-internacional-de-economia-cjzkc3ovc04fu01qm0nynvpk4.html", "gauchazh.clicrbs.com.br", None, "GZH (Aug 2019): Brazil 1st overall in Saint Petersburg with three golds, one silver and one bronze; team led by Germano Martinelli and the Zimmermann brothers", "team result")],
 2020: [yearly(2020, "Costa Guilhermo Cutrim"), xlsx("https://files.ecolymp.org/2020/IEO_Results_2020.xlsx", 2020), main_page(),
        press("https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/noticias/2020/10/estudantes-medalhistas-das-olimpiadas-internacionais-de-economia-e-matematica-sao-recebidos-pelo-presidente-da-republica", "gov.br", None, "MCTI (Oct 2020): the IEO-winning Brazilian team received by the President and the Economy minister; OBECON's Gustavo Wigman quoted", "event")],
 2021: [yearly(2021, "Ayres de Camargo"), xlsx("https://files.ecolymp.org/2021/IEO_Results_2021.xlsx", 2021), main_page(),
        press("https://www.objetivo.br/institucional/noticias.aspx?titulo=brasil-e-tricampeao-consecutivo-na-olimpiada-internacional-de-economia-ieo-2", "objetivo.br", "Nachtergaele", "Colegio Objetivo: Sebastiao Froes Nachtergaele Gomes Navarro and Nicolas Goulart Moura (Objetivo Integrado, 3rd year) gold at the online IEO 2021 (Latvia, 26 Jul-1 Aug); Brazil three-time champion", "2 of 5")],
 2022: [yearly(2022, "Fornielles"), xlsx("https://files.ecolymp.org/2022/IEO_Results_2022.xlsx", 2022), main_page(),
        press("https://www.obecon.org.br/mirella-da-obecon-a-notre-dame/", "obecon.org.br", "Mirella Diniz Wunderlich", "OBECON profile: Mirella Diniz Wunderlich (Juiz de Fora) on the 2022 delegation (Shanghai/online, 26 Jul-1 Aug 2022), first woman on a Brazilian IEO team", "one student")],
 2023: [yearly(2023, "Zanetti"), xlsx("https://files.ecolymp.org/2023/IEO_Results_2023.xlsx", 2023), main_page(),
        press("https://www.obecon.org.br/na-grecia-o-tao-aguardado-tetracampeonato/", "obecon.org.br", "Renato Timoteo Wanderley", "OBECON: fourth team title in Greece (1 Aug 2023) - three golds, one silver, one bronze; the five names")],
 2024: [yearly(2024, "Schmaltz"), xlsx("http://files.ieo-official.org/2024/IEO_2024_Results.xlsx", 2024), main_page(),
        press("https://exame.com/carreira/olimpiada-brasileira-de-economia-conheca-os-5-brasileiros-que-irao-participar-da-disputa-mundial/", "exame.com", None, "Exame (Jun 2024): the five OBECON winners selected for Hong Kong - Antonio Lima, Frederico Ribeiro, Joao Vitor Carvalho, Lucas Rivelli, Manuela Buesa", "full (pre-event, short names)")],
 2025: [yearly(2025, "Rivelli"), xlsx("https://files.ieo-official.org/2025/IEO_2025_Results.xlsx", 2025), main_page(),
        press("https://www.bcb.gov.br/conteudo/agendas/Documents/Lista_de_presen%C3%A7a%20OBECON.pdf", "bcb.gov.br", "Marina Cintra Luiz", "Banco Central do Brasil agenda (5 Aug 2025): attendance list of the delegation that represented Brazil at the IEO in Azerbaijan - full names of the five contestants and three leaders", "full (post-event, full names)"),
        press("https://portal.fgv.br/noticias/retrospectiva-2025-brasil-e-destaque-na-olimpiada-internacional-de-economia-com-premiacoes-historicas", "portal.fgv.br", "Antonio Gama", "FGV portal: Baku 2025 - two silvers, two bronzes, 1st in Finance; Antonio Gama named among the delegation", "team result"),
        press("https://www.obecon.org.br/terceira-fase-obecon-2025/", "obecon.org.br", "Lucas Monteiro Rivelli", "OBECON (Sep 2025): the five gold medallists of the 3rd phase represented Brazil at IEO 2025 in Baku (July 2025); Lucas Monteiro Rivelli quoted", "event")],
 2026: [main_page("Arthur Spuri"),
        press("https://braziljournal.com/brasil-ganha-tres-ouros-na-olimpiada-de-economia-e-tem-maior-nota-da-historia/", "braziljournal.com", "Artur Teixeira", "Brazil Journal (20 Jul 2026): three golds in Shenzhen - Arthur Spuri (Top Gold, 1st overall), Artur Teixeira (11th), Enzo Tavares (12th); best business case", "3 of 5"),
        press("https://tribunaonline.com.br/brasil/brasileiro-de-16-anos-conquista-recorde-na-olimpiada-internacional-de-economia-316687", "tribunaonline.com.br", "Arthur Spuri", "Tribuna Online / Folhapress (22 Jul 2026): Arthur Spuri, 16, Colegio Farias Brito (Fortaleza), 1st overall with 199.469; days earlier he won IPhO silver in Bucaramanga", "one student"),
        press("https://www.radarurgente.com.br/site/ler/brasileiro-de-16-anos-e-o-primeiro-sul-americano-a-vencer-olimpiada-internacional-de-economia-/34872", "radarurgente.com.br", "Spuri", "Radar Urgente / O Globo (24 Jul 2026): Arthur Spuri first South American to top the IEO; two other Brazilian golds", "one student"),
        press("https://pt.linkedin.com/posts/btgpactual_btgpactual-bancobtgpactual-obecon-activity-7447645060394835968-GJaB", "linkedin.com", "Luiza Ara", "BTG Pactual (Apr 2026): the delegation selected at the OBECON final - Arthur Spuri, Arthur Teixeira, Enzo Tavares, Luiza Araujo, Pedro Camara", "full (pre-event, short names)"),
        press("https://www.instagram.com/p/DbL-mKDq6A4/", "instagram.com", None, "Razoes para Acreditar (24 Jul 2026): 'Arthur Alencar Spuri, de Fortaleza' gold and top score at the IEO in Shenzhen", "one student (full name)")],
}

NOTES = {
 2018: "Moscow (1st IEO, 13 countries). Brazil joint 3rd team; Adriano Kenzo Inoue Bonora without individual award (press spells 'Bonara').",
 2019: "Saint Petersburg. First team title (Gold trophy). All five names verbatim from the official site.",
 2020: "Online (Astana host). Second team title. The 2020 yearly site lists names surname-first ('Costa Guilhermo Cutrim'); rows use the main site's first-name-first form.",
 2021: "Online (Riga host). Third team title. 'Sebastiao Froes' (2021 site) and 'Fróes' (2022 site) are the same person - rows use the accented form. Colegio Objetivo confirms Navarro and Goulart de Moura as its students.",
 2022: "Hybrid (China; Brazilian team took part online/Shanghai per OBECON). Silver trophy. Mirella Diniz Wunderlich first woman on a Brazilian team.",
 2023: "Volos, Greece. Fourth team title; OBECON's post names all five.",
 2024: "Hong Kong. Team 4th. Full names from the official spreadsheet; Exame's pre-event list uses short forms (Antonio Lima = Antonio Gama Lima, Frederico Ribeiro = Frederico Schmaltz de Rezende Ribeiro, Joao Vitor Carvalho = Joao Vitor de Castro Carvalho).",
 2025: "Baku. The official 2025 list gives short names (Lucas Rivelli, Antonio Lima, Fernando Avila, Maria Clara Souza, Marina Luiz); full names from the Banco Central attendance list of the same delegation (Lucas Monteiro Rivelli, Antonio Gama Lima, Fernando Giron Paranhos de Avila, Maria Clara Ribeiro Teixeira de Souza, Marina Cintra Luiz). Lucas Monteiro Rivelli (Instituto Alpha Lumen) competed for the third time before starting at Duke in Aug 2025. Marina Cintra Luiz without individual award.",
 2026: "Shenzhen, 12-20 Jul 2026 (9th IEO). Arthur Spuri = Arthur Alencar Spuri (Farias Brito, Fortaleza; IPhO 2026 silver days earlier) - Top Gold, best score in IEO history (199.469); Artur Teixeira ('Arthur' in BTG's post) and Enzo Tavares gold; Luiza Araujo bronze; Pedro Camara (= Pedro Paraguassu Camara of the IYPT 2026 team, identified from the delegation photos; Zurich 5-12 Jul immediately preceded Shenzhen) without individual award. Best business case. Full names for Teixeira, Tavares and Araujo not yet published.",
}

GLOBAL_NOTES = [
 "Nine editions attended (2018-2026, all of them), five contestants each: 45 records. Individual medals: 22 gold, 14 silver, 6 bronze (matches the ieo-official.org/countries/brazil tally); three members without award. Team Gold trophy 2019, 2020, 2021, 2023; Silver 2022; Bronze 2018.",
 "Official sources: yearly sites <year>.ieo-official.org/results (2018-2025; full rankings and medal lists), the results spreadsheets (files.ecolymp.org 2019-2023, files.ieo-official.org 2024-2025) and the Livewire results page ieo-official.org/results (all years via its year selector; 2026 is its default view). Medal bands: top 20 gold, 21-50 silver, 51-100 bronze (Brazil Journal 2026).",
 "Selection: OBECON (Olimpiada Brasileira de Economia, since 2018) - online first phase, written second phase, in-person third phase with a business case; the five gold medallists form the delegation.",
 "Name forms: rows use the fullest documented form (official spreadsheets 2020-2024; Banco Central list for 2025; press for Arthur Alencar Spuri 2026). Short official forms remain for Artur Teixeira, Enzo Tavares and Luiza Araujo (2026); 'Pedro Camara' is recorded as Pedro Paraguassu Camara (IYPT 2026 team member, photo identification).",
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
        "olympiadId": "ieo",
        "description": "Sources confirming Brazilian IEO contestants + results, per edition.",
        "provenanceClasses": {
            "official": "ieo-official.org (annual results page, yearly sites, results spreadsheets).",
            "primary": "OBECON (national organizer) posts; Banco Central do Brasil agenda list; schools; press (Exame, Brazil Journal, Folhapress/Tribuna, O Globo/Radar, GZH, FGV, gov.br).",
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
    md = ("# Per-Year Corroboration — Brazil at the IEO\n\n"
          "**Machine-readable:** `data/corroboration.json`. Rebuild: `python3 scripts/build_corroboration.py`; "
          "verify: `python3 scripts/verify_corroboration.py`. 2026-09-11 collection pass.\n\n## Notes\n\n"
          + "\n".join(f"- {n}" for n in GLOBAL_NOTES)
          + "\n\n## Summary\n\n| Year | Sources | Domains |\n|-----:|:--:|---------|\n" + "\n".join(lines)
          + "\n\n## Per-year sources\n\n" + "\n".join(details))
    with open(os.path.join(ROOT, "CORROBORATION.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Editions: {len(records)}")


if __name__ == "__main__":
    main()
