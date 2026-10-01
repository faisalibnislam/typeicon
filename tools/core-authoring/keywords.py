"""Search context and keywords for Core icons.

Data lives in tools/core-authoring/keywords/<category>.json:

    {
      "<icon-name>": {
        "context": "One to three plain sentences: what the drawing shows and where people use it.",
        "keywords": ["lowercase search terms", "synonyms", "use cases", ...]
      }
    }

export.py merges this into core-icons.json: keywords extend the tags, context is stored for search and
the icon page. Variants (file-plus) get the base's context and keywords combined with the badge's meaning.

Usage:
  .venv/bin/python tools/core-authoring/keywords.py dump CATEGORY [CATEGORY ...]   # icons to describe
  .venv/bin/python tools/core-authoring/keywords.py validate [CATEGORY ...]        # check keyword files
  .venv/bin/python tools/core-authoring/keywords.py lookup TERM [TERM ...]         # is a concept already covered?
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DIR = HERE / "keywords"

KEYWORD_RE = re.compile(r"^[a-z0-9][a-z0-9 '&+./-]{0,38}[a-z0-9+#.]$|^[a-z0-9]$")
MIN_KEYWORDS, MAX_KEYWORDS = 12, 40
EM_DASH, EN_DASH = chr(0x2014), chr(0x2013)
BANNED_IN_CONTEXT = [
    EM_DASH, EN_DASH, "vibrant", "seamless", "showcas", "highlighting", "underscor", "testament", "boasts",
    "a wide range", "diverse array", "it is important", "it's important", "delve", "robust", "pivotal",
    "serves as", "stands as", "not just", "not only",
]


def base_icons() -> list[dict]:
    doc = json.loads((ROOT / "assets/core/core-icons.json").read_text())
    return [m for m in doc["icons"] if m.get("dir", "svg") == "svg"]


def load(category: str) -> dict:
    p = DIR / f"{category}.json"
    return json.loads(p.read_text()) if p.exists() else {}


def load_all() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in sorted(DIR.glob("*.json")):
        out.update(json.loads(p.read_text()))
    return out


def lookup(terms: list[str]) -> None:
    """Which existing Core icons already cover a concept (by name, alias, tag, keyword or context)."""
    kw = load_all()
    planned = [c for bf in sorted((HERE / "plan20k" / "batches").glob("*.json")) for c in json.loads(bf.read_text())]
    for term in terms:
        t = term.lower().replace("-", " ")
        hits = []
        for m in base_icons():
            e = kw.get(m["name"], {})
            fields = {"name": [m["name"].replace("-", " ")], "alias": [a.replace("-", " ") for a in m["aliases"]],
                      "tag": m["tags"], "keyword": e.get("keywords", []), "context": [e.get("context", "").lower()]}
            where = [f for f, vals in fields.items() if any(t == v or (f == "context" and t in v) or
                                                            (f != "context" and t in v.split()) for v in vals)]
            if where:
                hits.append(f"{m['name']} ({', '.join(where)})")
        for c in planned:  # concepts planned for the 20k programme but maybe not drawn yet
            if t == c["name"].replace("-", " ") or t in c["name"].replace("-", " ").split() or t in c["draw"].lower():
                hits.append(f"{c['name']} (planned)")
        print(f"{term}: " + ("; ".join(hits[:12]) if hits else "not covered"))


def dump(categories: list[str]) -> None:
    for m in base_icons():
        if m["category"] in categories:
            df = m.get("derivedFrom")
            print(json.dumps({
                "name": m["name"], "category": m["category"], "description": m["description"],
                "tags": m["tags"], "aliases": m["aliases"],
                **({"derivedFrom": df} if df else {}),
            }, ensure_ascii=False))


def validate(categories: list[str] | None) -> int:
    icons = {m["name"]: m for m in base_icons()}
    problems = []
    files = ([f for c in categories for f in sorted(DIR.glob(f"{c}.json")) + sorted(DIR.glob(f"{c}__*.json"))]
             if categories else sorted(DIR.glob("*.json")))
    covered = set()
    for p in files:
        if not p.exists():
            problems.append(f"{p.name}: missing")
            continue
        try:
            data = json.loads(p.read_text())
        except json.JSONDecodeError as e:
            problems.append(f"{p.name}: invalid JSON: {e}")
            continue
        cat = p.stem.split("__")[0]  # keywords/<category>.json or keywords/<category>__<batch>.json
        for name, entry in data.items():
            covered.add(name)
            m = icons.get(name)
            if not m:
                problems.append(f"{name}: not a Core base icon")
                continue
            if m["category"] != cat:
                problems.append(f"{name}: belongs in keywords/{m['category']}.json, not {p.name}")
            ctx, kws = entry.get("context", ""), entry.get("keywords", [])
            if not (40 <= len(ctx) <= 400):
                problems.append(f"{name}: context should be 40-400 characters (has {len(ctx)})")
            low = ctx.lower()
            for b in BANNED_IN_CONTEXT:
                if b in low:
                    problems.append(f"{name}: context uses {b!r}")
            if not (MIN_KEYWORDS <= len(kws) <= MAX_KEYWORDS):
                problems.append(f"{name}: {len(kws)} keywords (want {MIN_KEYWORDS}-{MAX_KEYWORDS})")
            if len(set(kws)) != len(kws):
                problems.append(f"{name}: duplicate keywords")
            for k in kws:
                if not KEYWORD_RE.match(k):
                    problems.append(f"{name}: bad keyword {k!r} (lowercase letters, digits, spaces, - ' & + . / #)")
                if EM_DASH in k or EN_DASH in k:
                    problems.append(f"{name}: dash character in keyword {k!r}")
    wanted = {n for n, m in icons.items() if categories is None or m["category"] in categories}
    for n in sorted(wanted - covered):
        problems.append(f"{n}: no entry yet")
    for pr in problems[:200]:
        print("FAIL ", pr)
    print(f"{len(wanted & covered)}/{len(wanted)} icons described; {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__" and not (len(sys.argv) > 1 and sys.argv[1] in ("dump-brands", "validate-brands")):
    if len(sys.argv) > 1 and sys.argv[1] == "lookup":
        lookup(sys.argv[2:])
        sys.exit(0)
    if len(sys.argv) < 2 or sys.argv[1] not in ("dump", "validate"):
        print(__doc__)
        sys.exit(2)
    if sys.argv[1] == "dump":
        dump(sys.argv[2:])
    else:
        sys.exit(validate(sys.argv[2:] or None))


# --------------------------------------------------------------------------- brand logos (Simple Icons)
# assets/sources/brand-keywords/shard-N.json, keyed by Simple Icons slug: {"context": ..., "keywords": [...]}
BRAND_DIR = ROOT / "assets/sources/brand-keywords"
BRAND_SHARDS = 8


def brand_list() -> list[dict]:
    rows = [json.loads(line) for line in (ROOT / "build/catalog/designs.jsonl").read_text().splitlines()]
    brands = [d for d in rows if d["source"] == "simple-icons" and any(v["status"] == "published" for v in d["variants"])]
    return sorted(brands, key=lambda d: d["name"])


def brand_shard(i: int) -> list[dict]:
    b = brand_list()
    size = -(-len(b) // BRAND_SHARDS)
    return b[(i - 1) * size:i * size]


def load_brands() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in sorted(BRAND_DIR.glob("*.json")):
        out.update(json.loads(p.read_text()))
    return out


def dump_brands(i: int) -> None:
    for d in brand_shard(i):
        x = d.get("extra") or {}
        print(json.dumps({"slug": d["nativeName"], "title": x.get("title"), "website": x.get("sourceUrl"),
                          "aliases": d["aliases"]}, ensure_ascii=False))


def validate_brands(shards: list[int]) -> int:
    problems = []
    for i in shards:
        p = BRAND_DIR / f"shard-{i}.json"
        want = {d["nativeName"] for d in brand_shard(i)}
        if not p.exists():
            problems.append(f"{p.name}: missing")
            continue
        data = json.loads(p.read_text())
        for slug in sorted(want - set(data)):
            problems.append(f"shard-{i}: {slug}: no entry yet")
        for slug, e in data.items():
            if slug not in want:
                problems.append(f"shard-{i}: {slug}: not in this shard")
            ctx, kws = e.get("context", ""), e.get("keywords", [])
            if not (20 <= len(ctx) <= 400):
                problems.append(f"{slug}: context should be 20-400 characters")
            title = slug.replace("dot", ".")  # a brand's own name may contain a banned word (Pivotal, Underscore)
            for b in BANNED_IN_CONTEXT:
                if b in ctx.lower() and b not in title:
                    problems.append(f"{slug}: context uses {b!r}")
            if not (3 <= len(kws) <= 30) or len(set(kws)) != len(kws):
                problems.append(f"{slug}: want 3-30 unique keywords")
            for k in kws:
                if not KEYWORD_RE.match(k):
                    problems.append(f"{slug}: bad keyword {k!r}")
    for pr in problems[:200]:
        print("FAIL ", pr)
    print(f"{len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] in ("dump-brands", "validate-brands"):
    if sys.argv[1] == "dump-brands":
        dump_brands(int(sys.argv[2]))
    else:
        sys.exit(validate_brands([int(a) for a in sys.argv[2:]] or list(range(1, BRAND_SHARDS + 1))))
