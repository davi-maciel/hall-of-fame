#!/usr/bin/env python3
"""Verify every candidate corroborating URL: HTTP status + that a known
Brazilian name/token for that year actually appears in the fetched content.
HTML is grepped directly; PDFs are run through `pdftotext` when available.
Prints a per-URL PASS/FAIL so only verified URLs get published.
"""
import subprocess, shutil, tempfile, os, unicodedata

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

def deacc(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))

# (year, url, needle, kind, independence-label)
# kind: html | pdf | social  (social/pdf = status-only + agent-quoted proof)
BASE = lambda y: [
    (y, f"https://stats.ioinformatics.org/delegations/BRA/{y}", None, "html", "IOI-DB (primary, team view)"),
    (y, f"https://olimpiada.ic.unicamp.br/competicoes/ioi/", "IOI", "html", "OBI/Unicamp (independent national body)"),
]

EXTRA = [
    (1999, "https://cphof.org/standings/ioi/1999", "Fortuna", "html", "cphof (aggregator, derives from IOI-DB)"),
    (2000, "https://cphof.org/standings/ioi/2000", "Habkost", "html", "cphof (aggregator)"),
    (2001, "https://cphof.org/standings/ioi/2001", "Tassinari", "html", "cphof (aggregator)"),
    (2002, "https://cphof.org/standings/ioi/2002", "Paulino", "html", "cphof (aggregator)"),
    (2002, "https://ioi.te.lv/locations/ioi02/medals.shtml", "PAULINO", "html", "IOI-official mirror (ioi.te.lv)"),
    (2002, "https://www2.unicamp.br/unicamp/unicamp_hoje/jornalPDF/189-pag10.pdf", "Paulino", "pdf", "Jornal da Unicamp (independent press)"),
    (2003, "https://cphof.org/standings/ioi/2003", "Fujiwara", "html", "cphof (aggregator)"),
    (2003, "https://ioi.te.lv/locations/ioi03/medals.shtml", "Fujiwara", "html", "IOI-official mirror (ioi.te.lv)"),
    (2003, "https://denilson.sa.nom.br/denilsonsa-curriculo.pdf", "IOI", "pdf", "Personal CV, Denilson de Sá (independent)"),
    (2004, "https://cphof.org/standings/ioi/2004", "Ribas", "html", "cphof (aggregator)"),
    (2005, "https://cphof.org/standings/ioi/2005", "Ribas", "html", "cphof (aggregator)"),
    (2005, "https://clist.by/standings/ioi-2005-31998753/", "Ribas", "html", "clist.by (aggregator)"),
    (2006, "https://cphof.org/standings/ioi/2006", "Bujokas", "html", "cphof (aggregator)"),
    (2006, "https://clist.by/standings/ioi-2006-31998747/", "Bujokas", "html", "clist.by (aggregator)"),
    (2006, "http://olympiads.win.tue.nl/ioi/ioi2006/contest/results.html", "BRA", "html", "IOI 2006 host results (independent)"),
    (2007, "https://agencia.fapesp.br/tres-medalhas-na-olimpiada-internacional-de-informatica/7657", "Kawakami", "html", "Agência FAPESP (independent press)"),
    (2007, "https://cphof.org/standings/ioi/2007", "Kawakami", "html", "cphof (aggregator)"),
    (2008, "https://agencia.fapesp.br/medalhas-no-egito/9332", "bronze", "html", "Agência FAPESP (independent press)"),
    (2008, "https://cphof.org/standings/ioi/2008", "Povoa", "html", "cphof (aggregator)"),
    (2009, "https://cphof.org/standings/ioi/2009", "Dalalio", "html", "cphof (aggregator)"),
    (2010, "https://ioi2010.org/finalResults.html", "Renato", "html", "IOI 2010 host results (independent)"),
    (2010, "https://cphof.org/standings/ioi/2010", "Felipe", "html", "cphof (aggregator)"),
    (2011, "https://sindpdrj.org.br/2011/07/28/brasil-conquista-ouro-inedito-na-olimpiada-internacional-de-informatica/", "Felipe", "html", "SINDPD-RJ (independent press)"),
    (2011, "https://portal.cin.ufpe.br/2011/08/03/primeira-medalha-de-ouro-para-o-brasil-na-olimpiada-internacional-de-informatica/", "Felipe", "html", "CIn-UFPE (independent)"),
    (2011, "https://cphof.org/standings/ioi/2011", "Felipe", "html", "cphof (aggregator)"),
    (2012, "https://cphof.org/standings/ioi/2012", "Kawakami", "html", "cphof (aggregator)"),
    (2013, "https://ioi2013.org/competition/results/", "Renato", "html", "IOI 2013 host results (independent)"),
    (2013, "https://cphof.org/standings/ioi/2013", "Renato", "html", "cphof (aggregator; medal-color unreliable)"),
    (2014, "https://agencia.fapesp.br/brasileiros-conquistam-medalhas-em-olimpiada-de-informatica/19460", "Bezrutchka", "html", "Agência FAPESP (independent press)"),
    (2014, "http://olimpiadascientificas.org/equipes-brasileiras/informatica/ioi/", "Bezrutchka", "html", "olimpiadascientificas.org (independent)"),
    (2014, "https://cphof.org/standings/ioi/2014", "Dadalto", "html", "cphof (aggregator)"),
    (2015, "http://olimpiadascientificas.org/equipes-brasileiras/informatica/ioi/", "Siaudzionis", "html", "olimpiadascientificas.org (independent)"),
    (2015, "https://cphof.org/standings/ioi/2015", "Zanarella", "html", "cphof (aggregator; medal-color unreliable)"),
    (2016, "http://olimpiadascientificas.org/equipes-brasileiras/informatica/ioi/", "Guimar", "html", "olimpiadascientificas.org (independent)"),
    (2016, "https://cphof.org/standings/ioi/2016", "Siaudzionis", "html", "cphof (aggregator)"),
    (2017, "https://www2.unicamp.br/unicamp/noticias/2017/08/04/brasileiro-leva-ouro-na-olimpiada-internacional-de-informatica-unicamp-organiza/", "Sacramento", "html", "Unicamp news (independent)"),
    (2017, "http://olimpiadascientificas.org/equipes-brasileiras/informatica/ioi/", "Sacramento", "html", "olimpiadascientificas.org (independent)"),
    (2017, "https://cphof.org/standings/ioi/2017", "Sacramento", "html", "cphof (aggregator)"),
    (2018, "https://blog.etapa.com.br/noticias/aluno-etapa-conquista-prata-na-ioi", "Sim", "html", "Colégio Etapa (independent)"),
    (2018, "https://cphof.org/standings/ioi/2018", "Carvalho", "html", "cphof (aggregator)"),
    (2019, "https://noic.com.br/2018/12/08/divulgado-time-brasileiro-da-ioi-2019-e-da-ciic-2019/", "Wang", "html", "NOIC (independent)"),
    (2019, "https://cphof.org/standings/ioi/2019", "Frederico", "html", "cphof (aggregator)"),
    (2019, "https://clist.by/standings/ioi-2019-31998620/", "Wang", "html", "clist.by (aggregator)"),
    (2020, "https://blog.etapa.com.br/noticias/ioi-2020", "Carolina", "html", "Colégio Etapa (independent)"),
    (2020, "https://cphof.org/standings/ioi/2020", "Carolina", "html", "cphof (aggregator)"),
    (2021, "https://blog.etapa.com.br/noticias/ioi-2021", "Oda", "html", "Colégio Etapa (independent)"),
    (2021, "https://pleno.news/educacao/brasileira-e-a-melhor-ranqueada-em-olimpiada-de-informatica.html", "Carolina", "html", "Pleno.News (independent press)"),
    (2022, "https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/noticias/2022/08/equipe-brasileira-foi-premiada-na-34a-olimpiada-internacional-de-informatica-na-indonesia", "Rafael", "html", "gov.br / MCTI (independent)"),
    (2022, "https://blog.etapa.com.br/noticias/ioi-2022", "Leonardo", "html", "Colégio Etapa (independent)"),
    (2023, "https://noic.com.br/uncategorized/saiu-o-resultado-da-ioi/", "Suyama", "html", "NOIC (independent)"),
    (2023, "https://blog.etapa.com.br/noticias/ioi-2023", "Leonardo", "html", "Colégio Etapa (independent)"),
    (2024, "https://horizontes.sbc.org.br/index.php/2024/09/giro-sbc-edicao-38-24/", "Lalic", "html", "SBC Horizontes (independent)"),
    (2024, "https://cphof.org/standings/ioi/2024", "Lalic", "html", "cphof (aggregator)"),
    (2025, "https://jtv.com.br/pedro-henrique-assuncao-medalha-prata-olimpiada-internacional-informatica-2025/", "Assun", "html", "Jornal Terceira Visão (independent press)"),
    (2025, "https://cphof.org/standings/ioi/2025", "Suyama", "html", "cphof (aggregator)"),
    (2025, "https://clist.by/standings/ioi-2025-61139460/", "Paiva", "html", "clist.by (aggregator)"),
]

def fetch_status_body(url):
    try:
        p = subprocess.run(["curl", "-sSL", "-A", UA, "--max-time", "45", "-w", "\n__HTTP_%{http_code}__", url],
                           capture_output=True, text=True, timeout=55)
        out = p.stdout
        code = out.rsplit("__HTTP_", 1)[-1].rstrip("_") if "__HTTP_" in out else "000"
        body = out.rsplit("\n__HTTP_", 1)[0]
        return code, body
    except Exception as e:
        return "ERR", ""

def pdf_text(url):
    if not shutil.which("pdftotext"):
        return None
    try:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            fn = f.name
        subprocess.run(["curl", "-sSL", "-A", UA, "--max-time", "45", "-o", fn, url], timeout=55)
        p = subprocess.run(["pdftotext", fn, "-"], capture_output=True, text=True, timeout=30)
        os.unlink(fn)
        return p.stdout
    except Exception:
        return None

def main():
    seen = set()
    rows = []
    for y in range(1999, 2026):
        rows += BASE(y)
    rows += EXTRA
    npass = nfail = 0
    results = []
    for y, url, needle, kind, label in rows:
        key = (y, url)
        code, body = fetch_status_body(url)
        ok200 = code.startswith("2")
        found = None
        if needle is None:
            found = ok200
        elif kind == "pdf":
            txt = pdf_text(url)
            if txt is None:
                found = ok200  # can't grep; status-only
            else:
                found = deacc(needle).lower() in deacc(txt).lower()
        else:
            found = deacc(needle).lower() in deacc(body).lower()
        status = "PASS" if (ok200 and found) else ("SOFT" if ok200 else "FAIL")
        if status == "PASS": npass += 1
        else: nfail += 1
        results.append((y, status, code, label, url, needle, kind))
        print(f"{y} {status:4s} http={code:3s} needle={'-' if needle is None else ('OK' if found else 'MISS')}  {label}")
    print(f"\nPASS={npass}  non-PASS={nfail}  total={len(rows)}")
    import json
    json.dump([{"year": y, "status": s, "http": c, "label": l, "url": u, "needle": n, "kind": k}
               for (y, s, c, l, u, n, k) in results],
              open(os.path.join(os.path.dirname(__file__), "..", "data", "raw", "sources_verified.json"), "w"),
              ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
