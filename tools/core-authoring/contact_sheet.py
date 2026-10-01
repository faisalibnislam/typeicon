"""Render a quick contact sheet of assets/core SVGs (resvg) for design iteration.

Usage: .venv/bin/python tools/core-authoring/contact_sheet.py [out.png] [size]
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

import resvg_py
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]


def render(svg_path: Path, px: int, color: str = "#111") -> Image.Image:
    svg = svg_path.read_text().replace("currentColor", color)
    png = bytes(resvg_py.svg_to_bytes(svg_string=svg, width=px, height=px))
    return Image.open(io.BytesIO(png)).convert("RGBA")


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "build" / "core-contact-sheet.png"
    px = int(sys.argv[2]) if len(sys.argv) > 2 else 48
    names = [i["name"] for i in json.loads((ROOT / "assets/core/core-icons.json").read_text())["icons"]]
    cols = 6
    cell_w, cell_h = px * 3 + 40, px + 22
    rows = (len(names) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * cell_w, rows * cell_h), "white")
    draw = ImageDraw.Draw(sheet)
    for i, name in enumerate(names):
        x0, y0 = (i % cols) * cell_w + 8, (i // cols) * cell_h + 4
        for j, style in enumerate(("line", "rounded", "filled")):
            img = render(ROOT / "assets/core/svg" / style / f"{name}.svg", px)
            sheet.alpha_composite(img, (x0 + j * (px + 8), y0))
        draw.text((x0, y0 + px + 3), name, fill="#555")
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(out)
    print(out)


if __name__ == "__main__":
    main()
