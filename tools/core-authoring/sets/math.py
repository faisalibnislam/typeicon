"""TypeIcon Core: math."""
from dsl import D, P, ST, U, arc, circle, pt_on, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401


@icon("pi", "math", "Greek letter pi; the constant 3.14159…", tags=["math", "constant", "circle", "greek"])
def _(S):
    return [
        line(poly([(4, 8.5), (5.5, 6.5), (20, 6.5)], r=S.r)),
        line("M9 6.5V13C9 16.5 8 18.5 5.5 19.5"),
        line("M15.5 6.5V16.5C15.5 18.5 16.5 19.5 18.5 19.5C19.5 19.5 20 19.2 20.5 18.5"),
    ]


@icon("sigma", "math", "Greek capital sigma; summation", tags=["sum", "summation", "math", "greek"])
def _(S):
    return [line(poly([(18, 7), (18, 4.5), (6, 4.5), (12.5, 12), (6, 19.5), (18, 19.5), (18, 17)], r=S.r), stroke_miterlimit="2")]


@icon("infinity", "math", "Infinity sign; endless or unlimited", tags=["endless", "unlimited", "loop", "math"])
def _(S):
    if S.name == "line":
        # Crisp: straight crossing strokes meeting the loops at corners.
        return [line("M9.5 14.5L14.5 9.5C15.5 8.5 16.5 8 17.5 8A4 4 0 0 1 17.5 16C16.5 16 15.5 15.5 14.5 14.5L9.5 9.5C8.5 8.5 7.5 8 6.5 8A4 4 0 0 0 6.5 16C7.5 16 8.5 15.5 9.5 14.5Z")]
    return [line("M12 12C10 9.5 8.5 8 6.5 8A4 4 0 0 0 6.5 16C8.5 16 10 14.5 12 12C14 9.5 15.5 8 17.5 8A4 4 0 0 1 17.5 16C15.5 16 14 14.5 12 12")]


@icon("square-root", "math", "Square-root (radical) sign", tags=["radical", "root", "math"])
def _(S):
    return [line(poly([(3, 13), (5.5, 12), (9, 20), (13, 4.5), (21, 4.5)], r=S.r))]


@icon("percentage", "math", "Percent sign", tags=["percent", "discount", "rate", "math"])
def _(S):
    return [line(seg(18.5, 5.5, 5.5, 18.5)), shell(circle(7.5, 7.5, 2.5)), shell(circle(16.5, 16.5, 2.5))]


# --------------------------------------------------------------------------- operators and relations

@icon("integral", "math", "Integral sign; calculus integration", tags=["calculus", "integrate", "area", "math"])
def _(S):
    if S.name == "line":
        return [line("M17.5 4.5H15C13.2 4.5 12 5.7 12 7.5V16.5C12 18.3 10.8 19.5 9 19.5H6.5")]
    return [line("M17.5 5.5C17.5 4.3 16.5 3.5 15 3.5C13 3.5 12 4.8 12 7V17C12 19.2 11 20.5 9 20.5C7.5 20.5 6.5 19.7 6.5 18.5")]


@icon("plus-minus", "math", "Plus-minus sign; tolerance or both signs", tags=["tolerance", "plus", "minus", "approx", "math"])
def _(S):
    return [line(seg(12, 3.5, 12, 15.5)), line(seg(6, 9.5, 18, 9.5)), line(seg(6, 19.5, 18, 19.5))]


@icon("divide", "math", "Division sign (obelus)", tags=["division", "divided", "obelus", "operator", "math"])
def _(S):
    return [line(seg(5, 12, 19, 12)), dot(12, 6.5, 1.75), dot(12, 17.5, 1.75)]


@icon("multiply", "math", "Multiplication sign", tags=["times", "product", "operator", "math"])
def _(S):
    return [line(seg(7, 7, 17, 17)), line(seg(17, 7, 7, 17))]


@icon("equals", "math", "Equals sign", tags=["equal", "same", "result", "operator", "math"])
def _(S):
    return [line(seg(5, 9, 19, 9)), line(seg(5, 15, 19, 15))]


@icon("not-equal", "math", "Not-equal sign", tags=["unequal", "different", "inequality", "math"])
def _(S):
    return [line(seg(5, 9, 19, 9)), line(seg(5, 15, 19, 15)), line(seg(16, 4, 8, 20))]


@icon("approximately", "math", "Approximately-equal sign (double tilde)", tags=["approx", "about", "roughly", "estimate", "math"])
def _(S):
    def tilde(y):
        return f"M5 {y + 1}C6.3 {y - 1} 8.5 {y - 1.8} 10.8 {y - 0.3}C13.2 {y + 1.3} 15.6 {y + 1.8} 19 {y - 1}"
    return [line(tilde(8.5)), line(tilde(15.5))]


@icon("less-than", "math", "Less-than sign", tags=["less", "smaller", "inequality", "compare", "math"])
def _(S):
    return [line(poly([(18, 5.5), (6, 12), (18, 18.5)], r=S.r))]


@icon("greater-than", "math", "Greater-than sign", tags=["greater", "larger", "more", "inequality", "compare", "math"])
def _(S):
    return [line(poly([(6, 5.5), (18, 12), (6, 18.5)], r=S.r))]


@icon("less-equal", "math", "Less-than-or-equal sign", tags=["less", "equal", "inequality", "compare", "math"])
def _(S):
    return [line(poly([(18, 3.5), (6, 9), (18, 14.5)], r=S.r)), line(seg(6, 19.5, 18, 19.5))]


@icon("greater-equal", "math", "Greater-than-or-equal sign", tags=["greater", "equal", "inequality", "compare", "math"])
def _(S):
    return [line(poly([(6, 3.5), (18, 9), (6, 14.5)], r=S.r)), line(seg(6, 19.5, 18, 19.5))]


@icon("per-mille", "math", "Per-mille sign; parts per thousand", tags=["permille", "thousand", "promille", "rate", "math"])
def _(S):
    return [line(seg(13, 3.5, 4.5, 20.5)),
            shell(ellipse(5.5, 7, 1.75, 2.75)), shell(ellipse(12.5, 17, 1.75, 2.75)), shell(ellipse(19.25, 17, 1.75, 2.75))]


@icon("degree", "math", "Degree sign beside an angle; degrees of arc or temperature", tags=["degrees", "angle", "temperature", "unit", "math"])
def _(S):
    return [line(poly([(12.5, 6.5), (4, 19.5), (20.5, 19.5)], r=S.r)), shell(circle(18, 7, 3))]


@icon("function-fx", "math", "Function symbol fx", tags=["function", "formula", "fx", "spreadsheet", "math"])
def _(S):
    return [line("M12 4.4C11.4 3.8 10.7 3.5 10 3.5C8.5 3.5 7.5 4.5 7.5 6.5V20.5"),
            line(seg(4.5, 9.5, 11, 9.5)),
            line(seg(13.5, 10, 20, 19.5)), line(seg(20, 10, 13.5, 19.5))]


# --------------------------------------------------------------------------- Greek letters

@icon("theta", "math", "Greek small letter theta", tags=["greek", "angle", "letter", "math"])
def _(S):
    if S.name == "line":
        ring = "M6.5 9A5.5 5.5 0 0 1 17.5 9V15A5.5 5.5 0 0 1 6.5 15Z"
    else:
        ring = ellipse(12, 12, 5.5, 8)
    return [line(ring), line(seg(6.5, 12, 17.5, 12))]


@icon("alpha", "math", "Greek small letter alpha", tags=["greek", "letter", "first", "math"])
def _(S):
    return [line("M18.5 6.5C17 12 15 17.5 10.5 17.5C7.5 17.5 5 15.2 5 12C5 8.8 7.5 6.5 10.5 6.5C14.5 6.5 16.5 11 17.5 15C18 17 18.8 17.5 20 17.5")]


@icon("beta", "math", "Greek small letter beta", tags=["greek", "letter", "second", "math"])
def _(S):
    return [line("M7 21V8C7 5.3 9 3.5 11.5 3.5C13.8 3.5 15.5 5 15.5 7.3C15.5 9.5 13.8 11 11.5 11H10"),
            line("M11.5 11C15 11 17.5 12.8 17.5 15.7C17.5 18.5 15.3 20 12.5 20C10 20 8 19 7 17.5")]


@icon("gamma", "math", "Greek small letter gamma", tags=["greek", "letter", "photon", "math"])
def _(S):
    return [line("M4.5 7.5C5.5 6.7 7.2 6.6 8.3 8L12.6 14.6C13.8 16.5 14 18.5 13 20C12.3 21 11 21 10.5 20C10 19 10.5 17 11.8 15L19.5 6.5")]


@icon("delta", "math", "Greek capital letter delta; change or difference", tags=["greek", "change", "difference", "triangle", "math"])
def _(S):
    return [line(poly([(12, 4.5), (4, 19.5), (20, 19.5)], closed=True, r=S.r))]


@icon("lambda", "math", "Greek small letter lambda", tags=["greek", "function", "wavelength", "letter", "math"])
def _(S):
    return [line(poly([(5.5, 3.5), (8, 3.5), (17.5, 20.5), (20, 20.5)], r=S.r)), line(seg(12.2, 11, 5, 20.5))]


@icon("mu", "math", "Greek small letter mu; micro", tags=["greek", "micro", "mean", "letter", "math"])
def _(S):
    return [line(seg(6.5, 6.5, 6.5, 21)),
            line("M6.5 13.5C6.5 16 8 17.5 10.5 17.5C13 17.5 15 16 15 13.5"),
            line("M15 6.5V15C15 16.8 16 17.5 17.5 17.5H18.5" if S.name == "line" else "M15 6.5V15C15 16.8 16 17.5 17.5 17.5C18 17.5 18.5 17.3 18.8 17")]


@icon("omega", "math", "Greek capital letter omega; ohm", tags=["greek", "ohm", "resistance", "last", "math"])
def _(S):
    return [line("M4 19.5H9V17.3C6.6 15.8 5 13.3 5 10.7C5 6.7 8.1 3.7 12 3.7C15.9 3.7 19 6.7 19 10.7C19 13.3 17.4 15.8 15 17.3V19.5H20",
                 **({} if S.name == "line" else {}))]


@icon("phi", "math", "Greek small letter phi; golden ratio", tags=["greek", "golden", "ratio", "angle", "math"])
def _(S):
    ring = ellipse(12, 12, 7, 5.5) if S.name == "rounded" else "M9 6.5H15A5.5 5.5 0 0 1 15 17.5H9A5.5 5.5 0 0 1 9 6.5Z"
    return [line(ring), line(seg(12, 3, 12, 21))]


@icon("epsilon", "math", "Greek small letter epsilon", tags=["greek", "small", "error", "letter", "math"])
def _(S):
    return [line("M17.5 8C16.3 7 14.8 6.5 13 6.5C9.8 6.5 7.5 7.8 7.5 9.5C7.5 11.2 9.5 12 12.5 12H14"),
            line("M12.5 12C9.3 12 7 13.2 7 15C7 16.8 9.5 17.8 13 17.8C15 17.8 16.8 17.2 18 16.3")]


@icon("factorial", "math", "Factorial: n followed by an exclamation mark", tags=["factorial", "product", "combinatorics", "math"])
def _(S):
    return [line(seg(5, 8.5, 5, 19.5)),
            line("M5 12C5 9.8 6.5 8.5 8.5 8.5C10.5 8.5 12 9.8 12 12V19.5"),
            line(seg(18, 4, 18, 14.5)), dot(18, 19, 1.5)]


@icon("parentheses", "math", "Pair of round brackets", tags=["brackets", "parens", "group", "math", "code"], aliases=["parens"])
def _(S):
    return [line("M9 3.5C6.5 6 5 9 5 12C5 15 6.5 18 9 20.5"), line("M15 3.5C17.5 6 19 9 19 12C19 15 17.5 18 15 20.5")]


@icon("brackets-square", "math", "Pair of square brackets", tags=["brackets", "array", "group", "math", "code"])
def _(S):
    return [line(poly([(9, 3.5), (5, 3.5), (5, 20.5), (9, 20.5)], r=S.r)), line(poly([(15, 3.5), (19, 3.5), (19, 20.5), (15, 20.5)], r=S.r))]


@icon("fraction", "math", "Fraction one over two", tags=["fraction", "half", "ratio", "numerator", "denominator", "math"])
def _(S):
    return [line(poly([(10.5, 5), (12.5, 3.5), (12.5, 9)], r=S.r * 0.5)),
            line(seg(5, 12, 19, 12)),
            line("M9.5 16.5C9.5 15.3 10.6 14.5 12 14.5C13.4 14.5 14.5 15.3 14.5 16.5C14.5 18 12.5 18.8 9.5 20.5H14.5", stroke_miterlimit="2")]


@icon("exponent", "math", "Base x raised to the power two", tags=["power", "superscript", "squared", "exponent", "math"])
def _(S):
    return [line(seg(4, 9.5, 12.5, 20)), line(seg(12.5, 9.5, 4, 20)),
            line("M15 5.5C15 4.3 16 3.5 17.5 3.5C19 3.5 20 4.3 20 5.5C20 7 18.2 7.8 15 10H20", stroke_miterlimit="2")]


@icon("logarithm", "math", "Logarithm abbreviation log", tags=["log", "ln", "logarithmic", "function", "math"])
def _(S):
    g = ("M19.5 11V19.5C19.5 20.6 18.6 21.5 17.5 21.5H15.5" if S.name == "line" else "M19.5 11V19C19.5 20.4 18.6 21.5 17.3 21.5C16.7 21.5 16.2 21.3 15.8 21")
    return [line(seg(3, 4, 3, 17.5)),
            line(ellipse(9.25, 14.25, 2.25, 3.25)),
            line(ellipse(17.25, 14.25, 2.25, 3.25)), line(g)]


# --------------------------------------------------------------------------- geometry

@icon("angle", "math", "Angle between two rays with an arc", tags=["angle", "geometry", "degrees", "corner", "math"])
def _(S):
    return [line(poly([(18.5, 5), (4, 19.5), (20.5, 19.5)], r=S.r)), line(arc(4, 19.5, 8, -45, 0))]


@icon("triangle-math", "math", "Right triangle with a right-angle mark", tags=["triangle", "geometry", "pythagoras", "shape", "math"])
def _(S):
    return [shell(poly([(4, 3.5), (4, 20.5), (20.5, 20.5)], closed=True, r=S.r)), detail(poly([(4, 15), (9.5, 15), (9.5, 20.5)], r=S.r * 0.5))]


@icon("circle-math", "math", "Circle with its centre and radius marked", tags=["circle", "radius", "geometry", "shape", "math"],
      filled=lambda: D(P(circle(12, 12, 10)), ST(seg(12, 12, 21, 12), 2), P(circle(12, 12, 2))))
def _(S):
    # Line marks the centre with a square point (crisp), Rounded with a round one.
    centre = dot(12, 12, 1.75) if S.name == "rounded" else solid(rect(10.5, 10.5, 3, 3))
    return [shell(circle(12, 12, 9)), detail(seg(12, 12, 21, 12)), centre]


@icon("product-symbol", "math", "Capital pi product operator", tags=["product", "multiply", "series", "pi", "math"])
def _(S):
    return [line(seg(4, 4, 20, 4)), line(poly([(7, 4), (7, 20)], r=S.r)), line(seg(17, 4, 17, 20)),
            line(seg(4.5, 20, 9.5, 20)), line(seg(14.5, 20, 19.5, 20))]


@icon("empty-set", "math", "Empty-set symbol: circle with a slash", tags=["empty", "null", "set", "none", "math"])
def _(S):
    return [line(circle(12, 12, 6.5)), line(seg(17.5, 3.5, 6.5, 20.5))]


# --------------------------------------------------------------------------- sets and logic

@icon("union", "math", "Set union symbol", tags=["union", "set", "cup", "or", "math"])
def _(S):
    return [line("M5.5 4.5V12A6.5 6.5 0 0 0 18.5 12V4.5")]


@icon("intersection", "math", "Set intersection symbol", tags=["intersection", "set", "cap", "and", "math"])
def _(S):
    return [line("M5.5 19.5V12A6.5 6.5 0 0 1 18.5 12V19.5")]


@icon("subset", "math", "Subset symbol", tags=["subset", "set", "contained", "math"])
def _(S):
    return [line("M19 5H12A7 7 0 0 0 12 19H19")]


@icon("element-of", "math", "Element-of (set membership) symbol", tags=["element", "member", "in", "set", "belongs", "math"])
def _(S):
    return [line("M18 5.5H12A6.5 6.5 0 0 0 12 18.5H18"), line(seg(5.5, 12, 17, 12))]


@icon("for-all", "math", "Universal quantifier (turned A)", tags=["forall", "every", "universal", "logic", "math"])
def _(S):
    return [line(poly([(4.5, 4), (12, 20), (19.5, 4)], r=S.r)), line(seg(7.9, 11.5, 16.1, 11.5))]


@icon("exists", "math", "Existential quantifier (turned E)", tags=["exists", "there-is", "existential", "logic", "math"])
def _(S):
    return [line(poly([(5.5, 4), (18.5, 4), (18.5, 20), (5.5, 20)], r=S.r)), line(seg(7, 12, 18.5, 12))]


def _three_points(S, pts, filled=False):
    """Three points: square in Line (crisp, like butt caps), round in Rounded, heavier squares in Filled."""
    if filled:
        return U(*[P(rect(x - 2.1, y - 2.1, 4.2, 4.2)) for x, y in pts])
    if S.name == "line":
        return [solid(rect(x - 1.75, y - 1.75, 3.5, 3.5)) for x, y in pts]
    return [dot(x, y, 2) for x, y in pts]


_THEREFORE = [(12, 6.5), (5.5, 17.5), (18.5, 17.5)]
_BECAUSE = [(5.5, 6.5), (18.5, 6.5), (12, 17.5)]


@icon("therefore", "math", "Therefore sign: three dots in a triangle", tags=["therefore", "hence", "thus", "logic", "proof", "math"],
      filled=lambda: _three_points(None, _THEREFORE, True))
def _(S):
    return _three_points(S, _THEREFORE)


@icon("because", "math", "Because sign: three dots in an inverted triangle", tags=["because", "since", "reason", "logic", "proof", "math"],
      filled=lambda: _three_points(None, _BECAUSE, True))
def _(S):
    return _three_points(S, _BECAUSE)


# --------------------------------------------------------------------------- typographic symbols

@icon("number-sign", "math", "Number sign (hash)", tags=["hash", "pound", "number", "hashtag", "octothorpe"])
def _(S):
    return [line(seg(10, 4, 8, 20)), line(seg(16, 4, 14, 20)), line(seg(4.5, 9, 19.5, 9)), line(seg(4.5, 15, 19.5, 15))]


@icon("ampersand", "math", "Ampersand (and sign)", tags=["and", "ampersand", "symbol", "typography"])
def _(S):
    return [line("M19.5 20.5L9.8 10.2C8.4 8.7 7.8 7.7 7.8 6.5C7.8 4.8 9.1 3.5 10.8 3.5C12.5 3.5 13.8 4.8 13.8 6.5C13.8 8.4 12 9.7 9.5 11.2C6.6 13 5 14.6 5 16.8C5 19 6.9 20.5 9.3 20.5C12.4 20.5 15 18.6 17.5 14", stroke_miterlimit="2")]


@icon("asterisk", "math", "Asterisk", tags=["star", "footnote", "wildcard", "required", "multiply"])
def _(S):
    return [line(seg(12, 4, 12, 20)), line(seg(5.07, 8, 18.93, 16)), line(seg(18.93, 8, 5.07, 16))]


@icon("section-sign", "math", "Section sign", tags=["section", "legal", "paragraph", "law", "typography"])
def _(S):
    return [line("M16 5.5C15.2 4.2 13.8 3.5 12 3.5C9.8 3.5 8 4.8 8 6.5C8 10 16 10 16 14C16 15.6 14.8 16.6 13.3 17"),
            line("M8 18.5C8.8 19.8 10.2 20.5 12 20.5C14.2 20.5 16 19.2 16 17.5C16 14 8 14 8 10C8 8.4 9.2 7.4 10.7 7")]


@icon("paragraph-mark", "math", "Pilcrow (paragraph mark)", tags=["pilcrow", "paragraph", "formatting", "text", "typography"])
def _(S):
    return [shell("M12.5 3.5H10.5C7.7 3.5 5.5 5.5 5.5 8.25C5.5 11 7.7 13 10.5 13H12.5Z"),
            line(poly([(12.5, 20.5), (12.5, 3.5), (19, 3.5)], r=S.r)), line(seg(17, 3.5, 17, 20.5))]


@icon("copyright", "math", "Copyright symbol", tags=["copyright", "legal", "rights", "license", "c"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(arc(12, 12, 4.25, 45, 315))]


@icon("registered", "math", "Registered trademark symbol", tags=["registered", "trademark", "legal", "brand", "r"])
def _(S):
    return [shell(circle(12, 12, 9)),
            detail(poly([(9.5, 17), (9.5, 7), (12.5, 7)], r=S.r * 0.5)),
            detail("M12.5 7C14 7 15 8 15 9.5C15 11 14 12 12.5 12H9.5"), detail(seg(12.5, 12, 15, 17))]


@icon("trademark-symbol", "math", "Trademark symbol (TM)", tags=["trademark", "tm", "brand", "legal"])
def _(S):
    return [line(seg(2.5, 7, 10, 7)), line(seg(6.25, 7, 6.25, 17.5)),
            line(poly([(12.5, 17.5), (12.5, 7), (16.5, 13), (20.5, 7), (20.5, 17.5)], r=S.r * 0.5), stroke_miterlimit="2")]


# --------------------------------------------------------------------------- linear algebra and graphs

@icon("vector-arrow", "math", "Vector: letter v with an arrow above", tags=["vector", "arrow", "direction", "physics", "math"])
def _(S):
    return [line(seg(5, 5.5, 18.5, 5.5)), line(poly([(16, 3), (18.5, 5.5), (16, 8)], r=S.r)),
            line(poly([(6.5, 11.5), (12, 20.5), (17.5, 11.5)], r=S.r))]


@icon("matrix", "math", "Matrix: square brackets around a grid of entries", tags=["matrix", "array", "grid", "linear", "algebra", "math"])
def _(S):
    return [line(poly([(7, 3.5), (3.5, 3.5), (3.5, 20.5), (7, 20.5)], r=S.r)),
            line(poly([(17, 3.5), (20.5, 3.5), (20.5, 20.5), (17, 20.5)], r=S.r)),
            dot(9.5, 9, 1.5), dot(14.5, 9, 1.5), dot(9.5, 15, 1.5), dot(14.5, 15, 1.5)]


@icon("radian", "math", "Radian: circle sector with its angle marked", tags=["radian", "angle", "arc", "sector", "math"])
def _(S):
    return [line(circle(12, 12, 9)), line(poly([(21, 12), (12, 12), pt_on(12, 12, 9, -57.3)], r=S.r)),
            line(arc(12, 12, 5, -57.3, 0))]


@icon("axis", "math", "Pair of coordinate axes with arrowheads", tags=["axis", "axes", "chart", "coordinate", "graph", "math"])
def _(S):
    return [line(poly([(6, 4), (6, 18), (20, 18)], r=S.r)),
            line(poly([(3, 7), (6, 4), (9, 7)], r=S.r * 0.5)), line(poly([(17, 15), (20, 18), (17, 21)], r=S.r * 0.5))]


@icon("graph-function", "math", "Axes with a plotted curve", tags=["graph", "plot", "function", "curve", "chart", "math"])
def _(S):
    return [line(poly([(4, 3.5), (4, 20), (20.5, 20)], r=S.r)),
            line("M7.5 16.5C10.5 16.5 11.5 7.5 15 7.5C17 7.5 18.5 9 20 11")]


@icon("coordinates", "math", "Point plotted on coordinate axes", tags=["coordinates", "point", "xy", "plot", "cartesian", "math"])
def _(S):
    return [line(poly([(4, 3.5), (4, 20), (20.5, 20)], r=S.r)),
            dot(16, 8.5, 2.5),
            dot(16, 13.25, 1), dot(16, 16.5, 1), dot(11.25, 8.5, 1), dot(8, 8.5, 1)]
