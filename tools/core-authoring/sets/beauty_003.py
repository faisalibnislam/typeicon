"""TypeIcon Core: beauty (batch 003): ear jewellery tools and fragrance sampling."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "beauty"


def L(S, a, b):
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def rpts(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


@icon("ear-stretcher-taper", CAT, "Long slim cone taper with a flared wide end and a small rubber ring near it",
      tags=["ear gauge", "stretching", "taper", "body piercing", "ear stretching", "lobe", "jewelry"])
def _(S):
    k = S.r * 0.6
    body = rpts([(11, 21.5), (13, 21.5), (15.5, 7), (8.5, 7)], 45)
    flange = rpts([(6.5, 2.5), (17.5, 2.5), (17.5, 6), (6.5, 6)], 45)
    ring = rpts([(8.9, 11), (15.1, 11)], 45)
    return [shell(union(poly(body, closed=True, r=k), poly(flange, closed=True, r=k))),
            detail(poly(ring))]


@icon("helix-piercing", CAT, "Ear outline with a small hoop ring through the curved upper rim",
      tags=["ear piercing", "cartilage", "hoop", "earring", "body jewelry", "ear", "upper ear"])
def _(S):
    if S.name == "line":
        ear = "M6 6C11 2.5 17.5 4 18 10C18.3 14.5 14.5 15 14.5 18.5C14.5 21 12.5 22 10.5 21.5C8.5 21 6 19.5 6 18Z"
    else:
        ear = "M7.5 6C11 2.5 17.5 4 18 10C18.3 14.5 14.5 15 14.5 18.5C14.5 21 12.5 22 10.5 21.5C8.5 21 6 19.5 6 18L6 8Q6 6.8 7.5 6Z"
    return [shell(ear),
            detail("M10.5 10.5C12.5 10 13.5 11.5 13 13.5"),
            line(circle(17, 5.5, 3))]


@icon("roll-on-perfume", CAT, "Slim glass vial with a screw cap and a rollerball at the top of the bottle",
      tags=["rollerball", "perfume", "fragrance", "travel scent", "oil", "applicator", "bottle"])
def _(S):
    body = rect(6, 11, 12, 10.5, L(S, 1, 3))
    neck = rect(8.5, 5.5, 7, 6, 0)
    cap = rect(8, 1.5, 8, 4, L(S, 0, 1.5))
    return [shell(union(body, neck, cap)),
            detail(seg(8.5, 5.5, 15.5, 5.5)),
            dot(12, 8.5, 1.5)]


@icon("perfume-sample-vial", CAT, "Tiny thin glass tube with a small stopper and a line marking the liquid level",
      tags=["perfume", "sample", "tester", "fragrance", "decant", "vial", "miniature"])
def _(S):
    tube = rect(9, 7, 6, 14.5, L(S, 0.5, 2.5))
    return [shell(tube),
            shell(rect(8, 2.5, 8, 4.5, L(S, 0, 1.5))),
            detail(seg(9, 13, 15, 13))]


@icon("scent-blotter", CAT, "Long narrow paper testing strip with a pointed tip and wavy scent lines rising from it",
      tags=["perfume strip", "smelling strip", "fragrance tester", "mouillette", "sniff", "paper strip", "scent"])
def _(S):
    k = S.r * 0.6
    strip = rpts([(8.5, 22.5), (13.5, 22.5), (13.5, 11), (11, 6.5), (8.5, 11)], 40, 11, 16)
    return [shell(poly(strip, closed=True, r=k)),
            line("M10.5 2.5C9 4 12 5.5 10.5 7"),
            line("M16 2C14.5 3.5 17.5 5 16 6.5")]


@icon("fragrance-pyramid", CAT, "Triangle split into three stacked bands for top, heart and base scent notes",
      tags=["scent notes", "perfume", "top notes", "heart notes", "base notes", "perfumery", "fragrance"])
def _(S):
    return [shell(poly([(12, 2.5), (22, 21.5), (2, 21.5)], closed=True, r=S.r)),
            detail(seg(7.4, 11.5, 16.6, 11.5)),
            detail(seg(4.9, 16.5, 19.1, 16.5))]
