"""TypeIcon Core: professions (batch 003), workers, makers, traders, drivers, uniformed roles and performers.

Most icons are a bust (head circle over shoulders) with a hat or tool, or a small bust beside the
tool of the trade. Action poses (juggler, acrobat, tightrope walker) use a stick body like `person-standing`.
Layers are listed front first; layers behind are cut away around the front silhouette.
"""
from dsl import arc, circle, detail, dot, ellipse, icon, line, poly, rect, seg, shell, solid, Part  # noqa: F401
from dsl import LINE, D, P, ST, U, filled_region
from geometry import fmt, path_to_d, polar

CAT = "professions"


# --------------------------------------------------------------------------- layering (same idea as people.py)

def _paint(parts, S):
    regs = []
    for p in parts:
        if p.kind in ("dot", "solid"):
            regs.append(P(p.d))
        else:
            regs.append(ST(p.d, 2.0, S.cap, S.join, float(p.attrs.get("stroke_miterlimit", 4))))
    return U(*regs)


def _sil(parts, S):
    regs = []
    for p in parts:
        if p.kind in ("dot", "solid"):
            regs.append(P(p.d))
        elif p.kind == "shell":
            regs.append(U(P(p.d), ST(p.d, 2.0, S.cap, S.join, float(p.attrs.get("stroke_miterlimit", 4)))))
        else:
            regs.append(ST(p.d, 2.0, S.cap, S.join))
    return U(*regs)


def _grow(region, g):
    if g <= 0:
        return region
    return U(region, ST(path_to_d(region), 2 * g, "round", "round"))


def _unpack(layer, gap, fgap):
    if isinstance(layer, tuple):
        return layer
    return layer, gap, fgap


def _stroke_layers(S, layers, gap, fgap):
    parts, halo, _ = _unpack(layers[0], gap, fgap)
    out = list(parts)
    cover = _grow(_sil(parts, S), halo)
    for layer in layers[1:]:
        parts, halo, _ = _unpack(layer, gap, fgap)
        if not parts:
            continue
        vis = D(_paint(parts, S), cover)
        if abs(vis.area) > 0.01:
            out.append(solid(path_to_d(vis)))
        cover = U(cover, _grow(_sil(parts, S), halo))
    return out


def _filled_layers(layers, gap, fgap):
    parts, _, fh = _unpack(layers[0], gap, fgap)
    result = filled_region(parts)
    cover = _grow(result, fh)
    for layer in layers[1:]:
        parts, _, fh = _unpack(layer, gap, fgap)
        if not parts:
            continue
        f = filled_region(parts)
        result = U(result, D(f, cover))
        cover = U(cover, _grow(f, fh))
    return result


def figure(name, desc, tags, aliases=(), gap=1.5, fgap=None):
    fg = gap if fgap is None else fgap

    def deco(fn):
        icon(name, CAT, desc, tags=tags, aliases=aliases,
             filled=lambda: _filled_layers(fn(LINE), gap, fg))(lambda S: _stroke_layers(S, fn(S), gap, fg))
        return fn
    return deco


# --------------------------------------------------------------------------- shared shapes

def _bust(S, cx=12.0, top=14.0, hw=7.0, bottom=21.0):
    r = hw - (1.0 if S.name != "line" else 2.0)
    r = min(r, bottom - top)
    x0, x1 = cx - hw, cx + hw
    return (f"M{fmt(x0)} {fmt(bottom)}V{fmt(top + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x0 + r)} {fmt(top)}"
            f"H{fmt(x1 - r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(top + r)}V{fmt(bottom)}")


def _person(S, cx=12.0, hy=7.5, hr=3.5, top=14.0, hw=7.0, bottom=21.0):
    return [shell(circle(cx, hy, hr)), shell(_bust(S, cx, top, hw, bottom))]


def _role(S, cx=12.0, hy=10.0):
    return _person(S, cx, hy, 3.0, 16.0, 6.5)


def _left(S):
    """Small person on the left, for icons with a tool of the trade on the right."""
    return _person(S, 7, 9.5, 2.5, 14.5, 4.5)


def _right(S):
    return _person(S, 17, 9.5, 2.5, 14.5, 4.5)


def _u(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def _mouth(cx, y, w=2.8):
    """Open mouth: a small solid half disc."""
    h = w / 2
    return Part("dot", f"M{fmt(cx - h)} {fmt(y)}H{fmt(cx + h)}A{fmt(h)} {fmt(h)} 0 0 1 {fmt(cx - h)} {fmt(y)}Z")


def _hat(parts):
    return (parts, 0.0, 1.0)


def _mark(d):
    return Part("dot", d)


def _stick(S, cx=12.0, hy=4.5, hr=2.25):
    """Head dot, shoulders/arms, torso, legs like person-standing; returns parts."""
    return [dot(cx, hy, hr),
            line(poly([(cx - 5.5, 14.5), (cx - 3.5, 9.5), (cx + 3.5, 9.5), (cx + 5.5, 14.5)], r=S.r)),
            line(seg(cx, 9.5, cx, 14.5)),
            line(poly([(cx - 3.5, 21), (cx, 14.5), (cx + 3.5, 21)], r=S.r))]


def _helmet(S, cx, base, rad):
    """Hard hat: dome plus brim."""
    return [shell(f"M{fmt(cx - rad)} {fmt(base)}A{fmt(rad)} {fmt(rad)} 0 0 1 {fmt(cx + rad)} {fmt(base)}Z"),
            line(seg(cx - rad - 1.5, base, cx + rad + 1.5, base))]


def _cap(S, cx, base, w=3.2):
    """Small peaked cap: crown plus a short peak to the left."""
    return [shell(poly([(cx - w, base), (cx - w + 0.5, base - 2.5), (cx + w - 0.5, base - 2.5), (cx + w, base)], closed=True, r=S.r * 0.5)),
            line(seg(cx - w - 1.5, base, cx + w, base))]


# ============================================================================ chunk 1

@figure("lineworker", "A worker climbing a utility pole with a crossarm and a wire",
        tags=["lineman", "linesman", "electrician", "utility", "power lines", "pole", "climber"], aliases=["lineman"])
def _(S):
    return [[line(seg(17, 2.5, 17, 21.5)), line(seg(2.5, 5, 22, 5)),
             dot(8, 10, 2.25), line(seg(8, 13, 8, 17.5)),
             line(poly([(8, 14), (12.5, 13.5), (17, 12)], r=S.r)),
             line(poly([(8, 17.5), (12.5, 19.5), (17, 18)], r=S.r)),
             line(seg(8, 17.5, 6.5, 21.5))]]


@figure("solar-panel-installer", "A worker in a hard hat carrying a tilted solar panel grid",
        tags=["solar", "panel", "installer", "renewable", "photovoltaic", "roof", "energy"])
def _(S):
    panel = poly([(11, 8), (22, 5.5), (22, 15.5), (11, 18)], closed=True, r=S.r * 0.5)
    return [[shell(panel), detail(seg(16.5, 6.75, 16.5, 16.75)), detail(seg(11.5, 13, 21.5, 10.5))],
            _hat(_helmet(S, 7, 9, 3.5)),
            _person(S, 7, 11, 2.5, 15.5, 4.5)]


@figure("wind-turbine-technician", "A worker in a harness on the tower of a wind turbine below three blades",
        tags=["wind", "turbine", "technician", "renewable", "energy", "tower", "climber"])
def _(S):
    blades = [solid(poly([polar(11, 7.5, 1.4, a - 90), polar(11, 7.5, 6.3, a), polar(11, 7.5, 1.4, a + 90)], closed=True))
              for a in (-90, 30, 150)]
    return [blades + [dot(11, 7.5, 1.8), line(seg(11, 9, 11, 21.5)),
                      dot(18.5, 15.5, 1.75), line(seg(18.5, 17.5, 18.5, 20)), line(seg(18.5, 18.2, 11.5, 18.2)),
                      line(seg(18.5, 20, 17.5, 22)), line(seg(18.5, 20, 19.5, 22))]]


@figure("car-washer", "A worker spraying water from a hose onto a car with bubbles",
        tags=["car wash", "cleaner", "hose", "vehicle", "auto", "detailing", "valet"])
def _(S):
    body = poly([(10, 21), (10, 17.5), (13, 16.5), (14.5, 13.5), (19, 13.5), (20.5, 16.5), (22, 17.5), (22, 21)], closed=True, r=S.r * 0.5)
    return [[shell(body), detail(seg(10.5, 18.5, 21.5, 18.5))],
            [shell(circle(17, 5, 1.5)), shell(circle(21, 8.5, 1.25)), dot(13.5, 7.5, 1), line(seg(10.5, 10, 12.5, 9))],
            _person(S, 6, 9.5, 2.5, 14.5, 4)]


@figure("gas-station-attendant", "A worker in a cap beside a fuel pump",
        tags=["petrol", "fuel", "pump", "filling station", "gas pump", "attendant", "forecourt"])
def _(S):
    return [[shell(rect(13.5, 4, 7, 17, min(S.R, 2))), detail(rect(15, 6.5, 4, 3.5, 0.5)),
             line("M20.5 11.5H22.5V17")],
            _hat(_cap(S, 7, 8.2)),
            _person(S, 7, 10.5, 2.5, 15, 4.5)]


@figure("parking-attendant", "A worker in a cap writing a ticket beside a sign with a large P",
        tags=["parking", "valet", "car park", "ticket", "warden", "attendant", "lot"])
def _(S):
    return [[shell(rect(10.5, 2.5, 11, 10, min(S.R, 2))), detail("M14.5 10.5V5.5H17A1.75 1.75 0 0 1 17 9H14.5"),
             line(seg(16, 12.5, 16, 21.5))],
            _hat(_cap(S, 6, 8.2, 2.8)),
            _person(S, 6, 10.5, 2.25, 15, 3.75)]


@figure("handyperson", "A worker carrying an open toolbox with a hammer sticking out",
        tags=["handyman", "odd jobs", "repair", "toolbox", "fixer", "maintenance", "diy"], aliases=["handyman"])
def _(S):
    return [[shell(rect(11.5, 14, 10, 7, min(S.R, 1.5))), line("M14.5 14V12.5H18.5V14"),
             line(seg(16, 12.5, 18.5, 6)), solid(poly([(15.5, 4.5), (21, 6.5), (20.3, 8.3), (14.8, 6.3)], closed=True))],
            _person(S, 8, 9.5, 2.75, 14.5, 5)]


@figure("appliance-repair-technician", "A worker in a hard hat beside a washing machine",
        tags=["appliance", "repair", "washing machine", "technician", "fix", "screwdriver", "service"])
def _(S):
    return [[shell(rect(12.5, 3, 9.5, 18, min(S.R, 2))), shell(circle(17.25, 14, 2.75)), detail(seg(14.5, 6.5, 19.5, 6.5))],
            _hat(_helmet(S, 7, 8.8, 3)),
            _person(S, 7, 10.5, 2.5, 15, 4.5)]


@figure("glassblower", "A worker blowing through a long pipe with a round glass bubble at the end",
        tags=["glass", "blowing", "artisan", "furnace", "craft", "bubble", "blowpipe"])
def _(S):
    return [[line(seg(10, 9.5, 15.5, 7)), shell(circle(18.5, 6, 3.25))],
            _person(S, 7, 10, 2.5, 15, 4.5)]


@figure("potter", "Hands cupping a clay pot on a spinning wheel",
        tags=["pottery", "clay", "ceramics", "wheel", "pot", "craft", "artisan"])
def _(S):
    pot = "M14 4.5H19C19 6.5 21 8 21 11C21 13.5 19.5 14.5 19 15H14C13.5 14.5 12 13.5 12 11C12 8 14 6.5 14 4.5Z"
    return [[shell(pot), line(seg(10, 17.5, 22, 17.5)), line(seg(16, 17.5, 16, 21))],
            _person(S, 6.5, 9.5, 2.5, 14.5, 4.5)]


@figure("sculptor", "A person with a chisel beside a bust on a plinth",
        tags=["sculpture", "statue", "carving", "chisel", "mallet", "artist", "stone"])
def _(S):
    return [[shell(circle(17.5, 6.5, 2.75)), shell(rect(13, 17, 9, 4, 0.5)),
             line(_bust(S, 17.5, 12, 4.5, 17))],
            _person(S, 6.5, 9.5, 2.5, 14.5, 4.5)]


@figure("weaver", "A person seated at a loom with vertical threads and a shuttle",
        tags=["weaving", "loom", "textile", "thread", "fabric", "craft", "yarn"])
def _(S):
    return [[shell(rect(12, 3, 10, 18, min(S.R, 1.5))), detail(seg(15.5, 3.5, 15.5, 20.5)), detail(seg(18.5, 3.5, 18.5, 20.5)),
             detail(seg(12.5, 14, 21.5, 14))],
            _person(S, 6.5, 9.5, 2.5, 14.5, 4.5)]


@figure("calligrapher", "A person holding a brush above paper with a single bold stroke",
        tags=["calligraphy", "lettering", "brush", "ink", "handwriting", "scribe", "writing"])
def _(S):
    return [[shell(rect(11.5, 11, 10.5, 10, min(S.R, 1.5))), detail("M14 18C15.5 13 18 13 19.5 16"),
             line(seg(14, 9, 18.5, 3)), solid("M13.2 8.4L15.2 10.3L13 10.6Z")],
            _person(S, 6.5, 9.5, 2.5, 14.5, 4.5)]


@figure("printmaker", "A person rolling a brayer over an inked block",
        tags=["printmaking", "linocut", "brayer", "ink", "print", "block", "artist"])
def _(S):
    return [[shell(rect(11.5, 15, 10.5, 6, min(S.R, 1.5))), detail("M13.5 18C15 16.5 17 19.5 20 17.5"),
             shell(rect(11.5, 7.5, 10.5, 4, 1.5)), line("M16.75 7.5V4H21.5")],
            _person(S, 6.5, 9.5, 2.5, 14.5, 4.5)]


@figure("bookbinder", "A person pressing a book in a small screw press",
        tags=["bookbinding", "book", "press", "binding", "craft", "library", "conservator"])
def _(S):
    return [[shell(rect(12, 13, 9.5, 5, 0.5)), line(seg(11, 20.5, 22.5, 20.5)),
             line(seg(11, 10.5, 22.5, 10.5)), line(seg(16.75, 3, 16.75, 10.5)), line(seg(14, 3, 19.5, 3))],
            _person(S, 6, 9.5, 2.5, 14.5, 4)]


def _awning(S, x0=2, x1=22, top=3, bottom=8, n=5):
    """Scalloped awning: a trapezoid whose lower edge is a row of arcs."""
    w = (x1 - x0) / n
    d = f"M{fmt(x0 + 2)} {fmt(top)}H{fmt(x1 - 2)}L{fmt(x1)} {fmt(bottom)}"
    x = x1
    for _ in range(n):
        d += f"A{fmt(w / 2)} {fmt(w / 2)} 0 0 1 {fmt(x - w)} {fmt(bottom)}"
        x -= w
    return d + "Z"


# ============================================================================ chunk 2

@figure("winemaker", "A person with a bunch of grapes beside a wooden barrel",
        tags=["wine", "vineyard", "grapes", "barrel", "vintner", "winery", "cellar"], aliases=["vintner"])
def _(S):
    grapes = [dot(x, y, 1.4) for x, y in ((14.5, 3.8), (17.5, 3.8), (20.5, 3.8), (16, 6.6), (19, 6.6), (17.5, 9.4))]
    barrel = "M13 12.5C12 14.5 12 18.5 13 21H21C22 18.5 22 14.5 21 12.5Z"
    return [[shell(barrel), detail(seg(12.5, 15, 21.5, 15)), detail(seg(12.5, 18.5, 21.5, 18.5))] + grapes,
            _person(S, 6.5, 9.5, 2.5, 14.5, 4.5)]


@figure("brewer", "A person with a long mash paddle over a large kettle with a hop cone",
        tags=["beer", "brewery", "kettle", "mash", "hops", "brewing", "craft beer"], aliases=["beer-maker"])
def _(S):
    kettle = "M11.5 11H21.5V18A3 3 0 0 1 18.5 21H14.5A3 3 0 0 1 11.5 18Z"
    return [[shell(kettle), line(seg(10.5, 11, 22.5, 11)), line(seg(10.5, 3.5, 16, 14)),
             shell("M19 3C21 4.5 21 7 19 8.5C17 7 17 4.5 19 3Z")],
            _person(S, 6, 9.5, 2.5, 14.5, 4)]


@figure("fishmonger", "A person in an apron holding a large fish on a tray of ice",
        tags=["fish", "seafood", "market", "fishmonger", "fresh fish", "shop", "ice"], aliases=["fishseller"])
def _(S):
    fish = _u(ellipse(16, 9, 4.5, 2.75), poly([(19.5, 9), (22.5, 6), (22.5, 12)], closed=True))
    return [[shell(rect(11, 15.5, 11.5, 5, min(S.R, 1.5))), shell(fish), _mark(circle(13.8, 8.4, 0.8))],
            _person(S, 6, 9.5, 2.5, 14.5, 4)]


@figure("greengrocer", "A person behind a crate of vegetables holding up a carrot",
        tags=["vegetables", "produce", "grocer", "carrot", "market", "fruit seller", "shop"], aliases=["produce-seller"])
def _(S):
    carrot = poly([(14.5, 6.5), (19.5, 6.5), (17, 15)], closed=True, r=S.r * 0.4)
    return [[shell(rect(11, 14.5, 11.5, 6.5, min(S.R, 1.5))), detail(seg(11.5, 17.75, 22, 17.75))],
            [shell(carrot), line("M17 6.5V3.5"), line("M17 5C15.5 4 14.5 4 14 3"), line("M17 5C18.5 4 19.5 4 20 3")],
            _person(S, 6, 9.5, 2.5, 14.5, 4)]


@figure("street-food-vendor", "A person behind a small food cart with a striped umbrella",
        tags=["food cart", "street food", "hawker", "stall", "vendor", "umbrella", "snacks"], aliases=["hawker"])
def _(S):
    return [[shell("M11.5 8.5A5.5 5.5 0 0 1 22.5 8.5Z"), line(seg(17, 8.5, 17, 14)),
             shell(rect(11.5, 14, 11, 4, 1)), shell(circle(15, 20, 1.5))],
            _person(S, 6, 9.5, 2.5, 14.5, 4)]


@figure("ice-cream-vendor", "A person in a cap holding out an ice cream cone",
        tags=["ice cream", "cone", "vendor", "seller", "summer", "gelato", "cart"], aliases=["gelato-seller"])
def _(S):
    cone = poly([(14.5, 11), (20.5, 11), (17.5, 20.5)], closed=True, r=S.r * 0.3)
    return [[shell(cone), shell(circle(17.5, 7, 3.5))],
            _hat(_cap(S, 7, 8.2)),
            _person(S, 7, 10.5, 2.5, 15, 4.5)]


@figure("market-vendor", "A person behind a stall table under a scalloped awning with produce",
        tags=["market", "stall", "vendor", "trader", "awning", "farmers market", "seller"], aliases=["stallholder"])
def _(S):
    return [[shell(rect(3, 18, 18, 3, 0.5))] + [shell(circle(7.5, 16.25, 1.75)), shell(circle(16.5, 16.25, 1.75))],
            [shell(_awning(S, 2, 22, 2.5, 7.5))],
            _person(S, 12, 12, 2.25, 15.5, 4.5)]


@figure("shopkeeper", "A person in an apron standing in a shop doorway under a striped awning",
        tags=["shop", "store", "owner", "retail", "merchant", "awning", "storekeeper"], aliases=["storekeeper"])
def _(S):
    return [[shell(_awning(S, 2, 22, 2.5, 7.5)), line(seg(5, 9.5, 5, 21.5)), line(seg(19, 9.5, 19, 21.5))],
            _person(S, 12, 12.5, 2.5, 16.5, 4.5) + [detail(seg(12, 16.5, 12, 21))]]


@figure("newspaper-seller", "A person holding up a folded newspaper with a bundle under the other arm",
        tags=["newspaper", "news", "paper boy", "vendor", "press", "headline", "kiosk"], aliases=["paperboy"])
def _(S):
    return [[shell(rect(12, 4, 10, 13, min(S.R, 1.5))), detail(seg(14.5, 8.5, 19.5, 8.5)), detail(seg(14.5, 12.5, 19.5, 12.5))],
            _person(S, 6.5, 9.5, 2.5, 14.5, 4.5)]


@figure("auctioneer", "A person behind a lectern with a gavel on a block",
        tags=["auction", "gavel", "bidding", "sale", "hammer", "lot", "sold"])
def _(S):
    head = poly([(14.0, 5.5), (17.0, 3.5), (21.0, 7.5), (19.0, 10.5)], closed=True, r=S.r * 0.3)
    return [[shell(head), line(seg(16.5, 9, 12.5, 15.5)), line(seg(12, 21, 22, 21))],
            _person(S, 6.5, 9.5, 2.5, 14.5, 4.5)]


@figure("optician", "A person in a coat holding up a pair of glasses beside an eye chart",
        tags=["glasses", "eye test", "eyewear", "vision", "spectacles", "lenses", "eye chart"], aliases=["eye-tester"])
def _(S):
    return [[shell(rect(12, 3, 10, 8, min(S.R, 1.5))), detail(seg(14.5, 6, 17, 6)), detail(seg(14.5, 8.5, 19.5, 8.5)),
             shell(circle(14.5, 16.5, 2.5)), shell(circle(20, 16.5, 2.5)), line(seg(16.5, 15.5, 18, 15.5))],
            _person(S, 6, 9.5, 2.5, 14.5, 4)]


@figure("pet-groomer", "A person with clippers beside a fluffy poodle on a table",
        tags=["grooming", "poodle", "dog", "pet", "salon", "clippers", "haircut"], aliases=["dog-groomer"])
def _(S):
    return [[shell(circle(15.5, 13, 2.75)), shell(circle(19.5, 8.5, 2)), dot(19.5, 4.8, 1.3),
             line(seg(13.5, 15.5, 13.5, 19)), line(seg(17.5, 15.5, 17.5, 19)), shell(circle(11.8, 11, 1.4)),
             line(seg(11, 19.5, 22.5, 19.5))],
            _person(S, 6, 9.5, 2.5, 14.5, 4)]


@figure("dog-walker", "A person holding a leash to a small dog",
        tags=["dog", "walking", "leash", "pet", "pets", "lead", "puppy"], aliases=["pet-walker"])
def _(S):
    dog = _u(ellipse(16.5, 17, 4, 2.4), circle(21, 14, 2))
    return [[shell(dog), line(seg(13.5, 18, 13.5, 21.5)), line(seg(19, 18, 19, 21.5)), line("M12.5 16C11.5 15 11.3 14 11.5 13"),
             line("M10.5 13.5L19.5 13")],
            _person(S, 6, 9.5, 2.5, 14.5, 4)]


def _bike(S, with_rider=True):
    """Side view of a bicycle with a rider; returns parts."""
    parts = [line(circle(6, 17, 3.5)), line(circle(18, 17, 3.5)),
             line(poly([(6, 17), (10.5, 12), (15.5, 12), (18, 17)], r=S.r)), line(seg(10.5, 12, 12.5, 17)),
             line(seg(15.5, 12, 15.5, 9.5)), line(seg(14, 9.5, 17.5, 9.5))]
    return parts


# ============================================================================ chunk 3

@figure("mail-carrier", "A person in a cap with a mailbag strap across the body holding an envelope",
        tags=["postman", "postal", "mail", "letter carrier", "post office", "envelope", "mailman"], aliases=["postman", "mailman"])
def _(S):
    return [[shell(rect(14, 6, 8.5, 6.5, 1)), detail("M14.5 7L18.25 10L22 7")],
            _hat(_cap(S, 8, 8.2)),
            _person(S, 8, 10.5, 2.75, 15.5, 5.5) + [detail(seg(5, 17, 10.5, 21))]]


@figure("delivery-courier", "A person in a cap carrying a parcel box",
        tags=["parcel", "package", "delivery", "courier", "shipping", "box", "driver"], aliases=["parcel-carrier"])
def _(S):
    return [[shell(rect(13, 10, 9.5, 9.5, 1)), detail(seg(17.75, 10, 17.75, 19.5)), detail(seg(13, 13.5, 22.5, 13.5))],
            _hat(_cap(S, 7, 8.2)),
            _person(S, 7, 10.5, 2.5, 15, 4.5)]


@figure("food-delivery-rider", "A rider on a bicycle with a large square insulated box on the back",
        tags=["food delivery", "courier", "bicycle", "takeaway", "rider", "bike", "meal delivery"], aliases=["delivery-cyclist"])
def _(S):
    return [_bike(S) + [shell(rect(1.5, 3.5, 7.5, 7.5, 1)), dot(13, 4.5, 1.9), line(seg(13, 7.5, 10.5, 12)),
                        line(seg(12.5, 8.5, 15.5, 9.5))]]


@figure("bike-messenger", "A rider on a bicycle with a messenger bag slung across the back",
        tags=["cyclist", "messenger", "bag", "courier", "bike", "urban", "fixie"], aliases=["cycle-courier"])
def _(S):
    return [_bike(S) + [dot(13, 4.5, 1.9), line(seg(13, 7.5, 10.5, 12)), line(seg(12.5, 8.5, 15.5, 9.5)),
                        shell(poly([(8.2, 5.5), (11, 4.8), (11.5, 9), (8.7, 9.7)], closed=True))]]


@figure("truck-driver", "A person in a trucker cap beside a truck",
        tags=["lorry", "haulage", "trucker", "freight", "driver", "hgv", "transport"], aliases=["trucker", "lorry-driver"])
def _(S):
    truck = poly([(11, 8.5), (17, 8.5), (17, 11.5), (20, 11.5), (22.5, 15), (22.5, 18), (11, 18)], closed=True, r=S.r * 0.4)
    return [[shell(truck), shell(circle(14.5, 19, 1.75)), shell(circle(20, 19, 1.75))],
            _hat(_cap(S, 6.5, 8.2)),
            _person(S, 6.5, 10.5, 2.5, 15, 4.5)]


@figure("bus-driver", "A person in a cap seated behind a large flat bus steering wheel",
        tags=["bus", "driver", "coach", "public transport", "steering wheel", "chauffeur", "transit"], aliases=["coach-driver"])
def _(S):
    return [[shell(ellipse(12, 18.5, 8, 3)), detail(seg(12, 15.5, 12, 18.5))],
            _hat(_cap(S, 12, 7.2)),
            _person(S, 12, 9.5, 2.75, 14.5, 6.5)]


@figure("taxi-driver", "A person in a flat cap with a taxi sign above",
        tags=["taxi", "cab", "driver", "cabbie", "ride", "hire", "fare"], aliases=["cabbie", "cab-driver"])
def _(S):
    cap = poly([(8, 9.5), (8.5, 7.5), (14.5, 7.2), (16, 9.5)], closed=True, r=S.r * 0.4)
    return [[shell(rect(7.5, 2, 9, 3.5, 1))],
            _hat([shell(cap), line(seg(6.5, 9.5, 16, 9.5))]),
            _person(S, 12, 11.5, 2.75, 16.5, 6.5)]


@figure("chauffeur", "A person in a peaked cap holding a car door open",
        tags=["driver", "limousine", "limo", "private driver", "car", "door", "valet"], aliases=["limo-driver"])
def _(S):
    door = poly([(15, 6), (21.5, 3.5), (21.5, 19), (15, 21)], closed=True, r=S.r * 0.3)
    return [[shell(door), detail(poly([(17, 7), (19.5, 6), (19.5, 11), (17, 11.5)], closed=True))],
            _hat(_cap(S, 8, 8.2, 3.4)),
            _person(S, 8, 10.5, 2.75, 15.5, 5.5)]


@figure("train-conductor", "A person in a conductor cap holding a ticket with a punched hole",
        tags=["train", "rail", "guard", "ticket", "inspector", "railway", "punch"], aliases=["ticket-inspector"])
def _(S):
    return [[shell(rect(13, 8, 9.5, 8, 1)), detail(circle(17.75, 12, 1.25)), detail(seg(15, 8, 15, 16))],
            _hat(_cap(S, 7, 8.2)),
            _person(S, 7, 10.5, 2.5, 15, 4.5)]


@figure("train-driver", "A driver at the cab window of a locomotive with headlights below",
        tags=["locomotive", "engine driver", "railway", "engineer", "train", "cab", "rail"], aliases=["engine-driver"])
def _(S):
    return [[shell(rect(3.5, 3, 17, 18, min(S.R, 3))), detail(rect(6, 6, 12, 6.5, 1.5)), dot(12, 9.5, 1.6),
             dot(8, 16.5, 1.25), dot(16, 16.5, 1.25)]]


@figure("racing-driver", "A person in a full face helmet holding a checkered flag",
        tags=["race", "motorsport", "formula", "helmet", "checkered flag", "driver", "grand prix"], aliases=["race-driver"])
def _(S):
    flag = [solid(rect(x, y, 3, 3)) for x, y in ((16.5, 3), (19.5, 6), (16.5, 9))]
    return [[line(seg(15.5, 3, 15.5, 13))] + flag,
            [shell(circle(7.5, 10, 4.5)), detail(rect(4.3, 8.2, 6.4, 2.6, 1))],
            _person(S, 7.5, 10, 4.5, 16.5, 5)[1:]]


@figure("gondolier", "A person in a striped shirt and straw boater holding a long oar",
        tags=["gondola", "venice", "boatman", "oar", "straw hat", "boater", "rower"], aliases=["boatman"])
def _(S):
    hat = _u(rect(5.5, 4, 7, 4.5, 0.5), ellipse(9, 8.5, 5, 1.1))
    return [[line(seg(20.5, 2.5, 17.5, 17)), solid(poly([(16.2, 15.8), (19.2, 16.4), (20.5, 21.5), (17.2, 21.5)], closed=True))],
            _hat([shell(hat)]),
            _person(S, 9, 11, 2.75, 16, 5.5) + [detail(seg(5.5, 18, 12.5, 18))]]


@figure("vintage-aviator", "A person in a leather flying cap with goggles and a scarf",
        tags=["pilot", "flying cap", "goggles", "aviation", "scarf", "biplane", "pioneer"], aliases=["flying-ace"])
def _(S):
    cap = "M7.5 11C7.5 6 9.2 4 12 4C14.8 4 16.5 6 16.5 11Z"
    return [_hat([shell(cap), line(seg(6.5, 8, 17.5, 8))]),
            [shell(circle(12, 11, 4.5))],
            _person(S, 12, 11, 4.5, 17, 6.5)[1:] + [detail(seg(9.5, 17, 14.5, 17))]]


@figure("fighter-pilot", "A person in a flight helmet with a visor and an oxygen mask",
        tags=["jet", "pilot", "air force", "helmet", "visor", "aviator", "oxygen mask"], aliases=["jet-pilot"])
def _(S):
    return [[shell(circle(12, 9, 5.5)), detail(rect(8, 6.5, 8, 3.2, 1.2)),
             shell(poly([(9.5, 12.2), (14.5, 12.2), (13.5, 15), (10.5, 15)], closed=True, r=S.r * 0.3))],
            _person(S, 12, 9, 5.5, 17.5, 7)[1:]]


@figure("paratrooper", "A person hanging under an open round parachute canopy",
        tags=["parachute", "skydiver", "airborne", "jump", "drop", "soldier", "paratroops"], aliases=["skydiver"])
def _(S):
    return [[shell("M3.5 11A8.5 8.5 0 0 1 20.5 11Z"), detail(seg(9, 3, 9, 11)), detail(seg(15, 3, 15, 11)),
             line(seg(5, 11, 11, 16)), line(seg(19, 11, 13, 16)),
             dot(12, 17, 1.6), line(seg(12, 18.5, 12, 21.5))]]


# ============================================================================ chunk 4

def _star(cx, cy, r, ri=None):
    ri = r * 0.45 if ri is None else ri
    return poly([polar(cx, cy, r if k % 2 == 0 else ri, -90 + k * 36) for k in range(10)], closed=True)


@figure("general-officer", "A person in a peaked cap with stars on the shoulders",
        tags=["general", "army", "military", "officer", "commander", "brass", "stars"], aliases=["army-general"])
def _(S):
    cap = poly([(5.5, 5.5), (12, 3), (18.5, 5.5), (17, 8.5), (7, 8.5)], closed=True, r=S.r * 0.5)
    return [_hat([shell(cap), dot(12, 5.9, 1.1)]),
            _person(S, 12, 11, 2.75, 16, 6.5) + [_mark(_star(8, 19, 1.9)), _mark(_star(16, 19, 1.9))]]


@figure("drill-sergeant", "A person in a round brimmed campaign hat shouting with an open mouth",
        tags=["sergeant", "army", "military", "boot camp", "instructor", "shouting", "campaign hat"], aliases=["drill-instructor"])
def _(S):
    hat = _u(rect(8.5, 3, 7, 5, 1.5), ellipse(12, 8, 7.5, 1.2))
    return [_hat([shell(hat)]),
            [shell(circle(12, 11.5, 3.5)), _mouth(12, 11.8, 3), line(seg(17.5, 11, 20.5, 9.5)),
             line(seg(18, 14, 21, 15))],
            [shell(_bust(S, 12, 17, 6.5, 21))]]


@figure("royal-guard", "A person in a tall fur bearskin hat and a buttoned tunic standing at attention",
        tags=["guard", "bearskin", "palace", "sentry", "soldier", "ceremonial", "london"], aliases=["palace-guard"])
def _(S):
    hat = "M7.5 9.5C6.5 5 8.5 2.5 12 2.5C15.5 2.5 17.5 5 16.5 9.5Z"
    return [_hat([shell(hat), line(seg(7.5, 9.5, 16.5, 9.5))]),
            _person(S, 12, 12.5, 2.5, 17, 6.5) + [_mark(circle(12, 19, 0.9)), _mark(circle(9.5, 19.4, 0.8)), _mark(circle(14.5, 19.4, 0.8))]]


@figure("opera-singer", "A person with the mouth wide open and musical notes above",
        tags=["singer", "soprano", "tenor", "aria", "classical", "vocalist", "performer"], aliases=["soprano", "tenor"])
def _(S):
    notes = [dot(17.5, 9, 1.6), line(seg(19.1, 9, 19.1, 3.5)), line(poly([(19.1, 3.5), (21.8, 5)]))]
    return [notes,
            [shell(circle(9, 10, 3.25)), _mouth(9, 10.6, 2.6)],
            [shell(_bust(S, 9, 16, 6, 21))]]


@figure("choir-singer", "A person in a robe holding an open songbook with notes above",
        tags=["choir", "chorus", "singer", "hymn", "songbook", "vocal", "church"], aliases=["chorister"])
def _(S):
    book = poly([(5, 16), (12, 17.5), (19, 16), (19, 21), (12, 22), (5, 21)], closed=True, r=S.r * 0.3)
    return [[shell(book), detail(seg(12, 17.5, 12, 22))],
            [shell(circle(12, 9, 3.25)), _mouth(12, 9.6, 2.6)],
            [dot(5.5, 6, 1.4), line(seg(6.9, 6, 6.9, 2.5)), dot(18, 5, 1.4), line(seg(19.4, 5, 19.4, 1.8))]]


@figure("orchestra-conductor", "A person in a tailcoat raising a thin baton",
        tags=["conductor", "maestro", "baton", "orchestra", "music director", "symphony", "tailcoat"], aliases=["maestro"])
def _(S):
    return [[line(seg(17.5, 12, 21.5, 4.5)), dot(17.5, 13, 1.5), dot(4, 5.5, 1.3), line(seg(5.3, 5.5, 5.3, 2.5))],
            _person(S, 11, 9, 3, 14.5, 6) + [detail(poly([(8, 15), (11, 19), (14, 15)], r=S.r * 0.3))]]


@figure("pianist", "A person seated at an upright piano with the keys in front",
        tags=["piano", "keyboard", "keys", "musician", "recital", "accompanist", "classical"], aliases=["piano-player"])
def _(S):
    return [[shell(rect(3, 14, 18, 7, min(S.R, 2))), detail(seg(3, 17.5, 21, 17.5)), detail(seg(8, 17.5, 8, 21)),
             detail(seg(12, 17.5, 12, 21)), detail(seg(16, 17.5, 16, 21))],
            _person(S, 12, 6.5, 3, 11.5, 6.5)]


# ============================================================================ chunk 5

def _body_blob(cx0, cy0, r0, cx1, cy1, r1):
    """Instrument body: two overlapping circles (upper and lower bout)."""
    return _u(circle(cx0, cy0, r0), circle(cx1, cy1, r1))


@figure("violinist", "A person holding a violin under the chin with a bow across the strings",
        tags=["violin", "fiddle", "strings", "bow", "musician", "orchestra", "classical"], aliases=["fiddler"])
def _(S):
    return [[shell(_body_blob(15.5, 15, 2.2, 17.5, 17.5, 2.8)), line(seg(14.3, 13.8, 11, 11))],
            [line(seg(10.5, 21.5, 22.5, 11.5))],
            _person(S, 7, 9, 2.75, 14.5, 4.5)]


@figure("cellist", "A seated person with a cello between the knees drawing a bow across",
        tags=["cello", "strings", "bow", "musician", "orchestra", "classical", "string quartet"], aliases=["cello-player"])
def _(S):
    return [[shell(_body_blob(16.5, 12.5, 2.5, 16.5, 17.5, 3.7)), line(seg(16.5, 10, 16.5, 2.5))],
            [line(seg(11, 14, 22.5, 14.5))],
            _person(S, 6.5, 9, 2.5, 14.5, 4.5)]


@figure("guitarist", "A person strumming an acoustic guitar held across the body",
        tags=["guitar", "acoustic", "strum", "musician", "band", "folk", "player"], aliases=["guitar-player"])
def _(S):
    return [[shell(_body_blob(15, 16.5, 3.5, 12, 14, 2.5)),
             line(seg(16, 13.5, 21.5, 4.5)), dot(15, 16.5, 1.1)],
            _person(S, 6.5, 8, 2.5, 13.5, 4.5)]


@figure("drummer", "A person behind a drum with a stick raised and a cymbal on a stand",
        tags=["drums", "drum kit", "percussion", "sticks", "band", "musician", "snare"], aliases=["percussionist"])
def _(S):
    return [[shell(rect(5, 15, 11, 6, min(S.R, 2))), detail(seg(5, 17.5, 16, 17.5)),
             line(seg(7, 15, 3.5, 9)), line(seg(20, 11, 20, 20.5)), solid("M16.5 9.4A3.5 1 0 1 0 23.5 9.4A3.5 1 0 1 0 16.5 9.4Z")],
            _person(S, 10, 7.5, 2.75, 12, 4.5)]


@figure("trumpeter", "A person blowing a trumpet pointed forward",
        tags=["trumpet", "brass", "horn", "jazz", "band", "musician", "fanfare"], aliases=["trumpet-player"])
def _(S):
    return [[line(seg(11.5, 10.5, 17, 10.5)), shell(poly([(17, 10.5), (22, 6), (22, 15)], closed=True, r=S.r * 0.2)),
             line(seg(14, 7.5, 14, 10.5))],
            _person(S, 7, 10, 3, 15.5, 5)]


@figure("saxophonist", "A person playing a curved saxophone held in front of the body",
        tags=["saxophone", "sax", "jazz", "reed", "woodwind", "musician", "blues"], aliases=["sax-player"])
def _(S):
    return [[line("M11 11L14.5 11.5C18 12 17 18 19 19.5C20.5 20.5 22 19 21.5 17"),
             solid("M19.6 13.2H23.2L22.6 16.8H20.2Z")],
            _person(S, 6.5, 9, 2.75, 14.5, 4.5)]


@figure("flutist", "A person holding a transverse flute sideways at the lips",
        tags=["flute", "woodwind", "orchestra", "musician", "flautist", "piccolo", "classical"], aliases=["flautist"])
def _(S):
    return [[line(seg(9.5, 10, 22.5, 6.5))],
            _person(S, 6, 11, 2.75, 16, 4.5)]


@figure("harpist", "A seated person beside a tall harp with strings",
        tags=["harp", "strings", "orchestra", "musician", "classical", "celtic", "angel"], aliases=["harp-player"])
def _(S):
    return [[shell("M21.5 21V5C16 3 12.5 5.5 12.5 9.5L16.5 21Z"), detail(seg(18, 6, 18, 19))],
            _person(S, 6, 9, 2.5, 14.5, 4)]


@figure("accordionist", "A person squeezing an accordion with pleated bellows",
        tags=["accordion", "squeezebox", "folk", "bellows", "musician", "polka", "player"], aliases=["accordion-player"])
def _(S):
    return [[shell(rect(3, 13.5, 18, 8, min(S.R, 2))), detail(seg(7, 13.5, 7, 21.5)), detail(seg(10.75, 13.5, 10.75, 21.5)),
             detail(seg(14.5, 13.5, 14.5, 21.5)), detail(seg(17.25, 13.5, 17.25, 21.5))],
            _person(S, 12, 6.5, 2.75, 11, 5)]


@figure("busker", "A person playing music with an upturned hat on the ground holding coins",
        tags=["street musician", "street performer", "coins", "tips", "hat", "music", "performer"], aliases=["street-performer"])
def _(S):
    hat = "M13 16.5H22.5L21 21H14.5Z"
    return [[shell(hat), dot(16.2, 13.8, 1), dot(19.8, 13.8, 1)],
            [dot(17, 6, 1.6), line(seg(18.6, 6, 18.6, 1.5))],
            _person(S, 7, 9.5, 2.75, 14.5, 4.5)]


@figure("drum-major", "A person in a tall plumed hat holding a long mace upright",
        tags=["marching band", "parade", "mace", "baton", "shako", "band leader", "majorette"], aliases=["majorette"])
def _(S):
    return [[line(seg(20.5, 8, 20.5, 21.5)), shell(circle(20.5, 5, 2.5))],
            _hat([shell(rect(7.5, 3, 7.5, 6, 1)), detail(seg(7.5, 6, 15, 6))]),
            _person(S, 11.25, 11.5, 2.75, 16.5, 5.5)]


@figure("cheerleader", "A person with arms raised holding two pom poms",
        tags=["pom poms", "cheer", "sports", "squad", "rally", "school spirit", "pep"], aliases=["pom-pom-girl"])
def _(S):
    return [[dot(12, 5, 2.25), shell(poly([(9, 9.5), (15, 9.5), (17, 16), (7, 16)], closed=True, r=S.r * 0.4)),
             line(seg(9.5, 10, 6.5, 6.5)), line(seg(14.5, 10, 17.5, 6.5)),
             shell(circle(5, 4.5, 2.2)), shell(circle(19, 4.5, 2.2)),
             line(seg(10.5, 16, 10.5, 21)), line(seg(13.5, 16, 13.5, 21))]]


@figure("ballet-dancer", "A person in a tutu standing on pointe with arms in a curved circle overhead",
        tags=["ballet", "dancer", "tutu", "pointe", "ballerina", "dance", "classical"], aliases=["ballerina"])
def _(S):
    return [[line("M7 11C5.5 5 8.5 2.5 12 2.5C15.5 2.5 18.5 5 17 11"), dot(12, 6.5, 1.9), line(seg(12, 8.5, 12, 12.5)),
             shell(ellipse(12, 14, 6.5, 1.6)),
             line(seg(11, 15.5, 11, 21.5)), line(seg(13.5, 15.5, 17, 20.5))]]


@figure("actor", "A person holding up a comedy mask and a tragedy mask beside the face",
        tags=["theatre", "theater", "stage", "masks", "drama", "performer", "thespian"], aliases=["thespian"])
def _(S):
    mask = lambda x, y: f"M{x} {y}H{x + 8}V{y + 5}A4 4 0 0 1 {x} {y + 5}Z"
    return [[shell(mask(14, 12.5)), dot(16.2, 15.5, 0.75), dot(19.8, 15.5, 0.75), detail("M16.3 18.2Q18 19.7 19.7 18.2")],
            [shell(mask(14, 2.5)), dot(16.2, 5.5, 0.75), dot(19.8, 5.5, 0.75), detail("M16.3 9.2Q18 7.7 19.7 9.2")],
            _person(S, 6.5, 9.5, 2.5, 14.5, 4.5)]


# ============================================================================ chunk 6

@figure("stand-up-comedian", "A person smiling beside a microphone on a stand",
        tags=["comedy", "comic", "microphone", "mic", "joke", "stage", "open mic"], aliases=["comic"])
def _(S):
    return [[shell(rect(15.5, 3, 4, 7, 2)), line(seg(17.5, 10, 17.5, 21.5)), line(seg(14, 21.5, 21, 21.5))],
            [shell(circle(7, 9, 3)), _mouth(7, 9.6, 2.6)],
            [shell(_bust(S, 7, 14.5, 4.5, 21))]]


@figure("clown", "A face with a round red nose, a puffy wig and a large bow tie",
        tags=["circus", "jester", "funny", "nose", "party", "entertainer", "birthday"])
def _(S):
    bow = poly([(6.5, 16.5), (11, 18.5), (13, 18.5), (17.5, 16.5), (17.5, 21.5), (13, 19.5), (11, 19.5), (6.5, 21.5)], closed=True)
    return [[shell(circle(12, 10.5, 4)), _mark(circle(12, 11.5, 1.4)), dot(10.3, 9, 0.7), dot(13.7, 9, 0.7)],
            [shell(circle(6.5, 8, 2.6)), shell(circle(17.5, 8, 2.6)), shell(circle(12, 4.5, 2.3))],
            [shell(bow)]]


@figure("mime", "A person in a striped shirt and beret pressing a palm against an invisible wall",
        tags=["pantomime", "silent", "performer", "street artist", "beret", "invisible wall", "mimic"], aliases=["pantomime"])
def _(S):
    return [[shell(rect(14.5, 9, 3.5, 6, 1.75)), line(seg(21.5, 3, 21.5, 7.5)), line(seg(21.5, 11, 21.5, 15.5)),
             line(seg(21.5, 19, 21.5, 21.5))],
            _hat([shell("M3.5 6.8C3.5 4.2 6 3 8.5 3C11.5 3 13 4.2 13 6.8Z"), line(seg(3.5, 6.8, 13, 6.8))]),
            _person(S, 8.25, 9.5, 2.5, 14.5, 4.75) + [detail(seg(4.5, 17.5, 12, 17.5)), detail(seg(4.5, 20, 12, 20))]]


@figure("magician", "A person holding a wand beside a top hat with a rabbit popping out",
        tags=["magic", "rabbit", "top hat", "wand", "illusionist", "trick", "show"], aliases=["illusionist"])
def _(S):
    return [[shell(rect(14.5, 10.5, 6, 7.5, 0.5)), line(seg(12, 18.5, 23, 18.5))],
            [solid(ellipse(16.4, 6, 1.2, 3.5)), solid(ellipse(19, 6, 1.2, 3.5))],
            [line(seg(9.5, 16, 12, 12))],
            _person(S, 6, 9.5, 2.5, 14.5, 4)]


@figure("juggler", "A person with three balls arcing in the air above the hands",
        tags=["juggling", "balls", "circus", "street performer", "entertainer", "skill", "toss"], aliases=["juggling"])
def _(S):
    return [[dot(6, 5, 1.6), dot(12, 3.2, 1.6), dot(18, 5, 1.6), dot(12, 10.5, 2),
             line(seg(12, 13, 12, 18)), line(poly([(6.5, 8.5), (9, 12.5), (12, 14)], r=S.r * 0.5)),
             line(poly([(17.5, 8.5), (15, 12.5), (12, 14)], r=S.r * 0.5)),
             line(seg(12, 18, 9.5, 21.5)), line(seg(12, 18, 14.5, 21.5))]]


@figure("acrobat", "A person doing a handstand with the legs split in a V",
        tags=["gymnast", "handstand", "circus", "balance", "tumbler", "flexible", "performer"], aliases=["tumbler"])
def _(S):
    return [[line(seg(12, 13, 12, 8)), line(seg(9, 13, 15, 13)), line(seg(9, 13, 8.5, 21.5)), line(seg(15, 13, 15.5, 21.5)),
             dot(12, 17.5, 1.8), line(seg(12, 8, 6.5, 2.5)), line(seg(12, 8, 17.5, 2.5))]]


@figure("trapeze-artist", "A person hanging by the knees from a horizontal trapeze bar on two ropes",
        tags=["trapeze", "circus", "aerialist", "swing", "flying", "acrobat", "bar"], aliases=["aerialist"])
def _(S):
    return [[line(seg(5, 8, 19, 8)), line(seg(6.5, 2, 6.5, 8)), line(seg(17.5, 2, 17.5, 8)),
             line(seg(12, 8, 12, 15.5)), dot(12, 18.5, 2),
             line(poly([(12, 12), (8.5, 16)], r=0)), line(poly([(12, 12), (15.5, 16)], r=0))]]


@figure("tightrope-walker", "A person balancing on a thin line holding a long bending pole",
        tags=["tightrope", "high wire", "balance", "circus", "funambulist", "daring", "wire walker"], aliases=["funambulist"])
def _(S):
    return [[line("M2.5 12C7 9 17 9 21.5 12"), dot(12, 4.5, 2), line(seg(12, 7, 12, 15)),
             line(seg(12, 15, 10, 19.5)), line(seg(12, 15, 14, 19.5)), line(seg(2.5, 21, 21.5, 21))]]


@figure("stilt-walker", "A person standing on very tall thin stilts with long trousers",
        tags=["stilts", "tall", "circus", "parade", "street performer", "giant", "entertainer"], aliases=["stilts"])
def _(S):
    return [[dot(12, 3.8, 2), line(poly([(6.5, 11), (9, 7), (15, 7), (17.5, 11)], r=S.r)), line(seg(12, 7, 12, 11)),
             line(poly([(10.5, 11), (9, 15.5), (9, 22)], r=S.r * 0.5)), line(poly([(13.5, 11), (15, 15.5), (15, 22)], r=S.r * 0.5)),
             line(seg(7, 15.5, 11, 15.5)), line(seg(13, 15.5, 17, 15.5))]]


@figure("ringmaster", "A person in a top hat and tailcoat raising one arm",
        tags=["circus", "showman", "top hat", "host", "tent", "announcer", "big top"], aliases=["showman"])
def _(S):
    hat = _u(rect(7, 2.5, 7, 5.5), rect(4.5, 7, 12, 1.75, 0.5))
    return [[line(poly([(14.5, 18), (18.5, 13), (19.5, 6)], r=S.r * 0.5)), dot(19.5, 4.5, 1.3)],
            _hat([shell(hat)]),
            _person(S, 10.5, 11.5, 2.75, 16.5, 6) + [detail(poly([(8, 17), (10.5, 20.5), (13, 17)], r=S.r * 0.3))]]


@figure("strongman", "A person lifting a barbell with two large round weights overhead",
        tags=["weightlifter", "barbell", "circus", "muscle", "strength", "lifting", "bodybuilder"])
def _(S):
    return [[line(seg(5, 5, 19, 5)), shell(circle(3.8, 5, 2.6)), shell(circle(20.2, 5, 2.6)),
             line(seg(7.5, 16, 6, 5)), line(seg(16.5, 16, 18, 5))],
            _person(S, 12, 11.5, 2.75, 15.5, 6.5)]


@figure("puppeteer", "A person holding a wooden control bar with strings to a small marionette",
        tags=["marionette", "puppet", "strings", "puppetry", "theatre", "show", "control bar"], aliases=["marionette-operator"])
def _(S):
    return [[line(seg(8.5, 7, 21, 7)), line(seg(13, 7, 15.5, 13)), line(seg(18.5, 7, 17.5, 13)),
             dot(16.5, 14.8, 1.6), line(seg(16.5, 16.5, 16.5, 19.5)), line(seg(16.5, 19.5, 15, 22)),
             line(seg(16.5, 19.5, 18, 22))],
            _person(S, 6, 11, 2.5, 15.5, 4)]


@figure("ventriloquist", "A seated person with a small puppet dummy on the knee with a hinged jaw",
        tags=["dummy", "puppet", "voice", "comedy", "act", "talking doll", "performer"], aliases=["dummy-act"])
def _(S):
    return [[shell(circle(17, 12.5, 3)), detail(seg(14.8, 13.8, 19.2, 13.8)), shell(rect(14.5, 17, 5, 4.5, 1)),
             shell(rect(15.2, 4.5, 3.6, 4, 0.5)), line(seg(13.5, 9, 20.5, 9))],
            _person(S, 7, 9, 2.5, 14.5, 4.5)]


@figure("zookeeper", "A person in a bush hat holding a feed bucket beside a giraffe neck",
        tags=["zoo", "animal keeper", "giraffe", "feeding", "wildlife", "bucket", "safari"], aliases=["animal-keeper"])
def _(S):
    hat = _u(rect(4.5, 4, 5, 3.5, 1), ellipse(7, 7.5, 5, 1.1))
    neck = poly([(15, 21), (15.5, 9), (18.5, 9), (19.5, 21)], closed=True)
    head = "M14.5 8.5V6.5A2.5 2.5 0 0 1 17 4H20.5A1.5 1.5 0 0 1 22 5.5V7A1.5 1.5 0 0 1 20.5 8.5Z"
    return [[shell(_u(neck, head)), line(seg(16, 4, 16, 2.3)), line(seg(19.5, 4, 19.5, 2.3)), _mark(circle(17.3, 13.5, 0.9)),
             _mark(circle(17.8, 17.5, 0.9))],
            _hat([shell(hat)]),
            _person(S, 7, 10.5, 2.5, 15, 4.5)]


@figure("forester", "A person in a cap marking a tree trunk beside pine trees",
        tags=["forest", "ranger", "trees", "woodland", "logging", "forestry", "pine"], aliases=["forest-ranger"])
def _(S):
    pine = poly([(17, 2.5), (21.5, 9.5), (19.5, 9.5), (22, 15), (12, 15), (14.5, 9.5), (12.5, 9.5)], closed=True, r=S.r * 0.3)
    return [[shell(pine), line(seg(17, 15, 17, 21.5))],
            _hat(_cap(S, 6.5, 8.2)),
            _person(S, 6.5, 10.5, 2.5, 15, 4.5)]
