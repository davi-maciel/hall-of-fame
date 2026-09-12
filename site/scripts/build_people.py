#!/usr/bin/env python3
"""
Site-level entity resolution: merge every per-olympiad graph.json into one
canonical data/people.json (one entry per person, all participations).

Key rules:
- People are re-slugged from their DISPLAY NAME with a single unified slugifier
  (diacritics stripped, apostrophes dropped, kebab-case) — per-folder id quirks
  (e.g. imo's d-emidio) therefore cannot split identities.
- scripts/aliases.json merges known cross-dataset spelling variants and can
  override display names.
- When merged variants disagree on display name, the "richest" wins:
  most tokens, then most diacritics, then longest (same heuristic as icho's
  extractor). Every multi-variant merge is printed for human review.
- medal null is disambiguated into medalNote where known:
    * ijso: medalStatus from ijso/data/raw/ijso.json (unknown / inferred / ...)
    * oibf 2026: "pending" (roster announced, event not yet held)
    * everywhere else: null medal = confirmed no-award (confirmed below the award cut).

Run:  python3 site/scripts/build_people.py   (from repo root or anywhere)
"""
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
ROOT = SITE.parent
OUT = SITE / "data" / "people.json"

DATASETS = ["imo", "icho", "ioi", "ioaa", "ipho", "eupho", "oibf", "nbpho", "ijso", "oii", "egoi", "imcho", "oiaq", "apmo", "egmo", "oim", "conosur", "omcplp", "rioplatense", "rmm", "pagmo", "igo", "ibo", "oiab", "iao", "olaa", "iypt", "iol", "ieso", "igeo", "wopho", "ieo"]


def strip_diacritics(s: str) -> str:
    nfd = unicodedata.normalize("NFD", s)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn")


def slugify(name: str) -> str:
    base = strip_diacritics(name).lower()
    base = base.replace("'", "").replace("’", "")
    base = base.replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "-", base).strip("-")


def search_key(name: str) -> str:
    return re.sub(r"\s+", " ", strip_diacritics(name).lower()).strip()


def name_richness(name: str):
    nfd = unicodedata.normalize("NFD", name)
    marks = sum(1 for c in nfd if unicodedata.category(c) == "Mn")
    uppers = sum(1 for c in name if c.isupper())
    # more tokens > more diacritics > longer > FEWER capitals (prefers lowercase
    # particles: "dos Santos" over "Dos Santos")
    return (len(name.split()), marks, len(name), -uppers)


def load_medal_notes():
    """(slug, olympiad, year) -> medalNote for the known non-standard nulls."""
    notes = {}
    for ds in DATASETS:
        raw = ROOT / ds / "data" / "raw" / f"{ds}.json"
        if not raw.exists():
            continue
        for r in json.loads(raw.read_text(encoding="utf-8")):
            st = r.get("medalStatus")
            if not st:
                continue
            if st.startswith("unknown") or st == "medalist-color-unknown":  # any unknown-*
                note = "unknown"
            elif st.startswith("no-award-inferred"):
                note = "inferred-no-award"
            else:
                note = st
            notes[(slugify(r["rawName"]), ds, r["year"])] = note
    return notes


def main():
    aliases = json.loads((SITE / "scripts" / "aliases.json").read_text(encoding="utf-8"))
    slug_aliases = aliases.get("slugAliases", {})
    preferred = aliases.get("preferredNames", {})
    hide_variants = set(aliases.get("hideVariants", []))
    medal_notes = load_medal_notes()

    people = {}  # slug -> {names: set, participations: []}
    dataset_meta = {}

    for ds in DATASETS:
        gpath = ROOT / ds / "src" / "data" / "graph.json"
        g = json.loads(gpath.read_text(encoding="utf-8"))
        dataset_meta[ds] = {
            "students": g["metadata"]["studentCount"],
            "generatedAt": g["metadata"]["generatedAt"],
        }
        for s in g["students"].values():
            slug = slugify(s["name"])
            slug = slug_aliases.get(slug, slug)
            p = people.setdefault(slug, {"names": set(), "participations": [], "datasets": set()})
            p["names"].add(s["name"])
            p["datasets"].add(ds)
            for part in s["participations"]:
                entry = {
                    "olympiad": part["olympiad"],
                    "year": part["year"],
                    "medal": part["medal"],
                }
                note = medal_notes.get((slug, part["olympiad"], part["year"]))
                if part["medal"] is None:
                    if note:
                        entry["medalNote"] = note
                    elif part["olympiad"] == "oibf" and part["year"] == 2026:
                        entry["medalNote"] = "pending"
                    else:
                        entry["medalNote"] = "no-award"
                p["participations"].append(entry)

    out_people = []
    multi_variant = []
    cross_dataset = 0
    for slug, p in people.items():
        variants = sorted(p["names"])
        if len(variants) > 1:
            multi_variant.append((slug, variants))
        name = preferred.get(slug) or max(variants, key=name_richness)
        parts = sorted(p["participations"], key=lambda x: (x["year"], x["olympiad"]))
        # duplicate (olympiad, year) pairs would signal a bad merge — check
        seen = set()
        for x in parts:
            key = (x["olympiad"], x["year"])
            if key in seen:
                print(f"WARNING: duplicate participation {key} for {slug}", file=sys.stderr)
            seen.add(key)
        if len(p["datasets"]) > 1:
            cross_dataset += 1
        out_people.append({
            "id": slug,
            "name": name,
            "searchKey": search_key(name),
            "nameVariants": variants if len(variants) > 1 and slug not in hide_variants else [],
            "datasets": sorted(p["datasets"]),
            "participations": parts,
        })

    out_people.sort(key=lambda x: x["searchKey"])
    total_parts = sum(len(x["participations"]) for x in out_people)

    payload = {
        "meta": {
            "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "peopleCount": len(out_people),
            "participationCount": total_parts,
            "datasets": dataset_meta,
        },
        "people": out_people,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

    print(f"people: {len(out_people)}   participations: {total_parts}")
    print(f"cross-dataset people (in >1 olympiad dataset): {cross_dataset}")
    print(f"multi-variant name merges to review: {len(multi_variant)}")
    for slug, variants in multi_variant:
        print(f"  {slug}: {variants}")

    # identity gate: fail loudly if unresolved duplicate candidates exist
    import subprocess
    gate = subprocess.run([sys.executable, str(SITE / "scripts" / "find_duplicates.py")],
                          capture_output=True, text=True)
    if gate.returncode != 0:
        print("\n" + "=" * 60)
        print("IDENTITY GATE FAILED — unresolved duplicate candidates:")
        print(gate.stdout)
        print("Resolve each into aliases.json or distinct.json, then rebuild.")
        sys.exit(1)
    print("identity gate: clean (no unresolved duplicate candidates)")


if __name__ == "__main__":
    main()
