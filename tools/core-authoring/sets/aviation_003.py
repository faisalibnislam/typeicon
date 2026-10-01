"""TypeIcon Core: aviation (airports, cockpit, cabin, flying), batch 003."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt

CAT = "aviation"


def L(S, a, b):
    return a if S.name == "line" else b


def rc(S, cap):
    return min(S.R, cap)


def bar(p, q, w):
    """Corner points of a rectangle of width w laid along the segment p-q."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = math.hypot(dx, dy)
    nx, ny = -dy / n * w / 2, dx / n * w / 2
    return [(p[0] + nx, p[1] + ny), (q[0] + nx, q[1] + ny), (q[0] - nx, q[1] - ny), (p[0] - nx, p[1] - ny)]


# ============================================================================ chunk 1

@icon("air-race-pylon", CAT, "Tall cone shaped pylon gate with a small airplane banking past it",
      tags=["air race", "pylon", "racing", "air show", "pylon racing", "cone", "aerobatics"])
def _(S):
    pts = [(0, -6.5), (1, -4), (1, -1), (6, 2), (6, 3.5), (1, 2), (1, 4.5), (2.5, 6), (2.5, 7), (0, 6.2),
           (-2.5, 7), (-2.5, 6), (-1, 4.5), (-1, 2), (-6, 3.5), (-6, 2), (-1, -1), (-1, -4)]
    a = math.radians(40)
    c, sn = math.cos(a), math.sin(a)
    plane = [(17.5 + 0.62 * (x * c - y * sn), 9 + 0.62 * (x * sn + y * c)) for x, y in pts]
    return [
        shell(poly([(5, 3), (7, 3), (9.5, 17), (2.5, 17)], closed=True, r=S.r)),
        line(seg(2, 20, 10, 20)),
        shell(poly(plane, closed=True)),
    ]



@icon("seatback-pocket", CAT, "Back of an airline seat with a pocket holding a safety card and a magazine",
      tags=["seat pocket", "seat back", "safety card", "magazine", "airline seat", "cabin", "in-flight"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 19, rc(S, 3))),
        line(poly([(8, 14), (8, 7), (13, 7), (13, 14)], r=S.r)),
        line(poly([(15.5, 14), (15.5, 9.5)])),
        detail(rect(5.5, 13.5, 13, 5, rc(S, 1.5))),
    ]



@icon("cabin-interphone", CAT, "Wall handset on a coiled cord beside a small keypad panel in an aircraft cabin",
      tags=["interphone", "crew call", "cabin phone", "intercom", "handset", "flight attendant", "keypad"])
def _(S):
    return [
        shell(rect(11.5, 3, 10, 18, rc(S, 2.5))),
        dot(15, 12.5, 1.1), dot(18, 12.5, 1.1), dot(15, 16.5, 1.1), dot(18, 16.5, 1.1),
        shell(rect(14, 5.5, 4, 3, rc(S, 1))),
        shell(rect(2.5, 3, 4.5, 8.5, rc(S, 2.25))),
        line(poly([(4.75, 11.5), (4.75, 13), (3.5, 14.5), (6.5, 16.5), (3.5, 18.5), (6.5, 20.5)], r=S.r * 0.6)),
    ]



@icon("engine-indicating-display", CAT, "Cockpit screen with two round arc gauges side by side and bar graphs beneath",
      tags=["engine display", "eicas", "cockpit screen", "gauges", "engine monitor", "instruments", "flight deck"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 17, rc(S, 3))),
        detail(arc(8, 12, 3.5, 180, 360)),
        detail(arc(16, 12, 3.5, 180, 360)),
        detail(seg(8, 12, 9.8, 9.8)),
        detail(seg(16, 12, 17.8, 9.8)),
        detail(seg(5.5, 16.5, 10.5, 16.5)),
        detail(seg(13.5, 16.5, 18.5, 16.5)),
    ]


@icon("airworthiness-certificate", CAT, "Framed certificate with a small airplane at the top and a round seal at the bottom",
      tags=["airworthiness", "certificate", "aircraft registration", "inspection", "approval", "document", "compliance"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 19, rc(S, 2.5))),
        detail(seg(12, 5, 12, 11)),
        detail(poly([(8, 10), (12, 6.5), (16, 10)])),
        detail(circle(12, 16.5, 2)),
    ]


@icon("drop-zone-target", CAT, "Parachute canopy descending toward a round bullseye target on the ground",
      tags=["drop zone", "skydiving", "parachute", "landing target", "bullseye", "airdrop", "accuracy landing"])
def _(S):
    cp = [(12 - 6.5 * math.cos(math.radians(a)), 8 - 6 * math.sin(math.radians(a))) for a in (0, 30, 60, 90, 120, 150, 180)]
    return [
        shell(poly(cp, closed=True, r=S.r)),
        line(poly([(5.5, 8), (12, 12)])), line(poly([(18.5, 8), (12, 12)])),
        shell(circle(12, 18, 3)),
        dot(12, 18, 1),
    ]



# ============================================================================ chunk 2

@icon("crew-rest-bunk", CAT, "Small enclosed aircraft bunk with a curtain half drawn and a pillow inside",
      tags=["crew rest", "bunk", "sleeping berth", "pilot rest", "flight attendant", "long haul", "curtain"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 19, 15, rc(S, 3))),
        detail(rect(5, 8.5, 5, 4, rc(S, 1.5))),
        detail(poly([(5, 16.5), (10, 16.5)])),
        detail(poly([(13.5, 4.5), (14.5, 19.5)])),
        detail(poly([(16.5, 4.5), (16, 19.5)])),
        detail(poly([(19.5, 4.5), (19, 19.5)])),
    ]



@icon("anti-collision-beacon", CAT, "Side view of a fuselage with a small dome lamp on top giving off flashing rays",
      tags=["beacon", "anti-collision light", "strobe", "aircraft lights", "rotating beacon", "ground safety", "engine start"])
def _(S):
    return [
        shell(rect(2.5, 12, 19, 7.5, rc(S, 3.75))),
        shell(poly([(3.5, 12), (3, 7.5), (5.5, 7.5), (9, 12)], closed=True, r=S.r)),
        shell(poly([(11.5, 12), (11.5, 11), (14, 9.5), (16.5, 11), (16.5, 12)], closed=True, r=S.r)),
        dot(10, 15.75, 1), dot(14, 15.75, 1), dot(18, 15.75, 1),
        line(seg(14, 6.5, 14, 3)),
        line(seg(18.5, 8, 20.5, 6)),
        line(seg(9.5, 8, 8.5, 5.5)),
    ]



@icon("gate-check-tag", CAT, "Luggage tag on a looped strap printed with a stroller symbol",
      tags=["gate check", "stroller", "baggage tag", "pram", "luggage tag", "gate valet", "child equipment"])
def _(S):
    return [
        shell(poly([(8, 8), (16, 8), (18.5, 10.5), (18.5, 21), (5.5, 21), (5.5, 10.5)], closed=True, r=S.r)),
        line(poly([(9.5, 8.5), (9.5, 4.5), (10.5, 2.5), (13.5, 2.5), (14.5, 4.5), (14.5, 8.5)], r=S.r)),
        detail(arc(11.5, 15.5, 3, 180, 360)),
        detail(seg(8.5, 15.5, 14.5, 15.5)),
        detail(seg(14.5, 15.5, 16.5, 12)),
        dot(10, 18.6, 1), dot(15, 18.6, 1),
    ]



@icon("wing-spoiler", CAT, "Wing cross section with a panel raised from its upper surface and airflow breaking behind it",
      tags=["spoiler", "airbrake", "wing", "lift dump", "aerodynamics", "flight control", "speedbrake"])
def _(S):
    return [
        shell("M2.5 15C2.5 11.5 6 10 10 10L19 14L10 17.5C5 17.5 2.5 17 2.5 15Z" if S.name == "line" else "M2.5 15C2.5 11.5 6 10 10 10L18.5 14Q19.5 14.5 18.5 15L10 17.5C5 17.5 2.5 17 2.5 15Z"),
        shell(poly(bar((11.5, 9.5), (14.5, 4.5), 3), closed=True, r=S.r * 0.5)),
        line(seg(17.5, 3.5, 21.5, 3.5)),
        line(seg(18.5, 7.5, 21.5, 7.5)),
    ]



@icon("helicopter-collective", CAT, "Angled lever rising from a cockpit floor with a twist grip on its end beside a pilot seat edge",
      tags=["collective", "helicopter control", "throttle grip", "cockpit", "pilot", "lever", "rotorcraft"])
def _(S):
    return [
        line(seg(2.5, 21, 21.5, 21)),
        line(seg(5.5, 21, 10.5, 12)),
        shell(poly(bar((10.5, 12), (14.5, 5.5), 4), closed=True, r=S.r * 0.6)),
        shell(rect(17.5, 9, 4, 12, rc(S, 1.5))),
    ]



@icon("hand-propping", CAT, "Person standing in front of a small plane nose reaching up to swing the propeller by hand",
      tags=["propping", "start engine", "propeller", "swing prop", "light aircraft", "ground handling", "vintage plane"])
def _(S):
    return [
        shell(circle(4.5, 5, 2)),
        line(seg(4.5, 7.5, 4.5, 14.5)),
        line(poly([(4.5, 14.5), (2.5, 21)])), line(poly([(4.5, 14.5), (7, 21)])),
        line(poly([(4.5, 9.5), (8.5, 8), (12.5, 5.5)], r=S.r * 0.5)),
        line(seg(12.5, 5, 12.5, 21)),
        shell(rect(15, 11.5, 6.5, 8, rc(S, 3))),
    ]
