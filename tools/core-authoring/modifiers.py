"""Variant badges ("modifiers") and composition: file + plus -> file-plus, user + off -> user-off.

A variant is a real, separately named concept built from a base icon and a designed badge in the
bottom-right corner (box 13–23). The base is cut away around the badge with a shape-following gap
of 1.5 px, so the badge reads at small sizes. The "off" modifier cuts a diagonal slash instead.

Canonical SVGs keep editable strokes: the base is wrapped in a clip path (canvas minus the gap
region), and the badge is drawn on top. Filled designs subtract the same region from the base's
filled design and add the badge's filled design.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from dsl import (
    LINE, Part, Style, U, circle, dot, filled_region, line, path_to_d, poly, rect, regular, seg, shell,
    stroke_elements,
)
from geometry import P, ST
from pathops import Path

GAP = 1.5  # clearance between badge and base


@dataclass
class Modifier:
    suffix: str
    label: str
    tags: list[str]
    draw: Callable[[Style], list[Part]]


def _m(suffix, label, tags=()):
    def deco(fn):
        MODIFIERS[suffix] = Modifier(suffix, label, list(tags), fn)
        return fn
    return deco


MODIFIERS: dict[str, Modifier] = {}
C = 18.0  # badge centre


@_m("plus", "add", ["add", "new", "create"])
def _(S):
    return [line(seg(C, 14, C, 22)), line(seg(14, C, 22, C))]


@_m("minus", "remove", ["remove", "subtract", "less"])
def _(S):
    return [line(seg(14, C, 22, C))]


@_m("check", "done", ["done", "ok", "confirmed", "complete"])
def _(S):
    return [line(poly([(14, 18.2), (17, 21.2), (22, 15.2)], r=S.r * 0.5))]


@_m("x", "remove or cancel", ["cancel", "delete", "close", "remove"])
def _(S):
    return [line(seg(14.5, 14.5, 21.5, 21.5)), line(seg(21.5, 14.5, 14.5, 21.5))]


@_m("lock", "locked", ["locked", "secure", "private"])
def _(S):
    return [shell(rect(14, 17.5, 8, 5, min(S.R, 1.5))), line("M16 17.5V16A2 2 0 0 1 20 16V17.5")]


@_m("search", "search", ["find", "look up", "magnify"])
def _(S):
    return [shell(circle(17, 17, 2.75)), line(seg(19.1, 19.1, 22, 22))]


@_m("star", "favourite", ["favorite", "favourite", "starred"])
def _(S):
    pts = []
    for i in range(10):
        r = 4.6 if i % 2 == 0 else 2.0
        from dsl import pt_on
        pts.append(pt_on(18, 18.6, r, -90 + i * 36))
    return [shell(poly(pts, closed=True, r=S.r * 0.15), stroke_miterlimit="2")]


@_m("heart", "loved", ["like", "love", "favorite"])
def _(S):
    d = "M18 22L14.6 18.7A2.2 2.2 0 0 1 17.5 15.6L18 16.1L18.5 15.6A2.2 2.2 0 0 1 21.4 18.7Z"
    d_round = "M17.3 21.3L14.6 18.7A2.2 2.2 0 0 1 17.5 15.6L18 16.1L18.5 15.6A2.2 2.2 0 0 1 21.4 18.7L18.7 21.3Q18 22 17.3 21.3Z"
    return [shell(d if S.name == "line" else d_round)]


@_m("alert", "alert", ["warning", "error", "attention", "exclamation"])
def _(S):
    return [line(seg(C, 14, C, 18.8)), dot(C, 21.4, 1.1)]


@_m("question", "help", ["help", "unknown", "question"])
def _(S):
    return [line("M16 16.2A2 2 0 1 1 18.8 18C18.3 18.3 18 18.7 18 19.3"), dot(18, 21.6, 1.05)]


@_m("clock", "scheduled", ["time", "pending", "scheduled", "history"])
def _(S):
    return [shell(circle(C, C, 4)), line(poly([(18, 16), (18, 18), (19.6, 19)], r=S.r * 0.3))]


@_m("settings", "settings", ["gear", "configure", "preferences"])
def _(S):
    pts = []
    from dsl import pt_on
    for i in range(6):
        th = i * 60 - 90
        pts += [pt_on(C, C, 3.1, th - 22), pt_on(C, C, 4.6, th - 13), pt_on(C, C, 4.6, th + 13), pt_on(C, C, 3.1, th + 22)]
    return [shell(poly(pts, closed=True, r=S.r * 0.2)), shell(circle(C, C, 1.2))]


@_m("edit", "edit", ["pencil", "modify", "write"])
def _(S):
    return [shell(poly([(20.3, 14), (22, 15.7), (16.4, 21.3), (14.3, 21.7), (14.7, 19.6)], closed=True, r=S.r * 0.2))]


@_m("share", "share", ["send", "export", "forward"])
def _(S):
    return [line(seg(14.5, 21.5, 21.5, 14.5)), line(poly([(16.5, 14.5), (21.5, 14.5), (21.5, 19.5)], r=S.r * 0.5))]


@_m("download", "download", ["save", "get", "import"])
def _(S):
    return [line(seg(C, 14, C, 21.5)), line(poly([(14.8, 18.6), (18, 21.8), (21.2, 18.6)], r=S.r * 0.5))]


@_m("upload", "upload", ["send", "export", "publish"])
def _(S):
    return [line(seg(C, 22, C, 14.5)), line(poly([(14.8, 17.4), (18, 14.2), (21.2, 17.4)], r=S.r * 0.5))]


@_m("refresh", "sync", ["refresh", "reload", "sync", "update"])
def _(S):
    from dsl import arc
    return [line(arc(C, C, 3.6, 30, 300)), line(poly([(19.3, 13.6), (19.9, 15.2), (18.2, 15.8)], r=S.r * 0.3))]


@_m("bolt", "powered", ["power", "flash", "energy", "fast"])
def _(S):
    return [shell(poly([(19, 13.5), (15, 18.6), (18, 18.6), (17.2, 22.5), (21.2, 17.2), (18.3, 17.2)], closed=True, r=S.r * 0.15),
                  stroke_miterlimit="2")]


@_m("dollar", "paid", ["money", "price", "cost", "payment"])
def _(S):
    return [line("M20.4 15.8C20 15 19.1 14.7 18 14.7C16.7 14.7 15.8 15.3 15.8 16.3C15.8 18.6 20.4 17.4 20.4 19.8C20.4 20.8 19.4 21.4 18 21.4C16.9 21.4 16 21 15.6 20.2"),
            line(seg(C, 13.4, C, 14.7)), line(seg(C, 21.4, C, 22.6))]


@_m("code", "code", ["develop", "programming", "embed"])
def _(S):
    return [line(poly([(16, 15), (13.8, 18), (16, 21)], r=S.r * 0.4)), line(poly([(20, 15), (22.2, 18), (20, 21)], r=S.r * 0.4))]


@_m("pause", "paused", ["pause", "hold"])
def _(S):
    return [line(seg(16.4, 14.8, 16.4, 21.2)), line(seg(19.6, 14.8, 19.6, 21.2))]


@_m("play", "play", ["start", "run", "resume"])
def _(S):
    return [shell(poly([(15.8, 14.4), (21.8, 18), (15.8, 21.6)], closed=True, r=S.r * 0.4), stroke_miterlimit="2")]


@_m("off", "off / disabled", ["disabled", "off", "unavailable", "blocked"])
def _(S):
    return [line(seg(3, 3, 21, 21))]


# Modifier sets by category. Variants must make sense: math symbols get none, objects get many.
SETS: dict[str, list[str]] = {
    "none": [],
    "minimal": ["plus", "minus", "check", "x", "off"],
    "common": ["plus", "minus", "check", "x", "off", "lock", "search", "star", "heart", "alert", "edit", "settings", "share", "clock"],
    "full": ["plus", "minus", "check", "x", "off", "lock", "search", "star", "heart", "alert", "question", "clock", "settings",
             "edit", "share", "download", "upload", "refresh", "bolt", "dollar", "code", "pause", "play"],
}


def knockout_region(parts: list[Part], stroke: float = 2.0) -> Path:
    """Base area to cut away under the badge: badge geometry grown by the gap (round, so it hugs the shape)."""
    regions = []
    w = stroke + 2 * GAP
    for p in parts:
        regions.append(ST(p.d, w, "round", "round"))
        if p.kind in ("shell", "dot", "solid"):
            regions.append(P(p.d))
    return U(*regions)


_EL = __import__("re").compile(r'<path d="([^"]+)"([^>]*)/>')


def elements_region(elements: list[str], S: Style) -> Path:
    """Painted region of stroke-style SVG elements (as produced by icon.stroke(S)) in grid units."""
    import re
    regions = []
    for el in elements:
        for d, rest in _EL.findall(el):
            attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', rest))
            if attrs.get("fill") == "currentColor" and attrs.get("stroke") == "none":
                regions.append(P(d))
            else:
                regions.append(ST(d, S.w, S.cap, S.join, float(attrs.get("stroke-miterlimit", 4))))
    return U(*regions)


def compose(base, mod: Modifier, name: str, category: str, description: str, tags: list[str]):
    """Variant = base with a shape-following gap around the badge + the badge.

    The base is emitted as its exact outlined region (stroke already expanded, gap cut out) and the
    badge keeps editable strokes, so the SVG needs no clip paths or ids and renders the same everywhere.
    """
    from dsl import D, DslIcon

    ko = knockout_region(mod.draw(LINE))
    ko_thin = knockout_region(mod.draw(LINE), 1.0)  # keeps the 1.5 gap around the thinner badge stroke

    def stroke(S: Style) -> list[str]:
        region = D(elements_region(base.stroke(S), S), ko_thin if S.w < 2 else ko)
        return [f'<path d="{path_to_d(region)}" fill="currentColor" stroke="none"/>', *stroke_elements(mod.draw(S))]

    def filled() -> Path:
        return U(D(base.filled(), ko), filled_region(mod.draw(LINE)))

    ic = DslIcon(name, category, description, tags, [], draw=lambda S: [], modifiers="none",
                 derived_from={"name": base.name, "modifier": mod.suffix})
    ic.stroke = stroke  # type: ignore[method-assign]
    ic.filled = filled  # type: ignore[method-assign]
    return ic


# Search wording for variants: how the badge changes the base's meaning. "{n}" is the base name in words
# ("file", "credit card"). use: completes "Used for ..."; phrases: queries people type for this variant.
SEARCH: dict[str, tuple[str, list[str]]] = {
    "plus": ("adding or creating a new {n}", ["add {n}", "new {n}", "create {n}", "{n} add", "insert {n}"]),
    "minus": ("removing a {n} or reducing an amount", ["remove {n}", "{n} remove", "subtract {n}", "less {n}"]),
    "check": ("a {n} that is done, confirmed, verified or selected", ["{n} done", "{n} confirmed", "verified {n}", "{n} complete", "{n} ok"]),
    "x": ("deleting, cancelling, closing or rejecting a {n}", ["delete {n}", "cancel {n}", "remove {n}", "{n} error", "close {n}"]),
    "off": ("a {n} that is turned off, disabled, muted or unavailable", ["{n} off", "no {n}", "disable {n}", "{n} disabled", "{n} unavailable"]),
    "lock": ("a locked, private or protected {n}", ["locked {n}", "private {n}", "secure {n}", "{n} locked", "protected {n}"]),
    "search": ("searching for, finding or inspecting a {n}", ["search {n}", "find {n}", "{n} lookup", "browse {n}", "inspect {n}"]),
    "star": ("a starred, featured or favourite {n}", ["favorite {n}", "favourite {n}", "starred {n}", "featured {n}", "bookmark {n}"]),
    "heart": ("a liked, loved or saved {n}", ["like {n}", "love {n}", "saved {n}", "favorite {n}"]),
    "alert": ("a {n} that has a warning, error or needs attention", ["{n} warning", "{n} error", "{n} alert", "{n} problem", "{n} issue"]),
    "question": ("help, unknown status or questions about a {n}", ["{n} help", "{n} unknown", "{n} faq", "{n} question", "{n} info"]),
    "clock": ("a scheduled, pending, recent or timed {n}", ["{n} history", "scheduled {n}", "pending {n}", "recent {n}", "{n} time"]),
    "settings": ("settings, preferences or configuration for a {n}", ["{n} settings", "{n} preferences", "configure {n}", "{n} options", "manage {n}"]),
    "edit": ("editing, renaming or changing a {n}", ["edit {n}", "rename {n}", "change {n}", "modify {n}", "update {n}"]),
    "share": ("sharing, sending or exporting a {n}", ["share {n}", "send {n}", "export {n}", "forward {n}"]),
    "download": ("downloading, saving or importing a {n}", ["download {n}", "save {n}", "import {n}", "get {n}"]),
    "upload": ("uploading, publishing or sending a {n}", ["upload {n}", "publish {n}", "send {n}", "attach {n}"]),
    "refresh": ("syncing, reloading or updating a {n}", ["sync {n}", "refresh {n}", "reload {n}", "update {n}", "{n} sync"]),
    "bolt": ("a powered, fast, instant or automated {n}", ["fast {n}", "instant {n}", "{n} power", "automated {n}", "quick {n}"]),
    "dollar": ("the price, cost, payment or value of a {n}", ["{n} price", "{n} cost", "paid {n}", "{n} payment", "buy {n}"]),
    "code": ("the code, source or developer view of a {n}", ["{n} code", "{n} source", "{n} developer", "{n} api", "embed {n}"]),
    "pause": ("pausing or holding a {n}", ["pause {n}", "{n} paused", "hold {n}", "suspend {n}"]),
    "play": ("playing, starting or resuming a {n}", ["play {n}", "start {n}", "run {n}", "resume {n}"]),
}
