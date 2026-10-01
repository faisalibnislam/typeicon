"""TypeIcon Core: biochem (batch biochem_002).

Genetics diagrams, biomolecules, small molecules, molecular models and wet-lab microbiology equipment.
Rings are polygons, atoms are circles, bonds are plain strokes; everything is a simple symbol at 24 px.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "biochem"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def grow(d, g):
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def tube(d, w):
    return path_to_d(ST(d, w, "round", "round"))


def rot(d, deg, cx=12, cy=12):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def mk(S, x, y, r=1.25):
    """Small mark: square in Line, round in Rounded."""
    if S.name == "rounded":
        return dot(x, y, r)
    return Part("dot", rect(x - r, y - r, 2 * r, 2 * r))


def msolid(S, x, y, r=1.25):
    """Small solid mark in every style (square in Line, round in Rounded)."""
    if S.name == "rounded":
        return solid(circle(x, y, r))
    return solid(rect(x - r, y - r, 2 * r, 2 * r))


def cr(pts, closed=False):
    """Smooth path through points (Catmull-Rom as cubic Beziers)."""
    n = len(pts)
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}"
    return d + ("Z" if closed else "")


def vwave(x, y0, y1, amp, n):
    """Vertical wave (n half-waves) from y0 to y1."""
    h = (y1 - y0) / n
    d = f"M{fmt(x)} {fmt(y0)}"
    for i in range(n):
        sgn = -1 if i % 2 == 0 else 1
        d += f"Q{fmt(x + sgn * 2 * amp)} {fmt(y0 + h * (i + 0.5))} {fmt(x)} {fmt(y0 + h * (i + 1))}"
    return d


def hwave(x0, x1, y, amp, n):
    w = (x1 - x0) / n
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        sgn = -1 if i % 2 == 0 else 1
        d += f"Q{fmt(x0 + w * (i + 0.5))} {fmt(y + sgn * 2 * amp)} {fmt(x0 + w * (i + 1))} {fmt(y)}"
    return d


def ring(S, cx, cy, r, n=6, start=-90, rr=0.9):
    """Skeletal ring polygon (shell)."""
    return shell(poly(regular(cx, cy, r, n, start), closed=True, r=L(S, 0, rr)))


def stick(a, b, ra=0.0, rb=0.0):
    """Bond from a to b, shortened by ra at a and rb at b."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    return line(seg(a[0] + ux * ra, a[1] + uy * ra, b[0] - ux * rb, b[1] - uy * rb))


def helix_pts(cx, y0, y1, amp, turns, phase=0.0, n=17):
    pts = []
    for i in range(n):
        t = i / (n - 1)
        pts.append((cx + amp * math.cos(phase + 2 * math.pi * turns * t), y0 + (y1 - y0) * t))
    return pts


def helix(x, y0, y1, amp=4, turns=1.0, n=17):
    """Two crossing strands (paths)."""
    return (cr(helix_pts(x, y0, y1, amp, turns, 0.0, n)), cr(helix_pts(x, y0, y1, amp, turns, math.pi, n)))


# =========================================================================== genetics

@icon("blastocyst", CAT, "Hollow ball of cells with a small clump of inner cells attached to one side",
      tags=["embryo", "early embryo", "ivf", "stem cells", "development", "biology"])
def _(S):
    return [shell(circle(12, 12, 9)),
            Part("dot", poly(regular(8.4, 8.6, 3.4, 6, 0), closed=True, r=L(S, 0, 1.2))),
            Part("dot", poly(regular(12.2, 6.8, 1.9, 6, 0), closed=True, r=L(S, 0, 0.6)))]


@icon("nucleosome", CAT, "DNA strand wrapped twice around a round histone core like thread on a spool",
      tags=["histone", "chromatin", "dna packaging", "epigenetics", "genetics", "biology"])
def _(S):
    def y(y0, x):
        return y0 + (x - 3) * 4 / 18
    return [shell(rect(7.5, 3.5, 9, 17, 4.5)),
            line(seg(3, y(7, 3), 7.5, y(7, 7.5))), line(seg(16.5, y(7, 16.5), 21, y(7, 21))),
            detail(seg(7.5, y(7, 7.5), 16.5, y(7, 16.5))),
            line(seg(3, y(13, 3), 7.5, y(13, 7.5))), line(seg(16.5, y(13, 16.5), 21, y(13, 21))),
            detail(seg(7.5, y(13, 7.5), 16.5, y(13, 16.5)))]


@icon("dna-base-pair", CAT, "Two matching base blocks joined by dashed bonds between two backbone rails",
      tags=["base pair", "nucleotide", "hydrogen bond", "genetics", "adenine", "dna"])
def _(S):
    r = L(S, 0, 1.6)
    return [line(seg(3.5, 3, 3.5, 21)), line(seg(20.5, 3, 20.5, 21)),
            shell(rect(3.5, 7, 6, 10, min(S.R, 2))), shell(rect(14.5, 7, 6, 10, min(S.R, 2))),
            line(seg(10.5, 9.5, 13.5, 9.5)), line(seg(10.5, 14.5, 13.5, 14.5))]


@icon("dna-transcription", CAT, "Double helix opening into two strands with a single RNA strand peeling away",
      tags=["rna", "mrna", "gene expression", "unzipping", "genetics", "polymerase"])
def _(S):
    return [line("M8 22C8 18 16 18 16 13C16 9 20 8 20 3"),
            line("M16 22C16 18 8 18 8 13C8 9 4 8 4 3"),
            line(vwave(12, 13, 3, 1.4, 4))]


@icon("sex-chromosomes", CAT, "A large X shaped chromosome beside a smaller Y shaped chromosome",
      tags=["xy", "karyotype", "gender", "genetics", "sex determination", "biology"])
def _(S):
    return [line(seg(3, 4, 10.5, 20)), line(seg(10.5, 4, 3, 20)),
            line(poly([(15, 6), (18.5, 12.5), (22, 6)])), line(seg(18.5, 12.5, 18.5, 20))]


@icon("dna-methylation", CAT, "DNA helix with small round methyl tags on short sticks",
      tags=["epigenetics", "methyl group", "gene silencing", "genetics", "tag", "biology"])
def _(S):
    a, b = helix(7, 3, 21, 3.5, 1.0)
    parts = [line(a), line(b)]
    for y in (5, 12, 19):
        parts.append(line(seg(10, y, 15, y)))
        parts.append(solid(circle(18, y, 2.4)))
    return parts


@icon("dna-damage", CAT, "Double helix with one strand snapped and a lightning mark at the break",
      tags=["mutation", "lesion", "strand break", "uv damage", "genetics", "radiation"])
def _(S):
    a, b = helix(13, 3, 21, 4, 1.0)
    return [line(b), line("M17 3C17 6 13.5 7.5 10.5 9.5"), line("M10.8 14.5C13.5 16 17 16.5 17 21"),
            line(poly([(6.5, 8.5), (3.5, 12), (6.5, 12), (3.5, 15.5)]))]


@icon("dna-repair", CAT, "Double helix with an adhesive bandage patch wrapped diagonally across its middle",
      tags=["gene repair", "healing", "mend", "genetics", "crispr", "fix"])
def _(S):
    a, b = helix(12, 2.5, 21.5, 4.5, 1.0)
    band = rot(rect(3.5, 9.5, 17, 5, min(S.R, 2.5)), -45)
    cut = grow(band, 1.2)
    sa = path_to_d(D(ST(a, 2, S.cap, S.join), P(cut)))
    sb = path_to_d(D(ST(b, 2, S.cap, S.join), P(cut)))
    return [solid(sa), solid(sb), shell(band), detail(rot(seg(10, 12, 14, 12), -45)),]


@icon("supercoiled-dna", CAT, "Circular DNA twisted over itself into a tight coil",
      tags=["plasmid", "topology", "twisted dna", "coil", "genetics", "plectoneme"])
def _(S):
    a = [(12 + 4 * math.cos(2 * math.pi * i / 18), 7 + 10 * i / 18) for i in range(19)]
    b = [(12 - 4 * math.cos(2 * math.pi * i / 18), 7 + 10 * i / 18) for i in range(19)]
    return [line(cr(a)), line(cr(b)), line("M16 7A4 4 0 0 0 8 7"), line("M8 17A4 4 0 0 0 16 17")]


@icon("rna-hairpin", CAT, "Single strand folded back on itself with paired rungs and a round loop at the top",
      tags=["stem loop", "secondary structure", "rna folding", "genetics", "molecule", "trna"])
def _(S):
    return [line("M8.5 21V11.5C4.5 9 6 3 12 3C18 3 19.5 9 15.5 11.5V21"),
            line(seg(8.5, 14.5, 15.5, 14.5)), line(seg(8.5, 18.5, 15.5, 18.5))]


@icon("gene-locus", CAT, "Chromosome with one highlighted band and an arrow pointing at it",
      tags=["gene position", "chromosome map", "genetics", "band", "genome", "marker"])
def _(S):
    return [shell(rect(5, 3, 9, 18, 4.5)), detail(seg(5, 9, 14, 9)), detail(seg(5, 13, 14, 13)),
            line(seg(21, 11, 17.5, 11)), line(poly([(19.5, 8.5), (17, 11), (19.5, 13.5)]))]


@icon("operon", CAT, "DNA line with a bent promoter arrow and three gene blocks in a row",
      tags=["promoter", "gene cluster", "lac operon", "bacteria", "genetics", "regulation"])
def _(S):
    rr = min(S.R, 1)
    return [line(seg(2, 19.5, 22, 19.5)), line("M4 19.5V9H8"), line(poly([(6.5, 6.8), (9, 9), (6.5, 11.2)])),
            solid(rect(10.5, 10, 3, 6.5, rr)), solid(rect(15, 10, 3, 6.5, rr)), solid(rect(19.5, 10, 2.5, 6.5, rr))]


@icon("dna-barcoding", CAT, "Short double helix whose rungs turn into a row of barcode stripes",
      tags=["species identification", "dna test", "genetics", "taxonomy", "scan", "barcode"])
def _(S):
    a, b = helix(6.5, 3, 21, 3.5, 1.0, 13)
    rr = min(S.R, 0.8)
    return [line(a), line(b), solid(rect(13, 5, 2, 14, rr)), solid(rect(16.5, 5, 1.5, 14, rr)), solid(rect(19.5, 5, 2.5, 14, rr))]


@icon("bioinformatics", CAT, "DNA double helix beside a pair of code brackets",
      tags=["computational biology", "genomics", "sequence analysis", "code", "data", "genetics"])
def _(S):
    a, b = helix(6, 3, 21, 3.5, 1.0, 13)
    return [line(a), line(b), line(poly([(15, 8), (11.5, 12), (15, 16)])), line(poly([(19, 8), (22.5, 12), (19, 16)]))]


@icon("mrna-vaccine", CAT, "Round lipid nanoparticle with a curly RNA strand inside",
      tags=["vaccine", "lipid nanoparticle", "rna therapy", "immunization", "medicine", "genetics"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(hwave(6.5, 17.5, 12, 2.2, 4)), mk(S, 9.5, 7.2, 1.1), mk(S, 14.5, 16.8, 1.1)]


def fused(polys, shared, S):
    """Fused ring system: one outline for the union plus detail lines for the shared edges."""
    outline = union(*[poly(p, closed=True) for p in polys])
    return [shell(outline)] + [detail(seg(a[0], a[1], b[0], b[1])) for a, b in shared]


def oh(S, c, ang, r0, ln, rd=1.3):
    """Side stick leaving a ring vertex (radial direction ang) with a small solid atom on the end."""
    p0 = polar(c[0], c[1], r0, ang)
    p1 = polar(c[0], c[1], r0 + ln, ang)
    p2 = polar(c[0], c[1], r0 + ln + rd * 0.6, ang)
    return [line(seg(p0[0], p0[1], p1[0], p1[1])), msolid(S, p2[0], p2[1], rd)]


@icon("restriction-enzyme", CAT, "DNA ladder cut by a staggered step break that leaves two sticky end overhangs",
      tags=["sticky ends", "dna cutting", "enzyme", "molecular cloning", "genetics", "scissors"])
def _(S):
    return [line(seg(2, 8, 11.5, 8)), line(seg(2, 16, 7.5, 16)), line(seg(4.5, 8, 4.5, 16)),
            line(seg(15, 8, 22, 8)), line(seg(11, 16, 22, 16)), line(seg(18.5, 8, 18.5, 16)),
            ]


@icon("recombinant-dna", CAT, "Small DNA ring with an inserted solid segment pulled in at the gap",
      tags=["gene cloning", "plasmid", "genetic engineering", "insert", "biotechnology", "splice"])
def _(S):
    ring_d = arc(9, 12, 6.5, 40, 320)
    ins = tube(arc(11.8, 12, 6.5, -30, 30), 4.4)
    return [line(ring_d), solid(ins)]


@icon("glucose-molecule", CAT, "Six sided sugar ring with one oxygen corner and short hydroxyl sticks",
      tags=["sugar", "dextrose", "carbohydrate", "chemistry", "monosaccharide", "blood sugar"])
def _(S):
    c = (12, 12)
    parts = [ring(S, 12, 12, 4.2, 6, -90)]
    for a in (-90, 30, 90, 150, 210):
        parts += oh(S, c, a, 4.2, 3.0)
    parts.append(mk(S, *polar(12, 12, 4.2, -30), 1.2))
    return parts


@icon("fructose-molecule", CAT, "Five sided sugar ring with an oxygen corner and short side sticks",
      tags=["fruit sugar", "ketose", "carbohydrate", "chemistry", "monosaccharide", "sweetener"])
def _(S):
    c = (12, 12.5)
    parts = [ring(S, 12, 12.5, 4.4, 5, -90)]
    for a in (-90, -18, 126, 198):
        parts += oh(S, c, a, 4.4, 3.0)
    parts.append(mk(S, *polar(12, 12.5, 4.4, 54), 1.2))
    return parts


@icon("sucrose-molecule", CAT, "Six sided and five sided sugar rings joined by one bridge",
      tags=["table sugar", "disaccharide", "carbohydrate", "chemistry", "glycosidic bond", "sweetener"])
def _(S):
    return [ring(S, 6.5, 13, 4.2, 6, 0), ring(S, 17.5, 10.5, 3.8, 5, 180),
            line(seg(10.7, 13, 12.2, 11.8)), line(seg(12.2, 11.8, 13.7, 10.5)),
            mk(S, 12.2, 11.8, 1.2)]


@icon("polysaccharide", CAT, "Chain of four sugar rings linked end to end in a zigzag",
      tags=["starch", "cellulose", "glycogen", "carbohydrate", "polymer", "chemistry"])
def _(S):
    cs = [(4.8, 15.5), (9.6, 8.5), (14.4, 15.5), (19.2, 8.5)]
    parts = [ring(S, x, y, 2.9, 6, 0, 0.7) for x, y in cs]
    for (x0, y0), (x1, y1) in zip(cs, cs[1:]):
        a, b = (x0, y0), (x1, y1)
        ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
        p, q = polar(x0, y0, 2.9, ang if False else (-60 if y1 < y0 else 60)), polar(x1, y1, 2.9, (120 if y1 < y0 else -120))
        parts.append(line(seg(p[0], p[1], q[0], q[1])))
    return parts


@icon("atp-molecule", CAT, "Base block joined to a five sided sugar ring with a tail of three phosphate dots",
      tags=["adenosine triphosphate", "energy", "nucleotide", "cell energy", "biochemistry", "phosphate"])
def _(S):
    rr = min(S.R, 1.5)
    return [shell(rect(2.5, 5, 5, 6, rr)), line(seg(7.5, 8.2, 10.4, 7.4)),
            ring(S, 13.5, 8, 3.3, 5, -90, 0.7), line(seg(13.5, 10.8, 13.5, 16.5)),
            solid(circle(7.5, 18.8, 2)), solid(circle(13.5, 18.8, 2)), solid(circle(19.5, 18.8, 2))]


@icon("phospholipid", CAT, "Round head with two long tails hanging down, one of them kinked",
      tags=["lipid", "cell membrane", "bilayer", "fat", "amphipathic", "biochemistry"])
def _(S):
    return [shell(circle(12, 6.5, 3.6)), line(seg(10.3, 10, 10.3, 21)),
            line(poly([(13.7, 10), (13.7, 14), (16, 16.5), (16, 21)]))]


@icon("triglyceride", CAT, "Short vertical backbone with three zigzag fatty chains reaching right like an E",
      tags=["fat", "lipid", "oil", "glycerol", "fatty acids", "biochemistry"])
def _(S):
    def zz(y):
        pts = [(4.5, y)]
        x, up = 4.5, False
        for i in range(4):
            x += 4.4
            pts.append((x, y + (3 if not up else 0)))
            up = not up
        return line(poly(pts, r=S.r * 0.6))
    return [line(seg(4.5, 4, 4.5, 16)), zz(4), zz(10), zz(16)]


@icon("fatty-acid", CAT, "Long zigzag carbon chain with a small forked carboxyl group at one end",
      tags=["lipid", "omega 3", "carboxylic acid", "fat", "chain", "biochemistry"])
def _(S):
    pts = [(2.5, 17), (6, 14.5), (9.5, 17), (13, 14.5)]
    return [line(poly(pts, r=S.r * 0.6)), line(seg(13, 14.5, 16, 9.5)), line(seg(13, 14.5, 17, 16.5)),
            msolid(S, 16.8, 8.2, 1.4), msolid(S, 18.4, 17.3, 1.4)]


def sc(pts, s, dx, dy):
    return [(x * s + dx, y * s + dy) for x, y in pts]


@icon("cholesterol-molecule", CAT, "Four fused rings, three six sided and one five sided, with a short tail and a hydroxyl stick",
      tags=["steroid", "sterol", "lipid", "hdl ldl", "fat", "biochemistry"])
def _(S):
    r = 3.2
    A, B, C = (6.2, 15.2), (6.2 + 1.732 * r, 15.2), (6.2 + 2.598 * r, 15.2 - 1.5 * r)

    def hexa(c):
        return regular(c[0], c[1], r, 6, -90)
    ex = C[0] + 0.866 * r
    pr = r / (2 * math.sin(math.pi / 5))
    pc = (ex + pr * math.cos(math.pi / 5), C[1])
    pent = [polar(pc[0], pc[1], pr, 144 + 72 * k) for k in range(5)]
    shared = [((A[0] + 0.866 * r, A[1] - r / 2), (A[0] + 0.866 * r, A[1] + r / 2)),
              ((B[0] + 0.866 * r, B[1] - r / 2), (B[0], B[1] - r)),
              ((C[0] + 0.866 * r, C[1] - r / 2), (C[0] + 0.866 * r, C[1] + r / 2))]
    parts = fused([hexa(A), hexa(B), hexa(C), pent], shared, S)
    top = pent[2]
    parts.append(line(poly([top, (top[0] + 0.8, top[1] - 3.4), (top[0] - 1.2, top[1] - 5.6)], r=S.r * 0.6)))
    parts += oh(S, A, 90, r, 1.6)
    return parts


@icon("heme-group", CAT, "Square ring of four small five sided rings around a central iron dot",
      tags=["porphyrin", "hemoglobin", "iron", "blood", "biochemistry", "cofactor"])
def _(S):
    parts = [solid(circle(12, 12, 1.7))]
    for ang in (-90, 0, 90, 180):
        c = polar(12, 12, 6.9, ang)
        parts.append(shell(poly(regular(c[0], c[1], 2.6, 5, ang + 180), closed=True, r=L(S, 0, 0.6))))
    return parts


@icon("chlorophyll-molecule", CAT, "Ring of four small rings around a central dot with a long wavy tail",
      tags=["pigment", "photosynthesis", "plant", "green", "magnesium", "biochemistry"])
def _(S):
    parts = [solid(circle(12, 9, 1.3))]
    for ang in (-90, 0, 90, 180):
        c = polar(12, 9, 5.3, ang)
        parts.append(solid(poly(regular(c[0], c[1], 2.4, 5, ang + 180), closed=True, r=L(S, 0, 0.5))))
    parts.append(line(vwave(12, 16, 22, 1.4, 3)))
    return parts


@icon("dopamine-molecule", CAT, "Six sided ring with two hydroxyl sticks and a short chain ending in an amine group",
      tags=["neurotransmitter", "catecholamine", "brain chemistry", "reward", "hormone", "biochemistry"])
def _(S):
    c = (8.5, 10)
    parts = [ring(S, 8.5, 10, 4.8, 6, -90)]
    parts += oh(S, c, 150, 4.8, 2.6) + oh(S, c, 90, 4.8, 2.6)
    p = polar(8.5, 10, 4.8, -30)
    parts.append(line(poly([p, (p[0] + 3.5, p[1] + 2.4), (p[0] + 7, p[1])], r=0)))
    parts.append(msolid(S, p[0] + 8.2, p[1] - 0.6, 1.5))
    return parts


@icon("serotonin-molecule", CAT, "Six sided ring fused to a five sided ring with a hydroxyl stick and a short chain ending in an amine group",
      tags=["neurotransmitter", "happiness hormone", "mood", "indole", "brain chemistry", "biochemistry"])
def _(S):
    r = 4.2
    hc = (8.5, 15.5)
    ex = hc[0] + 0.866 * r
    pr = r / (2 * math.sin(math.pi / 5))
    pc = (ex + pr * math.cos(math.pi / 5), hc[1])
    pent = [polar(pc[0], pc[1], pr, 144 + 72 * k) for k in range(5)]
    parts = fused([regular(hc[0], hc[1], r, 6, -90), pent], [((ex, hc[1] - r / 2), (ex, hc[1] + r / 2))], S)
    parts += oh(S, hc, 210, r, 2.2)
    t = pent[2]
    parts.append(line(poly([t, (t[0] + 0.5, t[1] - 3.6), (t[0] + 3.2, t[1] - 5.2)], r=0)))
    parts.append(msolid(S, t[0] + 4.3, t[1] - 5.8, 1.4))
    return parts


# --------------------------------------------------------------------------- ball and stick helpers

def atom(x, y, r=2.6):
    return solid(circle(x, y, r))


def hyd(S, x, y, r=1.4):
    return msolid(S, x, y, r)


def link(a, b, ra, rb):
    return stick(a, b, ra, rb)


def dbl(a, b, off=1.7):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    nx, ny = -dy / n * off, dx / n * off
    return [line(seg(a[0] + nx, a[1] + ny, b[0] + nx, b[1] + ny)), line(seg(a[0] - nx, a[1] - ny, b[0] - nx, b[1] - ny))]


@icon("insulin-molecule", CAT, "Two short wavy chains, one above the other, linked by two small bridge bars",
      tags=["hormone", "peptide", "diabetes", "protein", "blood sugar", "biochemistry"])
def _(S):
    return [line(hwave(3, 15, 6.5, 1.6, 4)), line(hwave(3, 21, 17.5, 1.6, 6)),
            line(seg(7.5, 9.5, 7.5, 14.5)), line(seg(13.5, 9.5, 13.5, 14.5)),
            msolid(S, 7.5, 12, 1.2), msolid(S, 13.5, 12, 1.2)]


@icon("collagen-triple-helix", CAT, "Three thin strands braided tightly together into a rope",
      tags=["protein", "connective tissue", "skin", "fibre", "triple helix", "biochemistry"])
def _(S):
    parts = []
    for k in range(3):
        ph = 2 * math.pi * k / 3
        pts = [(12 + 4.2 * math.sin(2 * math.pi * 1.5 * i / 16 + ph), 2.5 + 19 * i / 16) for i in range(17)]
        parts.append(line(cr(pts)))
    return parts


@icon("vitamin-c-molecule", CAT, "Five sided ring with hydroxyl sticks and a short side chain with two more hydroxyl groups",
      tags=["ascorbic acid", "vitamin", "antioxidant", "nutrition", "citrus", "chemistry"])
def _(S):
    c = (8, 8.5)
    parts = [ring(S, 8, 8.5, 4.2, 5, -90, 0.7)]
    parts += oh(S, c, 198, 4.2, 2.2, 1.2) + oh(S, c, -90, 4.2, 2.4, 1.2)
    p = polar(8, 8.5, 4.2, 54)
    q = (p[0] + 3.4, p[1] + 3.8)
    parts.append(line(poly([p, q], r=0)))
    parts.append(line(seg(q[0], q[1], q[0] + 4.8, q[1] - 1.8)))
    parts.append(msolid(S, q[0] + 5.8, q[1] - 2.2, 1.3))
    parts.append(line(seg(q[0], q[1], q[0], q[1] + 3.6)))
    parts.append(msolid(S, q[0], q[1] + 4.6, 1.3))
    return parts


@icon("penicillin-molecule", CAT, "Small four sided ring fused to a five sided ring with a side chain and an acid group",
      tags=["antibiotic", "beta lactam", "drug", "medicine", "mold", "chemistry"])
def _(S):
    sq = [(3.5, 10), (9, 10), (9, 15.5), (3.5, 15.5)]
    pr = 5.5 / (2 * math.sin(math.pi / 5))
    pc = (9 + 5.5 / (2 * math.tan(math.pi / 5)), 12.75)
    pent = [polar(pc[0], pc[1], pr, 144 + 72 * k) for k in range(5)]
    parts = fused([sq, pent], [((9, 10), (9, 15.5))], S)
    t = pent[4]
    parts.append(line(poly([t, (t[0] - 1.5, t[1] - 3.6)])))
    parts.append(line(seg(t[0], t[1], t[0] + 3.8, t[1] - 3)))
    parts.append(msolid(S, t[0] - 1.9, t[1] - 4.8, 1.3))
    parts.append(msolid(S, t[0] + 5, t[1] - 3.8, 1.3))
    parts.append(line(poly([(3.5, 15.5), (2.5, 19.5)])))
    return parts


@icon("hormone-receptor", CAT, "Cup shaped receptor sitting in a membrane with a small molecule dropping in",
      tags=["ligand", "cell signalling", "binding site", "membrane protein", "endocrine", "biochemistry"])
def _(S):
    return [line("M7.5 8V15A4.5 4.5 0 0 0 16.5 15V8"), line(seg(2, 12, 7.5, 12)), line(seg(16.5, 12, 22, 12)),
            solid(circle(12, 8.5, 2.4))]


@icon("antigen", CAT, "Spiky round particle with a Y shaped antibody docking onto its notch",
      tags=["antibody", "immune response", "pathogen", "immunology", "epitope", "binding"])
def _(S):
    parts = [shell(circle(8.5, 12, 3.6))]
    for a in (-90, -45, 45, 90, 135, 180, 225):
        p = polar(8.5, 12, 3.6, a)
        q = polar(8.5, 12, 6.4, a)
        parts.append(line(seg(p[0], p[1], q[0], q[1])))
    parts.append(solid(poly([(12, 10), (15, 12), (12, 14)], closed=True, r=L(S, 0, 0.6))))
    parts.append(line(seg(22, 12, 18.5, 12)))
    parts.append(line(seg(18.5, 12, 16.5, 6)))
    parts.append(line(seg(18.5, 12, 16.5, 18)))
    return parts


@icon("ethanol-molecule", CAT, "Two linked carbon balls with small hydrogen balls around them and an oxygen with its hydrogen at one end",
      tags=["alcohol", "ethyl alcohol", "drink", "chemistry", "ball and stick", "c2h5oh"])
def _(S):
    c1, c2, o = (6, 13), (12.5, 9.5), (19, 13)
    hs = [(c1, (3, 6.5)), (c1, (3, 19)), (c2, (12.5, 3.2)), (o, (21, 19.5))]
    parts = [link(c1, c2, 2.6, 2.6), link(c2, o, 2.6, 2.4)]
    for a, h in hs:
        parts.append(link(a, h, 2.6, 1.2))
        parts.append(hyd(S, *h, 1.4))
    parts += [atom(*c1), atom(*c2), atom(*o, 2.4)]
    return parts


@icon("ammonia-molecule", CAT, "Central nitrogen ball with three hydrogen balls splayed below like a tripod",
      tags=["nh3", "nitrogen", "fertilizer", "gas", "chemistry", "ball and stick"])
def _(S):
    n = (12, 7.5)
    hs = [(4.5, 17), (12, 20), (19.5, 17)]
    parts = [link(n, h, 3, 1.4) for h in hs]
    parts += [hyd(S, *h, 1.9) for h in hs]
    parts.append(atom(*n, 3.2))
    return parts


@icon("ozone-molecule", CAT, "Three oxygen balls joined in a bent V shape",
      tags=["o3", "ozone layer", "oxygen", "atmosphere", "chemistry", "ball and stick"])
def _(S):
    a, b, c = (4.5, 17), (12, 7.5), (19.5, 17)
    r = L(S, 2.4, 2.9)
    return [link(a, b, r, r), link(b, c, r, r), atom(*a, r), atom(*b, r), atom(*c, r)]


@icon("hydrogen-peroxide-molecule", CAT, "Two joined oxygen balls with a hydrogen ball on each end, twisted like an open book",
      tags=["h2o2", "bleach", "antiseptic", "oxidizer", "chemistry", "ball and stick"])
def _(S):
    o1, o2 = (8.5, 13), (15.5, 11)
    h1, h2 = (3, 7), (21, 17)
    return [link(o1, o2, 2.6, 2.6), link(o1, h1, 2.6, 1.2), link(o2, h2, 2.6, 1.2),
            hyd(S, *h1, 1.5), hyd(S, *h2, 1.5), atom(*o1), atom(*o2)]


@icon("sulfuric-acid-molecule", CAT, "Central sulfur ball with four oxygen balls around it, two capped by small hydrogen balls",
      tags=["h2so4", "acid", "battery acid", "corrosive", "chemistry", "ball and stick"])
def _(S):
    s0 = (12, 12)
    os_ = [(12, 4.5), (12, 19.5), (4.5, 12), (19.5, 12)]
    parts = [link(s0, o, 3, 2.2) for o in os_]
    parts += [link((4.5, 12), (2.5, 18.5), 2.2, 1.2), link((19.5, 12), (21.5, 5.5), 2.2, 1.2),
              hyd(S, 2.5, 18.5, 1.4), hyd(S, 21.5, 5.5, 1.4)]
    parts += [atom(*o, 2.2) for o in os_]
    parts.append(atom(12, 12, 3.2))
    return parts


@icon("ethylene-molecule", CAT, "Two carbon balls joined by a double bar with two hydrogen balls on each end",
      tags=["ethene", "c2h4", "plant hormone", "alkene", "chemistry", "double bond"])
def _(S):
    c1, c2 = (8, 12), (16, 12)
    parts = dbl((10.6, 12), (13.4, 12), 1.7)
    for c, hs in ((c1, [(3, 6), (3, 18)]), (c2, [(21, 6), (21, 18)])):
        for h in hs:
            parts.append(link(c, h, 2.8, 1.2))
            parts.append(hyd(S, *h, 1.4))
    parts += [atom(*c1, 3), atom(*c2, 3)]
    return parts


@icon("acetic-acid-molecule", CAT, "Two carbon skeleton with a doubled oxygen at the upper right and a hydroxyl oxygen at the lower right",
      tags=["vinegar", "ethanoic acid", "carboxylic acid", "ch3cooh", "chemistry", "skeletal formula"])
def _(S):
    a, b = (3, 16), (9.5, 12)
    o2, oh_ = (13, 4.5), (16.5, 16)
    return [line(poly([a, b, oh_], r=0)) if False else line(seg(a[0], a[1], b[0], b[1])),
            line(seg(b[0], b[1], 15.5, 15.4)), *dbl(b, (12.4, 6.6), 1.7),
            msolid(S, 13.2, 4.6, 1.8), msolid(S, 17.8, 16.8, 1.8)]


@icon("naphthalene", CAT, "Two six sided rings fused side by side sharing one edge, with inner double bond lines",
      tags=["aromatic", "mothball", "polycyclic", "hydrocarbon", "chemistry", "c10h8"])
def _(S):
    r = 4.6
    w = 0.866 * r
    c1, c2 = (12 - w, 12), (12 + w, 12)
    polys = [regular(c1[0], c1[1], r, 6, -90), regular(c2[0], c2[1], r, 6, -90)]
    parts = fused(polys, [((12, 12 - r / 2), (12, 12 + r / 2))], S)
    for c, sgn in ((c1, -1), (c2, 1)):
        parts.append(detail(seg(c[0] + sgn * 2.2, c[1] - 1.9, c[0] + sgn * 2.2, c[1] + 1.9)) if False else Part("detail", seg(c[0] - 1.6, c[1] + 2.3, c[0] + 1.6, c[1] + 2.3)))
    return parts


@icon("cyclopentane-ring", CAT, "Single five sided ring with a small carbon dot at each corner",
      tags=["cycloalkane", "hydrocarbon", "ring", "c5h10", "chemistry", "skeletal formula"])
def _(S):
    pts = regular(12, 12.5, 7.5, 5, -90)
    return [line(poly(pts, closed=True, r=L(S, 0, 1.5)))] + [mk(S, x, y, 1.9) if False else solid(circle(x, y, 1.9)) if S.name == "rounded" else solid(rect(x - 1.7, y - 1.7, 3.4, 3.4)) for x, y in pts]


@icon("graphite-structure", CAT, "Three flat slanted sheets stacked in parallel layers",
      tags=["carbon", "layers", "graphene", "pencil lead", "crystal", "chemistry"])
def _(S):
    return [shell(poly([(7, y), (21, y), (17, y + 3), (3, y + 3)], closed=True, r=L(S, 0, 0.8))) for y in (3.5, 10.5, 17.5)]


@icon("ferrocene", CAT, "Iron atom dot sandwiched between two flat five sided rings, one above and one below",
      tags=["sandwich compound", "organometallic", "iron", "cyclopentadienyl", "chemistry", "metallocene"])
def _(S):
    def fl(cy, sgn):
        return [(12 + 8.5 * math.cos(math.radians(a)), cy + sgn * 3.4 * math.sin(math.radians(a))) for a in (-90, -18, 54, 126, 198)]
    r = L(S, 0, 1.2)
    return [shell(poly(fl(6.2, 1), closed=True, r=r)), shell(poly(fl(17.8, -1), closed=True, r=r)), solid(circle(12, 12, 1.6))]


@icon("dendrimer", CAT, "Central dot with branches that fork again and again outward like a round snowflake tree",
      tags=["branched polymer", "nanoparticle", "tree molecule", "macromolecule", "chemistry", "nanotechnology"])
def _(S):
    parts = [solid(circle(12, 12, 1.7))]
    for k in range(4):
        a = 45 + 90 * k
        p = polar(12, 12, 3.4, a)
        parts.append(line(seg(12, 12, p[0], p[1])))
        for da in (-42, 42):
            q = polar(p[0], p[1], 4.0, a + da)
            parts.append(line(seg(p[0], p[1], q[0], q[1])))
            parts.append(msolid(S, q[0], q[1], 1.3))
    return parts


@icon("rotaxane", CAT, "Dumbbell shaped rod with a big round stopper at each end and a ring threaded around its middle",
      tags=["molecular machine", "mechanically interlocked", "nanotechnology", "supramolecular", "chemistry", "ring on rod"])
def _(S):
    rr = L(S, 1.0, 3.0)
    return [line(seg(5, 12, 19, 12)), solid(rect(1.5, 9, 6, 6, rr)), solid(rect(16.5, 9, 6, 6, rr)),
            line(ellipse(12, 12, 3.4, 6.2))]


@icon("cross-linked-polymer", CAT, "Three parallel wavy chains joined at intervals by short bridge bonds",
      tags=["polymer network", "vulcanized rubber", "gel", "plastic", "chemistry", "crosslink"])
def _(S):
    parts = [line(hwave(2, 22, y, 1.3, 8)) for y in (5, 12, 19)]
    parts += [line(seg(7, 5, 7, 12)), line(seg(17, 5, 17, 12)), line(seg(12, 12, 12, 19))]
    return parts


@icon("tetrahedral-molecule", CAT, "Central atom with four bonds toward the corners of a tetrahedron, one wedge and one dashed",
      tags=["vsepr", "molecular geometry", "methane", "3d structure", "chemistry", "stereochemistry"])
def _(S):
    c = (11, 12)
    parts = [line(seg(11, 12, 11, 3.5)), line(seg(11, 12, 4, 18.5)),
             solid(poly([(11, 12), (19.5, 15), (17, 19.5)], closed=True, r=0))]
    for t0, t1 in ((0.25, 0.45), (0.55, 0.75), (0.85, 1.0)):
        a = (c[0] + (20 - c[0]) * t0, c[1] + (6 - c[1]) * t0)
        b = (c[0] + (20 - c[0]) * t1, c[1] + (6 - c[1]) * t1)
        parts.append(line(seg(a[0], a[1], b[0], b[1])))
    parts.append(atom(11, 12, 2.6))
    return parts


@icon("octahedral-molecule", CAT, "Central atom with six bonds along three crossing axes, each ending in a dot",
      tags=["coordination complex", "vsepr", "molecular geometry", "sf6", "3d structure", "chemistry"])
def _(S):
    ends = [(12, 3), (12, 21), (3, 14.5), (21, 9.5), (6.5, 6.5), (17.5, 17.5)]
    parts = [line(seg(12, 3, 12, 21)), line(seg(3, 14.5, 21, 9.5)), line(seg(6.5, 6.5, 17.5, 17.5))]
    parts += [msolid(S, x, y, 1.8) for x, y in ends]
    parts.append(atom(12, 12, 2.4))
    return parts


@icon("trigonal-planar-molecule", CAT, "Central atom with three bonds spread evenly at 120 degrees on a flat plane",
      tags=["vsepr", "molecular geometry", "bf3", "flat molecule", "chemistry", "120 degrees"])
def _(S):
    c = (12, 12.5)
    ends = [polar(c[0], c[1], 9, a) for a in (-90, 30, 150)]
    re = L(S, 2.0, 2.5)
    parts = [link(c, e, 2.4, re) for e in ends]
    parts += [atom(e[0], e[1], re) for e in ends]
    parts.append(shell(circle(c[0], c[1], 2.4)))
    return parts


@icon("space-filling-model", CAT, "Four overlapping spheres fused into one lumpy molecule shape",
      tags=["van der waals", "cpk model", "molecular model", "3d molecule", "chemistry", "spheres"])
def _(S):
    outline = union(circle(9, 10, 5.8), circle(16.5, 9, 4.4), circle(14, 16.5, 4.8), circle(7, 17, 3.6))
    return [shell(outline), detail(arc(9, 10, 3.3, 200, 290)) if False else detail(arc(14, 16.5, 2.2, 180, 300))]


@icon("dipole-molecule", CAT, "Bent three ball molecule with a crossed arrow below showing the direction of the dipole",
      tags=["polar molecule", "partial charge", "water", "electronegativity", "chemistry", "polarity"])
def _(S):
    o, h1, h2 = (10, 6.5), (4.5, 13), (15.5, 13)
    parts = [link(o, h1, 2.8, 1.6), link(o, h2, 2.8, 1.6), atom(*o, 2.8), hyd(S, *h1, 1.7), hyd(S, *h2, 1.7)]
    parts += [line(seg(5, 19, 19.5, 19)), line(seg(5, 16.5, 5, 21.5)),
              line(poly([(16.5, 16.3), (19.5, 19), (16.5, 21.7)]))]
    return parts


@icon("ion-atom", CAT, "Round atom with a nucleus, an orbit with electrons and a bold plus sign",
      tags=["cation", "charged atom", "ionization", "electron", "chemistry", "charge"])
def _(S):
    c = (10, 14)
    parts = [line(circle(10, 14, 7)), solid(circle(10, 14, 2.4))]
    for a in (150, 270):
        p = polar(10, 14, 7, a)
        parts.append(solid(circle(p[0], p[1], 1.9)))
    parts += [line(seg(18.5, 2.5, 18.5, 8.5)), line(seg(15.5, 5.5, 21.5, 5.5))]
    return parts


@icon("free-radical", CAT, "Small two ball molecule with a single unpaired dot beside it and a small spark",
      tags=["unpaired electron", "reactive species", "oxidative stress", "antioxidant", "chemistry", "radical"])
def _(S):
    a, b = (6, 16), (14, 16)
    parts = [link(a, b, 2.8, 2.8), atom(*a, 2.8), atom(*b, 2.8), solid(circle(17.5, 10.5, 1.8))]
    for ang in (-150, -90, -30):
        p = polar(17.5, 10.5, 3.6, ang)
        q = polar(17.5, 10.5, 5.4, ang)
        parts.append(line(seg(p[0], p[1], q[0], q[1])))
    return parts


@icon("polymerization", CAT, "Single small units on the left turning into a linked chain on the right, with an arrow between",
      tags=["monomer", "polymer chain", "plastic", "chain growth", "chemistry", "reaction"])
def _(S):
    parts = [shell(circle(4.5, y, 1.7)) for y in (5, 12, 19)]
    parts += [line(seg(9, 12, 13, 12)), line(poly([(11.2, 9.8), (13.4, 12), (11.2, 14.2)]))]
    parts += [shell(circle(19, y, 1.7)) for y in (4.5, 12, 19.5)]
    parts += [line(seg(19, 6.2, 19, 10.3)), line(seg(19, 13.7, 19, 17.8))]
    return parts


@icon("resonance-structures", CAT, "Two six sided rings with their inner bonds swapped, joined by a double headed arrow",
      tags=["benzene", "kekule", "delocalization", "aromatic", "chemistry", "electron pairs"])
def _(S):
    parts = [ring(S, 5.8, 12, 4.4, 6, -90, 0.7), ring(S, 18.2, 12, 4.4, 6, -90, 0.7)]
    parts.append(Part("dot", poly(regular(5.8, 12.4, 1.7, 3, -90), closed=True)))
    parts.append(Part("dot", poly(regular(18.2, 11.6, 1.7, 3, 90), closed=True)))
    parts += [line(seg(11, 12, 13, 12)), line(poly([(11.8, 10.6), (10.4, 12), (11.8, 13.4)])),
              line(poly([(12.2, 10.6), (13.6, 12), (12.2, 13.4)]))]
    return parts


@icon("cis-trans-isomers", CAT, "Two double bond molecules, one with both marked groups on the same side and one with them on opposite sides",
      tags=["geometric isomers", "stereoisomers", "alkene", "z e isomers", "chemistry", "double bond"])
def _(S):
    def mol(yc, d1, d2):
        parts = dbl((8, yc), (16, yc), 1.4)
        for x0, sgn, d in ((8, -1, d1), (16, 1, d2)):
            e = (x0 + sgn * 3.4, yc + d * 4.0)
            parts.append(line(seg(x0, yc, e[0], e[1])))
            parts.append(msolid(S, e[0] + sgn * 0.8, e[1] + d * 0.8, 1.7))
        return parts
    return mol(8.5, -1, -1) + mol(16.5, -1, 1)


@icon("entropy", CAT, "Neat grid of dots on the left and the same dots scattered randomly on the right, with an arrow between",
      tags=["disorder", "thermodynamics", "randomness", "second law", "physics", "chemistry"])
def _(S):
    parts = [msolid(S, x, y, 1.4) for x in (3.5, 7.5) for y in (6, 12, 18)]
    parts += [line(seg(10.8, 12, 13.8, 12)), line(poly([(12.4, 10.2), (14.2, 12), (12.4, 13.8)]))]
    for x, y in ((17, 5), (21, 9), (16.5, 11.5), (20.5, 14.5), (17.5, 18.5), (21.5, 20.5)):
        parts.append(msolid(S, x, y, 1.4))
    return parts


@icon("salt-bridge", CAT, "Inverted U shaped tube joining the tops of two beakers",
      tags=["electrochemistry", "galvanic cell", "voltaic cell", "electrolyte", "chemistry", "lab"])
def _(S):
    return [line("M3 12V20.5H9.5V12"), line("M14.5 12V20.5H21V12"),
            line("M6.2 15V9A5.8 5.8 0 0 1 17.8 9V15"),
            mk(S, 6.2, 18.3, 1.0),
            mk(S, 17.8, 18.3, 1.0)]


# =========================================================================== wet lab equipment

def drop_d(cx, top, w, h):
    """Small teardrop with its point up: tip at (cx, top), round bottom of width w, total height h."""
    ys = top + h - w / 2
    k = ys - top
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + w * 0.2)} {fmt(top + k * 0.4)} {fmt(cx + w / 2)} {fmt(ys - k * 0.3)} "
            f"{fmt(cx + w / 2)} {fmt(ys)}A{fmt(w / 2)} {fmt(w / 2)} 0 0 1 {fmt(cx - w / 2)} {fmt(ys)}"
            f"C{fmt(cx - w / 2)} {fmt(ys - k * 0.3)} {fmt(cx - w * 0.2)} {fmt(top + k * 0.4)} {fmt(cx)} {fmt(top)}Z")


@icon("gram-stain", CAT, "Glass slide holding small round and rod shaped cells, with a stain drop falling from above",
      tags=["bacteria", "microscope slide", "staining", "microbiology", "gram positive", "lab test"])
def _(S):
    return [shell(rect(2.5, 13, 19, 7.5, min(S.R, 2))),
            Part("dot", circle(7, 16.8, 1.6)), detail(seg(11, 16.8, 14, 16.8)), Part("dot", circle(17.5, 16.8, 1.6)),
            solid(drop_d(12, 2, 5, 7))]


@icon("coplin-jar", CAT, "Small upright glass jar with a lid and several microscope slides standing inside",
      tags=["staining jar", "slide jar", "histology", "lab glassware", "microscope slides", "microbiology"])
def _(S):
    return [solid(rect(4.5, 2.5, 15, 3, min(S.R, 1.2))), shell(rect(5.5, 6.5, 13, 15, min(S.R, 2.5))),
            detail(seg(9, 9, 9, 19)), detail(seg(12, 9, 12, 19)), detail(seg(15, 9, 15, 19))]


@icon("cell-spreader", CAT, "Thin rod bent into an L shape, spreading liquid across an open petri dish",
      tags=["hockey stick", "bacterial plating", "agar plate", "inoculation", "microbiology", "lab tool"])
def _(S):
    return [shell(rect(2.5, 15.5, 19, 5.5, min(S.R, 2))),
            line(poly([(21, 3), (11.5, 13.5), (5.5, 13.5)], r=S.r))]


@icon("serial-dilution", CAT, "Row of three test tubes, each holding less liquid than the last, with curved arrows between them",
      tags=["dilution series", "titration", "lab technique", "concentration", "microbiology", "test tubes"])
def _(S):
    parts = []
    for x, top in ((4.5, 11.5), (12, 14.5), (19.5, 17)):
        parts.append(shell(rect(x - 2.5, 9.5, 5, 12, 2.5)))
        parts.append(Part("dot", rect(x - 1.5, top, 3, 20.5 - top, 1.2)))
    parts += [line("M5.5 6.5Q8.5 2 11.5 6"), line("M12.5 6.5Q15.5 2 18.5 6")]
    return parts


@icon("colony-counter", CAT, "Petri dish with several colony dots under a magnifying lens on an arm",
      tags=["cfu", "bacterial colonies", "plate count", "magnifier", "microbiology", "lab equipment"])
def _(S):
    parts = [shell(circle(9.5, 14.5, 7.5)), Part("dot", circle(7, 13, 1.4)), Part("dot", circle(11.5, 17, 1.4)),
             Part("dot", circle(11.5, 12, 1.2)),
             line(circle(18, 6.5, 3.2)), line(seg(20.4, 4.1, 22, 2.5))]
    return parts


@icon("replica-plating", CAT, "Round velvet covered stamp pressed down onto a petri dish with colony dots",
      tags=["velveteen", "agar plate", "colony transfer", "screening", "microbiology", "lab technique"])
def _(S):
    return [shell(rect(2.5, 16.5, 19, 5, min(S.R, 2))), shell(rect(5.5, 7.5, 13, 4.5, min(S.R, 2))),
            line(seg(12, 2, 12, 7.5)),
            line(seg(8, 12, 8, 15)), line(seg(12, 12, 12, 15)), line(seg(16, 12, 16, 15))]


@icon("pipette-controller", CAT, "Pistol grip pipette gun with a long thin graduated pipette fitted at the front",
      tags=["pipette filler", "pipettor", "serological pipette", "lab tool", "liquid handling", "microbiology"])
def _(S):
    body = union(rect(2.5, 4.5, 11.5, 7.5, 3), rect(4.5, 10.5, 5.5, 10.5, 1.5))
    return [shell(body), detail(seg(6, 8.2, 10, 8.2)),
            line(seg(14, 8.2, 22, 8.2)), line(seg(17, 5, 17, 6.6)), line(seg(20, 5, 20, 6.6))]


@icon("cell-scraper", CAT, "Long handle ending in a small angled flat blade, like a tiny squeegee",
      tags=["tissue culture", "adherent cells", "harvest", "lab tool", "scraping", "microbiology"])
def _(S):
    blade = rot(rect(12.5, 5.3, 9.5, 3.4, min(S.R, 1.4)), 45, 17, 7)
    return [line(seg(3, 21, 15, 9)), shell(blade)]


@icon("dounce-homogenizer", CAT, "Tall narrow glass tube with a round ended pestle plunged inside it",
      tags=["tissue grinder", "cell lysis", "glass pestle", "sample prep", "lab glassware", "microbiology"])
def _(S):
    return [line("M7.5 5.5V16A4.5 4.5 0 0 0 16.5 16V5.5"), line(seg(5, 5.5, 19, 5.5)),
            line(seg(12, 2.5, 12, 12.5)), solid(circle(12, 15.3, 2.7))]


@icon("cell-strainer", CAT, "Small mesh cup sitting on top of the opening of a conical tube",
      tags=["filter", "sieve", "cell suspension", "centrifuge tube", "lab consumable", "microbiology"])
def _(S):
    return [shell(poly([(3.5, 3.5), (20.5, 3.5), (17.5, 11.5), (6.5, 11.5)], closed=True, r=L(S, 0, 1.2))),
            detail(seg(9.2, 5.5, 9.2, 10.5)), detail(seg(12, 5.5, 12, 10.5)), detail(seg(14.8, 5.5, 14.8, 10.5)),
            shell(poly([(7, 13), (17, 13), (14, 21.5), (10, 21.5)], closed=True, r=L(S, 0, 0.8)))]


@icon("syringe-filter", CAT, "Small round disc filter fitted on the tip of a syringe, with a drop falling below",
      tags=["membrane filter", "sterile filtration", "lab consumable", "sample prep", "syringe", "microbiology"])
def _(S):
    return [line(seg(8, 1.5, 16, 1.5)), shell(rect(8.5, 3.5, 7, 6.5, min(S.R, 2))), detail(seg(12, 4.5, 12, 7.5)),
            shell(rect(4.5, 11, 15, 4.5, min(S.R, 2))), solid(drop_d(12, 17, 3.4, 5))]


@icon("heat-block", CAT, "Flat metal block with tubes standing in its holes and a temperature display on the front",
      tags=["dry bath", "thermoblock", "incubator", "lab equipment", "sample heating", "microbiology"])
def _(S):
    return [shell(rect(2.5, 10, 19, 10.5, min(S.R, 3))), shell(rect(5, 3.5, 3.4, 6.5, 1.2)),
            shell(rect(10.3, 3.5, 3.4, 6.5, 1.2)), shell(rect(15.6, 3.5, 3.4, 6.5, 1.2)),
            detail(seg(6, 15.2, 11, 15.2)), mk(S, 15.5, 15.2, 1.2), mk(S, 18.5, 15.2, 1.2)]


@icon("flow-cytometry", CAT, "Thin stream carrying single round cells in a line through a laser beam, with a detector beside it",
      tags=["facs", "cell sorting", "laser", "cell counting", "immunology", "lab instrument"])
def _(S):
    return [line(seg(8, 2, 8, 22)), solid(circle(8, 5, 2.3)), solid(circle(8, 10, 2.3)),
            line(seg(1.5, 16.5, 8, 16.5)), line(seg(8, 16.5, 15.5, 16.5)),
            shell(rect(15.5, 11.5, 6, 10, min(S.R, 2)))]


@icon("nanopore-sequencing", CAT, "Single DNA strand threading through a small pore in a membrane band, with a signal line below",
      tags=["dna reading", "oxford nanopore", "long read", "genomics", "sequencer", "lab technology"])
def _(S):
    rr = min(S.R, 1.5)
    return [solid(rect(2, 8, 8, 3.2, rr)), solid(rect(14, 8, 8, 3.2, rr)), line(seg(12, 2, 12, 15.5)),
            line(poly([(2, 21), (6, 21), (6, 18.2), (9.5, 18.2), (9.5, 21), (14, 21), (14, 19.2), (17.5, 19.2), (17.5, 21), (22, 21)]))]


@icon("dna-sequencing-trace", CAT, "Row of sharp overlapping peaks with a dot above each one marking the called base",
      tags=["chromatogram", "sanger sequencing", "electropherogram", "genomics", "base calling", "lab data"])
def _(S):
    peaks = [(2, 20), (4.5, 20), (6, 11), (7.8, 20), (10, 20), (11.7, 7), (13.4, 20), (15, 20), (16.6, 13), (18.3, 20), (20, 20), (22, 20)]
    parts = [line(poly(peaks, r=0 if S.name == "line" else 0.8))]
    for x in (6, 11.7, 16.6):
        parts.append(msolid(S, x, 3.2, 1.3))
    return parts


@icon("elisa-well", CAT, "Cutaway of a single well with antibodies on the bottom, a captured antigen and a glowing tag on top",
      tags=["immunoassay", "microplate", "antibody test", "lab assay", "protein detection", "immunology"])
def _(S):
    return [line("M4.5 3V13A7.5 7.5 0 0 0 19.5 13V3"),
            line(seg(12, 20, 12, 17.4)), line(seg(12, 17.4, 9.8, 15)), line(seg(12, 17.4, 14.2, 15)),
            solid(circle(12, 11.8, 1.7)), line(seg(12, 6, 12, 7.4)), line(seg(8.8, 8, 9.6, 8.9)), line(seg(15.2, 8, 14.4, 8.9))]


@icon("pcr-tube-strip", CAT, "Row of small conical tubes joined in a strip with connected caps along the top",
      tags=["pcr", "thermocycler", "microtubes", "dna amplification", "lab consumable", "molecular biology"])
def _(S):
    parts = [shell(rect(2, 3, 20, 4.5, min(S.R, 2)))]
    for x in (4.5, 8.7, 12, 15.3, 19.5):
        pass
    for x in (4, 8, 12, 16, 20):
        parts.append(line(poly([(x - 1.2, 9.5), (x - 1.2, 15), (x, 20.5), (x + 1.2, 15), (x + 1.2, 9.5)]))) if False else parts.append(line(seg(x, 9, x, 17)))
        parts.append(line(seg(x, 17, x, 20.5)))
    return parts


@icon("spin-column", CAT, "Small column with a filter disc standing in a larger microtube, with a curved spin arrow",
      tags=["dna extraction", "purification kit", "microcentrifuge", "silica membrane", "lab consumable", "molecular biology"])
def _(S):
    return [line("M4.5 11.5V18.5A2.5 2.5 0 0 0 7 21H13A2.5 2.5 0 0 0 15.5 18.5V11.5"), line(seg(2.5, 11.5, 17.5, 11.5)),
            shell(rect(7, 3, 6, 11, min(S.R, 2))), detail(seg(7, 7, 13, 7)),
            line(arc(19, 5, 2.8, -80, 200)), line(poly([(16.5, 6.5), (16.5, 9.2), (19.2, 8.6)]))]
