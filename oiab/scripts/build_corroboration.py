#!/usr/bin/env python3
"""
Corroboration for Brazil at the OIAB (repo-standard). 2026-09-09 collection pass: every URL fetched and
content-verified. Editions: 2007-2019, 2021-2026 (19; 2020 cancelled by the pandemic).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OEB = "http://olimpiadadebiologia.edu.es/wp-content/uploads/"
OLC = "https://olimpiadascientificas.org/equipes-brasileiras/biologia/ibero/"
WB = "https://web.archive.org/web/"
SEL = "/https://olimpiadasbiologiasistema.butantan.gov.br/ResultadoSeletivaInternacional"


def src(url, domain, cls, coverage, confirms, needle=None):
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms}
    if needle:
        d["needle"] = needle
    return d


def official(url, needle=None, confirms="official results sheet (oiab.org archive): names, scores and medals", coverage="full", domain=None):
    dom = domain or ("oiab.org" if "oiab.org" in url else "olimpiadadebiologia.edu.es")
    return src(url, dom, "official", coverage, confirms, needle)


def olc(needle, coverage="full"):
    return src(OLC, "olimpiadascientificas.org", "primary", coverage, "olimpiadascientificas.org roster 2007-2017 (sources: OBB site, OIAB 2014 site)", needle)


def noic(url, needle, confirms, coverage="full"):
    return src(url, "noic.com.br", "primary", coverage, confirms, needle)


def press(url, domain, needle, confirms, coverage="full"):
    return src(url, domain, "primary", coverage, confirms, needle)


def obb(ts, needle, year):
    return src(WB + ts + SEL, "web.archive.org", "archive", "full (pre-event roster)",
               f"OBB 'Resultado definitivo da Seletiva Internacional' {year} (archived copy; live host gone): IBO + OIAB teams with school and city", needle)


SOURCES = {
 2007: [official(OEB + "2014/09/ResultadosOIAB-2007.pdf", "BRASIL", "official final table (ranks + scores; no medal column - medals from OLC/NOIC)"), olc("Negreiros Bessa"),
        src("https://noic.com.br/olimpiadas/biologia/oiab/", "noic.com.br", "primary", "medal counts only", "NOIC OIAB page: 2007 debut = 1st place with 1G 1S 2B", "1 medalha de ouro")],
 2008: [official(OEB + "2014/09/ResultadosOIAB-2008.pdf", "Camelo Filho"), olc("Camelo Filho")],
 2009: [official(OEB + "2014/09/ResultadosOIAB-2009.pdf", None, "official score sheet (scanned image; read visually): 3 Brazilians, S+2B"), olc("Nunes Benevides"),
        src("https://servicos.aridesa.com.br/grandesconquistas/img/2018/07/olimp_ibero_americana_bio.jpg", "aridesa.com.br", "primary", "one student", "Ari de Sá poster: Rafael Lima Viana on the 2009 team (image)")],
 2010: [official(OEB + "2014/09/ResultadosOIAB-2010.pdf", "REGIS DE FREITAS"), olc("Regis de Freitas")],
 2011: [official(OEB + "2014/09/ResultadosOIAB-2011.pdf", None, "official medal list (scanned image; read visually): 2 Brazilian bronzes; unawarded contestants not listed"), olc("Cayke")],
 2012: [official(OEB + "2014/09/ResultadosOIAB-2012.pdf", None, "official final results (scanned image; read visually): 2G + 2S"), olc("Antunes Filho"),
        press("https://oglobo.globo.com/brasil/educacao/estudantes-brasileiros-conquistam-ouro-na-olimpiada-ibero-americana-de-biologia-6072977", "oglobo.globo.com", "Ivan Tadeu", "O Globo: 2G (Antônio Pedro, Leonardo Costa) + 2S (Jéssica Lopes, Ivan Tadeu)", "first names + medals")],
 2013: [official(OEB + "2014/09/ResultadosOIAB-2013.pdf", None, "official final results (scanned image; read visually): 4 bronzes"), olc("Diniz Macedo"),
        press("https://agencia.fapesp.br/brasileiros-ganham-quatro-medalhas-em-olimpiada-ibero-americana-de-biologia/17873", "agencia.fapesp.br", "Diniz Macedo", "Agência FAPESP: four bronzes, full names + cities")],
 2014: [official(OEB + "2014/09/ResultadosOIAB-2014.pdf", "Voltani"), olc("Voltani"),
        noic("https://noic.com.br/biologia/brasil-ganha-4-medalhas-na-oiab/", "Voltani", "NOIC results post"),
        noic("https://noic.com.br/biologia/divulgadas-equipes-brasileiras-da-ibo-e-oiab/", "Voltani", "NOIC team announcement", "full (pre-event roster)"),
        press("https://agencia.fapesp.br/brasil-conquista-quatro-medalhas-em-olimpiada-de-biologia/19856", "agencia.fapesp.br", "Leticia Pereira de Souza", "Agência FAPESP: 1G 2S 1B")],
 2015: [official(OEB + "2016/08/ResultadosOIAB-2015.pdf", "NATSUBORI", "official report + medal table: Brazil 3 silvers (Feitosa Viana, Natsubori Sato, Nogueira Filho) + 1 bronze"), olc("Natsubori"),
        noic("https://noic.com.br/biologia/brasil-conquista-medalhas-de-prata-e-bronze-na-olimpiada-iberoamericana-de-biologia-oiab/", "Gerardo Albino", "NOIC results post (lists Sato as bronze - overruled by the official table)"),
        noic("https://noic.com.br/biologia/divulgada-a-equipe-brasileira-da-ibo-e-da-oiab-2015/", "Natsubori", "NOIC team announcement", "full (pre-event roster)"),
        press("https://jornaldachapada.com.br/2015/09/03/brasil-busca-o-ouro-na-olimpiada-ibero-americana-de-biologia-em-el-salvador/", "jornaldachapada.com.br", "Natsubori", "pre-event roster with schools", "full (pre-event roster)")],
 2016: [official(OEB + "2016/09/resultados_oiab_2016_brasilia.jpg", None, "official ranking (photo of the results sheet; read visually): G + 2S + B", "image (full ranking)"), olc("Adamian"),
        noic("https://noic.com.br/uncategorized/divulgadas-as-equipes-brasileiras-nas-internacionais-de-biologia/", "Adamian", "NOIC team announcement", "full (pre-event roster)"),
        press("https://revistagalileu.globo.com/Ciencia/noticia/2016/09/brasileiros-ganham-4-medalhas-na-olimpiada-ibero-americana-de-biologia.html", "revistagalileu.globo.com", "Teixeira Gomes", "Galileu: 1G 2S 1B with names")],
 2017: [official("http://www.oiab.org/clasificacion_XI_oiab_2017_azores.pdf", "Helmich"), olc("Helmich"),
        noic("https://noic.com.br/biologia/divulgados-os-representantes-do-brasil-nas-internacionais-de-biologia/", "Helmich", "NOIC team announcement (lists Olavo Borges Franco, later replaced by João Victor Almeida Oliveira Santos)", "pre-event roster")],
 2018: [official("http://www.oiab.org/ganadoresxiioiab.PDF", None, "official winners list (scanned image; read visually): 4 silvers"),
        noic("https://noic.com.br/biologia/brasil-conquista-4-pratas-na-oiab/", "Jaziel", "NOIC results post"),
        src("https://servicos.aridesa.com.br/grandesconquistas/img/2019/09/IBERO-BIOLOGIA-BIG.jpg", "aridesa.com.br", "primary", "one student", "Ari de Sá poster: João Pedro de Souza Bezerra silver (image)")],
 2019: [official("http://www.oiab.org/MEDALLERO%20XIII%20OIAB%202019%20Bolivia.pdf", "Haofu"),
        official("http://www.oiab.org/MEMORIA_OIAB_2019_Bolivia.pdf", "Haofu", "official memoir: same medal table"),
        noic("https://noic.com.br/biologia/4-medalhas-para-o-brasil-na-ibero-americana-de-biologia/", "Haofu", "NOIC results post: 2S + 2B")],
 2021: [official("http://www.oiab.org/medallero_oiab_2021_costa_rica.pdf", "Amano Tanaka"),
        official("http://www.oiab.org/memoria_oiab_2021.pdf", "Sonntag", "official memoir: participants + medals"),
        obb("20210723210710", "AMANO TANAKA", 2021)],
 2022: [obb("20220705114103", "BRENO TAQUES", 2022),
        press("https://massanews.com/noticia/noticias/educacao/estudante-de-curitiba-conquista-medalha-de-bronze-em-olimpiada-internacional/", "massanews.com", "Breno Taques Mussi Endres", "Prefeitura de Curitiba release (mirror): Breno Taques Mussi Endres bronze at the XV OIAB (Peru, virtual)", "one student"),
        press("https://bosquemananciais.org.br/index.php?area=ver_noticia&id=1234", "bosquemananciais.org.br", "Breno", "school news: Breno selected for the XV OIAB", "one student"),
        press("https://poti.ufpr.br/alunos-premiados-2022/", "poti.ufpr.br", "Breno Taques", "UFPR POTI 2022 awards list: Breno bronze", "one student")],
 2023: [official("http://www.oiab.org//Entrega_de_Premios_OIAB_2023_v2.pdf", "Nakata", "official award ceremony deck: ranks + medals"),
        official("http://www.oiab.org/Lista_de_olimpicos_participantes_OIAB_2023.pdf", "Albuquerque Damasceno", "official participants list"),
        obb("20231201053656", "ALBUQUERQUE DAMASCENO", 2023)],
 2024: [official("http://www.oiab.org/descargas/TABLA_FINAL_OIAB_2024_CUBA.pdf", "Arthur Kui", "official final table: scores + medal bands"),
        official("http://www.oiab.org/descargas/MEMORIA_OIAB_2024_CUBA.pdf", "Perry Resende", "official memoir: medal lists"),
        obb("20240721061254", "PERRY RESENDE", 2024),
        press("https://onorte.net/educacao/aluno-conquista-medalha-de-ouro-na-olimpiada-ibero-americana-de-biologia-1.1030862", "onorte.net", "Perry Resende", "O Norte (Butantan release): 2G + 2S with names")],
 2025: [official("http://www.oiab.org/Medallero_OIAB_2025.pdf", "Montenegro Campos", "official medal table (ranked; medal bands as colours)"),
        press("https://primiciadiario.com/archivo/2025/jovenes-docentes-iberoamericanos-se-reunen-quindio-colombiano-olimpiada-biologia/", "primiciadiario.com", "Montenegro", "Primicia (organizer-published article): full medal lists"),
        press("https://super.abril.com.br/ciencia/quatro-estudantes-brasileiros-sao-medalhistas-na-18a-olimpiada-iberoamericana-de-biologia/", "super.abril.com.br", "Ulisses", "Superinteressante: 3G (Top Gold) + 1S with schools"),
        press("https://abcdoabc.com.br/olimpiada-iberoamericana-de-biologia-4-medalhas-br/", "abcdoabc.com.br", "Ulisses", "Portal ABC do ABC (Butantan release)"),
        press("https://aridesa.com.br/wp-content/uploads/2025/11/ASA-0062-25-AN-VOLTA-OIAB-2025-OP-5colx40cm-V3.pdf", "aridesa.com.br", "Ulisses", "Ari de Sá poster: Francisco Ulisses silver", "one student")],
 2026: [press("https://educacao.uol.com.br/noticias/2026/09/05/historico-brasil-ganha-4-ouros-na-olimpiada-ibero-americana-de-biologia.ghtm", "educacao.uol.com.br", "Heronville", "UOL Educação (host/organizer Butantan release): four golds with names and schools"),
        press("https://www.cnnbrasil.com.br/ciencia/brasil-conquista-quatro-medalhas-de-ouro-na-19a-olimpiada-ibero-americana/", "cnnbrasil.com.br", "Heronville", "CNN Brasil: four golds"),
        press("https://www.cnnbrasil.com.br/ciencia/brasil-e-representado-por-quatro-estudantes-na-19a-olimpiada-ibero-americana/", "cnnbrasil.com.br", "Daltro", "CNN Brasil: team at the opening (roster)", "full (pre-event roster)"),
        press("https://espacodopovo.com.br/delegacao-brasileira-tem-desempenho-historico-na-19a-edicao-da-olimpiada-ibero-americana-de-biologia/", "espacodopovo.com.br", "Heronville", "Espaço do Povo: four golds"),
        press("https://www.abcdoabc.com.br/br4-ouros-olimpiada-ibero-americana-de-biologia/", "abcdoabc.com.br", "Heronville", "Portal ABC do ABC: four golds")],
}

NOTES = {
 2007: "Debut in Mexico City: 1st place overall. Official table has no medal column; 1G 1S 2B per OLC and NOIC. Full name 'Anderson Carlos Vasconcelos Brasil' from the official surname columns.",
 2009: "Three contestants (official codes 05-07; OLC agrees). An Ari de Sá poster printed before the event says 'one of four representatives' - a fourth never appears in the results.",
 2010: "Three contestants (official and OLC).",
 2011: "Official sheet lists medallists only: two bronzes. Cayke Felipe dos Anjos and Gabriel Drumond Ferreira (no award) rest on OLC alone.",
 2012: "Gold winner spelled 'Antonio Pedro de Sousa VIEIRA' on the official sheet vs 'Sousa Oliveira' on OLC; kept the official form (a FAPESP researcher record 'Antonio Pedro de Sousa Vieira', molecular biology, corroborates it). O Globo names him only as 'Antônio Pedro, do Ceará'.",
 2013: "Official sheet writes 'Rodrigues de Almeida, Enrique' - the Argentine typist hispanicized Lucas Henrique Rodrigues de Almeida (Barbacena-MG per FAPESP).",
 2015: "Medal conflict: the official report counts three Brazilian silvers and names Michael Natsubori Sato in the silver block; NOIC and OLC list him as bronze. Official wins.",
 2016: "Hosted in Brasília. Spelling 'Bernardo Gabriele Collaço' (official + NOIC) over OLC's 'Habriele Collação'.",
 2017: "Team announced by NOIC included Olavo Borges Franco (ES); the official results show João Victor Almeida Oliveira Santos (BA) in his place. Lucca Helmich = Top Gold (1st overall).",
 2018: "All four silver (official scan, NOIC).",
 2021: "Remote edition (Costa Rica). 'Bruna da Motta Sonntag' follows the OBB registration list; the OIAB sheet writes 'da Mota'.",
 2022: "Remote edition (Peru). No official results file on oiab.org and the organizer's (Butantan) news pages are offline under the 2026 electoral blackout. Team from the OBB selection list; only Breno Taques Mussi Endres's bronze is documented (Curitiba city hall, school, UFPR). Wikipedia's cumulative medal table implies 1G+2S for the other three - unknown assignment, medals left null with medalStatus.",
 2023: "Best result to date then: 3G (Vitarelli 3rd, Andrade de Almeida 2nd, Nakata de Carvalho 4th) + 1S.",
 2024: "Official table has medal bands (6 gold, 10 silver, 14 bronze); memoir lists the same names.",
 2025: "Paulo Vinícius Rodrigues de Azevedo = Top Gold (1st overall). Official medallero shows bands as colours; Primicia's article carries the explicit lists.",
 2026: "Hosted by Instituto Butantan (São Paulo, 30 Aug-5 Sep 2026): all four gold, best result ever. Names come from the host's press release as relayed by UOL/CNN/others; oiab.org has not yet posted the medallero (re-check).",
}

GLOBAL_NOTES = [
 "Editions: 2007-2019, 2021-2026 (19). 2020 cancelled (pandemic). Brazil competed in every edition and hosted 2008 (Rio), 2016 (Brasília) and 2026 (São Paulo). Teams of four except 2009 and 2010 (three).",
 "Backbone: the official results files collected on oiab.org's archive page (http://www.oiab.org/archivos.htm; 2007-2016 files are hosted by the Spanish OEB). Five of them (2009, 2011, 2012, 2013, 2018) and the 2016 photo are images - transcribed visually. 2022 has no official file.",
 "Brazilian side: OLC roster page (2007-2017), NOIC posts (2014-2019), the OBB's own 'Seletiva Internacional' lists (archived 2021-2024; the live host no longer resolves), FAPESP/press. The organizer's news site (butantan.gov.br) is offline under the São Paulo electoral blackout until after the 2026 state election.",
 "Awards: gold/silver/bronze + Mención de Honor (honorable-mention; none for Brazil so far). null = confirmed no award (2011) or unknown (2022, flagged with medalStatus).",
 "Names: OBB/NOIC full Brazilian forms preferred over the hispanicized official spellings; 18 students also appear in ibo/ijso/ioaa/ipho/math datasets (exact-name merges, see aliases notes).",
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
        "olympiadId": "oiab",
        "description": "Sources confirming Brazilian OIAB contestants + results, per edition.",
        "provenanceClasses": {
            "official": "oiab.org archive / OEB-hosted official results files and memoirs.",
            "primary": "olimpiadascientificas.org roster; NOIC; FAPESP and press; school posters.",
            "archive": "Wayback Machine copies of the OBB 'Seletiva Internacional' results page.",
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

    md = ("# Per-Year Corroboration — Brazil at the OIAB\n\n"
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
