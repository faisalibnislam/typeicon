"""TypeIcon Core: people & roles.

Busts share the proportions of the v0.1 `user` icon (head r 3.5 over shoulders 14 wide). Role icons
lower the head a little so a hat or helmet fits above it. Identifying detail stays on the head and the
left of the chest where possible: variant badges sit in the bottom-right corner.

Overlapping figures are drawn in layers (front first): back layers are cut away around the front
silhouette with a gap, in every style, so groups stay readable at 16 px.
"""
from dsl import LINE, arc, circle, detail, dot, ellipse, icon, line, poly, rect, seg, shell, solid  # noqa: F401
from dsl import D, P, ST, U, Part, filled_region
from geometry import fmt, path_to_d, polar

CAT = "people"


# --------------------------------------------------------------------------- layering

def _paint(parts, S):
    regs = []
    for p in parts:
        if p.kind in ("dot", "solid"):
            regs.append(P(p.d))
        else:
            regs.append(ST(p.d, 2.0, S.cap, S.join, float(p.attrs.get("stroke_miterlimit", 4))))
    return U(*regs)


def _sil(parts, S):
    """Solid silhouette of a layer (shell interiors included) used to hide what is behind it."""
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
    """A layer is a list of parts, or (parts, halo, filled_halo): how far it cuts away what lies behind it."""
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


def figure(name, desc, tags, aliases=(), gap=1.5, fgap=None, cat=CAT):
    """Register an icon drawn as layers: fn(S) -> [front layer, layer behind, ...]."""
    fg = gap if fgap is None else fgap

    def deco(fn):
        icon(name, cat, desc, tags=tags, aliases=aliases,
             filled=lambda: _filled_layers(fn(LINE), gap, fg))(lambda S: _stroke_layers(S, fn(S), gap, fg))
        return fn
    return deco


# --------------------------------------------------------------------------- shared shapes

def _bust(S, cx=12.0, top=14.0, hw=7.0, bottom=21.0):
    """Open-bottom shoulders (the v0.1 user body). Line has squarer shoulders than Rounded."""
    r = hw - (1.0 if S.name != "line" else 2.0)
    r = min(r, bottom - top)
    x0, x1 = cx - hw, cx + hw
    return (f"M{fmt(x0)} {fmt(bottom)}V{fmt(top + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x0 + r)} {fmt(top)}"
            f"H{fmt(x1 - r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(top + r)}V{fmt(bottom)}")


def _person(S, cx=12.0, hy=7.5, hr=3.5, top=14.0, hw=7.0, bottom=21.0):
    return [shell(circle(cx, hy, hr)), shell(_bust(S, cx, top, hw, bottom))]


# ============================================================================ groups

@figure("users", "Two people, one in front of the other", tags=["people", "group", "members", "accounts", "friends", "contacts"],
        aliases=["people"])
def _(S):
    return [_person(S, 9, 8.5, 3, 14.5, 6),
            _person(S, 16, 6.5, 2.75, 12.5, 5)]


@figure("user-group", "A group of three people", tags=["group", "people", "community", "members", "audience", "users"],
        aliases=["group"])
def _(S):
    return [_person(S, 12, 9.5, 3, 15.5, 6),
            _person(S, 6.5, 7, 2.5, 12.5, 3.5) + _person(S, 17.5, 7, 2.5, 12.5, 3.5)]


@figure("team", "Three people one behind the other", tags=["team", "colleagues", "staff", "group", "collaboration", "crew"])
def _(S):
    return [_person(S, 8, 10.5, 2.75, 16, 5),
            _person(S, 14, 7, 2.25, 12, 4),
            _person(S, 18.5, 4.5, 1.75, 8.5, 2.5)]


@figure("crowd", "Many people gathered together", tags=["crowd", "audience", "public", "population", "many people", "gathering"])
def _(S):
    return [_person(S, 12, 12.5, 2.25, 17, 4),
            _person(S, 6, 9.5, 2, 14, 3) + _person(S, 18, 9.5, 2, 14, 3),
            _person(S, 12, 5, 2, 9.5, 3)]


@figure("family", "Two adults with a child in front", tags=["family", "parents", "child", "kids", "household", "home"])
def _(S):
    return [_person(S, 12, 13, 2, 17.5, 3.5),
            _person(S, 7, 6.5, 2.5, 12, 4) + _person(S, 17, 6.5, 2.5, 12, 4)]


@figure("couple", "Two people side by side with a heart", tags=["couple", "love", "partners", "relationship", "pair", "dating"])
def _(S):
    heart = "M12 7.3L9.9 5.2A1.35 1.35 0 0 1 12 3.5A1.35 1.35 0 0 1 14.1 5.2Z"
    return [[solid(heart)],
            _person(S, 6.5, 9.5, 2.5, 14.5, 4) + _person(S, 17.5, 9.5, 2.5, 14.5, 4)]


# ============================================================================ single person

@figure("user-circle", "A person inside a circle; a profile avatar", tags=["avatar", "account", "profile", "user", "person"],
        aliases=["avatar"])
def _(S):
    sh = ("M6.34 19A6 6 0 0 1 17.66 19" if S.name != "line" else "M7 19.6V18.2A3.2 3.2 0 0 1 10.2 15H13.8A3.2 3.2 0 0 1 17 18.2V19.6")
    return [[shell(circle(12, 12, 9)), detail(circle(12, 9.25, 2.75)), detail(sh)]]


@figure("user-square", "A person inside a rounded square; an account picture", tags=["avatar", "account", "profile", "picture", "user"])
def _(S):
    return [[shell(rect(3, 3, 18, 18, S.R)), detail(circle(12, 9, 3)), detail(_bust(S, 12, 15, 5.5, 21))]]


@figure("profile", "A profile card with a portrait and a name line", tags=["profile", "bio", "about", "id", "account", "user page"])
def _(S):
    rr = 1.0 if S.name == "line" else 2.0
    sh = f"M8.5 15V{fmt(12.5 + rr)}A{rr} {rr} 0 0 1 {fmt(8.5 + rr)} 12.5H{fmt(15.5 - rr)}A{rr} {rr} 0 0 1 15.5 {fmt(12.5 + rr)}V15"
    return [[shell(rect(4.5, 3, 15, 18, min(S.R, 3))), detail(circle(12, 7.75, 2)), detail(sh), detail(seg(9, 18, 15, 18))]]


@figure("contact-card", "A contact card in front of another card", tags=["contact", "vcard", "rolodex", "address book", "card file"],
        aliases=["vcard", "rolodex"])
def _(S):
    rr = 1.0 if S.name == "line" else 1.5
    sh = f"M5.5 17V{fmt(15 + rr)}A{rr} {rr} 0 0 1 {fmt(5.5 + rr)} 15H{fmt(10.5 - rr)}A{rr} {rr} 0 0 1 10.5 {fmt(15 + rr)}V17"
    return [[shell(rect(3, 7, 15, 13, min(S.R, 3))), detail(circle(8, 11.5, 1.75)), detail(sh),
             detail(seg(12.5, 11.5, 15, 11.5)), detail(seg(12.5, 15, 15, 15))],
            [shell(rect(6, 3, 15, 13, min(S.R, 3)))]]


@figure("hand-raised", "A person raising one hand", tags=["raise hand", "question", "volunteer", "vote", "attention", "participant"],
        aliases=["raise-hand"])
def _(S):
    return [[dot(13, 5, 2.25),
             line(poly([(6.5, 2.5), (8, 9.5), (16.5, 9.5), (18, 14.5)], r=S.r)),
             line(seg(12.5, 9.5, 12.5, 14.5)),
             line(poly([(9, 21), (12.5, 14.5), (16, 21)], r=S.r))]]


# ============================================================================ full figures

@figure("person-standing", "A person standing upright", tags=["person", "stand", "human", "figure", "pedestrian", "body"],
        aliases=["standing"])
def _(S):
    return [[dot(12, 4.5, 2.25),
             line(poly([(6.5, 14.5), (8.5, 9.5), (15.5, 9.5), (17.5, 14.5)], r=S.r)),
             line(seg(12, 9.5, 12, 14.5)),
             line(poly([(8.5, 21), (12, 14.5), (15.5, 21)], r=S.r))]]


@figure("person-walking", "A person walking", tags=["walk", "pedestrian", "stroll", "steps", "hike", "on foot"],
        aliases=["walking", "pedestrian"])
def _(S):
    return [[dot(13.5, 4.5, 2.25),
             line(poly([(8.5, 13.5), (10.5, 10), (12.5, 9.5), (14.5, 12), (17, 13)], r=S.r)),
             line(seg(12.5, 9.5, 11, 15)),
             line(poly([(7.5, 21), (11, 15), (14, 17.5), (14.5, 21)], r=S.r))]]


@figure("person-running", "A person running", tags=["run", "jog", "sprint", "exercise", "fitness", "race"],
        aliases=["running", "runner"])
def _(S):
    return [[dot(15.5, 4.5, 2.25),
             line(poly([(6.5, 11.5), (9.5, 9), (13.5, 9), (16, 12), (19, 12.5)], r=S.r)),
             line(seg(13.5, 9, 11, 14.5)),
             line(poly([(4.5, 17.5), (8, 18.5), (11, 14.5), (14.5, 17), (13, 21)], r=S.r))]]


@figure("child", "A child with arms raised in play", tags=["kid", "child", "boy", "girl", "youth", "play"],
        aliases=["kid"])
def _(S):
    return [[dot(12, 6.5, 2.75),
             line(poly([(6, 7.5), (8.5, 12), (15.5, 12), (18, 7.5)], r=S.r)),
             line(seg(12, 12, 12, 16)),
             line(poly([(9, 21), (12, 16), (15, 21)], r=S.r))]]


@figure("elderly", "An older person walking with a cane", tags=["senior", "old", "elder", "aged", "grandparent", "cane"],
        aliases=["senior"])
def _(S):
    return [[dot(9.5, 5, 2.25),
             line("M12 8.5C13.8 9.8 14.3 12 13.5 15"),
             line(poly([(12.5, 9.5), (10, 12.5), (7.5, 13)], r=S.r)),
             line("M5 14.5A1.5 1.5 0 0 1 8 14.5V21"),
             line(poly([(10.5, 21), (13.5, 15), (16, 21)], r=S.r))]]


@figure("baby", "A baby's face with a curl of hair", tags=["infant", "newborn", "toddler", "child", "nursery", "baby"],
        aliases=["infant"])
def _(S):
    mouth = "M9.5 16A3 3 0 0 0 14.5 16" if S.name != "line" else poly([(9.5, 16), (10.5, 17.5), (13.5, 17.5), (14.5, 16)])
    return [[shell(circle(12, 12.5, 8.5)), detail("M13.2 7.4A1.6 1.6 0 1 1 11.8 5.2C11.5 4.7 11.8 4 12.5 3.8"),
             dot(9, 12.5, 1.2), dot(15, 12.5, 1.2), detail(mouth)]]


# ============================================================================ pictograms

@figure("man", "Pictogram of a man", tags=["male", "man", "restroom", "toilet", "gender", "gents"], aliases=["male"])
def _(S):
    return [[dot(12, 4.5, 2.5), shell(poly([(7, 9.5), (17, 9.5), (15.5, 16), (8.5, 16)], closed=True, r=S.r)),
             line(seg(10, 16, 10, 21)), line(seg(14, 16, 14, 21))]]


@figure("woman", "Pictogram of a woman", tags=["female", "woman", "restroom", "toilet", "gender", "ladies"], aliases=["female"])
def _(S):
    return [[dot(12, 4.5, 2.5), shell(poly([(9, 9.5), (15, 9.5), (17.5, 16.5), (6.5, 16.5)], closed=True, r=S.r)),
             line(seg(10, 16.5, 10, 21)), line(seg(14, 16.5, 14, 21))]]


@figure("gender-neutral", "Pictogram of a person of any gender, half trousers and half dress",
        tags=["all gender", "unisex", "non-binary", "restroom", "toilet", "inclusive"], aliases=["unisex", "all-gender"])
def _(S):
    return [[dot(12, 4.5, 2.5), shell(poly([(7, 9.5), (15.5, 9.5), (18, 16.5), (8.5, 16.5)], closed=True, r=S.r)),
             detail(seg(12, 9.5, 12, 16.5)),
             line(seg(10, 16.5, 10, 21)), line(seg(14, 16.5, 14, 21))]]


# ============================================================================ roles
# Role busts: head r 3 at y 10 so a hat fits above; shoulders 13 wide from y 16.

HY, HR, BT, BW = 10.0, 3.0, 16.0, 6.5


def _role(S, cx=12.0, hy=HY):
    return _person(S, cx, hy, HR, BT, BW)


def _u(*ds):
    """Union of closed shapes as one outline (d-string)."""
    return path_to_d(U(*[P(d) for d in ds]))


def _hat(parts):
    """A hat sits on the head: no gap in Line/Rounded, a small gap in Filled."""
    return (parts, 0.0, 1.0)


def _mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def _cross(cx, cy, arm=1.75, w=1.5):
    return _u(rect(cx - w / 2, cy - arm, w, 2 * arm), rect(cx - arm, cy - w / 2, 2 * arm, w))


@figure("student", "A person wearing a graduation cap", tags=["student", "graduate", "pupil", "learner", "school", "university"],
        aliases=["graduate"])
def _(S):
    return [_hat([shell(poly([(4, 5.8), (12, 3), (20, 5.8), (12, 8.6)], closed=True, r=S.r * 0.5)),
                  line(seg(18, 6.5, 18, 11))]),
            _role(S)]


@figure("teacher", "A teacher pointing at a small board", tags=["teacher", "tutor", "instructor", "educator", "professor", "school"],
        aliases=["tutor", "instructor"])
def _(S):
    return [[shell(rect(3, 3, 9, 6.5, min(S.R, 1.5))), line(seg(8.5, 12, 11, 15.5))],
            _person(S, 15, 10.5, 2.75, 16, 6)]


@figure("worker", "A person in a shirt and tie; an employee", tags=["employee", "staff", "office", "business", "clerk", "professional"],
        aliases=["employee", "staff"])
def _(S):
    tie = poly([(10.8, 16), (13.2, 16), (12.6, 17.6), (13.4, 20.2), (12, 21.5), (10.6, 20.2), (11.4, 17.6)], closed=True, r=S.r * 0.3)
    return [[shell(tie)], _role(S)]


@figure("chef", "A person in a chef's hat", tags=["chef", "cook", "kitchen", "restaurant", "culinary", "baker"], aliases=["cook"])
def _(S):
    toque = _u(circle(8.8, 6, 2.2), circle(12, 5.2, 2.2), circle(15.2, 6, 2.2), rect(9, 6, 6, 3))
    return [_hat([shell(toque)]), _role(S)]


@figure("doctor", "A doctor with a stethoscope around the neck", tags=["doctor", "physician", "medical", "health", "clinic", "gp"],
        aliases=["physician"])
def _(S):
    return [[line("M15 15V17.5A2.75 2.75 0 0 1 9.5 17.5V15"), shell(circle(7, 18.5, 1.5)),
             line("M9.5 17.5C9.5 18.3 9.3 18.6 8.5 18.6")],
            _role(S)]


@figure("nurse", "A nurse in a cap with a cross", tags=["nurse", "medical", "hospital", "care", "health", "clinic"])
def _(S):
    cap = poly([(6.5, 8.5), (8, 3), (16, 3), (17.5, 8.5)], closed=True, r=S.r * 0.6)
    return [_hat([shell(cap), _mark(_cross(12, 5.75, 1.6, 1.3))]), _role(S)]


@figure("police", "A police officer in a peaked cap", tags=["police", "officer", "cop", "law", "security", "sheriff"],
        aliases=["police-officer"])
def _(S):
    cap = poly([(6, 5.5), (12, 3), (18, 5.5), (16.5, 8.5), (7.5, 8.5)], closed=True, r=S.r * 0.5)
    return [_hat([shell(cap), dot(12, 5.75, 1.1)]), _role(S)]


@figure("firefighter", "A firefighter in a helmet with a front shield", tags=["firefighter", "fireman", "fire", "rescue", "emergency", "brigade"],
        aliases=["fireman"])
def _(S):
    shield = poly([(10, 3), (14, 3), (14, 6), (12, 7.5), (10, 6)], closed=True, r=S.r * 0.3)
    helmet = "M3.5 9.5L7 8.5A5 5 0 0 1 17 8.5L20.5 9.5Z"
    return [[shell(shield)], _hat([shell(helmet, stroke_miterlimit="2")]), _role(S)]


@figure("astronaut", "An astronaut in a space helmet", tags=["astronaut", "space", "cosmonaut", "spaceman", "nasa", "helmet"],
        aliases=["cosmonaut", "spaceman"])
def _(S):
    return [[shell(circle(12, 9, 6)), detail(rect(8, 6.5, 8, 5, min(S.R, 2.5)))],
            _person(S, 12, 9, 3, 17, 7.5)[1:]]


@figure("detective", "A detective in a hat with a magnifying glass", tags=["detective", "investigator", "spy", "sleuth", "private eye", "agent"],
        aliases=["investigator", "sleuth"])
def _(S):
    hat = poly([(5, 9), (19, 9), (16.5, 7.5), (15.5, 3.5), (12, 4.5), (8.5, 3.5), (7.5, 7.5)], closed=True, r=S.r * 0.5)
    return [[shell(circle(8, 16, 2.5)), line(seg(6.2, 17.8, 3.5, 20.5))],
            _hat([shell(hat)]),
            _role(S, 13)]


@figure("judge", "A judge in a curled wig", tags=["judge", "court", "law", "justice", "legal", "magistrate"],
        aliases=["magistrate"])
def _(S):
    wig = _u(circle(12, 8.5, 5), circle(7, 10, 2), circle(7, 13.5, 2), circle(17, 10, 2), circle(17, 13.5, 2))
    return [[shell(circle(12, 10.5, 3))], [shell(wig)], _person(S, 12, 10.5, 3, 16.5, 6.5)[1:]]


@figure("pilot", "A pilot in a peaked cap with wings", tags=["pilot", "aviator", "captain", "flight", "airline", "plane"],
        aliases=["aviator"])
def _(S):
    cap = poly([(5.5, 4.5), (18.5, 4.5), (16.5, 8.5), (7.5, 8.5)], closed=True, r=S.r * 0.5)
    return [_hat([shell(cap), detail(poly([(9, 6.5), (12, 7.3), (15, 6.5)], r=S.r * 0.3))]), _role(S)]


@figure("farmer", "A farmer in a wide straw hat", tags=["farmer", "agriculture", "farm", "rancher", "grower", "rural"])
def _(S):
    hat = _u(rect(8, 3.5, 8, 6, 2.5), ellipse(12, 8.5, 8.5, 1.25))
    return [_hat([shell(hat)]), _role(S)]


@figure("builder", "A builder in a hard hat", tags=["builder", "construction", "worker", "engineer", "contractor", "hard hat"],
        aliases=["construction-worker"])
def _(S):
    hat = "M5.5 9H7A5 5 0 0 1 17 9H18.5V10.5H5.5Z" if S.name == "line" else "M6 9H7A5 5 0 0 1 17 9H18A0.75 0.75 0 0 1 18 10.5H6A0.75 0.75 0 0 1 6 9Z"
    return [_hat([shell(hat), detail(seg(12, 4, 12, 9))]), _role(S)]


@figure("scientist", "A scientist holding a laboratory flask", tags=["scientist", "researcher", "lab", "chemist", "science", "experiment"],
        aliases=["researcher"])
def _(S):
    flask = poly([(6, 12.5), (9, 12.5), (9, 15), (11.5, 20.5), (3.5, 20.5), (6, 15)], closed=True, r=S.r * 0.4)
    return [[shell(flask), detail(seg(4.7, 18, 10.3, 18))], _role(S, 13.5)]


@figure("artist", "An artist in a beret holding a paintbrush", tags=["artist", "painter", "art", "creative", "painting", "beret"],
        aliases=["painter"])
def _(S):
    beret = "M6 9C5.5 6.5 8 4.8 12 4.8C15.8 4.8 18.2 6.2 17.8 8Z"
    tip = "M5 3C6.4 4.6 6.8 6.6 6.5 8.5H3.5C3.2 6.6 3.6 4.6 5 3Z"
    return [[solid(tip), line(seg(5, 10.5, 5, 17))],
            _hat([shell(beret)]),
            _role(S, 13.5)]


@figure("musician", "A person beside a music note", tags=["musician", "singer", "music", "band", "artist", "performer"],
        aliases=["singer"])
def _(S):
    return [[dot(4.75, 8.5, 1.75), line(seg(6, 8.5, 6, 3)), line(poly([(6, 3), (8, 4.5)], r=0))],
            _role(S, 14)]


@figure("photographer", "A person holding a camera up to their face", tags=["photographer", "camera", "photo", "journalist", "press", "shoot"])
def _(S):
    cam = _u(rect(4.5, 8.5, 15, 7, min(S.R, 2.5)), rect(6.5, 6.5, 4, 3, 0.5))
    return [[shell(cam), detail(circle(13, 12, 2))],
            _person(S, 12, 8.5, 3, 16.5, 6.5)]


@figure("mechanic", "A mechanic holding a spanner", tags=["mechanic", "repair", "technician", "garage", "fix", "maintenance"],
        aliases=["technician", "repairman"])
def _(S):
    return [[line(arc(8.5, 14, 2.5, 5, 245)), line(seg(6.7, 15.8, 3.5, 19.5))],
            _role(S, 13.5)]


@figure("waiter", "A waiter in a bow tie carrying a covered dish", tags=["waiter", "server", "restaurant", "service", "butler", "hospitality"],
        aliases=["waitress"])
def _(S):
    bow = poly([(12.8, 16.6), (14.6, 17.4), (15.4, 17.4), (17.2, 16.6), (17.2, 19.4), (15.4, 18.6), (14.6, 18.6), (12.8, 19.4)], closed=True)
    return [[shell("M3 10A3 3 0 0 1 9 10Z"), dot(6, 5.2, 1), line(seg(2.5, 12, 9.5, 12)), solid(bow)],
            _role(S, 15)]


@figure("cashier", "A cashier behind a cash register", tags=["cashier", "checkout", "till", "shop", "retail", "store clerk"],
        aliases=["checkout-clerk"])
def _(S):
    reg = _u(rect(3, 15, 10.5, 6, min(S.R, 1.5)), rect(4.5, 11, 5, 5, 0.5))
    return [[shell(reg), detail(seg(3, 18, 13.5, 18))],
            _role(S, 14.5)]


@figure("programmer", "A person working at a laptop", tags=["programmer", "developer", "coder", "engineer", "software", "hacker"],
        aliases=["developer", "coder"])
def _(S):
    return [[shell(rect(5, 12.5, 14, 8, min(S.R, 1.5))), line(seg(3, 20.5, 21, 20.5)),
             detail(poly([(10.5, 14.5), (9, 16.25), (10.5, 18)], r=S.r * 0.3)), detail(poly([(13.5, 14.5), (15, 16.25), (13.5, 18)], r=S.r * 0.3))],
            _person(S, 12, 7.5, 3, 13.5, 7.5)]


@figure("designer", "A person beside a pen nib", tags=["designer", "graphic design", "creative", "illustrator", "ux", "vector"],
        aliases=["graphic-designer"])
def _(S):
    nib = poly([(3.5, 4.5), (8.5, 4.5), (8.5, 7), (6, 11), (3.5, 7)], closed=True, r=S.r * 0.3)
    return [[shell(nib), detail(seg(6, 7.5, 6, 11))], _role(S, 14.5)]


@figure("lifeguard", "A lifeguard holding a life ring", tags=["lifeguard", "rescue", "beach", "pool", "swimming", "safety"])
def _(S):
    bands = [solid(poly([polar(7.5, 16.5, rr, a + da) for rr, da in ((1.6, -14), (5.3, -9), (5.3, 9), (1.6, 14))], closed=True))
             for a in (-45, 45, 135, 225)]
    return [[line(circle(7.5, 16.5, 3.5))] + bands, _role(S, 14)]


@figure("soldier", "A soldier in a combat helmet", tags=["soldier", "army", "military", "troops", "veteran", "defence"],
        aliases=["military"])
def _(S):
    helmet = "M5 10.5H19L17.5 8.5A5.5 5.5 0 0 0 6.5 8.5Z"
    star = poly([polar(12, 6.6, 1.9 if k % 2 == 0 else 0.8, -90 + k * 36) for k in range(10)], closed=True)
    return [_hat([shell(helmet), _mark(star)]), _role(S)]


def _crown(x0, x1, y0, ytop, ymid):
    m = (x0 + x1) / 2
    return poly([(x0, y0), (x0 - 0.5, ytop), (x0 + (m - x0) / 2, ymid), (m, ytop - 0.5), (x1 - (x1 - m) / 2, ymid), (x1 + 0.5, ytop), (x1, y0)], closed=True)


def _long_hair(S):
    return [shell("M6.5 17V10A5.5 5.5 0 0 1 17.5 10V17Z" if S.name == "line" else "M8 17A1.5 1.5 0 0 1 6.5 15.5V10A5.5 5.5 0 0 1 17.5 10V15.5A1.5 1.5 0 0 1 16 17Z")]


@figure("king", "A bearded king wearing a crown", tags=["king", "monarch", "royal", "ruler", "royalty", "chess"],
        aliases=["monarch"])
def _(S):
    beard = "M8.8 11C9 14 10.4 15.5 12 15.5C13.6 15.5 15 14 15.2 11Z"
    return [_hat([shell(_crown(7.5, 16.5, 8, 3.5, 6), stroke_miterlimit="2")]),
            ([shell(beard)], 0.0, 1.0),
            _role(S)]


@figure("queen", "A queen with long hair wearing a crown", tags=["queen", "monarch", "royal", "ruler", "royalty", "chess"])
def _(S):
    return [_hat([shell(_crown(8.5, 15.5, 8, 3.5, 6), stroke_miterlimit="2")]), _role(S), (_long_hair(S), 1.5, 1.5)]


@figure("prince", "A young prince wearing a small crown", tags=["prince", "royal", "royalty", "heir", "fairy tale", "crown"])
def _(S):
    return [_hat([shell(_crown(9, 15, 8, 5, 6.5), stroke_miterlimit="2")]), _role(S)]


@figure("princess", "A princess with long hair wearing a tiara", tags=["princess", "royal", "royalty", "fairy tale", "tiara", "crown"])
def _(S):
    return [_hat([shell(_crown(9.5, 14.5, 8, 5.5, 7), stroke_miterlimit="2")]), _role(S), (_long_hair(S), 1.5, 1.5)]


@figure("wizard", "A wizard with a pointed hat and long beard", tags=["wizard", "magic", "sorcerer", "mage", "fantasy", "witch"],
        aliases=["sorcerer", "mage"])
def _(S):
    hat = poly([(4.5, 9), (19.5, 9), (15.5, 7.5), (13.5, 3), (10.5, 3.5), (8.5, 7.5)], closed=True, r=S.r * 0.4)
    beard = "M9 11C9.5 15.5 11 19.5 12 21C13 19.5 14.5 15.5 15 11Z"
    return [_hat([shell(hat)]), [shell(beard)], _role(S)]


@figure("ninja", "A ninja with a masked face and headband ties", tags=["ninja", "martial arts", "stealth", "assassin", "warrior", "shinobi"])
def _(S):
    return [[shell(circle(11.5, 9.5, 4.5)), detail(rect(8, 8.25, 7, 2.5, min(S.R, 1.25))),
             line(seg(16, 8, 20, 6)), line(seg(16, 9.5, 20.5, 10.5))],
            _person(S, 11.5, 9.5, 4.5, 16.5, 6.5)[1:]]


@figure("pirate", "A pirate in a hat and eye patch", tags=["pirate", "buccaneer", "captain", "sea", "treasure", "corsair"],
        aliases=["buccaneer"])
def _(S):
    hat = "M4 8.5C6 8.5 7 4 12 4C17 4 18 8.5 20 8.5Z"
    return [_hat([shell(hat)]), [dot(10.5, 11, 1.4), line(seg(10.5, 11, 15.2, 8.7))], _role(S)]


@figure("superhero", "A superhero with a cape and a star on the chest", tags=["superhero", "hero", "cape", "comic", "super", "power"],
        aliases=["hero"])
def _(S):
    star = poly([polar(12, 18.6, 2 if k % 2 == 0 else 0.85, -90 + k * 36) for k in range(10)], closed=True)
    cape = poly([(8, 15), (16, 15), (21, 21), (3, 21)], closed=True, r=S.r * 0.5)
    return [[_mark(star)] + _person(S, 12, 10, 3, 16, 4.5), [shell(cape)]]


@figure("bride", "A bride wearing a long veil", tags=["bride", "wedding", "marriage", "veil", "bridal", "ceremony"])
def _(S):
    veil = "M12 4.5C8.5 4.5 7 7 6.5 10L3.5 20H20.5L17.5 10C17 7 15.5 4.5 12 4.5Z"
    return [_person(S, 12, 10, 3, 16, 5) + [dot(12, 5.3, 1.3)], [shell(veil)]]


@figure("groom", "A groom in a top hat and bow tie", tags=["groom", "wedding", "marriage", "bridegroom", "tuxedo", "ceremony"],
        aliases=["bridegroom"])
def _(S):
    hat = _u(rect(8.5, 3, 7, 5), rect(6, 7, 12, 1.75, 0.5))
    bow = poly([(9.8, 16.6), (11.6, 17.4), (12.4, 17.4), (14.2, 16.6), (14.2, 19.4), (12.4, 18.6), (11.6, 18.6), (9.8, 19.4)], closed=True)
    return [_hat([shell(hat)]), [shell(bow)], _role(S)]


# ============================================================================ handshake

def _cap(x0, y0, x1, y1, w=3.2):
    return ST(seg(x0, y0, x1, y1), w, "round", "round")


def _box(x, y, w, h, r=0.0):
    return P(rect(x, y, w, h, r))


def handshake_layers(S):
    """Two hands clasped: the right hand's thumb over the left hand's fingers. Also used by gestures/hand-shake-deal."""
    k = 0.5 if S.name == "line" else 1.5
    thumb = [shell(path_to_d(_cap(18, 9.8, 11, 7, 3)))]
    left = U(_box(2.5, 9.5, 7, 7.5, k), _box(7, 8.5, 10.5, 9.5, 3))
    front = [shell(path_to_d(left)), detail(seg(5.5, 9.5, 5.5, 17)),
             detail(seg(10.3, 18, 11.1, 14.3)), detail(seg(13.1, 18, 13.9, 14.3)), detail(seg(15.8, 18, 16.3, 15))]
    back = [shell(path_to_d(_box(14, 10, 7.5, 7.5, k))), detail(seg(18.5, 10, 18.5, 17.5))]
    return [thumb, front, back]


@figure("handshake", "Two hands shaking; agreement or greeting", tags=["handshake", "agreement", "deal", "partnership", "greeting", "trust"],
        aliases=["shake-hands"], gap=1.0)
def _(S):
    return handshake_layers(S)
