"""Kit jobs: private custom-icon validation and private kit builds."""
from __future__ import annotations

import hashlib

import psycopg
from fontTools.pens.svgPathPen import SVGPathPen
from psycopg.rows import dict_row

from typeicon_fonts.outline import OutlineError, svg_to_outline
from typeicon_fonts.svg_sanitize import SvgRejected, sanitize_svg

from .queue import Job, PermanentError
from .subset_build import build_package


def _fmt(v: float) -> str:
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def run_custom_icon_check(job: Job, database_url: str) -> dict:
    """Sanitize an uploaded SVG and convert it to a font outline. Marks the icon ready or rejected."""
    icon_id = job.payload["customIconId"]
    with psycopg.connect(database_url, row_factory=dict_row) as conn:
        row = conn.execute("SELECT id, owner_id, raw_svg, status FROM custom_icons WHERE id = %s", (icon_id,)).fetchone()
        if not row or row["owner_id"] != job.owner_id:
            raise PermanentError("custom icon not found for this owner")
        if row["status"] != "pending" or not row["raw_svg"]:
            return {"status": row["status"], "skipped": True}
        reasons: list[str] = []
        svg = sha = outline_d = None
        advance = None
        route = None
        try:
            san = sanitize_svg(row["raw_svg"].encode("utf-8"))
            svg, route, reasons = san.svg, san.route, list(san.reasons)
            sha = hashlib.sha256(svg.encode()).hexdigest()
            if san.removed:
                reasons.append("removed: " + ", ".join(sorted(set(san.removed)))[:300])
            if route == "font":
                try:
                    o = svg_to_outline(svg)
                    pen = SVGPathPen(None, ntos=_fmt)
                    o.path.draw(pen)
                    outline_d, advance = pen.getCommands(), o.advance
                    reasons += o.warnings
                except (OutlineError, SvgRejected) as e:
                    route = "svg-only"
                    reasons.append(f"outline: {e}")
            status = "ready"
        except SvgRejected as e:
            status, reasons = "rejected", [f"rejected: {e}"]
        conn.execute(
            """UPDATE custom_icons SET status = %s, svg = %s, svg_sha256 = %s, route = %s, reasons = %s,
                      outline_d = %s, outline_advance = %s, raw_svg = NULL WHERE id = %s""",
            (status, svg, sha, route, reasons, outline_d, advance, icon_id))
        conn.commit()
    return {"status": status, "route": route, "reasons": reasons}


def run_kit_build(job: Job, database_url: str) -> dict:
    p = job.payload
    if not job.scope.startswith("private:") or job.scope != f"private:{job.owner_id}":
        raise PermanentError("kit builds must run in the owner's private scope")
    with psycopg.connect(database_url, row_factory=dict_row) as conn:
        kv = conn.execute(
            """SELECT kv.selection, kv.formats, k.name, k.embed_id, k.owner_id FROM kit_versions kv JOIN kits k ON k.id = kv.kit_id
               WHERE kv.id = %s AND k.id = %s""", (p["kitVersionId"], p["kitId"])).fetchone()
    if not kv or kv["owner_id"] != job.owner_id:
        raise PermanentError("kit version not found for this owner")
    sel = kv["selection"]
    hosted = (kv["embed_id"], p["version"]) if p.get("hosted") else None
    result = build_package(job, database_url, name=kv["name"], slug=p["slug"], formats=list(kv["formats"]),
                           release=p["release"], variant_ids=[i["variantId"] for i in sel["items"]],
                           custom_icon_ids=sel["customIconIds"], owner_id=job.owner_id, hosted_embed=hosted)
    return result
