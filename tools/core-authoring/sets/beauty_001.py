"""TypeIcon Core: beauty (batch 001): salon and barber tools, furniture, hairstyles, facial hair and nail tools.

Objects are drawn upright or on a single 45 degree diagonal. Heads are simple front or side silhouettes: the
outline is the shell, the hairline and parting are details (knocked out in Filled), eyes are dots.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "beauty"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rpts(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def hole_ellipse(cx, cy, rx, ry):
    """Ellipse drawn the opposite way round, so it cuts a hole inside a same-path outer ellipse."""
    return (f"M{fmt(cx - rx)} {fmt(cy)}A{fmt(rx)} {fmt(ry)} 0 1 1 {fmt(cx + rx)} {fmt(cy)}"
            f"A{fmt(rx)} {fmt(ry)} 0 1 1 {fmt(cx - rx)} {fmt(cy)}Z")


# ============================================================================ hair tools

@icon("vent-brush", CAT, "Vented hairbrush with an oval head cut by two open slots and a tapered handle",
      tags=["hairbrush", "blow dry", "styling brush", "salon", "vent", "hair", "grooming"])
def _(S):
    head = rect(3.5, 2.5, 17, 13, L(S, 6, 6.5))
    handle = poly([(10, 14), (14, 14), (13.25, 21.5), (10.75, 21.5)], closed=True)
    return [shell(union(head, handle)),
            detail(seg(8, 6.5, 8, 11)), detail(seg(12, 6.5, 12, 11)), detail(seg(16, 6.5, 16, 11))]


@icon("edge-brush", CAT, "Slim double ended tool with a small bristle brush at one end and a fine comb at the other",
      tags=["edge control", "baby hair", "styling tool", "hair brush", "comb", "grooming", "salon"])
def _(S):
    k = S.r * 0.6
    d = [shell(rect(8, 10.5, 8, 3, L(S, 0, 1.2))),
         shell(poly([(16, 10), (22.5, 8.5), (22.5, 15.5), (16, 14)], closed=True, r=k)),
         shell(rect(2.5, 9, 5.5, 3, 0))]
    out = [Part(p.kind, rot(p.d, -45), p.attrs) for p in d]
    out.append(detail(poly(rpts([(18.5, 12), (20.5, 12)], -45))))
    out += [line(poly(rpts([(x, 12), (x, 16.5)], -45))) for x in (3.5, 6.5)]
    return out


@icon("hair-crimper", CAT, "Hinged styling iron with two ridged plates opened slightly above a short handle",
      tags=["crimping iron", "hair waver", "zigzag", "styling", "hot tool", "salon", "texture"])
def _(S):
    k = S.r * 0.6
    left = [(5.5, 3), (10, 3), (8.5, 6), (10, 9), (8.5, 12), (10, 15), (10, 17), (5.5, 17)]
    right = [(24 - x, y) for x, y in left]
    return [shell(poly(rpts(left, -7, 12, 17), closed=True, r=k)),
            shell(poly(rpts(right, 7, 12, 17), closed=True, r=k)),
            shell(rect(9, 16.5, 6, 5, L(S, 0, 1.5)))]


@icon("hair-bonnet", CAT, "Puffy sleep bonnet seen from the side with a gathered band along its lower edge",
      tags=["sleep cap", "satin bonnet", "night cap", "hair protection", "curly hair", "bedtime", "shower cap"])
def _(S):
    body = "M3.5 16.5C3.5 8.5 7.5 4.5 12 4.5C16.5 4.5 20.5 8.5 20.5 16.5Q12 21 3.5 16.5Z"
    return [shell(body), detail("M5 12.8Q12 16.5 19 12.8")]


@icon("sectioning-clip", CAT, "Long narrow duckbill hair clip with closed jaws and a hinge bump at the back",
      tags=["duckbill clip", "hair clip", "section", "salon", "styling", "pin curl clip", "hairdresser"])
def _(S):
    k = S.r * 0.6
    body = poly([(2.5, 8.5), (8, 8.5), (21.5, 12), (8, 15.5), (2.5, 15.5)], closed=True, r=k)
    return [Part("shell", rot(body, -28), {}), Part("detail", poly(rpts([(8.5, 12), (17.5, 12)], -28)), {}),
            Part("dot", rot(circle(5, 12, 1.3), -28), {})]


@icon("banana-clip", CAT, "Long curved comb clip shaped like a banana with a row of teeth along its inner edge",
      tags=["claw clip", "hair comb", "updo", "french twist clip", "hair accessory", "vertical clip", "ponytail"])
def _(S):
    outer = (11, 2.5), (1, 6), (1, 18), (11, 21.5)
    inner = (11, 21.5), (8, 17), (8, 7), (11, 2.5)
    d = "M11 2.5C1 6 1 18 11 21.5C8 17 8 7 11 2.5Z"
    teeth = []
    for t in (0.3, 0.5, 0.7):
        x, y = bez(*inner, t)
        teeth.append(line(seg(x - 0.5, y, x + 4.5, y)))
    return [shell(d)] + teeth


@icon("hair-fork", CAT, "Two pronged hair pin with long straight tines under a rounded decorative top",
      tags=["hair pin", "updo", "bun", "u pin", "french twist", "hair accessory", "prong"])
def _(S):
    return [shell(rect(6.5, 2.5, 11, 5, L(S, 1.5, 2.5))),
            line(seg(9, 7.5, 9, 21.5)), line(seg(15, 7.5, 15, 21.5))]


def _donut_filled():
    o = ellipse(12, 12, 9.5, 6.5)
    body = D(U(P(o), ST(o, 2)), P(ellipse(12, 12, 4, 1.5)),
             *[P(circle(x, y, 0.95)) for x, y in ((9, 8.2), (15, 8.2), (9, 15.8), (15, 15.8))])
    return body


@icon("hair-donut", CAT, "Thick ring of mesh sponge seen at an angle with a dotted texture",
      tags=["bun maker", "bun ring", "sponge ring", "updo", "hair accessory", "hair doughnut", "top knot"],
      filled=_donut_filled)
def _(S):
    outer = rect(2.5, 5.5, 19, 13, 6.5) if S.name == "line" else ellipse(12, 12, 9.5, 6.5)
    return [shell(outer + hole_ellipse(12, 12, 5, 2.5)),
            dot(9, 8.2, 0.95), dot(15, 8.2, 0.95), dot(9, 15.8, 0.95), dot(15, 15.8, 0.95)]


@icon("neck-duster", CAT, "Round fat brush of soft bristles fanning from a short handle",
      tags=["barber brush", "talcum brush", "hair sweep", "neck brush", "barbershop", "powder brush", "duster"])
def _(S):
    dome = "M5 13.5A7 9 0 0 1 19 13.5Z"
    return [shell(dome), detail("M12 12V6.5"), detail("M9.5 12L8 8"), detail("M14.5 12L16 8"),
            shell(rect(9, 13.5, 6, 3, L(S, 0, 1))),
            shell(rect(10.5, 16.5, 3, 5, L(S, 0, 1)))]


@icon("tint-bowl", CAT, "Shallow colour mixing bowl with a grip tab and a tint brush resting across it",
      tags=["hair colour", "hair color", "dye bowl", "mixing bowl", "salon", "tint brush", "bleach"])
def _(S):
    bowl = "M3 12H21C21 17 17 20.5 12 20.5C7 20.5 3 17 3 12Z"
    k = S.r * 0.6
    brush = [shell(rect(2.5, 5, 4.5, 4, 0)),
             shell(poly([(7, 5.5), (19, 5.5), (22, 7), (19, 8.5), (7, 8.5)], closed=True, r=k))]
    return [shell(bowl)] + [Part(p.kind, rot(p.d, -18, 12, 8), p.attrs) for p in brush]


@icon("color-swatch-ring", CAT, "Fan of three hair colour swatch locks hanging from one ring",
      tags=["colour chart", "color chart", "hair color", "shade", "swatch", "dye", "salon", "tint"])
def _(S):
    lock = [(11, 7.5), (13, 7.5), (13.9, 19.5), (10.1, 19.5)]
    out = [shell(circle(12, 4.25, 2))]
    for a in (-33, 0, 33):
        out.append(shell(poly(rpts(lock, a, 12, 6.25), closed=True, r=S.r * 0.5)))
    return out


@icon("hair-color-applicator-bottle", CAT, "Squeeze bottle with measuring marks on its side and a long tapered nozzle",
      tags=["applicator bottle", "dye bottle", "hair dye", "hair colour", "salon", "tint", "root touch up"])
def _(S):
    body = poly([(7, 21.5), (7, 11.5), (10.25, 8.5), (10.25, 7.5), (13.75, 7.5), (13.75, 8.5), (17, 11.5), (17, 21.5)],
                closed=True, r=S.r)
    nozzle = poly([(10.5, 7.5), (11.4, 2.5), (12.6, 2.5), (13.5, 7.5)], closed=True)
    return [shell(union(body, nozzle)), detail(seg(7, 14, 10, 14)), detail(seg(7, 18, 10, 18))]


@icon("clipper-guard", CAT, "Clip on clipper guard comb with a curved spine, four long teeth and a hole for the length number",
      tags=["guard comb", "clipper attachment", "barber", "hair clipper", "fade", "length guide", "trimmer comb"])
def _(S):
    spine = "M8.5 3.5C3 8 3 16 8.5 20.5H11.5V3.5Z"
    return [shell(spine),
            line(seg(11, 5.5, 21.5, 5.5)), line(seg(11, 9.5, 21.5, 9.5)),
            line(seg(11, 13.5, 21.5, 13.5)), line(seg(11, 17.5, 21.5, 17.5)),
            dot(7.5, 12, 1.25)]


@icon("razor-strop", CAT, "Leather strap hanging from a hook with a handle at the bottom end",
      tags=["strop", "razor sharpening", "straight razor", "leather strap", "barber", "shaving", "honing"])
def _(S):
    return [line("M12 6V4A1.75 1.75 0 1 0 8.5 4"),
            shell(rect(8.5, 6, 7, 11.5, 0)),
            detail(seg(12, 8.5, 12, 14)),
            shell(rect(9.5, 17.5, 5, 4.5, L(S, 0, 1.5)))]


@icon("shaving-stand", CAT, "Pedestal stand holding a shaving brush and a safety razor from a crossbar",
      tags=["shave stand", "shaving brush", "razor stand", "barber", "grooming", "wet shave", "shave set"])
def _(S):
    return [shell(rect(5.5, 19.5, 13, 2.5, L(S, 0, 1))),
            line(seg(12, 5, 12, 19.5)),
            line(seg(3, 4.5, 21, 4.5)),
            line(seg(6, 4.5, 6, 8)), shell(ellipse(6, 12, 2.6, 3.4)),
            shell(rect(15.5, 8, 6, 2.5, L(S, 0, 1))), line(seg(18.5, 4.5, 18.5, 8)), line(seg(18.5, 10.5, 18.5, 17))]


@icon("beard-shaping-tool", CAT, "Curved beard line template with three guide teeth along its top edge",
      tags=["beard stencil", "beard template", "line up", "shape up", "barber", "beard trim", "grooming"])
def _(S):
    body = "M3.5 5.5C3.5 15 7.5 21 12 21C16.5 21 20.5 15 20.5 5.5H16.8C16.8 11 14.8 16 12 16C9.2 16 7.2 11 7.2 5.5Z"
    return [shell(body), line(seg(8.7, 13.5, 8.7, 9.5)), line(seg(12, 16, 12, 11.5)), line(seg(15.3, 13.5, 15.3, 9.5))]


@icon("beard-bib", CAT, "Barber apron with a curved neck cutout and a suction cup at each upper corner",
      tags=["hair catcher", "beard apron", "trimming cape", "beard catcher", "barber", "grooming", "shaving"])
def _(S):
    d = "M3.5 7.5H8C8 12 16 12 16 7.5H20.5L18 21.5H6Z"
    return [shell(d), shell(circle(4.5, 4.5, 1.6)), shell(circle(19.5, 4.5, 1.6))]


@icon("comb-disinfectant-jar", CAT, "Tall lidded jar of liquid with two combs standing in it",
      tags=["barbicide", "sanitizer jar", "disinfecting", "barber", "salon hygiene", "clean combs", "sterilise"])
def _(S):
    return [shell(rect(5.5, 6.5, 13, 15, L(S, 1.5, 3))),
            shell(rect(4.5, 3, 15, 3.5, L(S, 0, 1.5))),
            detail("M5.5 11C8 9.5 10 12.5 12 11C14 9.5 16 12.5 18.5 11"),
            detail(seg(9.5, 14, 9.5, 18.5)), detail(seg(14.5, 14, 14.5, 18.5))]


@icon("shears-holster", CAT, "Leather holster pouch with two slots holding hair shears and a comb",
      tags=["scissor holster", "shear pouch", "tool belt", "hairdresser", "barber", "stylist", "salon belt"])
def _(S):
    return [shell(rect(3, 11.5, 18, 9.5, L(S, 1.5, 3))),
            detail(seg(12, 11.5, 12, 21)),
            shell(circle(4.75, 6, 1.6)), shell(circle(10.5, 6, 1.6)),
            line(seg(5.25, 7.5, 7.5, 11.5)), line(seg(10, 7.5, 7.5, 11.5)),
            line(seg(15.5, 4.5, 15.5, 11.5)), line(seg(19.5, 4.5, 19.5, 11.5))]


@icon("hair-mousse", CAT, "Aerosol can with a nozzle cap and a cloud of foam beside it",
      tags=["styling foam", "volumizer", "hair product", "aerosol", "curl foam", "salon", "styling mousse"])
def _(S):
    can = union(rect(4.5, 9.5, 8.5, 12, L(S, 1.5, 2.5)), rect(5.5, 5.5, 6.5, 4.5, 0), rect(7.25, 2.5, 3, 3, 0))
    cloud = union(circle(16.5, 7.5, 2.9), circle(20, 9.5, 2), circle(16.5, 12, 2.3))
    return [shell(can), detail(seg(5, 9.5, 13, 9.5)), shell(cloud)]


# ============================================================================ more tools and salon kit

@icon("pressing-comb", CAT, "Metal hot comb with wide teeth and a handle, with heat waves rising above it",
      tags=["hot comb", "straightening comb", "press and curl", "hair straightener", "salon", "heated comb", "styling"])
def _(S):
    return [shell(rect(2.5, 10, 13, 4, L(S, 0, 1.5))),
            line(seg(4.5, 14, 4.5, 20.5)), line(seg(8.75, 14, 8.75, 20.5)), line(seg(13, 14, 13, 20.5)),
            shell(rect(15.5, 10, 6, 4, L(S, 1, 2))),
            line("M6 2.5C7.2 4 4.8 5 6 6.5"), line("M11 2.5C12.2 4 9.8 5 11 6.5")]


@icon("hair-twist-sponge", CAT, "Rectangular sponge pad covered in round holes beside a coil of curly hair",
      tags=["twist sponge", "coil sponge", "curl sponge", "afro hair", "natural hair", "salon", "coils"])
def _(S):
    return [shell(rect(2.5, 5, 11, 14, L(S, 1.5, 3))),
            dot(6, 8.75, 0.95), dot(10, 8.75, 0.95), dot(6, 12, 0.95), dot(10, 12, 0.95),
            dot(6, 15.25, 0.95), dot(10, 15.25, 0.95),
            line("M18.5 4C21.5 4 21.5 8 18.5 8C16 8 16 12 18.5 12C21.5 12 21.5 16 18.5 16C16.5 16 16.5 19 18.5 20")]


@icon("peineta-comb", CAT, "Tall ornamental hair comb with an arched crown and short teeth along the bottom",
      tags=["spanish comb", "decorative comb", "mantilla comb", "hair accessory", "updo", "bridal", "flamenco"])
def _(S):
    return [shell("M3.5 14.5V11C3.5 6 7.2 2.8 12 2.8C16.8 2.8 20.5 6 20.5 11V14.5Z"),
            detail("M8 14.5V11.5C8 9 9.7 7.5 12 7.5C14.3 7.5 16 9 16 11.5V14.5"),
            line(seg(6, 14.5, 6, 21)), line(seg(10, 14.5, 10, 21)), line(seg(14, 14.5, 14, 21)), line(seg(18, 14.5, 18, 21))]


@icon("hair-clippings", CAT, "Small mound of cut hair on the floor with a pair of scissors lying beside it",
      tags=["cut hair", "hair pile", "trim", "haircut", "barber floor", "sweep", "scissors"])
def _(S):
    return [shell(circle(4.75, 5.5, 2.25)), shell(circle(4.75, 11.5, 2.25)),
            line(seg(6.7, 6.8, 20, 11)), line(seg(6.7, 10.3, 20, 3.5)),
            shell("M7 21.5C7 18 9 15.5 12 15.5C15 15.5 17.5 17.5 17.5 21.5Z"), detail("M10 21C10.5 19 12 18.5 13 19.5")]


@icon("uv-sterilizer-cabinet", CAT, "Small glass door cabinet with a tube lamp at the top, short rays and tools standing on a shelf",
      tags=["sterilizer", "uv cabinet", "disinfect", "salon hygiene", "tool sanitiser", "barber", "ultraviolet"])
def _(S):
    return [shell(rect(3.5, 2.5, 17, 19, L(S, 1.5, 3))),
            line(seg(7.5, 6.5, 16.5, 6.5)),
            line(seg(8.5, 9.5, 8.5, 11)), line(seg(12, 9.5, 12, 11)), line(seg(15.5, 9.5, 15.5, 11)),
            detail(seg(3.5, 16, 20.5, 16)),
            ]


@icon("towel-warmer-cabinet", CAT, "Box cabinet holding stacked folded towels with wavy steam lines rising above it",
      tags=["hot towel", "towel steamer", "barber shop", "spa", "heated towels", "warmer", "salon"])
def _(S):
    return [shell(rect(3.5, 9, 17, 11, L(S, 1.5, 3))),
            line(seg(7, 20, 7, 22)), line(seg(17, 20, 17, 22)),
            detail(seg(3.5, 13, 20.5, 13)), detail(seg(3.5, 16.5, 20.5, 16.5)),
            line("M8 2.5C9.3 4 6.7 5 8 6.5"), line("M12 2.5C13.3 4 10.7 5 12 6.5"), line("M16 2.5C17.3 4 14.7 5 16 6.5")]


@icon("rolling-stool", CAT, "Round padded stool on a single column with a five caster wheel base",
      tags=["salon stool", "stylist stool", "gas lift", "swivel stool", "casters", "barber", "tattoo stool"])
def _(S):
    return [shell(rect(5, 3.5, 14, 4.5, L(S, 1.5, 2.25))),
            line(seg(12, 8, 12, 15.5)),
            line(poly([(4.5, 18.5), (12, 15.5), (19.5, 18.5)])), line(seg(12, 15.5, 12, 18.5)),
            dot(4.5, 20.25, 1.5), dot(12, 20.25, 1.5), dot(19.5, 20.25, 1.5)]


@icon("salon-styling-chair", CAT, "Front view of a salon chair with a rounded back, armrests, a column and a round base",
      tags=["hydraulic chair", "hairdresser chair", "barber chair", "styling seat", "salon", "beauty salon", "stylist"])
def _(S):
    return [shell(rect(7, 2.5, 10, 9, L(S, 2, 4))),
            shell(rect(3.5, 11.5, 17, 3.5, L(S, 1, 1.75))),
            line(seg(4, 7.5, 4, 11.5)), line(seg(20, 7.5, 20, 11.5)),
            line(seg(12, 15, 12, 19.5)),
            shell(rect(4.5, 19.5, 15, 2.5, L(S, 0, 1.25)))]


@icon("salon-trolley", CAT, "Narrow rolling cart with three trays holding a bottle and a brush, on small wheels",
      tags=["tool cart", "stylist cart", "hairdresser trolley", "colour trolley", "beauty cart", "rolling cart", "salon"])
def _(S):
    return [line(seg(5, 3.5, 5, 18.5)), line(seg(19, 3.5, 19, 18.5)),
            line(seg(4, 8.5, 20, 8.5)), line(seg(4, 13.5, 20, 13.5)), line(seg(4, 18.5, 20, 18.5)),
            shell(rect(8.5, 3.5, 3, 4, 0)),
            dot(7, 21, 1.1), dot(17, 21, 1.1)]


@icon("styling-station", CAT, "Wall mirror above a narrow counter with a chair back in front of it",
      tags=["salon station", "hair station", "vanity", "mirror and counter", "barber station", "stylist", "workstation"])
def _(S):
    return [shell(rect(6, 2.5, 12, 9, L(S, 2, 4))), detail(seg(9, 8.5, 11.5, 6)),
            shell(rect(3, 13, 18, 3, L(S, 0, 1.25))),
            shell(rect(8, 17.5, 8, 4, L(S, 1, 2)))]


@icon("magnifying-lamp", CAT, "Round magnifier lamp with a lens ring on a jointed arm and a clamp base",
      tags=["beauty lamp", "esthetician lamp", "lash lamp", "facial lamp", "cosmetic lamp", "loupe light", "spa"])
def _(S):
    return [shell(circle(9, 8.5, 6.5)), detail(circle(9, 8.5, 2.9)),
            line("M13.7 13.2L18 17V19.5"),
            shell(rect(14.5, 19.5, 7, 2.5, L(S, 0, 1.25)))]


# ============================================================================ nails

@icon("french-manicure", CAT, "Fingertip with a long nail whose free edge is marked by a curved band",
      tags=["nail art", "white tip", "nails", "manicure", "nail salon", "polish", "bridal nails"])
def _(S):
    return [shell("M8.5 14V6.5C8.5 4.5 10 3 12 3C14 3 15.5 4.5 15.5 6.5V14Z"),
            detail("M8.5 7.5Q12 10.5 15.5 7.5"),
            line("M6 22V15C6 13.5 6.6 12.5 8 12.5"), line("M18 22V15C18 13.5 17.4 12.5 16 12.5")]


@icon("nail-drill", CAT, "Slim electric nail file handpiece with a small bit at the tip and a cord from the back",
      tags=["e-file", "electric nail file", "acrylic prep", "manicure tool", "nail technician", "cuticle", "salon tool"])
def _(S):
    k = S.r * 0.6
    body = poly([(7.5, 9.5), (17.5, 10.5), (17.5, 13.5), (7.5, 14.5)], closed=True, r=k)
    parts = [Part("shell", rot(body, -35), {}),
             Part("shell", rot(rect(3.5, 10.75, 4, 2.5, 0), -35), {}),
             Part("line", poly(rpts([(17.5, 12), (19.5, 12)], -35)), {})]
    parts.append(line(poly(rpts([(17.5, 12), (20, 12), (20, 16), (14, 18.5)], -35), r=S.r + 1.5)))
    return parts


@icon("dappen-dish", CAT, "Small glass dish on a thick base with a nail brush resting across its rim",
      tags=["acrylic liquid", "monomer dish", "nail brush", "nail tech", "acrylic nails", "liquid cup", "manicure"])
def _(S):
    return [shell(poly([(3.5, 11.5), (14.5, 11.5), (13, 17.5), (5, 17.5)], closed=True, r=S.r * 0.5)),
            shell(rect(5, 17.5, 8, 3.5, L(S, 0, 1.25))),
            line(seg(21, 3, 11, 9)), shell(poly([(11, 9), (8.5, 7.5), (7, 10), (9.5, 11)], closed=True))]


@icon("nail-dust-collector", CAT, "Low box with a hand rest cushion on top and a fan seen through the front vent",
      tags=["dust extractor", "nail table", "manicure station", "fan", "nail technician", "salon equipment", "vent"])
def _(S):
    return [shell(rect(4, 3.5, 16, 4, L(S, 1.5, 2))),
            shell(rect(2.5, 9, 19, 12.5, L(S, 1.5, 3))),
            detail(circle(12, 15.25, 3.4)), dot(12, 15.25, 1.0)]


@icon("manicure-bowl", CAT, "Curved fingertip bowl with four fingers dipping into the water",
      tags=["finger soak", "nail soak", "manicure", "hand soak", "water bowl", "nail salon", "spa"])
def _(S):
    bowl = "M3 12.5H21C21 17.5 17 20.5 12 20.5C7 20.5 3 17.5 3 12.5Z"
    return [shell(bowl), detail("M5 15.5Q8 14 10 15.5T15 15.5T19 15.5")] + \
        [line(seg(x, 3, x, 10)) for x in (7, 10.5, 14, 17.5)]


@icon("pedicure-chair", CAT, "Side view of a padded high backed chair with an armrest and a foot basin built into the front",
      tags=["spa chair", "foot spa", "nail salon", "massage chair", "foot basin", "pedicure", "throne chair"])
def _(S):
    return [shell(poly([(3.5, 3), (8.5, 3), (9.5, 14), (4.5, 14)], closed=True, r=S.r * 0.6)),
            shell(rect(4.5, 14, 11, 3.5, L(S, 0, 1.25))),
            line(seg(9, 9, 14.5, 9)),
            line(seg(8, 17.5, 8, 21)),
            shell("M14 17H21.5C21.5 20 19.5 21.5 17.75 21.5C16 21.5 14 20 14 17Z")]


@icon("nail-swatch-wheel", CAT, "Round display wheel with six false nail tips arranged around its edge",
      tags=["nail colour wheel", "nail color chart", "press on nails", "nail tips", "polish display", "nail salon", "swatch"])
def _(S):
    out = [shell(circle(12, 12, 4.2)), dot(12, 12, 1.1)]
    for i in range(6):
        a = i * 60 - 90
        x, y = polar(12, 12, 8.3, a)
        out.append(shell(rot(rect(x - 1.5, y - 2.3, 3, 4.6, L(S, 0.8, 1.5)), a + 90, x, y)))
    return out


@icon("dotting-tool", CAT, "Slim double ended stick with a small ball at each end and a dot of polish beside one tip",
      tags=["nail art tool", "dotting pen", "nail art", "manicure", "polish dot", "stylus", "nail technician"])
def _(S):
    ends = [rpts([(x, 12)], -40)[0] for x in (3.5, 20.5)]
    return [shell(rot(rect(7, 10, 10, 4, L(S, 0, 2)), -40)),
            line(poly(rpts([(4, 12), (7, 12)], -40))), line(poly(rpts([(17, 12), (20, 12)], -40))),
            dot(*ends[0], 1.9), dot(*ends[1], 1.9), dot(*rpts([(17, 17)], -40)[0], 1.5)]


# ============================================================================ heads and hair
# Front heads share one construction: a hair part (closed shell), a jaw line and two eye dots.

def jaw(hw=5.5, top=10.5, bottom=18, cx=12):
    """Open jaw line: two short sides and a semicircular chin (centre line)."""
    return f"M{fmt(cx - hw)} {fmt(top)}V{fmt(bottom - hw)}A{fmt(hw)} {fmt(hw)} 0 0 0 {fmt(cx + hw)} {fmt(bottom - hw)}V{fmt(top)}"


def cap(hw=6, top=2.8, side=10.5, hl=7.5, cx=12):
    """Hair cap: dome outside, curved hairline inside, tips ending at the temples."""
    return (f"M{fmt(cx - hw)} {fmt(side)}V{fmt(top + hw)}A{fmt(hw)} {fmt(hw)} 0 0 1 {fmt(cx + hw)} {fmt(top + hw)}V{fmt(side)}"
            f"C{fmt(cx + hw - 1.5)} {fmt(hl + 1.2)} {fmt(cx + hw - 3.5)} {fmt(hl)} {fmt(cx)} {fmt(hl)}"
            f"C{fmt(cx - hw + 3.5)} {fmt(hl)} {fmt(cx - hw + 1.5)} {fmt(hl + 1.2)} {fmt(cx - hw)} {fmt(side)}Z")


def eye(S, x, y, k=1.0):
    """Line eyes are crisp upright bars, Rounded eyes are soft ovals."""
    return Part("dot", rect(x - 0.9 * k, y - 1.4 * k, 1.8 * k, 2.8 * k) if S.name == "line" else ellipse(x, y, 1.05 * k, 1.45 * k))


def eyes(S, y=12.5, dx=2.5, cx=12, k=1.0):
    return [eye(S, cx - dx, y, k), eye(S, cx + dx, y, k)]


def face(S, hw=5.5, top=10.5, bottom=18, cx=12, ey=12.5):
    return [line(jaw(hw, top, bottom, cx))] + eyes(S, ey, hw * 0.45, cx)


@icon("bob-haircut", CAT, "Front view of a head with straight chin length hair cut level all around the face",
      tags=["bob", "short hair", "haircut", "hairstyle", "straight hair", "salon", "stylist"])
def _(S):
    band = ("M3 17.5V10C3 5.2 6.8 2.5 12 2.5C17.2 2.5 21 5.2 21 10V17.5H17V10.5C17 8 15 6.8 12 6.8"
            "C9 6.8 7 8 7 10.5V17.5Z")
    return [shell(band), line(jaw(5, 13.5, 18.5)), *eyes(S, 12, 2.4)]


@icon("bangs-hairstyle", CAT, "Front view of a head with long straight hair and a blunt fringe across the forehead",
      tags=["fringe", "bangs", "straight hair", "hairstyle", "haircut", "long hair", "salon"])
def _(S):
    band = "M3 20.5V10C3 5.2 6.8 2.5 12 2.5C17.2 2.5 21 5.2 21 10V20.5H17V8.5H7V20.5Z"
    return [shell(band), line(jaw(5, 14.5, 19.5)), *eyes(S, 12.5, 2.4)]


@icon("buzz-cut", CAT, "Front view of a head with hair clipped very short and even, shown as a thin cap with a few dots",
      tags=["clipper cut", "short hair", "military cut", "shaved", "barber", "haircut", "crew cut"])
def _(S):
    return [shell(cap(6.5, 2.5, 10.5, 7.5)), dot(9.5, 5.6, 0.8), dot(14.5, 5.6, 0.8), dot(12, 4.6, 0.8)] + face(S, 6.5, 10.5, 18.5)


@icon("flat-top-haircut", CAT, "Front view of a head with short sides and a tall block of hair with a perfectly level top",
      tags=["flat top", "crew cut", "barber", "military", "short sides", "haircut", "hairstyle"])
def _(S):
    hair = poly([(6, 10.5), (6, 2.5), (18, 2.5), (18, 10.5), (16, 7.8), (8, 7.8)], closed=True, r=S.r * 0.7)
    return [shell(hair)] + face(S, 6, 10.5, 18.5)


@icon("spiky-hair", CAT, "Front view of a head with short hair styled into sharp upward spikes",
      tags=["spikes", "gelled hair", "punk", "short hair", "hairstyle", "styling gel", "hedgehog"])
def _(S):
    hair = poly([(6, 10.5), (5.5, 5.5), (8.3, 6.8), (9, 2.2), (12, 5.8), (15, 2.2), (15.7, 6.8), (18.5, 5.5), (18, 10.5),
                 (16, 8.2), (8, 8.2)], closed=True, r=S.r * 0.5)
    return [shell(hair)] + face(S, 6, 10.5, 18.5)


@icon("side-part-hairstyle", CAT, "Front view of a head with short neat hair combed across from a clear parting line",
      tags=["side parting", "short back and sides", "neat hair", "classic cut", "barber", "gentleman", "hairstyle"])
def _(S):
    return [shell(cap(6.5, 2.5, 10.5, 7.6)), detail("M8.8 3.5C8.8 5.2 9.4 6.6 11 7.8")] + face(S, 6.5, 10.5, 18.5)


@icon("bowl-cut", CAT, "Front view of a head with an even rounded cap of hair, a straight fringe and a level edge all around",
      tags=["pudding bowl", "bowl haircut", "mushroom cut", "kids haircut", "fringe", "hairstyle", "round cut"])
def _(S):
    bowl = "M4.5 10.5V9C4.5 5 7.5 2.5 12 2.5C16.5 2.5 19.5 5 19.5 9V10.5Z"
    return [shell(bowl)] + face(S, 5.5, 10.5, 18.5)


@icon("bald-head", CAT, "Front view of a smooth bald head and shoulders with a small shine mark on top",
      tags=["baldness", "hair loss", "shaved head", "no hair", "alopecia", "skinhead", "smooth"])
def _(S):
    return [shell(ellipse(12, 9, 6.5, 7)), detail("M8.8 8C8.8 6.6 9.6 5.5 11 5"),
            *eyes(S, 10.5, 2.5), line("M3.5 22C4 19.8 7.5 19.2 12 19.2C16.5 19.2 20 19.8 20.5 22")]


@icon("comb-over", CAT, "Front view of a bald head with two long strands of hair combed across the crown",
      tags=["combover", "thinning hair", "hair loss", "balding", "receding", "hairstyle", "strands"])
def _(S):
    return [shell(ellipse(12, 10.5, 6.8, 8)), detail("M6 10.5C7.5 6.8 13 5.2 17.8 8"),
            *eyes(S, 13.2, 2.5), line("M3.5 22C4 19.8 7.5 19.2 12 19.2C16.5 19.2 20 19.8 20.5 22")]


@icon("sideburns", CAT, "Front view of a face with thick wide sideburns running down the cheeks from the ears to the jaw",
      tags=["sideburn", "mutton chops", "facial hair", "side whiskers", "barber", "grooming", "retro"])
def _(S):
    left = solid(poly([(5.5, 8.5), (8.5, 8.5), (8.5, 14), (7.2, 15.5), (5.5, 14)], closed=True))
    right = solid(poly([(18.5, 8.5), (15.5, 8.5), (15.5, 14), (16.8, 15.5), (18.5, 14)], closed=True))
    return [shell(cap(6.5, 2.8, 8.5, 6.5)), left, right, line("M6 14V15C6 17.5 8.5 19.5 12 19.5C15.5 19.5 18 17.5 18 15V14"), *eyes(S, 11.5, 2.2)]


@icon("chin-strap-beard", CAT, "Front view of a face with a thin line of beard following the jaw from ear to ear and no mustache",
      tags=["chinstrap", "jawline beard", "facial hair", "shadow beard", "barber", "grooming", "beard line"])
def _(S):
    strap = minus(circle(12, 12.5, 6.6), circle(12, 11, 4.7), rect(0, 0, 24, 10.5))
    return [shell(cap(6.5, 2.8, 10.5, 7)), solid(strap), *eyes(S, 10, 2.4)]


@icon("pigtails", CAT, "Front view of a head with a centre parting and two bunches of hair sticking out low on each side",
      tags=["pig tails", "bunches", "twin tails", "girl hairstyle", "kids hair", "hair ties", "hairstyle"])
def _(S):
    def lock(m):
        x = lambda v: fmt(12 + m * (v - 12))
        return (f"M{x(6.5)} 10.5C{x(4)} 10.5 {x(2.5)} 12.5 {x(2.5)} 15.5C{x(2.5)} 18.5 {x(3)} 20.2 {x(4.2)} 21.5"
                f"C{x(5.8)} 20.2 {x(6.8)} 17.5 {x(6.8)} 13.5Z")
    return [shell(cap(6, 2.8, 10.5, 7.5)), detail("M12 3.3V7.5"), shell(lock(1)), shell(lock(-1))] + face(S, 5.5, 10.5, 18.5)


@icon("space-buns", CAT, "Front view of a head with two round buns sitting high on either side of the top of the head",
      tags=["double buns", "top knots", "twin buns", "hair buns", "festival hair", "girl hairstyle", "hairstyle"])
def _(S):
    hair = union(cap(5.5, 4.8, 10.5, 8.2), circle(6.2, 5.2, 3.2), circle(17.8, 5.2, 3.2))
    return [shell(hair), detail("M12 5.3V8.2")] + face(S, 5.5, 10.5, 18.5)


@icon("dreadlocks", CAT, "Front view of a head with long rope like locks hanging past the shoulders on each side of the face",
      tags=["locs", "dreads", "rasta", "twists", "long locks", "natural hair", "hairstyle"])
def _(S):
    out = [shell(cap(6.3, 2.8, 9.5, 7))]
    for x0 in (3.2, 5.9):
        out.append(line(f"M{fmt(x0)} 8.5C{fmt(x0 - 1.2)} 11 {fmt(x0 + 1.2)} 13 {fmt(x0)} 15.5C{fmt(x0 - 1)} 17.5 {fmt(x0 + 0.5)} 19.5 {fmt(x0)} 21"))
        out.append(line(f"M{fmt(24 - x0)} 8.5C{fmt(24 - x0 + 1.2)} 11 {fmt(24 - x0 - 1.2)} 13 {fmt(24 - x0)} 15.5C{fmt(24 - x0 + 1)} 17.5 {fmt(24 - x0 - 0.5)} 19.5 {fmt(24 - x0)} 21"))
    return out + face(S, 4.3, 9.5, 17.5)


@icon("afro-hairstyle", CAT, "Front view of a head with a large rounded halo of textured hair around the face and above the head",
      tags=["afro", "natural hair", "curly hair", "big hair", "coily", "1970s", "hairstyle"])
def _(S):
    halo = union(circle(12, 11, 7.5), circle(5.5, 12.5, 3.8), circle(18.5, 12.5, 3.8), circle(7, 7, 4), circle(17, 7, 4), circle(12, 6.4, 4))
    opening = union(ellipse(12, 12.5, 4.6, 5.6), rect(7.4, 12.5, 9.2, 12))
    return [shell(minus(halo, opening)), line(jaw(4.6, 12.5, 18.1))] + eyes(S, 12, 2.2)


@icon("box-braids", CAT, "Front view of a head with many long thin braids hanging straight down past the shoulders",
      tags=["braids", "protective style", "knotless braids", "plaits", "long braids", "natural hair", "hairstyle"])
def _(S):
    out = [shell(cap(6.3, 2.8, 9.5, 7)), detail("M8.8 3.6V6.2"), detail("M15.2 3.6V6.2")]
    for x0 in (3, 5.9):
        out += [line(seg(x0, 8.5, x0, 19.5)), dot(x0, 21, 1.1), line(seg(24 - x0, 8.5, 24 - x0, 19.5)), dot(24 - x0, 21, 1.1)]
    return out + face(S, 4.3, 9.5, 17.5)


@icon("bantu-knots", CAT, "Front view of a head with a row of small coiled knots set evenly around the crown",
      tags=["knots", "coils", "natural hair", "twist out", "protective style", "african hair", "hairstyle"])
def _(S):
    knots = [polar(12, 10.5, 7.2, a) for a in (-165, -127, -90, -53, -15)]
    crown = union(ellipse(12, 12.5, 6, 6.8), *[circle(x, y, 2.6) for x, y in knots])
    return [shell(crown)] + [dot(x, y, 0.8) for x, y in knots] + eyes(S, 13.2, 2.4)


@icon("french-braid", CAT, "Back of a head with a braid woven close to the scalp in V shapes then hanging down in a plait",
      tags=["plait", "braided hair", "dutch braid", "braid", "hairstyle", "back view", "weave"])
def _(S):
    plait = poly([(10, 14.5), (9.2, 21.5), (14.8, 21.5), (14, 14.5)], closed=True, r=S.r * 0.6)
    return [shell(union(circle(12, 8.5, 6.5), plait)), detail("M9.3 4.6L12 7.2L14.7 4.6"), detail("M9.3 9L12 11.6L14.7 9"),
            detail("M10.5 17.2L12 18.6L13.5 17.2")]


@icon("french-twist", CAT, "Back of a head with the hair twisted into a vertical roll up the middle and held with a pin",
      tags=["chignon", "updo", "twist", "formal hair", "wedding hair", "hairstyle", "back view"])
def _(S):
    roll = rect(9.1, 5.5, 5.8, 15, L(S, 2, 2.9))
    return [shell(union(circle(12, 9, 7.2), roll)), detail("M9.6 9.5L14.4 12"), detail("M9.6 14.5L14.4 17"),
            line(seg(14.5, 4.5, 21, 2.5))]


@icon("half-up-half-down", CAT, "Back of a head with the upper section tied in a small knot and the rest of the hair hanging loose",
      tags=["half updo", "half ponytail", "loose hair", "top knot", "hairstyle", "back view", "long hair"])
def _(S):
    mass = union(circle(12, 10, 6.8), poly([(5.2, 10), (4, 20.5), (20, 20.5), (18.8, 10)], closed=True, r=S.r * 0.8))
    return [shell(mass), shell(circle(12, 3.6, 2.1)), detail("M7 11.5C9.5 13.4 14.5 13.4 17 11.5")]


EARS = [line("M4.6 11.5C3 11.5 3 15.5 4.6 15.5"), line("M19.4 11.5C21 11.5 21 15.5 19.4 15.5")]


@icon("cornrows", CAT, "Top view of a head with three parallel tight braids running from the forehead to the nape",
      tags=["braids", "canerows", "scalp braids", "natural hair", "braided rows", "african hair", "hairstyle"])
def _(S):
    head = union(ellipse(12, 13, 7.2, 8.4), poly([(10.3, 5), (12, 2.3), (13.7, 5)], closed=True))
    return [shell(head), detail(seg(8, 8, 8, 18)), detail(seg(12, 6.5, 12, 19)), detail(seg(16, 8, 16, 18))] + EARS


@icon("hair-transplant", CAT, "Top view of a head with a neat grid of tiny implanted dots across the front hairline",
      tags=["hair restoration", "follicles", "hair loss", "balding", "clinic", "surgery", "implant"])
def _(S):
    head = union(ellipse(12, 13, 7.2, 8.4), poly([(10.3, 5), (12, 2.3), (13.7, 5)], closed=True))
    pip = (lambda x, y: Part("dot", rect(x - 0.95, y - 0.95, 1.9, 1.9))) if S.name == "line" else (lambda x, y: dot(x, y, 1.05))
    return [shell(head)] + [pip(x, y) for y in (8.5, 12) for x in (8.5, 12, 15.5)] + EARS


# ----------------------------------------------------------------------------- side views and the cap
PROFILE = ("M8.5 21.5V16.7C5.2 15.3 3.5 12.5 3.5 9.5C3.5 5.3 7 2.5 11 2.5C15 2.5 18.5 5.2 18.5 9L21 13.3L18.3 14.2"
           "V15.6C18.3 16.8 17.3 17.5 16 17.5H14.5V21.5Z")


def scaled(d, k, ox=12.0, oy=22.0):
    return path_to_d(transform_path(P(d), (k, 0, 0, k, ox * (1 - k), oy * (1 - k))))


def side(S, extra=None, eye_at=(15.2, 10)):
    body = union(PROFILE, *extra) if extra else PROFILE
    return [shell(body), eye(S, *eye_at, 0.9)]


@icon("pixie-cut", CAT, "Side view of a head with very short cropped hair and a small swept fringe over the forehead",
      tags=["short cut", "cropped hair", "pixie", "women's haircut", "short hair", "hairstyle", "salon"])
def _(S):
    tuft = "M10 2.5C14 1.6 19.6 3.4 20.4 8.8C18.6 6.8 15.6 6.2 13 6.6Z"
    return side(S, [tuft]) + [detail("M13 6.9C10 7.1 7.8 8.6 7.2 11.8")]


@icon("undercut-hairstyle", CAT, "Side view of a head with long hair on top swept back and the sides and back shaved short below a sharp line",
      tags=["undercut", "shaved sides", "barber", "disconnected cut", "fade", "men's hairstyle", "haircut"])
def _(S):
    bump = "M3.2 8.8C1.8 4.5 5.5 1.6 11 1.6C16.5 1.6 19.6 4.5 19 8.8C16 6.8 7 6.8 3.2 8.8Z"
    return side(S, [bump]) + [detail("M3.8 10H12.5"), dot(6, 12.6, 0.8), dot(9, 13, 0.8), dot(7.4, 15, 0.8)]


@icon("mohawk-hairstyle", CAT, "Side view of a head with shaved sides and a tall strip of spiked hair from the forehead to the nape",
      tags=["mohican", "punk hair", "spikes", "mohawk", "shaved sides", "hairstyle", "fauxhawk"])
def _(S):
    spikes = poly([(4.2, 8), (4.6, 3.6), (7.2, 6), (8.6, 2.4), (11.3, 5.6), (13.8, 2.4), (15.2, 6), (17.8, 3.8), (18, 8)], closed=True, r=S.r * 0.4)
    return side(S, [spikes]) + [detail("M5.4 9.2C6.8 6.4 9 5.4 12 5.4C14.4 5.4 16.3 6.4 17.4 8.4")]


@icon("pompadour", CAT, "Side view of a head with hair swept up high and back from the forehead in a big rolled wave, short at the sides",
      tags=["quiff", "rockabilly", "elvis hair", "greaser", "men's hairstyle", "barber", "retro"])
def _(S):
    wave = "M6 11C5.4 6 9 2.8 14 2.8C19 2.8 21.8 5.6 21 10.4C19.4 8.4 17.4 7.8 15.4 8Z"
    k = 0.86
    return [shell(union(scaled(PROFILE, k), wave)), eye(S, 12 + 3.2 * k, 22 - 12 * k, 0.8), detail("M18.4 8.2C17.8 5.8 15.6 5 13.6 6")]


@icon("mullet", CAT, "Side view of a head with short hair on top and sides and long hair hanging down over the back of the neck",
      tags=["business in the front", "retro haircut", "80s hair", "long back", "hairstyle", "barber", "rock hair"])
def _(S):
    tail = poly([(5.5, 10), (2.8, 13), (3, 19), (5.5, 22), (8.6, 22), (8.6, 15)], closed=True, r=S.r * 0.6)
    return side(S, [tail]) + [detail("M15.6 5.8C12.5 6 9.5 7.2 7.8 10.2")]


@icon("man-bun", CAT, "Side view of a head with hair pulled back tight into a round bun at the crown and a short beard",
      tags=["top knot", "samurai bun", "hipster", "long hair men", "beard", "hairstyle", "bun"])
def _(S):
    beard = "M18.3 14.2C19 17.6 17 21 14.5 21.6V16Z"
    return side(S, [circle(4.6, 4.6, 3.2), beard]) + [detail("M17.8 7C14.8 4.8 10.8 4.4 7.8 5.4")]


@icon("slicked-back-hair", CAT, "Side view of a head with hair combed flat straight back from the forehead in smooth parallel lines",
      tags=["slick back", "gelled hair", "wet look", "pomade", "gentleman", "hairstyle", "combed back"])
def _(S):
    return side(S) + [detail("M17.3 6.4C13.5 4.2 8.5 4.6 5 8.6"), detail("M13.6 9.2C11 7.6 8.2 8 5.6 11")]


@icon("beehive-hairdo", CAT, "Side view of a head with hair piled into a tall rounded cone on top, smooth at the sides",
      tags=["beehive", "bouffant", "1960s hair", "retro hairstyle", "updo", "vintage", "tall hair"])
def _(S):
    cone = "M5.3 11.5C5.2 6.8 7.5 3.4 11 1.8C14.5 3.4 17 6.8 16.8 11.5Z"
    head = union(scaled(PROFILE, 0.82), cone)
    return [shell(head), eye(S, 14.6, 12.2, 0.8), detail("M6.8 8.4C9 9.6 13 9.6 15.8 8"), detail("M7.8 5C9.8 6 12.5 6 14.4 4.8")]


@icon("fade-haircut", CAT, "Side view of a head with short hair on top that fades to bare skin at the sides, shown by shrinking dots",
      tags=["skin fade", "taper", "barber", "short back and sides", "men's haircut", "gradient", "clippers"])
def _(S):
    cap_ = "M4.5 8.4C4 4.2 7 2 11 2C15.2 2 18.4 4.5 18.8 8.6C15 6.8 8 6.5 4.5 8.4Z"
    return side(S, [cap_]) + [detail("M4.2 9C8 7.2 15 7.2 18.6 9"),
                             dot(5.6, 11.4, 1.0), dot(8.4, 11.4, 1.0), dot(11.2, 11.4, 1.0),
                             dot(5.6, 13.9, 0.8), dot(8.4, 13.9, 0.8), dot(5.8, 15.9, 0.6)]


@icon("finger-waves", CAT, "Side view of a head with short hair set into flat S shaped ridged waves across the head",
      tags=["1920s hair", "marcel waves", "retro hairstyle", "flapper", "vintage", "waves", "art deco"])
def _(S):
    return side(S) + [detail("M17 7C15 4.4 12.8 8 10.8 5.4C9.5 3.8 7.5 4.2 5.8 6.4"),
                      detail("M12.8 11.2C11 9.2 9.2 12.2 7.4 10C6.6 9 5.8 9.4 5.2 10.2")]


@icon("hair-perm", CAT, "Side view of a head with rows of small perm rods wound tight across the hair",
      tags=["perm rods", "curlers", "rollers", "curling", "salon", "hair treatment", "permanent wave"])
def _(S):
    spots = [(5.2, 7), (8.4, 3.9), (12.8, 3.4), (16.4, 5.6), (4.4, 11.6)]
    return side(S, [circle(x, y, 2.4) for x, y in spots]) + [dot(x, y, 0.8) for x, y in spots]


@icon("hair-foils", CAT, "Side view of a head with several folded foil packets lying in layers across the hair",
      tags=["highlights", "foil highlights", "balayage", "hair colour", "salon", "bleach", "colouring"])
def _(S):
    k = 0.82
    packets = [rot(rect(2.2, 4.4, 7, 3.4), -12, 5.7, 6.1), rot(rect(2.2, 9.2, 7, 3.4), 6, 5.7, 10.9), rot(rect(2.6, 14, 6.4, 3.4), -8, 5.8, 15.7)]
    return [shell(union(scaled(PROFILE, k, 17, 22), *packets)), eye(S, 17 + (15.2 - 17) * k, 22 - 12 * k, 0.8)]


@icon("highlighting-cap", CAT, "Front view of a head in a snug cap dotted with holes, strands pulled through them and a hook tool beside it",
      tags=["highlight cap", "frosting cap", "streaks", "hair colour", "salon", "balayage", "crochet hook"])
def _(S):
    return [shell("M4.5 11.5A5.5 5.5 0 0 1 15.5 11.5Z"),
            dot(7, 9.8, 0.9), dot(10, 8.6, 0.9), dot(13, 9.8, 0.9),
            line(seg(7.6, 6.7, 7, 3.4)), line(seg(10, 6, 10, 2.5)), line(seg(12.4, 6.7, 13, 3.4)),
            line("M20.5 21.5V10.5C20.5 8.7 18.8 8.2 18.2 9.4")] + face(S, 5.5, 11.5, 19.5, 10, 14)


# ----------------------------------------------------------------------------- lower face and facial hair
LOWER_JAW = "M5.5 3V9C5.5 15 8.5 21.5 12 21.5C15.5 21.5 18.5 15 18.5 9V3"


@icon("pencil-mustache", CAT, "Lower face with a very thin narrow line mustache just above the upper lip, split by a small gap",
      tags=["thin mustache", "moustache", "facial hair", "retro", "gentleman", "barber", "grooming"], aliases=["pencil-moustache"])
def _(S):
    return [line(LOWER_JAW), line(seg(7.3, 12.3, 11, 12.3)), line(seg(13, 12.3, 16.7, 12.3)), line(seg(10.2, 16.6, 13.8, 16.6))]


@icon("walrus-mustache", CAT, "Lower face with a thick bushy mustache that droops over the whole upper lip and past the mouth corners",
      tags=["bushy mustache", "moustache", "handlebar", "facial hair", "grooming", "barber", "old fashioned"], aliases=["walrus-moustache"])
def _(S):
    must = ("M12 11C13.6 9.8 16.4 9.8 18 11.2C18.9 13.4 18.8 16 17.6 18.6C16.8 16.4 14.8 14.8 12 14.6"
            "C9.2 14.8 7.2 16.4 6.4 18.6C5.2 16 5.1 13.4 6 11.2C7.6 9.8 10.4 9.8 12 11Z")
    return [line(LOWER_JAW), shell(must, stroke_miterlimit="2")]


@icon("horseshoe-mustache", CAT, "Lower face with a mustache running down both sides of the mouth to the jaw in an upside down U",
      tags=["horseshoe moustache", "biker mustache", "facial hair", "grooming", "barber", "retro", "chevron"], aliases=["horseshoe-moustache"])
def _(S):
    return [line(LOWER_JAW), line(poly([(9, 19), (9, 12), (15, 12), (15, 19)], r=S.r * 0.6))]


@icon("soul-patch", CAT, "Lower face with a small tuft of hair just below the lower lip and no other facial hair",
      tags=["goatee", "chin tuft", "facial hair", "jazz beard", "grooming", "barber", "beard"])
def _(S):
    return [line(LOWER_JAW), line(seg(10, 13.2, 14, 13.2)), shell(poly([(10.4, 16.2), (13.6, 16.2), (12, 19.4)], closed=True, r=S.r * 0.3))]


@icon("van-dyke-beard", CAT, "Lower face with an upturned mustache and a separate pointed goatee on the chin, cheeks bare",
      tags=["goatee", "pointed beard", "waxed mustache", "facial hair", "musketeer", "barber", "grooming"])
def _(S):
    must = ("M12 12C10.5 10.8 8.8 10.8 7.2 11.8C6 12.6 5 12 4.2 10.2C4.3 13.6 6.4 15 8.8 14.6C10.4 14.4 11.4 13.4 12 12.8"
            "C12.6 13.4 13.6 14.4 15.2 14.6C17.6 15 19.7 13.6 19.8 10.2C19 12 18 12.6 16.8 11.8C15.2 10.8 13.5 10.8 12 12Z")
    return [line("M5.5 3V9C5.5 14 7.2 17.5 9 19.2"), line("M18.5 3V9C18.5 14 16.8 17.5 15 19.2"), 
            shell(must, stroke_miterlimit="2"),
            shell(poly([(9.2, 16.8), (14.8, 16.8), (12, 21.5)], closed=True, r=S.r * 0.4))]
