"""Merge the 20k concept plan (plan20k/<domain>.json) into drawing batches.

Drops concepts whose name is invalid, reserved for CSS, shaped like a generated badge variant, already used by
an existing icon name or alias, or a duplicate of another planned concept (compared without hyphens and with a
trailing plural "s" removed). Writes plan20k/batches/<category>_NNN.json (BATCH concepts each) and prints a
summary.

Usage: .venv/bin/python tools/core-authoring/plan20k_merge.py [--batch 80]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from check import NAME_RE, RESERVED_CLASS_NAMES  # noqa: E402
from modifiers import MODIFIERS  # noqa: E402

PLAN = HERE / "plan20k"
BATCHES = PLAN / "batches"
STYLE_WORDS = re.compile(r"-(alt|outline|outlined|filled|solid|line|rounded|\d+)$")


def key(name: str) -> str:
    k = name.replace("-", "")
    return k[:-1] if k.endswith("s") and len(k) > 4 else k


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=80)
    ap.add_argument("--append", action="store_true",
                    help="keep existing batch files (designers may be using them); add batches only for new concepts")
    args = ap.parse_args()
    core = json.loads((HERE.parents[1] / "assets/core/core-icons.json").read_text())["icons"]
    taken = {m["name"] for m in core} | {a for m in core for a in m["aliases"]}
    taken_keys = {key(n) for n in taken}
    badge_suffixes = tuple(f"-{s}" for s in MODIFIERS)

    kept: dict[str, dict] = {}
    seen_keys: set[str] = set()
    batched: dict[str, int] = defaultdict(int)  # category -> highest existing batch number
    if args.append:
        for bf in BATCHES.glob("*.json"):
            for c in json.loads(bf.read_text()):
                seen_keys.add(key(c["name"]))
            cat_id, num = bf.stem.rsplit("_", 1)
            batched[cat_id] = max(batched[cat_id], int(num))
    dropped = defaultdict(int)
    per_domain = {}
    for f in sorted(PLAN.glob("*.json")):
        try:
            items = json.loads(f.read_text())
        except json.JSONDecodeError:
            print(f"skip {f.name}: invalid JSON")
            continue
        n0 = len(kept)
        for it in items:
            name = str(it.get("name", "")).strip().lower()
            cat = str(it.get("category", "")).strip()
            draw = str(it.get("draw", "")).strip().replace("—", ", ").replace("–", "-")
            if not NAME_RE.match(name) or not cat or not draw:
                dropped["invalid"] += 1
            elif name in RESERVED_CLASS_NAMES:
                dropped["reserved css name"] += 1
            elif name.endswith(badge_suffixes) or STYLE_WORDS.search(name):
                dropped["badge or style suffix"] += 1
            elif name in taken or key(name) in taken_keys:
                dropped["already in library"] += 1
            elif key(name) in seen_keys:
                dropped["duplicate across domains"] += 1
            else:
                seen_keys.add(key(name))
                kept[name] = {"name": name, "category": cat, "draw": draw, "domain": f.stem}
        per_domain[f.stem] = len(kept) - n0

    BATCHES.mkdir(parents=True, exist_ok=True)
    if not args.append:
        for old in BATCHES.glob("*.json"):
            old.unlink()
    by_cat = defaultdict(list)
    for c in kept.values():
        by_cat[c["category"]].append(c)
    n_batches = 0
    for cat, items in sorted(by_cat.items()):
        for i in range(0, len(items), args.batch):
            n_batches += 1
            cid = cat.replace("-", "_")
            bid = f"{cid}_{batched[cid] + i // args.batch + 1:03d}"  # also the sets/<bid>.py module name
            (BATCHES / f"{bid}.json").write_text(json.dumps(items[i:i + args.batch], indent=1) + "\n")
    print(json.dumps({"kept": len(kept), "dropped": dict(dropped), "batches": n_batches,
                      "categories": {c: len(v) for c, v in sorted(by_cat.items())}}, indent=1))


if __name__ == "__main__":
    main()
