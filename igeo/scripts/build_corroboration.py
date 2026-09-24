#!/usr/bin/env python3
"""
Corroboration for Brazil at the iGeo (repo-standard). 2026-09-10 collection pass, 2026-09-16 roster/team-size pass,
2026-09-17 debut (2016) pass, 2026-09-18 attendance pass. Editions attended: 2016, 2018, 2019, 2022-2026 (8). Rosters are partial: the official
iGeo results list gold medallists only, so Brazilian names come from OBG (national organizer) posts, schools and
press. No usable names for 2019 and 2023.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = "https://geoolympiad.org/wp-content/uploads/2025/04/"


def src(url, domain, cls, coverage, confirms, needle=None, timing="post", names=None):
    # names: person ids (site/data/people.json slugs) this source names although its text
    # cannot be fetched or parsed (Instagram/Facebook post, image) - curator attestation,
    # read by site/scripts/check_source_names.py as level "attested".
    d = {"url": url, "domain": domain, "cls": cls, "coverage": coverage, "confirms": confirms,
         "timing": timing}
    if needle:
        d["needle"] = needle
    if names:
        d["names"] = list(names)
    return d


def official(year, fname=None, confirms="iGeo official results: gold medallists and team rankings only (no Brazilian entry)", needle=None, timing="post"):
    url = RES + (fname or f"{year}-iGeo-Results.pdf")
    return src(url, "geoolympiad.org", "official", "gold medallists + team ranking", confirms, needle, timing)


def press(url, domain, needle, confirms, coverage="full", timing="post", names=None):
    return src(url, domain, "primary", coverage, confirms, needle, timing, names)


SOURCES = {
 2016: [official(2016),
        press("https://web.archive.org/web/20251109131732/https://www.unifal-mg.edu.br/comunicacao/universidadeparticipadeolimpiadainternacionaldegeografia", "unifal-mg.edu.br (Wayback)", "Ana Byatriz Santos", "UNIFAL-MG press office, 2016-09-01 (the team leader's own university): 'A equipe do Brasil foi formada pelo professor ... Clibson Alves dos Santos, pelo professor Roberto Greco da ... Unicamp e por três alunos do ensino médio ... sendo eles: Ana Byatriz Santos, Gabriella Abreu e José Carlos Castro da Silva (Escola Estadual Ensino Profissional Salaberga Torquato Gomes de Matos, Maranguape - Ceará)' - the only source with surnames; also 'primeira vez que uma equipe brasileira participa', no medals", "full (3 of 3) + team size (3)"),
        press("https://web.archive.org/web/20160904154252/http://www.crede01.seduc.ce.gov.br/index.php/listanoticias/noticias-anteriores/3082-alunos-da-escola-profissional-salaberga-torquato-conquistam-vaga-na-olimpiada-internacional-de-geografia-em-pequim", "crede01.seduc.ce.gov.br (Wayback)", "Gabriella Vital", "CREDE 01 / SEDUC-CE, 2016-08-18: 'Os alunos José Carlos, Ana Byatriz e Gabriella Vital, da Escola Estadual de Educação Profissional (EEEP) Salaberga Torquato, localizada em Maranguape, estão em Pequim' and 'Os participantes são os únicos estudantes brasileiros na Olimpíada' - team size, given names only", "3 students (given names) + team size (3)", timing="event"),
        press("https://salaberga.com/salaberga/portalsalaberga/app/main/", "salaberga.com", "Gabriella Vital", "EEEP Salaberga Torquato Gomes de Matos (Ceará) school portal: 'Nossos estudantes José Carlos, Ana Byatriz e Gabriella Vital representaram o Brasil na 13ª Olimpíada Internacional de Geografia em Pequim, China' - first names only", "3 students, first names only"),
        press("https://www.unifal-mg.edu.br/geografia/historico-de-noticias/", "unifal-mg.edu.br", "Clibson Alves dos Santos foi um dos representantes do Brasil", "UNIFAL-MG Geography course news archive (live): 'O Prof. Dr. Clibson Alves dos Santos foi um dos representantes do Brasil na 13ª Olimpíada Internacional de Geografia, que ocorreu entre os dias 16 e 22 de agosto de 2016, em Pequim na China' plus the link to the full press-office item - no student names", "event + team leader (no names)")],
 2018: [official(2018), press("https://www.facebook.com/colegionucleo/photos/temos-mais-um-aluno-n%C3%BAcleo-provando-seu-conhecimento-para-o-mundo-marina-hutzler/1763515040405071", "facebook.com", None, "Colégio Núcleo (Recife) Facebook, 2018-07-19, PRE-EVENT: 'Marina Hutzler conquistou o 1º lugar do Brasil na iGEO (Olimpíada Internacional de Geografia) e vai representar o país na próxima etapa, dessa vez no Canadá. Ela embarca no próximo dia 29' - read in the browser 2026-09-18 (the post is a login shell to plain fetches)", "one student (pre-event)", timing="pre"),
        press("http://www.cmp.eb.mil.br/index.php/cmp-noticias/344-alunos-do-cmb-sao-destaques-em-olimpiada-de-geografia", "cmp.eb.mil.br", None, "Comando Militar do Planalto (2018-06-05, host now refuses connections; text via search index): Lucas Caetano Filippo and Guilherme Lomba Shittine (Colégio Militar de Brasília, 3rd year) selected for the four-student team representing Brazil at the iGeo in Quebec - the only team-size statement found for 2018", "2 students + team size (4)", timing="pre"),
        press("https://www.calameo.com/books/005823758ff8f3195c5f2", "calameo.com", None, "Jornal O Garanca no. 2 (Colegio Militar de Brasilia internal newsletter, Aug 2018), p. 3 'Alunos do CMB sao destaque em Olimpiada Brasileira de Geografia': Lucas Caetano Filippo and Guilherme Lomba, both 3o A/EM, 'foram selecionados para compor a equipe de quatro estudantes que representara o Brasil na Olimpiada Internacional de Geografia, a ser realizada em Quebec - Canada'; OBG 2017 gold medallists who sat the English-language international selection in 2018 - read in the Calameo viewer 2026-09-17 (pre-event wording; the text is not exposed to plain fetches)", "2 students + team size (4), pre-event", timing="pre")],
 2019: [official(2019)],
 2022: [official(2022), press("https://www.facebook.com/obgeografia/videos/616207526523982", "facebook.com", "Lauren", "OBG video post (caption read in the browser 2026-09-19: 'Os estudantes, Lucas Lang, Lauren Schuantes, Manuela Teixeira e Karen Gomes representaram o time brasileiro na edicao de 2022'): Lucas Lang, Lauren Schuantes, Manuela Teixeira and Karen Gomes represented Brazil at the online iGeo 2022 (Paris)", "full", "post", ["lucas-lang", "lauren-schuantes", "manuela-teixeira", "karen-gomes"])],
 2023: [official(2023, confirms="iGeo 2023 official results: 45 teams / 177 students; gold medallists and team rankings only, but Brazil appears under 'Favourite poster selected by students' - positive proof a Brazilian team competed", needle="Tunisia, Brazil"),
        press("https://portal.ige.unicamp.br/news/2022-12/unicamp-recebe-final-da-olimpiada-geobrasil", "portal.ige.unicamp.br", "quatro estudantes", "Unicamp IG (co-organizer of the national final): the English test would be one of the marks used 'para a seleção de quatro estudantes que vão formar a equipe brasileira na 19ª Olimpíada Internacional de Geografia' in Bandung 2023 - team size, no names", "team size (4), pre-event", timing="pre")],
 2024: [official(2024), press("https://tribunaonline.com.br/atribunanasescolas/feras-da-geografia-se-destacam-na-irlanda-198302", "tribunaonline.com.br", "Azurza", "A Tribuna (ES): Pablo Fernando de Azurza Nogueira e Gómez Alvarez bronze (first Brazilian/South American iGeo medal, short form 'Nogueira Gomez'), Gabriel Volpato Lima on the team; two more (CE, BH) unnamed", "2 of 4"),
        press("https://noic.com.br/uncategorized/entrevista-com-pablo-primeiro-brasileiro-medalhista-na-igeo/", "noic.com.br", "primeiro brasileiro medalhista", "NOIC interview with the 2024 bronze medallist ('Pablo Alvarez')", "one student"),
        press("https://facepevirtual.org.br/facepe/equipe-brasileira-conquista-medalha-de-bronze-na-olimpiada-internacional-de-geografia-na-irlanda/", "facepevirtual.org.br", "Valentina Vale Farias Cruz", "FACEPE/UNIFAL-MG (the OBG's support foundation): 'A equipe brasileira foi composta pelos estudantes Gabriel Volpato Lima, Pablo Fernando de Azurza Nogueira e Gómez Alvarez, Davi de Magalhães Vianna Navarro e Valentina Vale Farias Cruz' - full team of four plus team leaders", "full (4 of 4) + team size")],
 2025: [src("https://geoolympiad.org/wp-content/uploads/2025/10/2025-iGeo-Results-and-Report.pdf", "geoolympiad.org", "official", "gold medallists + team ranking", "iGeo 2025 official results and report: gold medallists and team rankings only", None), press("https://www.instagram.com/p/DLYyq35MAsg/", "instagram.com", None, "OBG (national organizer) Instagram: the four selected for iGeo 2025 - Isabela Granado Santos, João Lucas Dantas Barbosa, Bárbara Pinheiro Puget Cruz, Clara Gonzalez Ferreira Pinto Sampaio", "full (pre-event roster)", timing="pre"),
        press("https://regionalnorte.com.br/estudantes-paraenses-sao-selecionadas-para-olimpiada-internacional-de-geografia-na-tailandia", "regionalnorte.com.br", "Granado", "Regional Norte: Isabela Granado and Bárbara Puget (Colégio Santa Rosa, Belém) selected; team of four from N/NE", "2 of 4 (pre-event)", timing="pre"),
        press("https://www.instagram.com/p/DM0VacVsMYU/", "instagram.com", None, "Colegio Santa Rosa (Belem) Instagram, 2025-08-01, POST-EVENT (caption pasted by the maintainer 2026-09-22, confirms bronze): 'Nossa aluna Isabela Granado conquistou a medalha de bronze na categoria individual da Olimpíada Internacional de Geografia 2025 (iGEO), realizada em Bangkok, na Tailândia' - the school's own confirmation that she travelled and competed, and the first direct corroboration of the 2025 bronze (read in the browser 2026-09-18; captions are not exposed to plain fetches)", "one student: attendance + medal (post-event)", "post", ["isabela-granado-santos"]),
        press("https://www.instagram.com/p/DM1GXAqPBIk/", "instagram.com", None, "Movimento Meninas Olimpicas, 2025-08-01, POST-EVENT (caption pasted by the maintainer 2026-09-19): 'O Brasil conquistou uma medalha de bronze na Olimpíada Internacional de Geografia (iGeo)!!! A equipe brasileira contou com uma maioria feminina, Bárbara Pinheiro e Clara Sampaio compuseram a equipe juntamente com a medalhista Isabela Granado. A competição foi realizada em Bangkok, Tailândia' - three of the four named as having made up the team that competed (read in the browser 2026-09-18; the same post is mirrored at facebook.com/meninas.olimpicas/posts/1153176893501793, whose permalink 400s to plain fetches)", "3 of 4: attendance (post-event)", "post", ["barbara-pinheiro-puget-cruz", "clara-gonzalez-ferreira-pinto-sampaio", "isabela-granado-santos"]),
        press("https://noic.com.br/quem-somos/", "noic.com.br", "Seleção Brasileira de Geografia a disputar a iGeo 2025 em Bangkok", "NOIC staff page - João Lucas Dantas Barbosa is now NOIC's Geography coordinator and his biography, written after the event, says he became 'parte da Seleção Brasileira de Geografia a disputar a iGeo 2025 em Bangkok, na Tailândia'; the only post-event statement found for the fourth 2025 member", "one student: attendance (post-event bio)"),
        press("https://noic.com.br/materiais-geografia/guia-de-estudos/igeo/", "noic.com.br", "Equipe Brasil na Cerimônia de Encerramento da iGeo Bangkok 2025", "NOIC iGeo study guide, bylined 'Por Pablo Fernando Nogueira e João Lucas Dantas Barbosa' (the 2024 medallist and a 2025 team member), illustrated with Bangkok 2025 photographs captioned 'Equipe Brasil na Cerimônia de Encerramento da iGeo Bangkok 2025', 'Realização do WRT na iGeo Bangkok 2025', 'Apresentação do pôster da Equipe Brasil na iGeo 2025' and 'Isabela Granado, segunda medalhista da história do Brasil na iGeo'", "event + medal (post-event)")],
 2026: [press("https://www.instagram.com/p/DcLny4cjo-R/", "instagram.com", None, "Colégio Militar de Fortaleza Instagram, 2026-08-18, POST-EVENT: Tiago Sales bronze at iGeo 2026 (Istanbul, 10-17 Aug), Brazil's only 2026 medal and third ever; the same post states 'a equipe brasileira representada por quatro alunos', the only post-event team-size statement for 2026 (caption pasted by the maintainer 2026-09-19: 'a equipe brasileira representada por quatro alunos, entre os quais o Aluno Tiago Sales ... que conquistou a medalha de bronze na competicao individual')", "one student + medal + team size (4)", "post", ["tiago-sales"]),
        press("https://www.instagram.com/p/DcEdsF_EbMH/", "instagram.com", None, "OBG Instagram, 2026-08-15: 'A equipe brasileira já está na Turquia e participou da cerimônia de abertura da Olimpíada Internacional de Geografia nesta segunda-feira dia 10/08' - event-day proof that a Brazilian team was in Istanbul, but the caption names nobody (re-read in the browser 2026-09-18)", "event, no names", timing="event"),
        press("https://wscom.com.br/noticias/noticias-locais/2026/03/05/estudante-paraibana-representa-o-brasil-na-olimpiada-internacional-de-geografia-em-istambul/", "wscom.com.br", "Bianca Ribas", "WSCOM: Bianca Ribas (Colégio Motiva, João Pessoa) selected for iGeo 2026", "one student (pre-event)", timing="pre"),
        press("https://agoralaguna.com.br/2026/04/theodora-flor-estudante-de-laguna-representara-estado-em-olimpiada-de-geografia-na-turquia/", "agoralaguna.com.br", "Theodora", "Agora Laguna: Theodora Flor (Laguna-SC) selected for iGeo 2026", "one student (pre-event)", timing="pre"),
        press("https://www.instagram.com/p/Db-9ogylVuf/", "instagram.com", None, "Colégio Motiva João Pessoa Instagram, 2026-08-13 (EVENT DAY, the olympiad ran 10-17 Aug): 'Nossa aluna Bianca Ribas está representando o Brasil na International Geography Olympiad (iGeo), em Istambul, na Turquia, ao lado dos melhores estudantes de Geografia do planeta!' and 'Até a próxima segunda-feira, dia 17, os participantes encaram provas escritas, trabalhos de campo e desafios'; also 'a seleção brasileira, formada por apenas quatro estudantes' (read in the browser 2026-09-18; mirrored on the school's Facebook page)", "one student: attendance (event-day) + team size (4)", timing="event", names=["bianca-ribas"]),
        press("https://www.sulinfoco.com.br/estudante-de-laguna-representa-o-brasil-na-olimpiada-internacional-de-geografia-na-turquia/", "sulinfoco.com.br", "Theodora Flor já está em Istambul", "Sul in Foco (SC), 2026-08-11 (EVENT DAY): 'A estudante lagunense Theodora Flor já está em Istambul, na Turquia, onde representa o Brasil na Olimpíada Internacional de Geografia (iGeo) 2026. A competição segue até a próxima segunda-feira (17)'; the same item adds 'A equipe do país também conta com representantes de Brasília, Fortaleza e Paraíba', which places the still-unnamed fourth member in Brasília", "one student: attendance (event-day) + 4th member's city", timing="event")],
}

NOTES = {
 2016: "Beijing (debut, 16-22 Aug), roster resolved 2026-09-17. The three students all came from one school, EEEP Salaberga Torquato Gomes de Matos (Maranguape-CE), and were selected through the 2nd OBG 2016 (35,917 students / 1,184 schools); the team leaders were Clibson Alves dos Santos (UNIFAL-MG) and Roberto Greco (Unicamp), and CNPq paid for the trip. TEAM SIZE 3, not 4, stated twice: UNIFAL-MG's press office ('por três alunos do ensino médio', against a cap the same item gives as 'uma equipe de até 4 alunos e 2 professores') and CREDE 01 / SEDUC-CE ('Os participantes são os únicos estudantes brasileiros na Olimpíada'). No medals ('apesar dos alunos não terem conquistado medalhas'). TRAP 1: surnames exist in exactly one source - UNIFAL-MG - and its live URL (unifal-mg.edu.br/comunicacao/universidadeparticipadeolimpiadainternacionaldegeografia) now returns HTTP 500 from a Drupal/MySQL disk error, so the Wayback capture is cited; the live UNIFAL-MG Geography news archive is kept as the pointer to it. TRAP 2: the third student's surname is UNRESOLVED - UNIFAL-MG writes 'Gabriella Abreu' while CREDE-01 and the school both write 'Gabriella Vital'; the record uses the UNIFAL-MG form because that item is the one that gives surnames for the whole team, and the two forms were NOT merged. TRAP 3: CREDE-01's archived page is entity-encoded (&uacute; etc.), so only accent-free needles verify against it. TRAP 4: the old OBG site obgeografia.org is alive (HTTP 200, not 410 - that is the later unifal-mg.edu.br/obgeografia address) but its 2015/2016/2017 edition pages carry no international roster.",
 2018: "Quebec City. Marina Hutzler (Colégio Núcleo) plus Lucas Caetano Filippo and Guilherme Lomba Shittine (Colégio Militar de Brasília), from the Comando Militar do Planalto item of 2018-06-05; that item also states the team had four students, which is the team-size evidence for 2018. TRAP: every Brazilian-Army copy of that item is unreachable - cmp.eb.mil.br resets the connection, depa.eb.mil.br/noticias/227-... returns 403 and eb.mil.br/.../content/id/8928063 is a 404 with no Wayback capture; the text is only readable through the search index. VERIFIED 2026-09-17 in the Calameo viewer: the CMB newsletter O Garanca no. 2 (Aug 2018, p. 3) prints the same story - both names and 'equipe de quatro estudantes' - so the two CMB names no longer rest on a snippet alone, though both CMB sources are pre-event selection announcements (no post-event source confirms they travelled). Fourth member unknown. ATTENDANCE STILL UNCONFIRMED for all three after the 2026-09-18 pass - every 2018 source is a selection/send-off announcement, including Colégio Núcleo's, which is dated 2018-07-19 and says Marina Hutzler 'vai representar o país ... Ela embarca no próximo dia 29': the rest of the CMB's own Calaméo archive was read page by page (O Garança 3rd and 4th editions and the 124-page Revista CMB 2018, all posted Feb 2019, plus the July 2019 issue) and none of them mentions Quebec, the iGeo or any olympiad of geography - issue 2's pre-event note is the only CMB print mention of the trip; the Wayback Machine was offline that day, so the unreachable Army copies could not be retried from an archive. Incidental: the Revista CMB 2018 roll of pupils spells the second student 'Guilherme Schittine Bezerra Lomba' (Sch-, against the record's 'Shittine').",
 2019: "Hong Kong. Nothing beyond the official results (gold medallists + team rankings, 43 teams / 166 students, no Brazilian entry): no Brazilian name and no team-size statement was found - OBG's old site (unifal-mg.edu.br/obgeografia) now returns HTTP 410, the host site's participant booklets do not list delegations, and no Brazilian press item on the 2019 team surfaced.",
 2022: "Online edition (Paris). Four short-form names from OBG's video post.",
 2023: "Bandung. Still no names. Two things were settled: Brazil definitely competed (the official results name Brazil among the 'favourite poster' winners) and the team was four students (Unicamp IG, co-organizer of the national final, on the selection that followed the December 2022 final).",
 2024: "Dublin/Maynooth. First Brazilian iGeo medal (bronze, Pablo Fernando de Azurza Nogueira e Gómez Alvarez - A Tribuna's 'Pablo Fernando de Azurza Nogueira Gomez' and NOIC's 'Pablo Alvarez' are short forms). Roster completed 2026-09-16 from FACEPE/UNIFAL-MG, which names the full team of four and so also settles the team size: the two members A Tribuna left unnamed are Davi de Magalhães Vianna Navarro (Colégio Militar de Belo Horizonte) and Valentina Vale Farias Cruz (Colégio Militar de Fortaleza); Gabriel Volpato Lima and Pablo are from Colégio FAESA (Vitória).",
 2025: "Bangkok. Roster first recorded from the OBG selection announcement; ATTENDANCE CONFIRMED for all four on 2026-09-18, each from a source published after the competition ended: Isabela Granado from her school's own post (Colégio Santa Rosa, 01/08), Bárbara Pinheiro Puget Cruz and Clara Gonzalez Ferreira Pinto Sampaio from Movimento Meninas Olímpicas (01/08, 'compuseram a equipe'), and João Lucas Dantas Barbosa from his NOIC staff biography ('a disputar a iGeo 2025 em Bangkok') plus the NOIC iGeo guide he co-wrote, which is illustrated with Bangkok 2025 closing-ceremony, exam and poster photographs. Isabela Granado Santos's bronze (second Brazilian medal) no longer rests on the 2026-08 DATA_STATUS verification alone - the school post states it outright. TRAP: the Meninas Olímpicas post mis-types the dates as '26 de junho e 1 de agosto'; every other source puts the edition in late July-1 August 2025. The @igeo.brazil Instagram account that the 2025 team set up (cited in the NOIC guide) has since been removed.",
 2026: "Istanbul (10-17 Aug 2026). Tiago Sales (Colégio Militar de Fortaleza) bronze - Brazil's third medal. ATTENDANCE CONFIRMED 2026-09-18 for the other two named members from items published while the olympiad was running: Bianca Ribas 'está representando o Brasil ... em Istambul' (her school, 13/08) and Theodora Flor 'já está em Istambul' (Sul in Foco, 11/08). Team size 4 is now stated post-event by the Colégio Militar de Fortaleza. The fourth member is STILL UNNAMED, but Sul in Foco places the delegation's home cities as Laguna, Brasília, Fortaleza and Paraíba - so the missing student is from Brasília, and no press or school item naming a Brasília student surfaced. OBG's Instagram documents the trip without ever naming anyone: 08/08 'O Brasil já está a caminho da Turquia', 15/08 opening ceremony, 21/08 wrap-up 'Chegamos ao fim da iGeo 2026'. TRAPS: geoolympiad.org has published no 2026 results document (its results library still stops at 2025); FACEPE still has no 2026 article; and Agora Laguna ran the same 11/08 'está em Istambul' story but sits behind a Cloudflare challenge that 403s plain fetches, so Sul in Foco is cited instead.",
}

GLOBAL_NOTES = [
 "Editions attended: 2016, 2018, 2019, 2022-2026 (8; 2017 skipped, 2020 cancelled, 2021 online edition not entered). Brazilian medals: bronze 2024, 2025, 2026.",
 "COVERAGE IS PARTIAL: iGeo's official results list only gold medallists, so Brazilian rosters depend on OBG (Olimpíada Brasileira de Geografia) posts, schools and press. 2019 and 2023 have no usable names; 2018 has 3 of 4 and 2026 3 of 4; 2016 (3 of 3), 2022, 2024 and 2025 are complete. OBG's old site (unifal-mg.edu.br/obgeografia) returns HTTP 410 and its Instagram is only partly indexed (anonymous visitors see the three newest posts).",
 "TEAM SIZE: up to four students per country is the iGeo rule (OBG's own page: 'equipes de quatro alunos e dois mentores'), but that is a cap, not evidence for a given year - the 2016 debut team was three. Edition-specific statements were found for 2016 (UNIFAL-MG and CREDE-01/SEDUC-CE, three students), 2018 (Comando Militar do Planalto), 2023 (Unicamp IG), 2024 (FACEPE names all four) and 2026 (Colégio Militar de Fortaleza, post-event, and Colégio Motiva); 2022 and 2025 rest on the OBG rosters already recorded. 2019 remains unverified.",
 "Selection via the OBG national final (UNIFAL-MG, later Unicamp): a written round, a paper and simulated tests in English; travel depends on funding, so a year's team can be smaller than the rule allows.",
 "ATTENDANCE (2026-09-18 pass): because most Brazilian names come from selection announcements, every named student was re-checked against evidence published during or after the competition. Confirmed: all four for 2025 and, for 2026, Bianca Ribas and Theodora Flor (Tiago Sales was already confirmed by his medal). Still pre-event only: all three named 2018 students (Marina Hutzler, Lucas Caetano Filippo and Guilherme Lomba Shittine) - no source places any of them in Quebec City. 2016, 2022, 2023 and 2024 rest on items written after their editions.",
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
        "olympiadId": "igeo",
        "description": "Sources confirming Brazilian iGeo contestants + results, per edition (partial coverage).",
        "provenanceClasses": {
            "official": "geoolympiad.org results PDFs (gold medallists + team rankings).",
            "primary": "OBG Instagram/Facebook posts; school and press news; NOIC.",
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
    md = ("# Per-Year Corroboration — Brazil at the iGeo\n\n"
          "**Machine-readable:** `data/corroboration.json`. Rebuild: `python3 scripts/build_corroboration.py`; "
          "verify: `python3 scripts/verify_corroboration.py`. 2026-09-10 collection pass; 2026-09-16 roster/team-size pass; 2026-09-17 debut (2016) pass; 2026-09-18 attendance pass.\n\n## Notes\n\n"
          + "\n".join(f"- {n}" for n in GLOBAL_NOTES)
          + "\n\n## Summary\n\n| Year | Sources | Domains |\n|-----:|:--:|---------|\n" + "\n".join(lines)
          + "\n\n## Per-year sources\n\n" + "\n".join(details))
    with open(os.path.join(ROOT, "CORROBORATION.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Editions: {len(records)}")


if __name__ == "__main__":
    main()
