#!/usr/bin/env python3
"""
Extract Brazilian IMO competitor records from the official imo-official.org
individual-results page (saved at data/raw/bra_individual.html) into the flat
record array data/raw/imo.json.

Source: https://www.imo-official.org/results/individual/country/BRA/
This is the authoritative IMO results database. One record per (person, year).

This step is kept separate from build_graph.py so the raw extraction is
traceable and re-runnable. It is deterministic and idempotent.
"""
import re
import html as ihtml
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC_HTML = os.path.join(ROOT, "data", "raw", "bra_individual.html")
OUT_JSON = os.path.join(ROOT, "data", "raw", "imo.json")

# imo-official award CSS modifier -> our medal enum
AWARD_MAP = {
    "gold": "gold",
    "silver": "silver",
    "bronze": "bronze",
    "hm": "honorable-mention",
}


def main():
    raw = open(SRC_HTML, encoding="utf-8", errors="replace").read()
    tbody = raw[raw.find("<tbody>"):raw.find("</tbody>")]
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", tbody, re.S)

    records = []
    for r in rows:
        ym = re.search(r"/results/team/year/(\d{4})/country/BRA/", r)
        if not ym:
            continue
        year = int(ym.group(1))

        # Two name markups exist on the page:
        #  - normal:   <span data-person-name data-name="..." data-surname="...">
        #  - "anomaly" (1979 team): <span data-results-anomaly-name data-name="..." data-surname="...">
        nm = re.search(r'data-name="([^"]*)"\s+data-surname="([^"]*)"', r)
        given = ihtml.unescape(nm.group(1)).strip() if nm else ""
        surname = ihtml.unescape(nm.group(2)).strip() if nm else ""
        # A literal "?" given name means the source does not record it (1979 "Sebastião").
        if given == "?":
            given = ""
        raw_name = (given + " " + surname).strip()

        # Rank: normal rows put it in the section-start cell; anomaly rows use data-rank-value.
        rk = re.search(r'data-table__section-start"[^>]*>(\d+)</td>', r)
        if not rk:
            rk = re.search(r'data-rank-value="(\d+)"', r)
        rank = int(rk.group(1)) if rk else None

        aw = re.search(r"data-table__award-circle--(\w+)", r)
        medal = AWARD_MAP.get(aw.group(1)) if aw else None

        rec = {
            "rawName": raw_name,
            "olympiadId": "imo",
            "year": year,
            "medal": medal,
        }
        if rank is not None:
            rec["rank"] = rank
        records.append(rec)

    # Deterministic order: by year ascending, then rank ascending, then name.
    records.sort(key=lambda x: (x["year"], x.get("rank", 10**9), x["rawName"]))

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Wrote {len(records)} records to {OUT_JSON}")


if __name__ == "__main__":
    main()
