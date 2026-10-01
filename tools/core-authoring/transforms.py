"""Find Core designs that are rotations, mirrors or copies of another design.

Designers often draw directional siblings (arrow-left, caret-down, align-right, flip-vertical) by rotating
or mirroring coordinates in code. They are useful icons, but the counting policy (docs/policies/
catalog-counts.md) does not count transform-derived artwork as independent concepts. This module detects
them from the artwork itself, so the rule holds however the icon was written:

  * Line and Filled are rasterised at 32 px;
  * for every pair (a, b) the 8 symmetries of the square are applied to b (identity included, which
    catches plain copies under two names);
  * if both styles match with IoU >= THRESHOLD, the later design (in definition order) is recorded as
    derived from the earlier one, e.g. {"name": "arrow-narrow-right", "transform": "rotated 90°"}.

Transform-derived designs are still published under their own names; they are only excluded from the
counts and get no generated variants.
"""
from __future__ import annotations

import numpy as np

THRESHOLD = 0.97
PX = 32

# numpy transform of b's mask -> SVG transform that maps b onto a
_SYMMETRIES = [
    ("identical artwork", lambda m: m),
    ("rotated 90°", lambda m: np.rot90(m, 1)),
    ("rotated 180°", lambda m: np.rot90(m, 2)),
    ("rotated 270°", lambda m: np.rot90(m, 3)),
    ("mirrored horizontally", lambda m: m[:, ::-1]),
    ("mirrored vertically", lambda m: m[::-1, :]),
    ("mirrored diagonally", lambda m: m.T),
    ("mirrored anti-diagonally", lambda m: np.rot90(m, 2).T),
]


def _masks(icons, style: str) -> np.ndarray:
    from typeicon_fonts.raster import render_svg_mask
    from export import filled_svg, stroke_svg
    from geometry import LINE, path_to_d
    out = np.zeros((len(icons), PX, PX), dtype=np.float32)
    for i, ic in enumerate(icons):
        svg = filled_svg(path_to_d(ic.filled())) if style == "filled" else stroke_svg(ic.stroke(LINE), LINE, None)
        out[i] = np.asarray(render_svg_mask(svg, PX)) >= 128
    return out


def detect(icons) -> dict[str, dict]:
    """Return {derived_name: {"name": original_name, "transform": str}} for icons without derived_from."""
    cand = [ic for ic in icons if not ic.derived_from]
    if len(cand) < 2:
        return {}
    line, filled = _masks(cand, "line"), _masks(cand, "filled")
    n = len(cand)
    fl, ff = line.reshape(n, -1), filled.reshape(n, -1)
    sl, sf = fl.sum(1), ff.sum(1)
    best: dict[int, tuple[float, int, str]] = {}
    BLOCK = 2048  # rows per block: memory stays ~BLOCK x n floats, fine at 50,000 designs
    for label, fn in _SYMMETRIES:
        tl = np.stack([fn(m) for m in line]).reshape(n, -1)
        tf = np.stack([fn(m) for m in filled]).reshape(n, -1)
        stl, stf = tl.sum(1), tf.sum(1)
        for r0 in range(0, n, BLOCK):
            r1 = min(n, r0 + BLOCK)
            il = fl[r0:r1] @ tl.T
            iou_l = il / np.maximum(sl[r0:r1, None] + stl[None, :] - il, 1)
            inter_f = ff[r0:r1] @ tf.T
            iou_f = inter_f / np.maximum(sf[r0:r1, None] + stf[None, :] - inter_f, 1)
            score = np.minimum(iou_l, iou_f)  # score[a, b]: T(b) vs a
            rows = np.arange(r0, r1)
            score[rows - r0, rows] = 0
            for ai, b in zip(*np.nonzero(score >= THRESHOLD)):
                a = int(ai) + r0
                if a < b and (b not in best or score[ai, b] > best[b][0]):  # b (later) derives from a (earlier)
                    best[int(b)] = (float(score[ai, b]), a, label)
    derived: dict[str, dict] = {}
    for b, (_, a, label) in sorted(best.items()):
        root = a
        while root in best:  # chains resolve to the first-drawn design
            root = best[root][1]
        via = "" if root == a else f" of {cand[a].name}"
        derived[cand[b].name] = {"name": cand[root].name, "transform": label + via}
    return derived
