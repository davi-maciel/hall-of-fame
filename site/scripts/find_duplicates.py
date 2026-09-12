#!/usr/bin/env python3
"""
Identity-split detector: flags pairs of people in site/data/people.json that are
plausibly the SAME person under a different name spelling.

Detection classes (per surname block):
  SUBSET    significant tokens of A ⊆ tokens of B            (high confidence)
  INITIAL   A has an initial that expands to a token of B,
            all other tokens compatible                       (high confidence)
  SUFFIX    identical except a Filho/Neto/Júnior/Sobrinho
            suffix present on one side                        (medium)
  FIRSTLAST first and last tokens match, middles conflict     (low — often distinct)
  FUZZY     first tokens match, surnames within edit
            distance 2 (typo class)                           (medium)

Hard negative: two people who share a (olympiad, year) team are DISTINCT.
Suppression: pairs already merged via aliases.json, or listed in distinct.json.

Output: candidates sorted by confidence, with each side's participations as
evidence. Resolve every candidate into aliases.json (merge) or distinct.json
(keep separate), then re-run until silent. build_people.py runs this in report
mode on every build.
"""
import itertools
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
# A school-olympiad career can't span more than ~10 years (Maio at ~11 to a final
# IMO at ~19 is the extreme). Pairs whose combined career would exceed this are
# not candidates.
MAX_CAREER_SPAN = 10
STOP = {"de", "da", "do", "dos", "das", "e"}
SUFFIX = {"filho", "neto", "junior", "jr", "sobrinho", "segundo"}


def fold(s):
    nfd = unicodedata.normalize("NFD", s)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn").lower()


def tokens(name):
    return [t for t in re.sub(r"[^a-z\s]", " ", fold(name)).split() if t not in STOP]


def edit_distance(a, b):
    if abs(len(a) - len(b)) > 2:
        return 3
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[-1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def compatible(ta, tb):
    """Every token of the shorter name matches the longer: exact, or initial-expansion."""
    if len(ta) > len(tb):
        ta, tb = tb, ta
    used = [False] * len(tb)
    initials = 0
    for t in ta:
        hit = None
        for j, u in enumerate(tb):
            if used[j]:
                continue
            if t == u or (len(t) == 1 and u.startswith(t)) or (len(u) == 1 and t.startswith(u)):
                hit = j
                if t != u:
                    pass
                break
        if hit is None:
            return None
        if t != tb[hit] and (len(t) == 1 or len(tb[hit]) == 1):
            initials += 1
        used[hit] = True
    return "INITIAL" if initials else "SUBSET"


def classify(a, b):
    ta, tb = tokens(a["name"]), tokens(b["name"])
    if not ta or not tb:
        return None
    if ta == tb:
        # Same significant tokens, different slug (only stopwords like 'de' differ):
        # build_people keys on the full name, so these never auto-merge.
        return "SUBSET"
    # SUFFIX: identical after dropping a trailing suffix token from one side
    sa = ta[:-1] if ta and ta[-1] in SUFFIX else ta
    sb = tb[:-1] if tb and tb[-1] in SUFFIX else tb
    if sa == sb and ta != tb:
        return "SUFFIX"
    if len(ta) != len(tb):
        c = compatible(ta, tb)
        if c:
            return c
    if ta[0] == tb[0] and ta[-1] == tb[-1] and len(ta) == len(tb):
        return "FIRSTLAST"
    if ta[0] == tb[0] and ta[-1] != tb[-1] and edit_distance(ta[-1], tb[-1]) <= 2:
        return "FUZZY"
    return None


CONFIDENCE = {"SUBSET": 3, "INITIAL": 3, "SUFFIX": 2, "FUZZY": 2, "FIRSTLAST": 1}


def surname_keys(p):
    """Block on EVERY significant token (+ 4-char prefix of the last, for FUZZY).
    Blocking only on the last token misses short-form names whose trailing
    surnames were truncated (e.g. 'Carolina Moura' vs 'Carolina Moura Valle
    Costa' — different last tokens, same person)."""
    ts = tokens(p["name"])
    if not ts:
        return []
    last = ts[-1] if ts[-1] not in SUFFIX or len(ts) == 1 else ts[-2]
    return list(set(ts + [last[:4]]))


def main():
    data = json.loads((SITE / "data" / "people.json").read_text(encoding="utf-8"))
    aliases = json.loads((SITE / "scripts" / "aliases.json").read_text(encoding="utf-8"))
    distinct = json.loads((SITE / "scripts" / "distinct.json").read_text(encoding="utf-8"))
    suppressed = {tuple(sorted(p[:2])) for p in distinct.get("pairs", [])}
    people = data["people"]

    blocks = defaultdict(list)
    for p in people:
        for k in set(surname_keys(p)):
            blocks[k].append(p)

    seen = set()
    cands = []
    for block in blocks.values():
        for a, b in itertools.combinations(block, 2):
            key = tuple(sorted((a["id"], b["id"])))
            if key in seen or key in suppressed:
                continue
            seen.add(key)
            cls = classify(a, b)
            if not cls:
                continue
            # hard negative: same-team co-occurrence
            ta = {(x["olympiad"], x["year"]) for x in a["participations"]}
            tb = {(x["olympiad"], x["year"]) for x in b["participations"]}
            if ta & tb:
                continue
            # implausible combined career span
            ys = [y for _, y in ta | tb]
            if max(ys) - min(ys) > MAX_CAREER_SPAN:
                continue
            cands.append((CONFIDENCE[cls], cls, a, b))

    cands.sort(key=lambda c: (-c[0], c[2]["id"]))
    hi = sum(1 for c in cands if c[0] >= 2)
    print(f"{len(cands)} candidate pair(s) — {hi} medium/high confidence, {len(cands)-hi} low\n")
    for conf, cls, a, b in cands:
        def desc(p):
            parts = " · ".join(f"{x['year']} {x['olympiad']} {x['medal'] or '-'}" for x in p["participations"])
            return f"{p['name']}  [{parts}]"
        print(f"[{cls}] {desc(a)}\n{' ' * (len(cls) + 3)}{desc(b)}")
        print(f"  -> merge:    add to aliases.json  \"{b['id']}\": \"{a['id']}\"  (or reverse)")
        print(f"  -> distinct: add to distinct.json [\"{min(a['id'],b['id'])}\", \"{max(a['id'],b['id'])}\", \"<reason>\"]\n")
    return 0 if not cands else 1


if __name__ == "__main__":
    sys.exit(main())
