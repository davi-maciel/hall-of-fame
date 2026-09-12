#!/usr/bin/env python3
"""
Corroboration for Brazil at the OLAA (repo-standard). 2026-09-10 collection pass: every URL fetched and
content-verified. Editions: 2009-2025 (17, all attended; 2020 virtual, 2021 hybrid; 2025 hosted with two teams).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WIKI = "https://pt.wikipedia.org/wiki/Olimp%C3%ADada_Latino-Americana_de_Astronomia_e_Astron%C3%A1utica"
OLC = "https://olimpiadascientificas.org/equipes-brasileiras/astronomia/olaa/"


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def wiki(needle):
    return src(WIKI, "pt.wikipedia.org", "primary", "full", "pt.wikipedia 'Delegações brasileiras' (OBA-sourced per-year rosters with medals, cities and leaders)", needle)


def olc(needle, sub=""):
    return src(OLC + sub, "olimpiadascientificas.org", "primary", "full", "olimpiadascientificas.org roster 2009-2012 (medals + states)", needle)


def noic(url, needle, confirms, coverage="full"):
    return src(url, "noic.com.br", "primary", coverage, confirms, needle)


def press(url, domain, needle, confirms, coverage="full"):
    return src(url, domain, "primary", coverage, confirms, needle)


SOURCES = {
 2009: [wiki("Tafarello"), olc("Tafarello")],
 2010: [wiki("Pomgeluppi"), olc("Pomgeluppi"), olc("Smaira", "olaa-2010/")],
 2011: [wiki("Bordoni"), olc("Bordoni")],
 2012: [wiki("Pedarnig"), olc("Pedarnig"),
        press("https://extra.globo.com/noticias/educacao/vida-de-calouro/estudantes-brasileiros-participam-da-olimpiada-latino-americana-de-astronomia-astronautica-5983975.html", "extra.globo.com", "Pedarnig", "Extra (OBA release): full 2012 roster with cities", "full (pre-event roster)")],
 2013: [wiki("Sontag")],
 2014: [wiki("Heringer"), noic("https://noic.com.br/uncategorized/equipe-brasileira-da-olaa-e-mais-premiada-de-todos-os-tempos/", "Hagemaister", "NOIC results post: 3G + 2S"),
        noic("https://noic.com.br/uncategorized/alunos-selecionados-para-ioaa-e-olaa/", "HAGEMAISTER", "NOIC team announcement (IOAA + OLAA)", "full (pre-event roster)"),
        press("https://g1.globo.com/educacao/noticia/2014/10/brasil-ganha-tres-medalhas-de-ouro-em-olimpiada-latina-de-astronomia.html", "g1.globo.com", "Heringer", "G1: 3G + 2S with cities")],
 2015: [wiki("Renner"), noic("https://noic.com.br/uncategorized/equipe-brasileira-da-olaa-e-a-mais-premiada-de-todos-os-tempos/", "Renner", "NOIC results post: 4G + 1S"),
        noic("https://noic.com.br/astronomia-2/divulgadas-as-equipes-brasileiras-das-internacionais-de-astronomia/", "Renner", "NOIC team announcement (Vitor Gomes Pires listed as reserve; Felipe Vieira Coimbra later replaced)", "pre-event roster"),
        press("https://revistagalileu.globo.com/Ciencia/noticia/2015/10/brasileiros-conquistam-cinco-medalhas-na-olimpiada-latino-americana-de-astronomia-e-astronautica.html", "revistagalileu.globo.com", "Schuch", "Galileu: 4G + 1S, full names (Ana Paula Lopes Schuch)")],
 2016: [wiki("Verras"), noic("https://noic.com.br/astronomia-2/divulgadas-as-equipes-das-olimpiadas-internacionais-de-astronomia/", "Thimoteo", "NOIC team announcement (Victor Praxedes Rael listed; replaced by Nicolas Almeida Verras)", "pre-event roster"),
        press("https://g1.globo.com/educacao/noticia/brasil-vence-olimpiada-latino-americana-de-astronomia-e-astronautica.ghtml", "g1.globo.com", "Verras", "G1: 2G + 2S + 1B with names")],
 2017: [wiki("Apendino"), noic("https://noic.com.br/uncategorized/divulgados-os-times-das-olimpiadas-internacionais-de-astronomia/", "Apendino", "NOIC team announcement", "full (pre-event roster)"),
        press("https://g1.globo.com/educacao/noticia/brasil-conquista-quatro-medalhas-de-ouro-em-olimpiada-de-astronomia-e-astronautica-no-chile.ghtml", "g1.globo.com", "Apendino", "G1: 4G + 1S with cities")],
 2018: [wiki("Klitzke"), noic("https://noic.com.br/astronomia-2/brasil-se-destaca-na-olaa-2018/", "Katarine", "NOIC results post: 4G + 1S"),
        noic("https://noic.com.br/uncategorized/veja-as-equipes-brasileiras-das-olimpiadas-internacionais-de-astronomia/", "Klitzke", "NOIC team announcement with schools", "full (pre-event roster)"),
        press("https://g1.globo.com/educacao/noticia/2018/10/23/brasil-conquista-quatro-ouros-e-uma-prata-em-olimpiada-latino-americana-de-astronomia.ghtml", "g1.globo.com", "Klitzke", "G1: 4G + 1S")],
 2019: [wiki("Fabrizio"), noic("https://noic.com.br/astronomia-2/brasil-conquista-4-ouros-e-1-prata-na-olaa-2019/", "Fabrizio", "NOIC results post: 4G + 1S with full names")],
 2020: [wiki("Sobreira"), noic("https://noic.com.br/uncategorized/confira-o-resultado-do-brasil-na-olaa/", "Sobreira", "NOIC results post (virtual edition): 4G + 1B"),
        press("https://www12.senado.leg.br/radio/1/noticia/2020/12/10/brasil-ganha-5-medalhas-em-olimpiada-de-astronomia-e-astronautica", "senado.leg.br", "Sobreira", "Rádio Senado: 4G + 1B with names")],
 2021: [wiki("Gregio"), press("https://agenciabrasil.ebc.com.br/educacao/noticia/2021-11/brasil-ganha-cinco-ouros-em-olimpiada-de-astronomia-e-astronautica/", "agenciabrasil.ebc.com.br", "Gregio", "Agência Brasil: five golds, names, ages, schools"),
        press("https://g1.globo.com/educacao/noticia/2021/11/16/brasil-leva-5-medalhas-de-ouro-na-olimpiada-latino-americana-de-astronomia-e-astronautica.ghtml", "g1.globo.com", "Gregio", "G1: five golds + special prizes")],
 2022: [wiki("Chalfun"), press("https://jornaldachapada.com.br/2022/10/24/mundo-selecao-brasileira-faz-bonito-na-olimpiada-latino-americana-de-astronomia-e-astronautica/", "jornaldachapada.com.br", "Chalfun", "Jornal da Chapada (OBA release): five golds, names, ages, schools")],
 2023: [wiki("Segrini"), noic("https://noic.com.br/uncategorized/resultado-da-seletiva-de-astronomia/", "Mychel", "NOIC selection result (short names)", "pre-event roster"),
        press("https://jc.ne10.uol.com.br/colunas/enem-e-educacao/2023/10/15617811-brasil-conquista-cinco-medalhas-em-olimpiada-latina-de-astronomia.html", "jc.ne10.uol.com.br", "Segrini", "JC: 2G + 3S with names")],
 2024: [wiki("Gurjão"), press("https://horacampinas.com.br/estudante-de-valinhos-e-ouro-na-olimpiada-latino-americana-de-astronomia-e-astronautica/", "horacampinas.com.br", "Gurjão", "Hora Campinas: 4G + 1B (short names)")],
 2025: [wiki("Waiandt"), press("https://agenciabrasil.ebc.com.br/educacao/noticia/2025-09/equipes-brasileiras-sao-premiadas-em-olimpiada-de-astronomia", "agenciabrasil.ebc.com.br", "Waiandt", "Agência Brasil: ten Brazilians, 9G + 1S, full names and cities")],
}

NOTES = {
 2009: "First OLAA (Rio de Janeiro). Wikipedia gives short forms (Rafael Tafarello, Catarina Neves...); OLC has the full names used here.",
 2011: "Second name of the silver medallist: OLC 'Lucas Henrique Moraes' vs Wikipedia 'Morais' - OLC form kept.",
 2013: "Wikipedia only (OBA-sourced); no press/NOIC coverage found. Two of the five are exact matches elsewhere (Rubens Martins Bezerra Farias IJSO 2012; Weslley de Vasconcelos Rodrigues da Silva OLAA 2012).",
 2015: "Hosted (Rio/Barra do Piraí). Vitor Gomes Pires (reserve in April) replaced Felipe Vieira Coimbra; 'Ana Paula Lopes Schuch' per Galileu (Wikipedia 'Shuch', NOIC 'Schuch').",
 2016: "Nicolas Almeida Verras took the place announced for Victor Praxedes Rael. Mateus Siqueira Thimóteo = the OMCPLP/Cono Sur/APMO/RMM contestant (Mogi das Cruzes, same year) - assumed identity.",
 2020: "Virtual edition (Ecuador, 16-30 Nov).",
 2021: "Hybrid edition (Peru). All five gold - first clean sweep.",
 2022: "Second clean sweep (Panama).",
 2025: "Hosted (Rio de Janeiro / Barra do Piraí): ten Brazilian contestants (host allowance), 9G + 1S. The Wikipedia TOTAL row (18 silver) is stale; per-year rows sum to 21.",
}

GLOBAL_NOTES = [
 "Editions 2009-2025 (17), Brazil in every one; hosted 2009, 2011, 2015, 2025. Teams of five (ten in 2025 as host). Every Brazilian ever entered medalled: 63 gold, 21 silver, 6 bronze.",
 "Backbone: pt.wikipedia's OBA-sourced per-year delegation lists, corroborated by NOIC (2014-2020, 2023), G1/Galileu/Agência Brasil/regional press (2012, 2014-2025) and OLC (2009-2012). The OBA site (site.oba.org.br / oba.org.br) did not resolve during collection; olaa.oba.org.br likewise.",
 "Selection: OBA level-4 top scorers sit online and in-person selection rounds; the top five go to the IOAA and the next five to the OLAA (mixed-gender rule), so many rows are exact matches in ioaa/ (see aliases notes).",
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
        "olympiadId": "olaa",
        "description": "Sources confirming Brazilian OLAA contestants + results, per edition.",
        "provenanceClasses": {
            "official": "(none reachable - OBA/OLAA sites offline during collection)",
            "primary": "pt.wikipedia OBA-sourced rosters; NOIC; press releases via G1, Agência Brasil, Galileu, Senado, regional outlets; olimpiadascientificas.org.",
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

    md = ("# Per-Year Corroboration — Brazil at the OLAA\n\n"
          "**Machine-readable:** `data/corroboration.json`. Rebuild: `python3 scripts/build_corroboration.py`; "
          "verify: `python3 scripts/verify_corroboration.py`. 2026-09-10 collection pass.\n\n## Notes\n\n"
          + "\n".join(f"- {n}" for n in GLOBAL_NOTES)
          + "\n\n## Summary\n\n| Year | Sources | Domains |\n|-----:|:--:|---------|\n" + "\n".join(lines)
          + "\n\n## Per-year sources\n\n" + "\n".join(details))
    with open(os.path.join(ROOT, "CORROBORATION.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Editions: {len(records)}")
    print("Wrote data/corroboration.json + CORROBORATION.md")


if __name__ == "__main__":
    main()
