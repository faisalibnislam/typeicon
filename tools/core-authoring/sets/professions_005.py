"""TypeIcon Core: professions and roles (batch professions_005).

Families, life stages, mobility and medical-support figures, and a last group of working roles.
Figures are drawn as in the activities set: a head disc over 2 px limbs, polylines filleted with S.r so Line
and Rounded differ. Women are shown with a dress, men and neutral adults with trousers. Overlapping parts are
cut away with a gap where needed so small scenes stay readable at 16 px.
"""
from __future__ import annotations

import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, filled_region, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import I, fmt, path_to_d, polar  # noqa: F401

CAT = "professions"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def pl(S, pts, closed=False, k=1.0):
    return poly(pts, closed=closed, r=S.r * k)


def u(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def heart(cx, top, k=1.0):
    """Small solid heart whose top notch is at (cx, top)."""
    def p(x, y):
        return f"{fmt(cx + x * k)} {fmt(top + y * k)}"
    return (f"M{p(0, 3.8)}L{p(-2.1, 1.7)}A{fmt(1.35 * k)} {fmt(1.35 * k)} 0 0 1 {p(0, 0)}"
            f"A{fmt(1.35 * k)} {fmt(1.35 * k)} 0 0 1 {p(2.1, 1.7)}Z")


def hd(x, y, r=2.25):
    return dot(x, y, r)


class Fig:
    """Geometry of one standing figure: head (x, y) radius r, shoulders and hips."""

    def __init__(self, x, y=4.5, r=2.25, torso=6.5, foot=21.5):
        self.x, self.y, self.r = x, y, r
        self.neck = y + r + 0.75
        self.sh = y + r + 2.5          # shoulder height for arms
        self.hip = self.neck + torso
        self.foot = foot


def man(S, x, y=4.5, r=2.25, torso=6.5, foot=21.5, legs=2.0):
    f = Fig(x, y, r, torso, foot)
    return f, [hd(x, y, r), line(seg(x, f.neck, x, f.hip)),
               line(pl(S, [(x - legs, foot), (x, f.hip), (x + legs, foot)]))]


def woman(S, x, y=4.5, r=2.25, torso=6.5, foot=21.5, legs=1.4):
    f = Fig(x, y, r, torso, foot)
    skirt = min(f.hip + 1.5, foot - 3.0)
    dress = pl(S, [(x - 1.4, f.neck), (x + 1.4, f.neck), (x + 3.4, skirt), (x - 3.4, skirt)], closed=True, k=0.5)
    return f, [hd(x, y, r), shell(dress), line(seg(x - legs, skirt, x - legs, foot)),
               line(seg(x + legs, skirt, x + legs, foot))]


# ============================================================================ families and life stages

@icon("expectant-couple", CAT, "A woman with a rounded belly and a man resting his hand on it.",
      tags=["pregnant couple", "expecting", "parents to be", "pregnancy", "baby bump", "maternity", "new baby"])
def _(S):
    return [hd(6.5, 4.5), line(seg(6.5, 7.5, 6.5, 13)), shell(circle(9.5, 12, 3.2)),
            line(pl(S, [(5, 21.5), (7.5, 16), (10, 21.5)])),
            hd(19, 4.5), line(seg(19, 7.5, 19, 14)),
            line(pl(S, [(19, 9.5), (17, 11), (13.5, 11.5)])),
            line(pl(S, [(17, 21.5), (19, 14), (21, 21.5)]))]


@icon("parent-with-stroller", CAT, "An adult figure pushing a hooded baby stroller.",
      tags=["stroller", "pram", "buggy", "baby", "walk with baby", "pushchair", "parenting"])
def _(S):
    hood = "M12.5 11.5A5 5 0 0 1 17.5 6.5V11.5Z"
    basket = "M12.5 11.5H21.5A4.5 4.5 0 0 1 17 16H12.5Z"
    return [hd(5, 4.5), line(seg(5, 7.5, 5, 14)),
            line(pl(S, [(3, 21.5), (5, 14), (7, 21.5)])),
            line(pl(S, [(5, 9.5), (9, 11.5), (12.5, 11.5)])),
            shell(hood, stroke_miterlimit="2"), shell(basket, stroke_miterlimit="2"),
            line(seg(14.5, 16, 16, 18.5)), dot(16.5, 20, 1.75)]


@icon("child-on-shoulders", CAT, "An adult carrying a small child sitting on their shoulders.",
      tags=["shoulder ride", "piggyback", "carry child", "dad and kid", "parade", "outing", "parent and child"])
def _(S):
    return [hd(12, 3.2, 1.75), line(seg(12, 5.5, 12, 8.2)),
            line(pl(S, [(12, 6.5), (9.5, 4.2)])), line(pl(S, [(12, 6.5), (14.5, 4.2)])),
            line(pl(S, [(12, 8.2), (7.5, 9), (7.5, 14)])), line(pl(S, [(12, 8.2), (16.5, 9), (16.5, 14)])),
            hd(12, 11.5, 2.25), line(seg(12, 14.5, 12, 17.5)),
            line(seg(7.5, 14, 16.5, 14)),
            line(pl(S, [(10, 21.5), (12, 17.5), (14, 21.5)]))]


@icon("parent-carrying-baby-in-carrier", CAT,
      "An adult with a baby facing outward in a front carrier on the chest.",
      tags=["baby carrier", "babywearing", "sling", "infant", "papoose", "parenting", "front carrier"])
def _(S):
    return [hd(12, 3.8, 2.25),
            line(pl(S, [(5.5, 12), (6.5, 8), (17.5, 8), (18.5, 12)])),
            shell(rect(8, 10.5, 8, 10, L(S, 1, 3.5))),
            dot(12, 13.8, 1.6), detail(pl(S, [(9.8, 18.2), (12, 16), (14.2, 18.2)]))]


@icon("siblings", CAT, "Two children of different heights standing side by side holding hands.",
      tags=["brother", "sister", "brothers and sisters", "kids", "children", "family", "sibling"])
def _(S):
    return [hd(6.5, 9.5, 2), line(seg(6.5, 12.5, 6.5, 16.5)),
            line(pl(S, [(4.7, 21.5), (6.5, 16.5), (8.3, 21.5)])),
            line(pl(S, [(6.5, 14), (9.5, 14), (12, 13)])),
            hd(17, 4.5), line(seg(17, 7.5, 17, 14)),
            line(pl(S, [(15, 21.5), (17, 14), (19, 21.5)])),
            line(pl(S, [(17, 9), (14.5, 13), (12, 13)]))]


def _baby(S, x):
    return [hd(x, 6.5, 2.4), line(seg(x - 2.6, 12, x + 2.6, 12)),
            shell(rect(x - 1.7, 10.5, 3.4, 8, L(S, 0.4, 1.7)))]


@icon("triplets", CAT, "Three identical babies side by side in a row.",
      tags=["three babies", "multiples", "newborns", "baby trio", "infants", "birth", "same age"])
def _(S):
    return _baby(S, 4.5) + _baby(S, 12) + _baby(S, 19.5)


def _kid(S, x, y=11.0, foot=21.5):
    f = Fig(x, y, 2.0, 4.5, foot)
    return f, [hd(x, y, 2.0), line(seg(x, f.neck, x, f.hip)),
               line(pl(S, [(x - 1.7, foot), (x, f.hip), (x + 1.7, foot)]))]


def _family3(S, left, right, name_kid="kid"):
    fl, pl_ = left(S, 4.5)
    fr, pr = right(S, 19.5)
    fk, pk = _kid(S, 12.0, 11.5)
    arms = [line(pl(S, [(4.5, 9.5), (7.2, 13), (9.5, 14)])), line(pl(S, [(19.5, 9.5), (16.8, 13), (14.5, 14)])),
            line(seg(12, fk.sh + 0.3, 9.5, 14)), line(seg(12, fk.sh + 0.3, 14.5, 14))]
    return pl_ + pr + pk + arms


@icon("two-dads-family", CAT, "Two men with a small child between them, holding hands.",
      tags=["gay dads", "same sex parents", "lgbtq family", "two fathers", "family", "dads", "adoptive parents"])
def _(S):
    return _family3(S, man, man)


@icon("two-moms-family", CAT, "Two women with a small child between them, holding hands.",
      tags=["lesbian moms", "same sex parents", "lgbtq family", "two mothers", "family", "moms", "adoptive parents"])
def _(S):
    return _family3(S, woman, woman)


@icon("single-parent-family", CAT, "One adult holding hands with a child on each side.",
      tags=["single mom", "single dad", "lone parent", "one parent", "family", "parent with kids", "two children"])
def _(S):
    f, p = man(S, 12.0)
    fa, pa = _kid(S, 4.5, 11.0)
    fb, pb = _kid(S, 19.5, 11.0)
    arms = [line(pl(S, [(12, 9.5), (9, 12.5), (7, 14)])), line(pl(S, [(12, 9.5), (15, 12.5), (17, 14)])),
            line(seg(4.5, fa.sh + 0.3, 7, 14)), line(seg(19.5, fb.sh + 0.3, 17, 14))]
    return p + pa + pb + arms


@icon("male-couple", CAT, "Two men standing side by side holding hands, with a small heart above.",
      tags=["gay couple", "two men", "same sex couple", "lgbtq", "partners", "love", "husbands"])
def _(S):
    f1, p1 = man(S, 6.5, 9.5, torso=5.0)
    f2, p2 = man(S, 17.5, 9.5, torso=5.0)
    return [solid(heart(12, 3, 1.3))] + p1 + p2 + [
        line(pl(S, [(6.5, 14), (9.5, 16), (12, 16)])), line(pl(S, [(17.5, 14), (14.5, 16), (12, 16)]))]


@icon("female-couple", CAT, "Two women standing side by side holding hands, with a small heart above.",
      tags=["lesbian couple", "two women", "same sex couple", "lgbtq", "partners", "love", "wives"])
def _(S):
    f1, p1 = woman(S, 6.5, 9.5, torso=5.0)
    f2, p2 = woman(S, 17.5, 9.5, torso=5.0)
    return [solid(heart(12, 3, 1.3))] + p1 + p2 + [
        line(pl(S, [(6.5, 14), (9.5, 16), (12, 16)])), line(pl(S, [(17.5, 14), (14.5, 16), (12, 16)]))]


@icon("elderly-couple", CAT, "Two older figures holding hands, the one on the right leaning on a cane.",
      tags=["grandparents", "senior couple", "retired", "old couple", "grandma and grandpa", "aged", "retirement"])
def _(S):
    f1, p1 = woman(S, 6.0, 5.0, torso=6.0)
    return p1 + [
        hd(16.5, 5.5), line("M16 8.5Q15 11.5 15.5 14"),
        line(pl(S, [(13.5, 21.5), (15.5, 14), (17.5, 21.5)])),
        line(pl(S, [(6, 10.5), (9.5, 13), (13, 13)])), line(pl(S, [(16, 10), (14.5, 13), (13, 13)])),
        line("M21.5 21.5V14A1.5 1.5 0 0 0 18.5 14"), line(seg(16.5, 10, 19.5, 13.5))]


@icon("adoption", CAT, "Two open hands cupping a small child, with a heart above.",
      tags=["adopt", "adopted child", "foster care", "child welfare", "new family", "orphan", "forever home"])
def _(S):
    return [solid(heart(12, 2, 1.1)),
            hd(12, 10.2, 2), line(seg(12, 13.2, 12, 16.5)),
            line(pl(S, [(9, 12), (12, 14), (15, 12)])),
            line("M3 12.5Q3.5 21 12 21Q20.5 21 21 12.5"), line("M7 17.5Q10 19.5 13 19")]


@icon("foster-parent", CAT, "An adult sheltering a child under one arm beneath a small house roof.",
      tags=["foster care", "guardian", "carer", "shelter", "safe home", "child protection", "fostering"])
def _(S):
    return [line(pl(S, [(3, 8), (12, 2.5), (21, 8)])),
            hd(8.5, 11, 2.25), line(seg(8.5, 14, 8.5, 17.5)),
            line(pl(S, [(6.5, 21.5), (8.5, 17.5), (10.5, 21.5)])),
            line(pl(S, [(8.5, 14.5), (12.5, 14.5), (15, 14.5)])),
            hd(16, 12.2, 1.75), line(seg(16, 14.5, 16, 17.5)),
            line(pl(S, [(14.5, 21.5), (16, 17.5), (17.5, 21.5)]))]


@icon("multigenerational-family", CAT, "A grandparent with a cane, a parent and a child in a row of three heights.",
      tags=["three generations", "grandparent", "grandchild", "family tree", "extended family", "grandma", "ancestors"])
def _(S):
    f1, p1 = man(S, 5.5, 6.5, torso=5.5)
    f2, p2 = man(S, 13, 8.0, torso=5.0)
    fk, pk = _kid(S, 19.5, 12.0)
    return p1 + p2 + pk + [line("M1.8 21.5V13A1.2 1.2 0 0 1 4.2 13"), line(seg(5.5, 11.5, 3, 13)),
                           line(pl(S, [(5.5, 11.5), (8.5, 14), (11, 14)])),
                           line(pl(S, [(13, 13), (15, 15), (17, 15)])), line(pl(S, [(19.5, 15.5), (17, 15)]))]


@icon("family-hug", CAT, "Three people of different sizes wrapped together in a group hug.",
      tags=["group hug", "hugging", "family", "embrace", "together", "love", "huddle"])
def _(S):
    return [hd(5.5, 5, 2.25), hd(18.5, 5, 2.25), hd(12, 9.5, 1.75),
            line(seg(5.5, 8, 5.5, 15)), line(seg(18.5, 8, 18.5, 15)),
            line(seg(12, 11.7, 12, 15.5)),
            line(pl(S, [(5.5, 10), (9, 14.5), (15, 14.5), (18.5, 10)])),
            line(pl(S, [(3.7, 21.5), (5.5, 15), (7.3, 21.5)])),
            line(pl(S, [(16.7, 21.5), (18.5, 15), (20.3, 21.5)])),
            line(pl(S, [(10.7, 21.5), (12, 15.5), (13.3, 21.5)]))]


@icon("parent-reading-to-child", CAT, "A seated adult with a child on the lap and an open book held in front.",
      tags=["story time", "bedtime story", "reading aloud", "storybook", "read to kids", "parenting", "literacy"])
def _(S):
    book = "M13.5 9.5L17.75 11L22 9.5V16L17.75 17.5L13.5 16Z"
    return [hd(4.5, 4.5), line(pl(S, [(4.5, 7.5), (4.5, 16), (12, 16), (12, 21.5)])),
            hd(9, 8, 1.75), line(seg(9, 10.5, 9, 15)),
            shell(book, stroke_miterlimit="2"), detail(seg(17.75, 11, 17.75, 17.5)),
            line(pl(S, [(4.5, 9.5), (7, 12.5), (12, 13.5)]))]


@icon("parent-helping-first-steps", CAT, "An adult bending down to hold the hands of a toddler taking a step.",
      tags=["toddler", "learning to walk", "first steps", "baby walking", "milestone", "parenting", "walker"])
def _(S):
    return [hd(5.5, 6, 2.25), line(pl(S, [(5.8, 9), (8, 15)])),
            line(pl(S, [(5.5, 21.5), (8, 15), (10.5, 21.5)])),
            line(pl(S, [(6.8, 10.5), (11, 13), (15, 13.5)])),
            hd(18.5, 10, 1.75), line(seg(18.5, 12.5, 18.5, 16.5)),
            line(pl(S, [(16, 21.5), (18, 16.5), (21, 19), (21.5, 21.5)])),
            line(pl(S, [(18.5, 13.5), (15, 13.5)]))]


@icon("godparent", CAT, "An adult cradling a baby in a long christening gown that flares to the hem.",
      tags=["christening", "baptism", "baby naming", "baby gown", "sponsor", "newborn", "ceremony"])
def _(S):
    gown = pl(S, [(12, 11.6), (16.5, 11.6), (18.8, 21.5), (9.7, 21.5)], closed=True, k=0.4)
    return [hd(5, 4.5), line(seg(5, 7.5, 5, 14)),
            line(pl(S, [(3, 21.5), (5, 14), (7, 21.5)])),
            hd(14.2, 7.6, 1.9), shell(gown),
            line(pl(S, [(5, 9.5), (7.5, 14.5), (13, 15)]))]


@icon("teenager", CAT, "A teen in a hooded top looking down at a phone.",
      tags=["teen", "adolescent", "youth", "hoodie", "phone", "earbuds", "smartphone"])
def _(S):
    bust = "M3.5 21V17A4 4 0 0 1 7.5 13H11.5A4 4 0 0 1 15.5 17V21" if S.name == "line" else \
        "M3.5 21V17.5A4.5 4.5 0 0 1 8 13H11A4.5 4.5 0 0 1 15.5 17.5V21"
    return [shell(bust), line("M4.5 13V9.5A5 5 0 0 1 14.5 9.5V13"), dot(9.5, 9.8, 2.1),
            detail(seg(9.5, 14.5, 9.5, 18)),
            shell(rect(17, 9, 4.5, 8, 1.2)), line(pl(S, [(15.5, 19), (17.5, 17)]))]


@icon("life-stages", CAT, "A row of four figures growing from a baby to a child, an adult and an older person with a cane.",
      tags=["ages of man", "growing up", "aging", "lifecycle", "baby to elder", "generations", "stages of life"])
def _(S):
    return [hd(3, 17.8, 1.6), line(seg(3, 19.6, 3, 21.5)),
            hd(8, 12.5, 1.8), line(seg(8, 14.8, 8, 17.8)),
            line(pl(S, [(6.7, 21.5), (8, 17.8), (9.3, 21.5)])),
            hd(13.5, 5.5, 2.25), line(seg(13.5, 8.5, 13.5, 15)),
            line(pl(S, [(12, 21.5), (13.5, 15), (15, 21.5)])),
            hd(18.8, 8.2, 2), line("M18.3 11.2Q17.6 13.5 18.3 16.2"),
            line(pl(S, [(16.9, 21.5), (18.3, 16.2), (19.7, 21.5)])),
            line("M22 21.5V14.5"), line(seg(18.5, 12.5, 22, 14.5))]


@icon("preschooler", CAT, "A small child walking with a backpack bigger than the torso.",
      tags=["kindergarten", "nursery", "first day of school", "toddler", "backpack", "little kid", "daycare"])
def _(S):
    return [hd(13.5, 6, 2.25), line(seg(13.5, 9, 13.5, 16)),
            line(pl(S, [(11.7, 21.5), (13.5, 16), (15.3, 21.5)])),
            shell(rect(3.5, 9, 6.5, 10, L(S, 1, 2.5))), detail(seg(5, 14.5, 8.5, 14.5)),
            line(seg(10, 11.5, 13.5, 11.5)), line(pl(S, [(13.5, 11), (17, 14.5)]))]


def _walker(S, x, head_y=9.5):
    return [hd(x, head_y, 1.7), line(seg(x, head_y + 2.4, x, 16.5)),
            line(pl(S, [(x - 1.5, 21.5), (x, 16.5), (x + 1.5, 21.5)])),
            solid(rect(x - 4.2, head_y + 2, 2.6, 5.8, L(S, 0.3, 1.2)))]


@icon("school-kids", CAT, "Three children with backpacks walking in a row.",
      tags=["schoolchildren", "pupils", "walk to school", "students", "backpacks", "classmates", "primary school"])
def _(S):
    return _walker(S, 6.5) + _walker(S, 13.5) + _walker(S, 20.5)


def _hold(S, x, y, torso, side):
    """Child figure whose arm reaches to hand height 14.5 on side -1 (left) or +1 (right)."""
    f = Fig(x, y, 2.0, torso, 21.5)
    return [hd(x, y, 2.0), line(seg(x, f.neck, x, f.hip)),
            line(pl(S, [(x - 1.6, 21.5), (x, f.hip), (x + 1.6, 21.5)]))], f


@icon("group-of-children", CAT, "Three small children of different heights holding hands in a row.",
      tags=["kids playing", "children", "friends", "playground", "kindergarten", "holding hands", "toddlers"])
def _(S):
    a, fa = _hold(S, 4.5, 6.5, 5.5, 1)
    b, fb = _hold(S, 12, 10.5, 3.5, 0)
    c, fc = _hold(S, 19.5, 8.0, 4.5, -1)
    return a + b + c + [line(pl(S, [(4.5, fa.sh), (6, 14.5), (8.2, 14.5)])), line(pl(S, [(12, fb.sh), (10, 14.5), (8.2, 14.5)])),
                        line(pl(S, [(12, fb.sh), (14, 14.5), (15.8, 14.5)])), line(pl(S, [(19.5, fc.sh), (17.8, 14.5), (15.8, 14.5)]))]


@icon("wheelchair-user", CAT, "A seated figure in a manual wheelchair with a large rear wheel.",
      tags=["wheelchair", "disability", "accessible", "mobility", "disabled person", "paraplegic", "access"])
def _(S):
    return [hd(11.5, 3.5, 2.25), line(pl(S, [(11, 6.5), (10, 13.5), (16.5, 13.5), (17, 18.5), (20, 18.5)])),
            line(pl(S, [(10.5, 8.5), (14, 11.5), (14.5, 11.5)])), line(pl(S, [(6.5, 6), (7.5, 11.5)])),
            shell(circle(9.5, 16.5, 4.2)), dot(9.5, 16.5, 1.0)]


@icon("power-wheelchair-user", CAT, "A seated figure in a powered wheelchair with a joystick on the armrest.",
      tags=["electric wheelchair", "motorised", "joystick", "disability", "mobility", "power chair", "accessible"])
def _(S):
    return [hd(9.5, 3.5, 2.25), line(pl(S, [(9.5, 6.5), (9, 13), (15, 13), (16.5, 17)])),
            line(pl(S, [(6.5, 6), (6.5, 14)])),
            line(pl(S, [(9.5, 8.5), (12, 11.5), (16, 11)])), line(seg(16.5, 11, 16.5, 8.8)), dot(16.5, 8, 1.2),
            shell(rect(5, 15, 14, 3, L(S, 0.5, 1.5))), dot(8, 20, 1.9), dot(17, 20, 1.9)]


@icon("sports-wheelchair-user", CAT, "A figure leaning forward in a low racing wheelchair with steeply angled wheels.",
      tags=["wheelchair racing", "paralympic", "adaptive sport", "racing chair", "disabled athlete", "para sport", "wheelchair basketball"])
def _(S):
    return [hd(16.5, 5.5, 2.25), line(pl(S, [(14.5, 8.5), (10.5, 14)])),
            line(pl(S, [(10.5, 14), (16, 15), (18, 19)])),
            line(pl(S, [(14, 9.5), (12.5, 13), (10.5, 14.5)])),
            shell(ellipse(9, 17, 3.2, 4.6)), dot(9, 17, 0.9), dot(19.5, 21, 1.1)]


@icon("handcycle-rider", CAT, "A reclined rider in a low three wheeled handcycle turning hand cranks.",
      tags=["handbike", "hand cycling", "para cycling", "adaptive cycling", "paralympic", "disabled athlete", "recumbent"])
def _(S):
    return [hd(7.5, 6, 2.25), line(pl(S, [(8, 9), (9, 14.5), (15.5, 16)])),
            line(pl(S, [(8.5, 10), (13, 12), (16, 12.5)])),
            shell(circle(17.5, 13, 1.7)),
            shell(circle(6, 17.5, 3.6)), dot(6, 17.5, 0.9),
            line(seg(16, 15, 19.5, 19.5)), dot(19.5, 20, 1.6)]


@icon("person-with-cane", CAT, "A figure walking with a single cane held in one hand.",
      tags=["walking stick", "cane", "mobility aid", "senior", "balance", "support", "walking aid"])
def _(S):
    return [hd(8.5, 4.5), line(seg(8.5, 7.5, 8.5, 14.5)),
            line(pl(S, [(5, 21.5), (8.5, 14.5), (11.5, 21.5)])),
            line(pl(S, [(8.5, 9.5), (12, 12.5), (16.5, 13.5)])),
            line("M19 21.5V13.5A1.5 1.5 0 0 0 16 13.5")]


# ============================================================================ mobility, support and medical aids

def bust_d(S, cx, top, hw, bottom=21.0):
    r = min(hw - L(S, 2.0, 1.0), bottom - top)
    x0, x1 = cx - hw, cx + hw
    return (f"M{fmt(x0)} {fmt(bottom)}V{fmt(top + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x0 + r)} {fmt(top)}"
            f"H{fmt(x1 - r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(top + r)}V{fmt(bottom)}")


@icon("person-with-quad-cane", CAT, "A figure leaning on a cane that ends in a small four footed base.",
      tags=["quad cane", "four point cane", "walking aid", "balance", "stroke recovery", "mobility aid", "rehab"])
def _(S):
    return [hd(8.5, 4.5), line(seg(8.5, 7.5, 8.5, 14.5)),
            line(pl(S, [(5, 21.5), (8.5, 14.5), (11.5, 21.5)])),
            line(pl(S, [(8.5, 9.5), (12, 12.5), (17.5, 13.5)])),
            line("M19.5 19V13.5A1.5 1.5 0 0 0 16.5 13.5"),
            line(pl(S, [(16.5, 21.5), (18, 19), (21, 19), (22.5, 21.5)]))]


@icon("person-with-prosthetic-leg", CAT, "A standing figure with one lower leg replaced by a straight rod ending in a flat foot.",
      tags=["prosthesis", "amputee", "artificial leg", "limb difference", "prosthetic", "disability", "mobility"])
def _(S):
    return [hd(9.5, 4.5), line(seg(9.5, 7.5, 9.5, 14)),
            line(pl(S, [(5.5, 13), (9.5, 9.5), (13.5, 13)])),
            line(pl(S, [(9.5, 14), (6.5, 21.5)])),
            line(pl(S, [(9.5, 14), (13.5, 16), (13.5, 21), (18, 21)]))]


@icon("person-with-prosthetic-arm", CAT, "A figure with one forearm replaced by a jointed mechanical hand with a pincer.",
      tags=["prosthesis", "artificial arm", "bionic", "limb difference", "amputee", "robotic hand", "prosthetic"])
def _(S):
    return [hd(9, 4.5), line(seg(9, 7.5, 9, 14)),
            line(pl(S, [(7, 21.5), (9, 14), (11, 21.5)])),
            line(pl(S, [(9, 9.5), (5.5, 14)])),
            line(pl(S, [(9, 9.5), (14.5, 12)])), dot(14.5, 12, 1.5),
            line(seg(14.5, 12, 17.5, 8.5)),
            line(pl(S, [(21.5, 6.5), (17.5, 8.5), (21.5, 11.5)]))]


@icon("running-blade-athlete", CAT, "A running figure with a curved J shaped running blade in place of the rear lower leg.",
      tags=["paralympic", "para athlete", "sprinter", "amputee runner", "prosthetic", "track and field", "adaptive sport"])
def _(S):
    return [hd(15.5, 4.5), line(pl(S, [(14, 8), (10.5, 14)])),
            line(pl(S, [(13, 9.5), (16.5, 12), (20, 10.5)])), line(pl(S, [(13, 9.5), (9, 10), (6.5, 13)])),
            line(pl(S, [(10.5, 14), (15, 16.5), (14, 21.5)])),
            line("M10.5 14L8.5 17.5C7.5 20 5 21 2.5 19.5")]


@icon("person-with-cochlear-implant", CAT, "A head in side view with a round coil on the scalp and a wire running down to the ear.",
      tags=["hearing implant", "deaf", "hearing loss", "implant", "ear", "hearing technology", "audiology"])
def _(S):
    head = u(circle(11, 9.5, 6.5), poly([(16, 7.5), (20, 12), (16, 13)], closed=True), rect(8, 12, 6.5, 9))
    return [shell(head), dot(8, 7.2, 1.7), detail(pl(S, [(8, 9), (8.5, 12.5), (10.5, 14.5)]))]


@icon("person-with-oxygen", CAT, "A figure with a nasal tube leading to a small wheeled oxygen tank.",
      tags=["oxygen therapy", "copd", "nasal cannula", "breathing", "respiratory", "portable oxygen", "lung disease"])
def _(S):
    return [hd(5.5, 4.5), line(seg(5.5, 7.5, 5.5, 14)),
            line(pl(S, [(3.5, 21.5), (5.5, 14), (7.5, 21.5)])),
            line(pl(S, [(5.5, 9.5), (8, 12.5), (10.5, 13.5)])),
            line("M7.5 5.8C11 6.5 12 9 14.5 11"),
            shell(rect(14.5, 8, 5.5, 11, L(S, 2, 2.75))), line(seg(17.25, 5, 17.25, 8)),
            dot(15.5, 21, 1.1), dot(19, 21, 1.1)]


@icon("mobility-scooter-user", CAT, "A seated figure on a four wheeled mobility scooter with a front basket and tiller.",
      tags=["electric scooter", "senior mobility", "disability scooter", "power scooter", "accessible", "elderly", "motorised"])
def _(S):
    return [hd(8, 3.5, 2.25), line(pl(S, [(8, 6.5), (7.5, 12.5), (13, 12.5), (13.5, 15)])),
            line(pl(S, [(8, 8.5), (11.5, 10.5), (15.5, 9.5)])), line(pl(S, [(14, 8), (17, 8)])),
            line(seg(16, 8.5, 16, 15)),
            shell(rect(4.5, 15, 15, 3, L(S, 0.5, 1.5))),
            dot(7, 20.2, 1.8), dot(17.5, 20.2, 1.8),
            shell(rect(18.5, 9.5, 3.5, 3.5, L(S, 0.3, 1)))]


@icon("person-with-knee-scooter", CAT, "A figure resting one bent knee on the pad of a wheeled knee scooter.",
      tags=["knee walker", "injury", "broken ankle", "foot surgery", "recovery", "non weight bearing", "mobility aid"])
def _(S):
    return [hd(8, 4.5), line(seg(8, 7.5, 8, 14)),
            line(pl(S, [(8, 14), (6.5, 21.5)])),
            line(pl(S, [(8, 14), (12.5, 15.5), (9.5, 20)])),
            line(pl(S, [(8, 9.5), (12, 10), (17, 9)])),
            line(seg(17, 8, 17, 19.5)), line(seg(11, 14.5, 17, 14.5)), dot(17, 21, 1.4), dot(10.5, 21, 1.1)]


@icon("person-with-arm-sling", CAT, "A figure with one arm bent in a triangular sling tied at the neck.",
      tags=["broken arm", "shoulder injury", "arm support", "fracture", "recovery", "first aid", "injured"])
def _(S):
    return [hd(11, 4.5), line(seg(11, 7.5, 11, 14)),
            line(pl(S, [(9, 21.5), (11, 14), (13, 21.5)])),
            line(pl(S, [(11, 9), (7, 14)])),
            shell(pl(S, [(10, 11), (19, 11), (19, 15)], closed=True, k=0.4)),
            line(pl(S, [(11, 9), (15, 11)])), dot(20.5, 11.5, 1.2)]


@icon("person-with-neck-brace", CAT, "A head and shoulders figure wearing a tall cervical collar.",
      tags=["cervical collar", "whiplash", "neck injury", "spine", "orthopedic", "brace", "support collar"])
def _(S):
    return [dot(12, 6.2, 3.3), shell(rect(8.5, 9.5, 7, 6, L(S, 1, 2.5))), detail(seg(8.5, 12.5, 15.5, 12.5)),
            shell(bust_d(S, 12, 16, 7.5, 21))]


@icon("person-with-leg-cast", CAT, "A figure on a crutch with one lower leg in a thick cast.",
      tags=["broken leg", "plaster cast", "fracture", "crutches", "injury", "recovery", "orthopedic"])
def _(S):
    return [hd(10, 4.5), line(seg(10, 7.5, 10, 14)),
            line(pl(S, [(10, 14), (8.5, 21.5)])),
            line(pl(S, [(10, 14), (14.5, 16.5)])),
            shell(rect(13, 16.5, 4, 5, L(S, 0.8, 1.8))),
            line(pl(S, [(10, 9.5), (7.5, 13)])), line(seg(8.8, 9, 4, 21.5)), line(seg(6.5, 13.5, 8.5, 13.5))]


@icon("person-with-ear-defenders", CAT, "A head and shoulders figure wearing large over-ear defenders.",
      tags=["ear protection", "noise cancelling", "hearing protection", "sensory", "loud noise", "ear muffs", "quiet"])
def _(S):
    return [dot(12, 10.2, 3.2), line("M5.5 11A6.5 7.5 0 0 1 18.5 11"),
            shell(rect(3.5, 9, 4, 6.5, L(S, 1, 2))), shell(rect(16.5, 9, 4, 6.5, L(S, 1, 2))),
            shell(bust_d(S, 12, 17, 6.5, 21))]


@icon("stairlift-user", CAT, "A seated figure riding a chair that travels along a rail above a staircase.",
      tags=["stair lift", "chair lift", "stairs", "elderly", "mobility", "home adaptation", "accessible home"])
def _(S):
    return [line(poly([(8, 21.5), (12, 21.5), (12, 18.5), (16, 18.5), (16, 15.5), (20, 15.5), (20, 12.5), (22, 12.5)], r=L(S, 0, 0.5))),
            line(seg(2, 17.5, 22, 6)),
            hd(8.5, 3.8, 2.25), line(pl(S, [(8.5, 6.8), (8.5, 11.5), (13.5, 11.5), (14, 15)])),
            line(seg(5.5, 6.5, 5.5, 12)), line(seg(8.5, 11.5, 8.5, 13.5))]


@icon("wheelchair-ramp-user", CAT, "A figure in a wheelchair rolling up a sloped ramp toward a door.",
      tags=["ramp", "accessible entrance", "wheelchair access", "disability", "step free", "accessibility", "mobility"])
def _(S):
    return [shell(pl(S, [(2, 21.5), (15, 14), (22, 14), (22, 21.5)], closed=True, k=0.4), stroke_miterlimit="2"),
            shell(rect(18, 3.5, 4, 8.5, L(S, 0.5, 1.5))),
            hd(8.5, 4.5, 1.9), line(pl(S, [(8.5, 7), (8, 11), (12, 10.5)])),
            shell(circle(8.5, 13.5, 2.6))]


@icon("person-with-gait-trainer", CAT, "A child standing inside a wheeled walking frame with a support sling under the hips.",
      tags=["gait trainer", "walker", "pediatric", "cerebral palsy", "physical therapy", "assisted walking", "mobility frame"])
def _(S):
    return [line(pl(S, [(5, 20), (5, 9.5), (19, 9.5), (19, 20)])),
            hd(12, 4.5, 2), line(seg(12, 7.5, 12, 15)),
            line(pl(S, [(10.5, 21.5), (12, 15), (13.5, 21.5)])),
            line(pl(S, [(5.5, 13.5), (8, 16), (16, 16), (18.5, 13.5)])),
            dot(5, 21, 1.3), dot(19, 21, 1.3)]


@icon("person-with-standing-frame", CAT, "A figure upright in a padded standing frame with straps at the hips and knees.",
      tags=["standing frame", "stander", "supported standing", "physical therapy", "disability", "rehab", "paediatric"])
def _(S):
    return [hd(9, 4.5), line(seg(9, 7.5, 9, 20.5)),
            line(pl(S, [(4.5, 12), (9, 9.5), (13.5, 12)])),
            line(pl(S, [(15.5, 8), (15.5, 20), (21, 20)])),
            line(seg(9, 13.5, 15.5, 13.5)), line(seg(9, 17.5, 15.5, 17.5)),
            dot(7, 21.5, 1.1), dot(19, 21.5, 1.1)]


@icon("person-with-leg-braces", CAT, "A standing figure whose legs wear long braces with side bars and cross straps.",
      tags=["orthosis", "kafo", "leg support", "calipers", "polio", "mobility", "orthopedic brace"])
def _(S):
    return [hd(12, 4.5), line(seg(12, 7.5, 12, 13)),
            line(pl(S, [(6.5, 13), (12, 9.5), (17.5, 13)])),
            line(pl(S, [(12, 13), (9.5, 21.5)])), line(pl(S, [(12, 13), (14.5, 21.5)])),
            line(seg(5.5, 17, 10.7, 17)), line(seg(13.3, 17, 18.5, 17))]


@icon("person-with-ankle-foot-orthosis", CAT, "A lower leg in a molded brace that runs down the calf and under the foot.",
      tags=["afo", "foot drop", "ankle brace", "orthotic", "calf brace", "gait support", "orthopedic"])
def _(S):
    return [shell(poly([(5, 2.5), (14, 2.5), (14, 15.5), (21.5, 15.5), (21.5, 21.5), (5, 21.5)], closed=True, r=L(S, 0, 1.5))),
            detail(seg(5, 6.5, 14, 6.5)), detail(seg(5, 10.5, 14, 10.5))]


@icon("person-with-insulin-pump", CAT, "A figure with a small pump clipped at the waist and a tube running to the belly.",
      tags=["diabetes", "insulin", "pump", "blood sugar", "medical device", "type 1", "glucose"])
def _(S):
    return [hd(8.5, 4.5), line(seg(8.5, 7.5, 8.5, 14)),
            line(pl(S, [(6.5, 21.5), (8.5, 14), (10.5, 21.5)])),
            line(pl(S, [(8.5, 9.5), (5.5, 14)])),
            shell(rect(14.5, 10.5, 6, 8, L(S, 1, 2))), dot(17.5, 13.5, 1.0),
            line("M14.5 16H13Q11 16 10.5 12.5")]


@icon("person-with-feeding-tube", CAT, "A figure beside a pole holding a feed bag, with a tube running to the abdomen.",
      tags=["enteral feeding", "peg tube", "tube feeding", "medical", "nutrition", "gastrostomy", "care"])
def _(S):
    return [hd(6.5, 4.5), line(seg(6.5, 7.5, 6.5, 14)),
            line(pl(S, [(4.5, 21.5), (6.5, 14), (8.5, 21.5)])),
            line(pl(S, [(6.5, 9.5), (4, 14)])),
            line(seg(21.5, 2.5, 21.5, 21.5)), line(pl(S, [(21.5, 2.5), (16.5, 2.5), (16.5, 4)])),
            shell(rect(13.5, 4, 6, 5.5, 2)),
            line("M16.5 9.5V13Q16.5 15 14 15H11Q8.5 15 7.5 12.5")]


@icon("person-with-eye-patch", CAT, "A head and shoulders figure with a patch over one eye held by a strap.",
      tags=["eyepatch", "lazy eye", "amblyopia", "eye injury", "vision", "pirate look", "ophthalmology"])
def _(S):
    return [shell(circle(12, 8.5, 5.5)), shell(bust_d(S, 12, 16.5, 7, 21)),
            detail(seg(6.7, 5.4, 17.3, 11.6)),
            mark(ellipse(14.7, 9.9, 2.4, 2.1)), mark(circle(9.3, 8.2, 0.95))]


@icon("seated-transfer-board", CAT, "A seated figure sliding along a board that bridges a wheelchair and a bed.",
      tags=["slide board", "patient transfer", "wheelchair to bed", "caregiving", "mobility", "rehab", "care transfer"])
def _(S):
    return [line(pl(S, [(3.5, 6), (3.5, 15.5)])), shell(circle(6, 19, 2.2)),
            line(seg(4.5, 15.5, 19.5, 15.5)), shell(rect(17, 15.5, 5.5, 5, L(S, 0.5, 1.5))),
            hd(11, 4.5, 2.25), line(seg(11, 7.5, 11, 13)),
            line(pl(S, [(11, 13), (15, 13), (15, 14)])),
            line(pl(S, [(11, 9.5), (13.5, 12), (14.5, 13)]))]



# ============================================================================ working roles
# Head and shoulders figure on the left (head r 3), one identifying prop on the right.

def bst(S, cx=6.5, hy=9.0, hr=3.0, top=15.0, hw=4.5, bottom=21.0):
    return [shell(circle(cx, hy, hr)), shell(bust_d(S, cx, top, hw, bottom))]


def dome(cx, y, w, h):
    return f"M{fmt(cx - w)} {fmt(y)}A{fmt(w)} {fmt(h)} 0 0 1 {fmt(cx + w)} {fmt(y)}Z"


def rot_pts(pts, deg, cx, cy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rbox(cx, cy, w, h, deg, r=0.0):
    """Rotated rectangle outline (d-string) centred at (cx, cy)."""
    pts = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]
    return poly(rot_pts(pts, deg, cx, cy), closed=True, r=r)


def rot_ellipse(cx, cy, rx, ry, deg):
    """Ellipse rotated by deg (clockwise on screen) as two SVG arcs."""
    a = math.radians(deg)
    p1 = (cx - rx * math.cos(a), cy - rx * math.sin(a))
    p2 = (cx + rx * math.cos(a), cy + rx * math.sin(a))
    return (f"M{fmt(p1[0])} {fmt(p1[1])}A{fmt(rx)} {fmt(ry)} {fmt(deg)} 1 0 {fmt(p2[0])} {fmt(p2[1])}"
            f"A{fmt(rx)} {fmt(ry)} {fmt(deg)} 1 0 {fmt(p1[0])} {fmt(p1[1])}Z")


def chord(cx, cy, r, deg, off):
    """Chord of a circle in direction deg at perpendicular offset off, as a d-string."""
    a = math.radians(deg)
    dx, dy = math.cos(a), math.sin(a)
    nx, ny = -dy, dx
    h = math.sqrt(max(r * r - off * off, 0))
    mx, my = cx + nx * off, cy + ny * off
    return seg(mx - dx * h, my - dy * h, mx + dx * h, my + dy * h)


@icon("cheesemaker", CAT, "A figure in a flat cap holding a round cheese wheel with a wedge cut out.",
      tags=["cheese", "dairy", "fromager", "artisan", "creamery", "cheese wheel", "cheese maker"])
def _(S):
    cx, cy, r = 16.2, 14, 6
    a0, a1 = polar(cx, cy, r, -52), polar(cx, cy, r, -8)
    wheel = (f"M{fmt(cx)} {fmt(cy)}L{fmt(a0[0])} {fmt(a0[1])}A{fmt(r)} {fmt(r)} 0 1 0 {fmt(a1[0])} {fmt(a1[1])}Z")
    return (bst(S, 6, 9.5, 3.0, 15.5, 4.5) + [shell(wheel, stroke_miterlimit="2"), dot(14, 16.5, 0.9),
            dot(17.5, 17.8, 0.8), dot(12.8, 13, 0.7)])


@icon("dairy-farmer", CAT, "A figure in a cap beside a tall milk churn with a lid and two handles.",
      tags=["milk", "dairy", "churn", "farmer", "cattle", "farm", "milkman"])
def _(S):
    churn = pl(S, [(15, 8), (19, 8), (19, 10.5), (21, 12.5), (21, 21), (13, 21), (13, 12.5), (15, 10.5)], closed=True, k=0.3)
    return (bst(S, 5, 9.5, 3.0, 15.5, 4.0) + [shell(dome(5, 7.4, 3.8, 3.2)), line(seg(1.2, 7.4, 8.8, 7.4)),
            shell(churn), line(seg(14, 6, 20, 6)), line(pl(S, [(13, 14), (11.5, 14), (11.5, 17.5), (13, 17.5)])),
            line(pl(S, [(21, 14), (22.5, 14), (22.5, 17.5), (21, 17.5)]))])


@icon("net-fisher", CAT, "A figure throwing a round casting net that spreads open as a circle of mesh.",
      tags=["fisherman", "cast net", "fishing net", "fishing", "angler", "mesh", "net fishing"])
def _(S):
    mesh = [detail(chord(16.5, 10, 5.5, 45, o)) for o in (-3.4, 0, 3.4)] + [detail(chord(16.5, 10, 5.5, -45, o)) for o in (-3.4, 0, 3.4)]
    return [hd(5, 6, 2.25), line(seg(5, 9, 5, 15.5)),
            line(pl(S, [(3, 21.5), (5, 15.5), (7, 21.5)])),
            line(pl(S, [(5, 10.5), (8.5, 7.5), (11, 8.5)])),
            shell(circle(16.5, 10, 5.5))] + mesh


@icon("falconer", CAT, "A figure with a raised gloved arm and a falcon perched on the fist.",
      tags=["falconry", "hawk", "bird of prey", "raptor", "glove", "hawking", "falcon"])
def _(S):
    return [hd(5, 6, 2.25), line(seg(5, 9, 5, 15.5)),
            line(pl(S, [(3, 21.5), (5, 15.5), (7, 21.5)])),
            line(pl(S, [(5, 10.5), (9, 14.5), (13.5, 14.5)])),
            line(pl(S, [(5, 10.5), (2.5, 14)])),
            shell(rot_ellipse(17, 9.2, 4.6, 2.5, -62)), hd(20.2, 4.3, 1.5), line(seg(21.7, 4.6, 23, 5.4)),
            line(seg(16.5, 13.5, 15, 18))]


@icon("dog-trainer", CAT, "A figure with a treat pouch at the hip raising one finger to a sitting dog.",
      tags=["dog training", "obedience", "pet", "puppy class", "treats", "canine", "behaviourist"])
def _(S):
    dog = pl(S, [(15.5, 11.5), (19.5, 10.5), (21.5, 15), (21, 19.5), (14.5, 19.5), (16, 15)], closed=True, k=0.8)
    return (bst(S, 5.5, 9.5, 3.0, 15.5, 4.5) + [mark(rect(8.5, 17.5, 3, 3.2, 0.8)),
            line(pl(S, [(9, 16.5), (11.5, 12.5), (11.5, 7)])),
            shell(dog), hd(17.2, 8, 2.2), line(pl(S, [(15.4, 8.8), (13.8, 9.6)])),
            line(pl(S, [(19, 6.5), (20.8, 9.5)]))])


@icon("helicopter-pilot", CAT, "A figure in a flight helmet with a microphone boom, seated beneath a two blade rotor.",
      tags=["chopper", "aviator", "rotorcraft", "flying", "flight helmet", "aircrew", "rescue pilot"])
def _(S):
    return [line(seg(2, 3, 22, 3)), line(seg(12, 3, 12, 6.5)),
            shell(circle(12, 11, 4.2)), mark(rect(8.4, 10, 7.2, 2.4, 1.2)),
            shell(bust_d(S, 12, 18, 7, 21)),
            line(pl(S, [(8, 13.5), (8.6, 16), (11.2, 16.2)]))]


@icon("deckhand", CAT, "A figure in a knit cap coiling a thick rope around a deck cleat.",
      tags=["sailor", "crew", "deck crew", "mooring", "rope", "seaman", "ship"])
def _(S):
    return (bst(S, 6, 9.5, 3.0, 15.5, 4.5) + [shell(dome(6, 7.8, 3.5, 3.6)), dot(6, 3.5, 1.1)]
            + [line(seg(13.5, 18, 22.5, 18)), line(seg(18, 18, 18, 21.5)),
               line(pl(S, [(14.5, 13), (21.5, 18.5)])), line(pl(S, [(21.5, 13), (14.5, 18.5)])),
               line(pl(S, [(10.5, 14), (14.5, 13)]))])


@icon("lighthouse-keeper", CAT, "A figure holding a lantern at the foot of a striped lighthouse.",
      tags=["lighthouse", "beacon", "coast", "sea", "light keeper", "lamp", "watchman"])
def _(S):
    tower = pl(S, [(15.5, 21.5), (16.8, 9), (21.2, 9), (22.5, 21.5)], closed=True, k=0.4)
    return (bst(S, 5.5, 9.5, 3.0, 15.5, 4.5) +
            [shell(rect(10.5, 15.5, 3, 4.5, 0.8)), line("M10.8 15.5A1.2 1.2 0 0 1 13.2 15.5"),
             shell(tower), detail(seg(16.2, 14, 21.8, 14)),
             shell(rect(16.5, 5.2, 4.5, 3.8, 0.4)), line(pl(S, [(15.5, 5.2), (18.75, 2.5), (22, 5.2)]))])


@icon("toll-collector", CAT, "A figure in a booth window under a canopy roof beside a raised barrier arm.",
      tags=["toll booth", "motorway", "highway", "fee", "barrier", "toll gate", "cashier"])
def _(S):
    return [shell(pl(S, [(1.5, 8.5), (3.5, 4.5), (12.5, 4.5), (14.5, 8.5)], closed=True, k=0.4)),
            shell(rect(3, 10.5, 10, 10.5, L(S, 0.5, 1.5))), dot(8, 14, 1.8), line(seg(5.5, 17.5, 10.5, 17.5)),
            shell(rect(16, 16.5, 3, 5, L(S, 0.3, 1))), line(seg(17.5, 16.5, 22.5, 9)), dot(21, 11, 0.7)]


@icon("telephone-operator", CAT, "A figure in a headset plugging a cord into a switchboard panel of round sockets.",
      tags=["switchboard", "call centre", "headset", "exchange", "retro phone", "receptionist", "patch cord"])
def _(S):
    return (bst(S, 6.5, 10, 3.0, 16, 4.0) + [line(arc(6.5, 10, 5.4, 190, 350)),
            shell(rect(12.8, 3.5, 9.7, 9.5, L(S, 0.5, 1.5))),
            dot(15.3, 6.5, 0.8), dot(17.65, 6.5, 0.8), dot(20, 6.5, 0.8),
            dot(15.3, 10, 0.8), dot(17.65, 10, 0.8), dot(20, 10, 0.8),
            line(pl(S, [(17.65, 13), (17.65, 17.5), (12, 17.5)]))])


@icon("card-dealer", CAT, "A figure in a bow tie fanning playing cards over a stack of chips.",
      tags=["croupier", "casino", "poker", "blackjack", "gambling", "cards", "chips"])
def _(S):
    return (bst(S, 5, 9.5, 3.0, 15.5, 4.0) +
            [mark(poly([(3.2, 14.6), (5, 15.7), (3.2, 16.8)], closed=True)), mark(poly([(6.8, 14.6), (5, 15.7), (6.8, 16.8)], closed=True)),
             shell(rbox(13.3, 8, 4.2, 6.5, -18, L(S, 0.3, 1))), shell(rbox(16.7, 7.4, 4.2, 6.5, 0, L(S, 0.3, 1))),
             shell(rbox(20.1, 8, 4.2, 6.5, 18, L(S, 0.3, 1))),
             shell(ellipse(17, 20.3, 4.2, 1.1)), shell(ellipse(17, 17.5, 4.2, 1.1))])

# ============================================================================ working roles (second group)

@icon("generations", CAT, "Three heads and shoulders in a row, small, medium and large, the oldest with a hair bun.",
      tags=["three generations", "family tree", "ages", "grandparent", "parent", "child", "lineage"])
def _(S):
    return [shell(circle(4.2, 13.2, 1.9)), shell(bust_d(S, 4.2, 17.5, 2.7, 21.5)),
            shell(circle(11.8, 10, 2.5)), shell(bust_d(S, 11.8, 15, 3.0, 21.5)),
            shell(circle(19.3, 7.2, 3.0)), shell(bust_d(S, 19.3, 12.8, 3.7, 21.5)),
            solid(circle(19.3, 2.8, 1.3))]


@icon("companion-aide", CAT, "A standing aide pushing a wheelchair with a seated person from behind.",
      tags=["wheelchair pusher", "carer", "caregiver", "support worker", "personal assistant", "escort", "assisted mobility"])
def _(S):
    return [hd(4, 4.5), line(seg(4, 7.5, 4, 14)),
            line(pl(S, [(2, 21.5), (4, 14), (6, 21.5)])),
            line(pl(S, [(4, 9.5), (7.5, 12), (11.5, 10.5)])),
            line(seg(11.5, 9.5, 11.5, 14)),
            hd(16.5, 5, 2.25), line(pl(S, [(16.5, 8), (16.5, 13), (21.5, 13), (21.5, 17)])),
            shell(circle(16, 18.3, 3.2))]


@icon("usher", CAT, "A figure aiming a small flashlight whose beam spreads over a row of seats.",
      tags=["cinema", "theatre", "theater", "seating", "flashlight", "torch", "aisle"])
def _(S):
    beam = pl(S, [(13.8, 14.2), (22.5, 12), (19.5, 21.5)], closed=True, k=0.4)
    return (bst(S, 5, 10, 3.0, 16, 4.0) +
            [shell(rbox(11, 13.4, 4.4, 2.6, 25, L(S, 0.3, 1.1))), shell(beam), line(pl(S, [(8.5, 16.5), (9, 15)])),
             shell(rect(11.5, 3, 11, 5.5, L(S, 0.5, 1.5)))])


@icon("film-projectionist", CAT, "A figure beside a film projector with two reels on top throwing a beam of light.",
      tags=["cinema", "movie theatre", "projector", "reels", "film", "screening", "projection booth"])
def _(S):
    return (bst(S, 4.8, 9.5, 2.8, 15.5, 3.8) +
            [shell(circle(11.6, 8.2, 1.9)), shell(circle(16, 8.2, 1.9)),
             shell(rect(9.8, 12.6, 8, 7, L(S, 0.5, 1.4))), shell(rect(17.8, 14.4, 2, 3.4, 0.4)),
             line(seg(21, 14.2, 22.5, 12.2)), line(seg(21, 17.8, 22.5, 19.8))])


@icon("stage-manager", CAT, "A figure in a headset holding a clipboard beside the edge of a stage curtain.",
      tags=["theatre", "theater", "backstage", "production", "cue", "clipboard", "show caller"])
def _(S):
    return (bst(S, 6.5, 10, 3.0, 16, 4.2) + [line(arc(6.5, 10, 5.4, 190, 350)),
            shell(rect(11.2, 6.5, 6.8, 12.5, L(S, 0.5, 1.4))), detail(seg(13.2, 10.5, 16, 10.5)), detail(seg(13.2, 14, 16, 14)),
            line("M22 2.5Q19.8 12 22.4 21.5")])


@icon("voice-actor", CAT, "A figure in headphones speaking toward a studio microphone with a round pop filter.",
      tags=["voiceover", "dubbing", "recording studio", "narrator", "microphone", "audiobook", "voice talent"])
def _(S):
    return (bst(S, 6.5, 10, 3.0, 16, 4.2) + [line(arc(6.5, 10, 5.4, 190, 350)),
            shell(ellipse(14.6, 10, 1.2, 3.3)),
            shell(rect(18.8, 5.5, 3, 7, 1.5)), line("M20.3 12.5V21.5")])


@icon("kitchen-porter", CAT, "A figure scrubbing a plate over a deep sink with soap suds.",
      tags=["dishwasher", "dish washing", "scullery", "washing up", "restaurant kitchen", "dishes", "cleaning"])
def _(S):
    return (bst(S, 5.2, 9.5, 3.0, 15.5, 4.2) +
            [shell(circle(16.5, 8.5, 3.2)), shell(rect(11, 15, 11.5, 6.5, L(S, 0.5, 1.6))),
             line(pl(S, [(8.5, 15.5), (10.5, 12), (12.2, 10.5)])), dot(21.2, 11.8, 0.8), dot(12.2, 12.8, 0.8)])


@icon("food-critic", CAT, "A figure with a notepad above a covered serving dish, rating a meal.",
      tags=["restaurant reviewer", "gourmet", "review", "dining", "taste test", "notepad", "cloche"])
def _(S):
    return (bst(S, 5, 9.5, 3.0, 15.5, 4.0) +
            [shell(rect(13.5, 2.5, 8, 9, L(S, 0.5, 1.4))), detail(seg(15.8, 5.8, 19.2, 5.8)), detail(seg(15.8, 8.6, 19.2, 8.6)),
             shell(dome(16.5, 19.5, 5.5, 5)), line(seg(9.5, 19.5, 23, 19.5))])


@icon("babysitter", CAT, "An adult sitting on the floor stacking toy blocks with a small child.",
      tags=["nanny", "childminder", "child care", "playtime", "toy blocks", "kids", "sitter"])
def _(S):
    return [hd(4.5, 8, 2.25), line(pl(S, [(4.5, 11), (4.5, 19), (9, 19)])),
            line(pl(S, [(4.5, 12.5), (7, 14.5), (10.5, 14)])),
            hd(20, 11.5, 1.8), line(pl(S, [(20, 14), (20, 19), (16, 19)])),
            line(pl(S, [(20, 15), (18, 14.5), (16.5, 13.5)])),
            solid(rect(11.2, 15.4, 3.8, 3.8, 0.4)), solid(rect(11.2, 11, 3.8, 3.6, 0.4))]


@icon("social-worker", CAT, "A figure holding a folder marked with a small house and a heart.",
      tags=["case worker", "welfare", "family support", "counsellor", "community care", "case file", "housing"])
def _(S):
    folder = pl(S, [(10.5, 20.5), (10.5, 5.5), (14.5, 5.5), (16, 7.5), (22.5, 7.5), (22.5, 20.5)], closed=True, k=0.4)
    return (bst(S, 5, 9.5, 3.0, 15.5, 4.0) +
            [shell(folder), detail(pl(S, [(13.2, 14), (16.5, 10.8), (19.8, 14)])), mark(heart(16.5, 15.2, 0.95))])


@icon("cafeteria-server", CAT, "A figure in a hairnet holding a ladle over a row of food pans.",
      tags=["lunch lady", "canteen", "school dinner", "serving line", "dinner lady", "hairnet", "cafeteria"])
def _(S):
    return (bst(S, 5, 9.5, 3.0, 15.5, 4.0) + [shell(dome(5, 7.4, 3.5, 3.0))] +
            [line(seg(11.5, 4, 17, 9.2)), shell(circle(18.4, 11, 2)),
             shell(rect(11, 16, 5, 4.5, L(S, 0.3, 1))), shell(rect(17.5, 16, 5, 4.5, L(S, 0.3, 1)))])


@icon("funeral-director", CAT, "A figure in a dark suit and tie standing beside a single tall lily.",
      tags=["undertaker", "mortician", "burial", "memorial", "condolence", "mourning", "lily"])
def _(S):
    lily = "M17.5 10.5C14 9 13.2 5.5 14.2 3C15.8 4 16.8 5 17.5 6.2C18.2 5 19.2 4 20.8 3C21.8 5.5 21 9 17.5 10.5Z"
    return (bst(S, 6, 9.5, 3.0, 15.5, 4.8) +
            [detail(pl(S, [(4, 15.5), (6, 18.5), (8, 15.5)])), mark(poly([(6, 17.6), (5.2, 18.6), (6, 21), (6.8, 18.6)], closed=True)),
             shell(lily), line(seg(17.5, 10.5, 17.5, 21.5)), line(pl(S, [(17.5, 17), (20.8, 14.5)]))])


@icon("surf-instructor", CAT, "A figure carrying a long surfboard under one arm above a rolling wave.",
      tags=["surfing", "surf coach", "surf school", "beach", "surfboard", "waves", "lessons"])
def _(S):
    pts = [(0, -8), (2.8, -2.5), (2.4, 4.5), (1.2, 7.5), (-1.2, 7.5), (-2.4, 4.5), (-2.8, -2.5)]
    board = [(17 + x * math.cos(math.radians(12)) - y * math.sin(math.radians(12)),
              11 + x * math.sin(math.radians(12)) + y * math.cos(math.radians(12))) for x, y in pts]
    return [hd(5, 4.5), line(seg(5, 7.5, 5, 14.5)),
            line(pl(S, [(3, 21.5), (5, 14.5), (7, 21.5)])),
            line(pl(S, [(5, 9.5), (8.5, 11.5), (13, 12)])),
            shell(pl(S, board, closed=True, k=1.2)),
            line("M10 21.5Q12 18.8 14 21.5T18 21.5T22 21.5")]


@icon("martial-arts-instructor", CAT, "A figure in a wrap jacket with a belt standing in a ready stance, fists raised.",
      tags=["karate", "judo", "taekwondo", "sensei", "dojo", "black belt", "gi"])
def _(S):
    return [hd(12, 4.5),
            shell(pl(S, [(8.5, 9.5), (15.5, 9.5), (15.2, 16), (8.8, 16)], closed=True, k=0.5)),
            detail(pl(S, [(10.5, 9.5), (12, 12.5), (13.5, 9.5)])), mark(rect(8.8, 13.4, 6.4, 1.8)),
            line(pl(S, [(8.4, 10.8), (5.8, 13.8), (5.8, 9.5)])), line(pl(S, [(15.6, 10.8), (18.2, 13.8), (18.2, 9.5)])),
            line(seg(10.5, 16, 6.5, 21.5)), line(seg(13.5, 16, 17.5, 21.5))]


@icon("boxing-trainer", CAT, "A figure holding up two padded focus mitts for a boxer to strike.",
      tags=["boxing coach", "pad work", "focus mitts", "gym", "sparring", "punch", "fitness trainer"])
def _(S):
    return [shell(circle(12, 10.5, 3)), shell(bust_d(S, 12, 16.5, 5, 21.5)),
            shell(rect(2.5, 2.5, 5.5, 7, L(S, 1.5, 2.6))), dot(5.25, 6, 1.0),
            shell(rect(16, 2.5, 5.5, 7, L(S, 1.5, 2.6))), dot(18.75, 6, 1.0),
            line(pl(S, [(7.2, 18), (5.2, 14), (5.2, 10.5)])), line(pl(S, [(16.8, 18), (18.8, 14), (18.8, 10.5)]))]


@icon("dockworker", CAT, "A figure in a hard hat beside a shipping container hanging from a crane hook.",
      tags=["longshoreman", "stevedore", "port worker", "container", "harbour", "crane", "shipping"])
def _(S):
    return (bst(S, 5.5, 10, 3.0, 16, 4.5) + [shell(dome(5.5, 7.8, 3.8, 3.4)), line(seg(1.3, 7.8, 9.7, 7.8)),
            line(pl(S, [(17, 2.8), (13, 9)])), line(pl(S, [(17, 2.8), (21, 9)])), dot(17, 2.6, 1.3),
            shell(rect(11.5, 9, 10.5, 8, L(S, 0.4, 1.2))), detail(seg(15.2, 9, 15.2, 17)), detail(seg(18.4, 9, 18.4, 17))])


@icon("tile-setter", CAT, "A kneeling figure with a notched trowel beside a grid of square tiles.",
      tags=["tiler", "tiling", "flooring", "bathroom", "mosaic", "grout", "trowel"])
def _(S):
    return [hd(8, 5.5, 2.25), line(pl(S, [(8, 8.5), (6.5, 14.5), (8.5, 21), (2.5, 21.5)])),
            line(pl(S, [(7.8, 10), (10.5, 12), (12.5, 10.5)])),
            shell(rbox(15, 8.5, 5.5, 2.4, -20, L(S, 0.3, 1))),
            shell(rect(12.5, 13, 10, 8.5, L(S, 0.5, 1.4))), detail(seg(17.5, 13, 17.5, 21.5)), detail(seg(12.5, 17.25, 22.5, 17.25))]
