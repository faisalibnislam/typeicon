"""Font scaling tiers: can one style font hold 5k / 20k / 50k icons?

Uses real outlines from the catalog build (cycled to reach the tier size) with two keywords per
glyph (like pack fonts: namespaced + local). Measures compile time, file sizes, GSUB structure,
OpenType Sanitizer, HarfBuzz load + shaping time. Output: build/bench/font-scaling.json.
Run: .venv/bin/python tools/font-builder/bench/font_scaling.py [5000 20000 50000]
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from fontTools.svgLib.path import parse_path
from fontTools.ttLib import TTFont
from pathops import Path as PPath

from typeicon_fonts.compiler import FontSpec, GlyphSpec, compile_font
from typeicon_fonts.validate import Shaper, run_ots

ROOT = Path(__file__).resolve().parents[3]


def load_outlines(limit: int) -> list[tuple[str, int]]:
    out = []
    with (ROOT / "build/catalog/designs.jsonl").open() as fh:
        for line in fh:
            d = json.loads(line)
            for v in d["variants"]:
                if v["status"] == "published" and v.get("outline"):
                    out.append((v["outline"]["d"], v["outline"]["advance"]))
                    break
            if len(out) >= limit:
                break
    return out


def words(i: int) -> str:
    a = "abcdefghijklmnopqrstuvwxyz"
    s = ""
    n = i
    for _ in range(4):
        s += a[n % 26]
        n //= 26
    return s


def tier(n: int, outlines, out_dir: Path) -> dict:
    glyphs = []
    for i in range(n):
        d, adv = outlines[i % len(outlines)]
        p = PPath()
        parse_path(d, p.getPen())
        cp = 0x100000 + i
        glyphs.append(GlyphSpec(f"u{cp:X}", [cp], [f"icon-{words(i)}-{i}", f"{words(i)}{i}"], p, adv))
    spec = FontSpec(f"Bench {n}", f"Bench{n}-Regular", "0.1.0", glyphs)
    t0 = time.perf_counter()
    files = compile_font(spec, out_dir, formats=("otf", "ttf", "woff2"))
    compile_s = time.perf_counter() - t0
    res = {"glyphs": n, "keywords": 2 * n, "compileSeconds": round(compile_s, 1)}
    for fmt, p in files.items():
        res[f"{fmt}Bytes"] = p.stat().st_size
    f = TTFont(files["otf"], lazy=True)
    gsub = f["GSUB"].table
    res["gsubLookups"] = len(gsub.LookupList.Lookup)
    res["gsubLookupTypes"] = sorted({lk.LookupType for lk in gsub.LookupList.Lookup})
    res["gsubSubtables"] = sum(len(lk.SubTable) for lk in gsub.LookupList.Lookup)
    res["numGlyphs"] = f["maxp"].numGlyphs
    for fmt in ("otf", "ttf", "woff2"):
        t0 = time.perf_counter()
        ok, msg = run_ots(files[fmt])
        res[f"ots_{fmt}"] = "pass" if ok else msg[:200]
        res[f"otsSeconds_{fmt}"] = round(time.perf_counter() - t0, 2)
    t0 = time.perf_counter()
    s = Shaper(files["otf"])
    res["hbLoadMs"] = round((time.perf_counter() - t0) * 1000, 1)
    probes = [0, n // 2, n - 1]
    t0 = time.perf_counter()
    ok = all(s.glyph_names(f"icon-{words(i)}-{i}") == [f"u{0x100000 + i:X}"] and s.glyph_names(f"{words(i)}{i}") == [f"u{0x100000 + i:X}"] for i in probes)
    res["shapingCorrect"] = ok
    text = " ".join(f"icon-{words(i)}-{i}" for i in range(0, n, max(1, n // 200)))
    t0 = time.perf_counter()
    for _ in range(20):
        s.glyph_names(text)
    res["shape200KeywordsMs"] = round((time.perf_counter() - t0) * 1000 / 20, 2)
    return res


def main():
    tiers = [int(x) for x in sys.argv[1:]] or [5000, 20000, 50000]
    outlines = load_outlines(20000)
    out = ROOT / "build/bench"
    out.mkdir(parents=True, exist_ok=True)
    results = []
    for n in tiers:
        r = tier(n, outlines, out / f"tier-{n}")
        print(json.dumps(r))
        results.append(r)
    (out / "font-scaling.json").write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
