#!/usr/bin/env python3
"""Verify every URL in data/corroboration.json: HTTP status + (where possible)
that a Brazilian name for that year actually appears in the fetched content.

Needle policy per source entry:
  - explicit "needle" field  -> that string must appear (diacritics-insensitive);
  - coverage == "full"       -> ANY surname from that year's roster (from
                                src/data/graph.json) must appear;
  - otherwise                -> status-only check (no content assertion).

PDFs are text-extracted with pypdf. Social/login-walled hosts often 403/999 —
those failures are reported but are liveness problems, not data problems.

Writes data/corroboration_check.json and prints a summary. Generic: the same
script is used in every olympiad folder (imo, icho, ioaa, ioi, ...).
"""
import io
import json
import re
import ssl
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORR = ROOT / "data" / "corroboration.json"
GRAPH = ROOT / "src" / "data" / "graph.json"
OUT = ROOT / "data" / "corroboration_check.json"

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
TIMEOUT = 25
STOPWORDS = {"da", "de", "do", "dos", "das", "e", "van", "von", "del", "la", "filho", "junior", "neto", "jr"}


def fold(s: str) -> str:
    nfd = unicodedata.normalize("NFD", s)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn").lower()


def roster_needles(graph, year):
    """Distinctive surname tokens (folded) for everyone competing that year."""
    needles = set()
    for s in graph["students"].values():
        if any(p["year"] == year for p in s["participations"]):
            toks = [t for t in fold(s["name"]).split() if t not in STOPWORDS and len(t) >= 4]
            if toks:
                needles.add(toks[-1])  # last significant token = surname-ish
    return needles


def fetch(url, _depth=0):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE  # some .gov.br/.uz chains are broken; content check matters more
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as r:
            body = r.read(8_000_000)
            return r.status, r.headers.get("Content-Type", ""), body
    except urllib.error.HTTPError as e:
        # urllib < 3.11 does not auto-follow 308
        if e.code in (301, 302, 307, 308) and e.headers.get("Location") and _depth < 3:
            return fetch(urllib.parse.urljoin(url, e.headers["Location"]), _depth + 1)
        raise


def body_text(url, ctype, body):
    if url.lower().split("?")[0].endswith(".pdf") or "pdf" in ctype.lower():
        try:
            from pypdf import PdfReader

            reader = PdfReader(io.BytesIO(body))
            return "\n".join((p.extract_text() or "") for p in reader.pages)
        except Exception:
            return ""  # unextractable PDF -> content check inconclusive
    for enc in ("utf-8", "latin-1"):
        try:
            return body.decode(enc)
        except Exception:
            continue
    return ""


def check_one(entry, needles_for_year):
    url = entry["url"]
    explicit = entry.get("needle")
    use_roster = explicit is None and entry.get("coverage") == "full"
    try:
        status, ctype, body = fetch(url)
    except Exception as e:
        return {**entry_key(entry), "status": "FAIL-HTTP", "detail": f"{type(e).__name__}: {e}"[:200]}
    if status != 200:
        return {**entry_key(entry), "status": "FAIL-HTTP", "detail": f"HTTP {status}"}
    if not explicit and not use_roster:
        return {**entry_key(entry), "status": "PASS-STATUS", "detail": "200 (no content assertion)"}
    text = re.sub(r"\s+", " ", fold(re.sub(r"<[^>]+>", " ", body_text(url, ctype, body))))
    if not text:
        return {**entry_key(entry), "status": "PASS-STATUS", "detail": "200 (content not extractable)"}
    if explicit:
        ok = fold(explicit) in text
        return {**entry_key(entry), "status": "PASS" if ok else "FAIL-NEEDLE", "detail": f"needle {explicit!r}"}
    hit = next((n for n in needles_for_year if n in text), None)
    return {
        **entry_key(entry),
        "status": "PASS" if hit else "FAIL-NEEDLE",
        "detail": f"roster surname {hit!r}" if hit else "no roster surname found",
    }


def entry_key(entry):
    return {"year": entry["_year"], "url": entry["url"], "domain": entry["domain"], "cls": entry["cls"]}


def main():
    corr = json.loads(CORR.read_text(encoding="utf-8"))
    graph = json.loads(GRAPH.read_text(encoding="utf-8"))

    jobs = []
    for yrec in corr["years"]:
        needles = roster_needles(graph, yrec["year"])
        for s in yrec["sources"]:
            jobs.append(({**s, "_year": yrec["year"]}, needles))

    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(lambda j: check_one(*j), jobs))

    tally = {}
    for r in results:
        tally[r["status"]] = tally.get(r["status"], 0) + 1

    OUT.write_text(
        json.dumps(
            {
                "checkedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "summary": tally,
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"{CORR.parent.parent.name}: {len(results)} URLs checked -> {tally}")
    for r in results:
        if r["status"].startswith("FAIL"):
            print(f"  {r['status']:12} {r['year']} {r['url'][:90]}  ({r['detail'][:80]})")


if __name__ == "__main__":
    main()
