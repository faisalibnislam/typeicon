"""TypeIcon Core: stationery (batch 002): packing, filing, fasteners and office machines."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d

CAT = "stationery"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap):
    return min(S.R, cap)


# ============================================================================ packing and handling

@icon("package-dimensions", CAT, "Box in perspective with a dimension line and end ticks above its width",
      tags=["box size", "parcel size", "measure", "shipping", "length width height", "cargo"])
def _(S):
    return [shell(poly([(3, 12), (3, 21), (15, 21), (15, 12)], closed=True, r=S.r)),
            shell(poly([(3, 12), (6, 9), (18, 9), (15, 12)], closed=True, r=S.r)),
            shell(poly([(15, 12), (18, 9), (18, 18), (15, 21)], closed=True, r=S.r)),
            line(seg(3, 4, 18, 4)), line(seg(3, 2.5, 3, 5.5)), line(seg(18, 2.5, 18, 5.5))]


@icon("fragile-symbol", CAT, "Stemmed wine glass with a crack through its bowl, the handling mark for fragile goods",
      tags=["fragile", "glass", "handle with care", "breakable", "shipping mark", "crack"])
def _(S):
    bowl = "M6.5 3H17.5C17.5 8.5 15.5 12 12 12C8.5 12 6.5 8.5 6.5 3Z"
    return [shell(bowl), line("M12 12V20"), line(seg(8, 20.5, 16, 20.5)),
            detail(poly([(12, 3), (10.5, 6), (13.5, 8), (12, 11)], r=S.r * 0.5))]


@icon("this-side-up", CAT, "Two parallel arrows pointing upward over a base line, the handling mark for orientation",
      tags=["this way up", "upright", "orientation", "shipping mark", "handling", "keep upright"])
def _(S):
    return [line(poly([(5.5, 9.5), (8, 6), (10.5, 9.5)], r=S.r)), line(seg(8, 6.5, 8, 17)),
            line(poly([(13.5, 9.5), (16, 6), (18.5, 9.5)], r=S.r)), line(seg(16, 6.5, 16, 17)),
            line(seg(4, 21, 20, 21))]


@icon("keep-dry-symbol", CAT, "Open umbrella with raindrops above its canopy, the handling mark for keep dry",
      tags=["keep dry", "umbrella", "rain", "shipping mark", "waterproof", "protect from water"])
def _(S):
    canopy = "M3 17A9 9 0 0 1 21 17Z" if S.name == "line" else "M3 17A9 9 0 0 1 21 17Q16.5 15 12 17Q7.5 15 3 17Z"
    return [shell(canopy), line("M12 17V20.5a1.75 1.75 0 0 1-3.5 0"),
            line(seg(6, 2, 5, 4.5)), line(seg(12, 1.5, 11, 4)), line(seg(18, 2, 17, 4.5))]


@icon("packing-slip", CAT, "Adhesive pouch stuck on a box with a folded document visible inside",
      tags=["packing list", "invoice pouch", "shipping label", "parcel", "documents enclosed", "delivery note"])
def _(S):
    return [shell(rect(2.5, 4, 19, 16, rr(S, 2))),
            detail(rect(6, 7.5, 12, 9, rr(S, 1.5))),
            detail(seg(9, 11, 15, 11)), detail(seg(9, 13.5, 13, 13.5))]


@icon("wooden-crate", CAT, "Slatted wooden crate with a diagonal brace across the front",
      tags=["crate", "shipping crate", "box", "freight", "wood", "storage"])
def _(S):
    return [shell(rect(3, 3, 18, 18, rr(S, 4))),
            detail(seg(3, 8.5, 21, 8.5)), detail(seg(3, 15.5, 21, 15.5)),
            detail(seg(7, 15.5, 17, 8.5))]


@icon("pallet-jack", CAT, "Manual pallet truck with long flat forks and a tall handle with a loop grip",
      tags=["pallet truck", "hand truck", "warehouse", "forks", "lift", "logistics"])
def _(S):
    return [shell(poly([(3, 14.5), (19.5, 14.5), (21, 18.5), (3, 18.5)], closed=True, r=S.r * 0.6)),
            line(seg(7, 14.5, 7, 4.5)), line(seg(3.5, 4.5, 10.5, 4.5)),
            dot(7, 21, 1.2), dot(18, 21, 1.2)]


# ============================================================================ binders and folders

@icon("ring-binder", CAT, "Upright binder with a label window on the spine and a finger hole near its base",
      tags=["binder", "folder", "lever arch", "file", "office", "documents", "organizer"])
def _(S):
    return [shell(rect(4.5, 2, 15, 20, rr(S, 2.5))),
            detail(rect(8, 5, 8, 5, rr(S, 1))), detail(circle(12, 17, 1.5))]


@icon("binder-clip", CAT, "Triangular clip body with two wire handles raised above it",
      tags=["clamp", "paper clip", "foldback clip", "hold papers", "office", "fastener"])
def _(S):
    return [shell(poly([(3, 21), (7, 10), (17, 10), (21, 21)], closed=True, r=S.r)),
            line(poly([(9, 10), (6, 3.5)], r=0)), line(poly([(15, 10), (18, 3.5)], r=0)),
            detail(seg(7, 15, 17, 15))]


@icon("bulldog-clip", CAT, "Flat metal clip with a wide spring lever on top and a bar across the front",
      tags=["spring clip", "letter clip", "paper clamp", "document clip", "hold papers", "office"])
def _(S):
    return [shell(rect(3, 11.5, 18, 8.5, rr(S, 2))),
            shell(poly([(7, 11.5), (8.5, 4), (15.5, 4), (17, 11.5)], closed=True, r=S.r)),
            detail(seg(6, 16, 18, 16))]


@icon("brass-fastener", CAT, "Round domed head with two flat prongs bent apart below it, like a split pin",
      tags=["paper fastener", "split pin", "brad", "cotter pin", "binding", "crafts", "mini brad"])
def _(S):
    return [shell(ellipse(12, 6.5, 5.5, 3.5) if S.name == "rounded" else poly([(6.5, 10), (6.5, 7), (9, 3.5), (15, 3.5), (17.5, 7), (17.5, 10)], closed=True)),
            line(poly([(10.5, 10), (10.5, 14), (5, 21)], r=S.r)),
            line(poly([(13.5, 10), (13.5, 14), (19, 21)], r=S.r))]


@icon("hanging-folder", CAT, "File folder with hooked rails at both top corners and a small label tab",
      tags=["suspension file", "file cabinet", "filing", "hanging file", "office", "archive"])
def _(S):
    return [shell(rect(5, 9, 14, 12, rr(S, 2))),
            line(poly([(2.5, 8.5), (2.5, 4.5), (21.5, 4.5), (21.5, 8.5)], r=S.r)),
            detail(rect(9, 13, 6, 3, rr(S, 1)))]


@icon("expanding-file", CAT, "Accordion file with pleated sides, a closed flap and an elastic band around it",
      tags=["accordion file", "document organizer", "expanding folder", "paperwork", "filing", "elastic"])
def _(S):
    return [shell(poly([(5, 4), (19, 4), (21, 21), (3, 21)], closed=True, r=S.r)),
            detail(poly([(4.2, 11), (12, 16), (19.8, 11)], r=S.r)),
            detail(seg(16.5, 4, 17.5, 21))]


@icon("index-dividers", CAT, "Stack of sheets with staggered tabs sticking out along the right edge",
      tags=["tab dividers", "section tabs", "binder tabs", "organizer", "filing", "index tabs"])
def _(S):
    return [shell(poly([(3, 2), (21, 2), (21, 6), (18, 6), (18, 9), (21, 9), (21, 13), (18, 13), (18, 16), (21, 16),
                        (21, 20), (18, 20), (18, 22), (3, 22)], closed=True, r=S.r * 0.5)),
            detail(seg(7, 7, 13, 7)), detail(seg(7, 12, 13, 12)), detail(seg(7, 17, 13, 17))]


@icon("sheet-protector", CAT, "Clear plastic sleeve with punched holes along the left and a ruled page inside",
      tags=["document sleeve", "plastic pocket", "binder sleeve", "page protector", "clear pocket", "filing"])
def _(S):
    return [shell(rect(4, 2, 16, 20, rr(S, 2.5))),
            dot(7.5, 6, 1.25), dot(7.5, 12, 1.25), dot(7.5, 18, 1.25),
            detail(seg(11.5, 7, 16.5, 7)), detail(seg(11.5, 12, 16.5, 12)), detail(seg(11.5, 17, 16.5, 17))]


@icon("magazine-file", CAT, "Upright holder with a slanted cutaway front and a page standing up inside it",
      tags=["magazine holder", "literature rack", "document holder", "desk organizer", "brochure holder", "file box"])
def _(S):
    return [shell(poly([(4, 22), (4, 14.5), (20, 9), (20, 22)], closed=True, r=S.r)),
            line(poly([(8, 13), (8, 3), (17, 3), (17, 10)], r=S.r))]


@icon("file-sorter", CAT, "Desktop rack with vertical slots holding folders of different heights",
      tags=["desk sorter", "file rack", "document organizer", "folder holder", "paper sorter", "office"])
def _(S):
    return [shell(rect(3, 15, 18, 6, rr(S, 2))),
            line(poly([(4.5, 15), (4.5, 7), (10, 7), (10, 15)], r=S.r)),
            line(poly([(13.5, 15), (13.5, 3.5), (19.5, 3.5), (19.5, 15)], r=S.r))]


@icon("pocket-folder", CAT, "Folder with a tab and a diagonal pocket across its front",
      tags=["pocket folder", "presentation folder", "portfolio folder", "document folder", "folder", "business card"])
def _(S):
    return [shell(poly([(3, 20), (3, 4.5), (9, 4.5), (11, 7), (21, 7), (21, 20)], closed=True, r=S.r)),
            detail(seg(3, 17, 21, 12))]


@icon("elastic-folder", CAT, "Closed folder with elastic bands stretched across two opposite corners",
      tags=["corner straps", "closure band", "document folder", "elastic strap", "portfolio", "paper holder"])
def _(S):
    return [shell(rect(4, 3, 16, 18, rr(S, 3))),
            detail(poly([(4, 9.5), (9.5, 9.5), (9.5, 3)], r=0)),
            detail(poly([(20, 14.5), (14.5, 14.5), (14.5, 21)], r=0))]


@icon("portfolio-case", CAT, "Large flat case with a carrying handle and a zipper running around three sides",
      tags=["art portfolio", "document case", "folio", "briefcase", "zip case", "artwork carrier"])
def _(S):
    return [shell(rect(2.5, 6.5, 19, 14, rr(S, 3))),
            line(poly([(8, 6.5), (8, 3), (16, 3), (16, 6.5)], r=S.r)),
            detail(poly([(6, 17), (6, 10.5), (18, 10.5), (18, 17)], r=S.r * 0.5))]


@icon("card-catalog", CAT, "Cabinet with a grid of small drawers, each with a pull knob",
      tags=["library catalog", "index cabinet", "drawers", "card index", "filing cabinet", "archive"])
def _(S):
    return [shell(rect(3, 3, 18, 18, rr(S, 3))),
            detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15)), detail(seg(12, 3, 12, 21)),
            dot(7.5, 6, 1.1), dot(16.5, 6, 1.1), dot(7.5, 12, 1.1), dot(16.5, 12, 1.1),
            dot(7.5, 18, 1.1), dot(16.5, 18, 1.1)]


@icon("cash-box", CAT, "Metal box with a folding handle on top and a small lock plate on the front",
      tags=["money box", "petty cash", "lock box", "strongbox", "cash tin", "safe box"])
def _(S):
    return [shell(rect(3, 8.5, 18, 12, rr(S, 2.5))),
            line(poly([(8, 8.5), (8, 4.5), (16, 4.5), (16, 8.5)], r=S.r)),
            detail(seg(3, 12.5, 21, 12.5)),
            Part("dot", rect(10, 13.5, 4, 3.5, 0.5))]


@icon("comb-bound-document", CAT, "Stack of pages held along the left edge by a plastic comb spine with teeth",
      tags=["plastic comb binding", "bound report", "booklet", "presentation copy", "spiral", "report"])
def _(S):
    return [shell(rect(6, 3, 15, 18, rr(S, 2.5))),
            line(seg(3.5, 3, 3.5, 21)),
            detail(seg(3.5, 6.5, 10, 6.5)), detail(seg(3.5, 10.5, 10, 10.5)),
            detail(seg(3.5, 14.5, 10, 14.5)), detail(seg(3.5, 18.5, 10, 18.5))]


@icon("memo-clip-holder", CAT, "Weighted round base with a coiled wire stem ending in a small clip holding a note",
      tags=["note holder", "memo holder", "desk clip", "photo clip", "reminder", "coil stand"])
def _(S):
    return [shell(rect(4, 18.5, 16, 3, rr(S, 1.5))),
            line("M12 18.5C7 16.5 17 13.5 12 11"),
            shell(rect(5, 3, 14, 8, rr(S, 1.5))),
            detail(seg(8.5, 7, 15.5, 7))]


@icon("staple-remover", CAT, "Pair of jaws with two pointed teeth nearly meeting at the front, joined at the back",
      tags=["staple puller", "de-stapler", "jaw remover", "office tool", "pull staples", "paper"])
def _(S):
    return [shell(poly([(3, 4.5), (14, 4.5), (21, 10.5), (14, 9), (8, 9), (8, 15), (14, 15), (21, 13.5), (14, 19.5), (3, 19.5)],
                       closed=True, r=S.r * 0.8))]


@icon("hole-punch", CAT, "Desk punch with a long lever arm across the top and two round punch holes in the base",
      tags=["paper punch", "two hole punch", "office", "binder holes", "desk tool", "perforator"])
def _(S):
    return [shell(rect(3, 13, 18, 8, rr(S, 2.5))),
            shell(poly([(3, 10), (3, 5.5), (21, 3), (21, 10)], closed=True, r=S.r)),
            detail(circle(8, 17, 1.4)), detail(circle(16, 17, 1.4))]


@icon("hand-hole-punch", CAT, "Plier style punch with two handles and a round cutter at the jaw above a small hole",
      tags=["pliers punch", "single hole punch", "craft punch", "leather", "ticket punch", "handheld"])
def _(S):
    return [shell(rect(11, 3.5, 10, 5.5, rr(S, 2))),
            shell(rect(11, 13.5, 10, 5.5, rr(S, 2))),
            line(poly([(11, 6.25), (7, 6.25), (3, 13)], r=S.r)),
            line(poly([(11, 16.25), (8, 16.25), (5, 21.5)], r=S.r))]


@icon("rubber-band", CAT, "Loose elastic loop twisted into a stretched figure of eight shape",
      tags=["elastic band", "hair band", "stretchy loop", "office supply", "bundle", "bind"])
def _(S):
    return [shell("M3.5 8C3.5 4 9.5 4.5 12 12C14.5 19.5 20.5 20 20.5 16C20.5 12 15 11 12 12C9 13 3.5 12 3.5 8Z" if S.name == "line"
                  else "M3.5 8C3.5 4 9.5 4.5 12 12C14.5 19.5 20.5 20 20.5 16C20.5 12 15 11.5 12 12C9 12.5 3.5 12 3.5 8Z")]

# ============================================================================ tapes, bands and cutting

@icon("rubber-band-ball", CAT, "Ball made of curved elastic bands crossing and wrapping around each other",
      tags=["elastic ball", "bands ball", "office supply", "bouncy ball", "stretch", "bundle"])
def _(S):
    return [shell(circle(12, 12, 9)),
            detail(f"M3.5 9Q12 {L(S, 17, 16.4)} 20.5 9"), detail(f"M3.5 15Q12 {L(S, 7, 7.6)} 20.5 15"), detail("M9 3.5Q5 12 9 20.5")]


@icon("tape-roll", CAT, "Adhesive tape roll with a hollow core and a short strip peeling off the edge",
      tags=["sticky tape", "adhesive", "sellotape", "scotch tape", "packing tape", "clear tape"])
def _(S):
    return [shell(circle(11, 10, 7.5)), detail(circle(11, 10, 2.5)),
            line(poly([(11, 17.5), (21.5, 17.5), (21.5, 20.5)], r=S.r * 0.6))]


@icon("washi-tape", CAT, "Roll of patterned paper tape with stripes and a torn end hanging down",
      tags=["masking tape", "decorative tape", "paper tape", "craft tape", "scrapbooking", "journaling"])
def _(S):
    return [shell("M8 5.5H17A3 6 0 0 1 17 17.5H8A3 6 0 0 1 8 5.5Z"),
            detail(seg(11.5, 5.5, 11.5, 17.5)), detail(seg(15, 5.5, 15, 17.5)),
            line(poly([(9, 17.5), (9, 21.5), (11, 20), (13, 21.5), (15, 19.5)], r=S.r * 0.5))]


@icon("tape-dispenser", CAT, "Weighted desk dispenser with a roll on top and a strip of tape leaving at the front",
      tags=["sellotape dispenser", "desk tape", "tape cutter", "office", "adhesive", "sticky tape"])
def _(S):
    return [shell(rect(2.5, 18.5, 19, 3, rr(S, 1.5))),
            shell(circle(10, 9.5, 5.5)), detail(circle(10, 9.5, 1.5)),
            line(poly([(15.5, 11), (19, 13), (21.5, 13)], r=S.r * 0.6)),
            line(poly([(19, 13), (19, 16)], r=0))]


@icon("stapled-pages", CAT, "Stack of pages with a diagonal staple in the top left corner and a lifted corner",
      tags=["stapled", "stapler", "document", "paperwork", "pages", "fastened papers"])
def _(S):
    return [shell(poly([(4.5, 2.5), (19.5, 2.5), (19.5, 15), (13, 21.5), (4.5, 21.5)], closed=True, r=S.r)),
            detail(poly([(13, 21.5), (13, 15), (19.5, 15)], r=S.r * 0.5)),
            detail(seg(7.5, 8, 11.5, 6))]


@icon("paperclip-dispenser", CAT, "Round desk holder with a paperclip clinging to its magnetic top",
      tags=["magnetic paperclip holder", "clip holder", "desk organizer", "paper clips", "office", "magnet"])
def _(S):
    return [shell(poly([(3.5, 21), (6, 15), (18, 15), (20.5, 21)], closed=True, r=S.r)),
            line("M9 14.5V5.5a3 3 0 0 1 6 0V12.5a1.5 1.5 0 0 1-3 0V7.5")]


@icon("paper-guillotine", CAT, "Gridded cutting board with a long arm blade hinged at one corner",
      tags=["paper cutter", "guillotine trimmer", "paper trimmer", "cutting blade", "craft", "office"])
def _(S):
    return [shell(rect(3, 13, 18, 8, rr(S, 4))),
            detail(seg(3, 17, 21, 17)), detail(seg(12, 13, 12, 21)),
            line(seg(4.5, 10.5, 20.5, 3)), dot(4.5, 10.5, 1.5), dot(20.5, 3, 1.5)]


@icon("rotary-paper-trimmer", CAT, "Flat trimmer base with a straight rail and a small sliding cutter head on it",
      tags=["paper trimmer", "paper cutter", "rotary cutter", "photo trimmer", "craft cutter", "cut paper"])
def _(S):
    return [shell(rect(3, 7, 18, 14, rr(S, 2.5))),
            detail(seg(3, 11.5, 21, 11.5)),
            Part("dot", rect(13, 9.5, 5, 7, 1.2))]


@icon("cutting-mat", CAT, "Rectangular mat with a square grid and ruler tick marks along the edges",
      tags=["self healing mat", "craft mat", "cutting board", "grid mat", "hobby", "quilting"])
def _(S):
    return [shell(rect(3, 3, 18, 18, rr(S, 3))),
            detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)),
            detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15))]


# ============================================================================ drafting and drawing

@icon("t-square", CAT, "Long ruler blade joined at a right angle to a short thick head, forming a T",
      tags=["drafting square", "drawing ruler", "technical drawing", "straight edge", "architect", "draughting"])
def _(S):
    return [shell(poly([(3, 3), (7, 3), (7, 10), (21, 10), (21, 14), (7, 14), (7, 21), (3, 21)], closed=True, r=S.r)),
            dot(15, 12, 0.9)]


@icon("french-curve", CAT, "Flat drawing template with flowing irregular curved edges and a curved inner cutout",
      tags=["curve template", "drafting curve", "ship curve", "drawing template", "technical drawing", "design"])
def _(S):
    return [shell("M3 18C3 10 8 6 12 8C15 10 15 4 20 4C22.5 4 22 8 20 10C16 14 14 19 8 20.5C5 21 3 20 3 18Z"),
            detail("M7.5 16C7.5 12.5 10.5 11 13 12.5")]


@icon("architect-scale", CAT, "Triangular prism ruler seen at an angle with scale tick marks on its front face",
      tags=["scale ruler", "triangular ruler", "drafting scale", "blueprint", "measure", "engineer scale"])
def _(S):
    return [shell(poly([(2, 10), (2, 19), (18, 19), (18, 10)], closed=True, r=S.r * 0.5)),
            shell(poly([(2, 10), (6, 5.5), (22, 5.5), (18, 10)], closed=True, r=S.r * 0.5)),
            shell(poly([(18, 10), (22, 5.5), (22, 14.5), (18, 19)], closed=True, r=S.r * 0.5)),
            detail(seg(6, 10, 6, 13.5)), detail(seg(10, 10, 10, 15)), detail(seg(14, 10, 14, 13.5))]


@icon("lettering-stencil", CAT, "Rectangular sheet with cut out letter shapes arranged in a row",
      tags=["letter stencil", "alphabet template", "stencil", "sign painting", "craft", "lettering guide"])
def _(S):
    return [shell(rect(2.5, 5, 19, 14, rr(S, 3))),
            detail(poly([(5.5, 15.5), (8, 8.5), (10.5, 15.5)], r=0)), detail(seg(6.5, 13, 9.5, 13)),
            detail(circle(16, 12, 2.5))]


@icon("circle-template", CAT, "Flat stencil with a row of circular holes of decreasing size",
      tags=["circle guide", "drawing template", "drafting", "stencil", "round holes", "technical drawing"])
def _(S):
    return [shell(rect(2, 6, 20, 12, rr(S, 3))),
            detail(circle(7, 12, 2.5)), detail(circle(13.5, 12, 1.5)), dot(18.5, 12, 1)]


@icon("drafting-table", CAT, "Tilted drawing board on a stand with a straight parallel bar across the board",
      tags=["drawing board", "architect desk", "blueprint table", "art table", "draughting", "easel desk"])
def _(S):
    return [shell(poly([(4, 4.5), (20, 4.5), (21.5, 13), (2.5, 13)], closed=True, r=S.r)),
            detail(seg(3.5, 9, 20.5, 9)),
            line(seg(8, 13, 6, 21)), line(seg(16, 13, 18, 21)), line(seg(7, 18, 17, 18))]


@icon("slide-rule", CAT, "Long ruler with a central sliding strip, scale ticks and a cursor hairline",
      tags=["slipstick", "calculating ruler", "logarithm", "engineering", "vintage calculator", "math"])
def _(S):
    return [shell(rect(2, 8, 20, 8, rr(S, 4))),
            detail(seg(2, 12, 22, 12)),
            detail(seg(6, 8, 6, 12)), detail(seg(9.5, 8, 9.5, 12)), detail(seg(13, 8, 13, 12)),
            line(seg(17.5, 4, 17.5, 20))]


@icon("tracing-light-pad", CAT, "Flat glowing panel with short light rays above it and a sheet of paper on top",
      tags=["light box", "tracing pad", "light table", "drawing", "animation", "calligraphy"])
def _(S):
    return [shell(rect(3, 10, 18, 11, rr(S, 2.5))),
            detail(rect(6.5, 13, 11, 5, rr(S, 1))),
            line(seg(12, 2, 12, 6)), line(seg(5, 3.5, 6.8, 6.5)), line(seg(19, 3.5, 17.2, 6.5))]


@icon("tally-counter", CAT, "Round hand counter with a digit window, a push button on top and a finger ring below",
      tags=["click counter", "hand tally", "people counter", "clicker", "count", "attendance"])
def _(S):
    return [shell(rect(4.5, 7, 15, 10, rr(S, 3.5))),
            detail(rect(8, 10, 8, 4, rr(S, 1))),
            line(seg(12, 7, 12, 3.5)), line(seg(9, 3, 15, 3)),
            line("M9 17V19A3 3 0 0 0 15 19V17")]


@icon("pantograph", CAT, "Lattice of four hinged bars forming a parallelogram with a stylus and a pencil at the ends",
      tags=["copying frame", "drawing tool", "scaling tool", "linkage", "parallelogram", "tracing"])
def _(S):
    return [shell(poly([(4.5, 8), (13, 4), (19.5, 10), (11, 14)], closed=True, r=S.r * 0.6)),
            line(seg(11, 14, 8.5, 21)), line(seg(19.5, 10, 21.5, 16.5)),
            dot(4.5, 8, 1.4)]


@icon("geometry-set", CAT, "Open flat tin holding a ruler, a protractor and a compass laid side by side",
      tags=["math set", "maths set", "school supplies", "compass and ruler", "protractor", "drawing instruments"])
def _(S):
    return [shell(rect(2, 4, 20, 16, rr(S, 3))),
            detail(rect(4.5, 7.5, 3, 9, 0)),
            detail("M9.5 16.5A3.5 3.5 0 0 1 16.5 16.5Z"),
            detail(poly([(18, 16.5), (19, 8), (20, 16.5)], r=0))]


@icon("paperweight", CAT, "Glass dome with a swirl inside, resting on a sheet of paper",
      tags=["glass paperweight", "desk ornament", "dome", "keepsake", "office", "snow globe"])
def _(S):
    return [shell("M4 18A8 10 0 0 1 20 18Z" if S.name == "line" else "M4 18Q4 8 12 8Q20 8 20 18Z"),
            detail("M12 15.5A2.5 2.5 0 1 1 14.5 13"),
            line(seg(2, 21.5, 22, 21.5))]


@icon("desk-nameplate", CAT, "Wedge shaped name block with lines of text on its angled front face",
      tags=["name plate", "name block", "desk sign", "office sign", "name tag", "executive"])
def _(S):
    return [shell(poly([(3, 20), (5.5, 7.5), (18.5, 7.5), (21, 20)], closed=True, r=S.r)),
            detail(seg(8, 12, 16, 12)), detail(seg(9, 16, 15, 16))]


@icon("desk-organizer", CAT, "Desk caddy with compartments holding pens, a notepad and a ruler",
      tags=["pen holder", "desk caddy", "office organizer", "stationery holder", "pencil cup", "tidy desk"])
def _(S):
    return [shell(rect(3, 11, 18, 10, rr(S, 2.5))),
            detail(seg(9, 11, 9, 21)), detail(seg(15, 11, 15, 21)),
            line(seg(5, 11, 4, 4.5)), line(seg(7, 11, 7.5, 3.5)),
            line(poly([(10.5, 11), (10.5, 6), (13.5, 6), (13.5, 11)], r=S.r * 0.5)),
            line(seg(18, 11, 18, 4))]


@icon("desk-blotter", CAT, "Large rectangular desk pad with triangular leather pockets at its corners",
      tags=["desk pad", "writing pad", "desk mat", "office", "leather corners", "paper protector"])
def _(S):
    return [shell(rect(2.5, 4, 19, 16, rr(S, 2.5))),
            detail(seg(2.5, 9, 7.5, 4)), detail(seg(16.5, 4, 21.5, 9)),
            detail(seg(2.5, 15, 7.5, 20)), detail(seg(16.5, 20, 21.5, 15))]


@icon("newtons-cradle", CAT, "Frame with balls hanging in a row on strings and the outermost ball swung out",
      tags=["newton's cradle", "executive toy", "desk toy", "momentum", "pendulum", "physics"])
def _(S):
    return [line(poly([(3, 21.5), (3, 3), (21, 3), (21, 21.5)], r=S.r)),
            line(seg(12, 3, 12, 16)), line(seg(15.5, 3, 15.5, 16)), line(seg(19, 3, 19, 16)),
            line(seg(9, 3, 5.5, 14.5)),
            dot(12, 17.5, 1.8), dot(15.5, 17.5, 1.8), dot(19, 17.5, 1.8), dot(5.2, 15.8, 1.8)]


@icon("business-card-holder", CAT, "Small desk stand holding an upright stack of business cards",
      tags=["card stand", "card display", "name card holder", "desk accessory", "contact cards", "office"])
def _(S):
    return [shell(rect(2.5, 15, 19, 6, rr(S, 2))),
            line(poly([(6, 15.5), (8, 4), (20, 4), (18, 15.5)], r=S.r * 0.6)),
            detail(seg(11, 8, 17, 8))]


@icon("mouse-pad", CAT, "Pad with a raised wrist rest strip at the front and a computer mouse on it",
      tags=["mousepad", "mouse mat", "wrist rest", "desk mat", "computer accessory", "gaming"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, rr(S, 4))),
            detail(seg(2.5, 17, 21.5, 17)),
            detail(rect(9.5, 5.5, 5, 7, 2.5)), detail(seg(12, 5.5, 12, 8.5))]


@icon("air-duster-can", CAT, "Aerosol can with a trigger nozzle and a long thin straw pointing forward",
      tags=["compressed air", "canned air", "keyboard cleaner", "dust blower", "spray can", "cleaning"])
def _(S):
    return [shell(poly([(4, 21), (4, 10.5), (6.5, 8.5), (10.5, 8.5), (13, 10.5), (13, 21)], closed=True, r=S.r)),
            shell(rect(5.5, 4, 6, 3, rr(S, 1))),
            line(poly([(11.5, 5.5), (21.5, 5.5)], r=0)),
            detail(seg(4, 15.5, 13, 15.5))]


@icon("laptop-stand", CAT, "Angled open frame stand with a laptop tilted on top of it",
      tags=["notebook stand", "computer riser", "ergonomic stand", "desk accessory", "laptop riser", "workstation"])
def _(S):
    return [shell(poly([(3, 12.5), (21, 7.5), (21, 10.5), (3, 15.5)], closed=True, r=S.r * 0.5)),
            line(poly([(6.5, 16), (4, 21.5)], r=0)), line(poly([(17.5, 12), (20, 21.5)], r=0)),
            line(seg(5, 19, 19, 19))]


@icon("monitor-arm", CAT, "Articulated arm clamped to a desk edge holding a flat monitor out on its end",
      tags=["monitor mount", "screen arm", "desk mount", "display bracket", "ergonomic", "workstation"])
def _(S):
    return [shell(rect(11, 3, 10, 8, rr(S, 2))),
            line(poly([(6, 20), (6, 13.5), (11, 8)], r=S.r)),
            shell(rect(2.5, 19.5, 7, 2.5, 0)), dot(6, 13.5, 1.4)]


@icon("monitor-riser", CAT, "Low shelf platform with a monitor on top and a keyboard slid under it",
      tags=["monitor stand", "desk shelf", "screen riser", "desk organizer", "ergonomic", "keyboard storage"])
def _(S):
    return [shell(rect(5, 2.5, 14, 6.5, rr(S, 2))),
            shell(rect(3, 11.5, 18, 3, rr(S, 1.5))),
            line(seg(5, 14.5, 5, 21)), line(seg(19, 14.5, 19, 21)),
            shell(rect(8.5, 17.5, 7, 3, rr(S, 1)))]


def _rot(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


@icon("stationery-supplies", CAT, "Ruler and pencil standing side by side, the sign for office and school supplies",
      tags=["office supplies", "school supplies", "pencil and ruler", "writing tools", "back to school", "stationery shop"])
def _(S):
    return [shell(rect(3, 3, 6.5, 18, rr(S, 2))),
            detail(seg(3, 7, 6.5, 7)), detail(seg(3, 11, 6.5, 11)), detail(seg(3, 15, 6.5, 15)),
            shell(poly([(13.5, 3), (20.5, 3), (20.5, 15), (17, 21), (13.5, 15)], closed=True, r=S.r * 0.6)),
            detail(seg(13.5, 7, 20.5, 7))]


@icon("comb-binding-machine", CAT, "Machine with a punching lever on top and a plastic comb with teeth at the front",
      tags=["binding machine", "comb binder", "document binder", "punch and bind", "office machine", "report binding"])
def _(S):
    return [shell(rect(3, 10, 18, 11, rr(S, 2.5))),
            line(poly([(5.5, 10), (5, 4), (18, 3.5)], r=S.r)),
            detail(seg(6, 14, 18, 14)),
            detail(seg(7, 14, 7, 18)), detail(seg(10.5, 14, 10.5, 18)),
            detail(seg(14, 14, 14, 18)), detail(seg(17.5, 14, 17.5, 18))]


@icon("typewriter", CAT, "Front view of a typewriter with a roller holding a sheet of paper above rows of round keys",
      tags=["vintage typewriter", "manual typewriter", "writer", "author", "retro office", "typing"])
def _(S):
    return [shell(poly([(3, 21), (5, 12.5), (19, 12.5), (21, 21)], closed=True, r=S.r)),
            line(seg(3, 9.5, 21, 9.5)),
            line(poly([(7.5, 8.5), (7.5, 2.5), (16.5, 2.5), (16.5, 8.5)], r=S.r * 0.5)),
            dot(8, 16, 1.2), dot(12, 16, 1.2), dot(16, 16, 1.2),
            dot(7, 19, 1.2), dot(12, 19, 1.2), dot(17, 19, 1.2)]


@icon("adding-machine", CAT, "Desk calculator with a paper roll on top feeding a printed tape and a keypad below",
      tags=["calculator", "accounting machine", "printing calculator", "bookkeeping", "tape calculator", "cash register"])
def _(S):
    return [shell(rect(3, 11, 18, 10, rr(S, 2.5))),
            shell(circle(7, 6.5, 3.5)),
            line(poly([(10.5, 6.5), (15, 6.5), (15, 2.5)], r=S.r * 0.5)),
            dot(7, 15, 0.95), dot(10.5, 15, 0.95), dot(14, 15, 0.95), dot(17.5, 15, 0.95),
            dot(7, 18, 0.95), dot(10.5, 18, 0.95), dot(14, 18, 0.95), dot(17.5, 18, 0.95)]


@icon("time-card-machine", CAT, "Wall box with a clock dial on top and a slot at the bottom holding an inserted time card",
      tags=["time clock", "punch clock", "clocking in", "attendance", "time recorder", "timesheet"])
def _(S):
    return [shell(rect(5, 2.5, 14, 14.5, rr(S, 3))),
            detail(circle(12, 8, 3.5)), dot(12, 8, 1),
            detail(seg(8, 13.5, 16, 13.5)),
            line(poly([(9.5, 15), (9.5, 21.5), (14.5, 21.5), (14.5, 15)], r=S.r * 0.4))]


@icon("overhead-projector", CAT, "Box base with a flat glass stage and an arm holding a mirrored head above it",
      tags=["transparency projector", "classroom projector", "acetate", "teaching", "lecture", "presentation"])
def _(S):
    return [shell(rect(3, 13, 18, 8, rr(S, 2.5))),
            detail(rect(5.5, 15.5, 13, 3, 0.5)),
            line(poly([(17.5, 13), (17.5, 5.5), (14.5, 5.5)], r=S.r * 0.6)),
            shell(rect(5, 3, 9.5, 5, rr(S, 2)))]


@icon("document-camera", CAT, "Base plate with a bendable arm and a camera head pointing down at a sheet of paper",
      tags=["visualizer", "doc cam", "classroom camera", "presenter camera", "teaching", "scanner arm"])
def _(S):
    return [shell(rect(3, 18.5, 18, 3, rr(S, 1.5))),
            line(poly([(6.5, 18.5), (6.5, 10.5), (13, 5)], r=S.r)), dot(6.5, 10.5, 1.4),
            shell(rect(12, 2.5, 9, 4.5, rr(S, 2))),
            line(seg(14.5, 9.5, 12, 15.5)), line(seg(19, 9.5, 21, 15.5))]


@icon("plotter-printer", CAT, "Wide format printer with a long sheet of paper feeding out of the front",
      tags=["large format printer", "wide format", "blueprint printer", "poster printer", "cad printer", "drawing printer"])
def _(S):
    return [shell(rect(2.5, 3.5, 19, 8, rr(S, 3))),
            detail(seg(6, 7.5, 18, 7.5)),
            shell(poly([(6, 13.5), (18, 13.5), (19.5, 21.5), (4.5, 21.5)], closed=True, r=S.r * 0.5)),
            detail(seg(9, 17.5, 15, 17.5))]


@icon("microfilm-reader", CAT, "Desk machine with a tall viewing screen above a flat film carrier stage",
      tags=["microfiche reader", "film viewer", "archive viewer", "library", "newspaper archive", "records"])
def _(S):
    return [shell(rect(5, 2.5, 14, 10, rr(S, 2.5))),
            detail(rect(8, 5.5, 8, 4, 0.5)),
            shell(rect(3, 14.5, 18, 6.5, rr(S, 2.5))),
            detail(rect(7, 16.5, 10, 2.5, 0.5))]


@icon("desk-phone", CAT, "Office telephone with the handset resting on top and a keypad with extra line buttons",
      tags=["office phone", "landline", "telephone", "business phone", "corded phone", "reception"])
def _(S):
    return [shell(poly([(3, 9.5), (3, 4.5), (21, 4.5), (21, 9.5), (18.5, 9.5), (18.5, 7.5), (5.5, 7.5), (5.5, 9.5)],
                       closed=True, r=S.r)),
            shell(poly([(2.5, 21.5), (4, 12), (20, 12), (21.5, 21.5)], closed=True, r=S.r)),
            dot(8.5, 15.5, 1.1), dot(12, 15.5, 1.1), dot(15.5, 15.5, 1.1),
            dot(8, 18.8, 1.1), dot(12, 18.8, 1.1), dot(16, 18.8, 1.1)]


@icon("conference-phone", CAT, "Low triangular speaker phone with rounded points, a central grille and small buttons",
      tags=["speakerphone", "conference call", "meeting phone", "star phone", "audio conferencing", "office"])
def _(S):
    r = L(S, 0, 4)
    return [shell(poly([(12, 3.5), (21.5, 19), (2.5, 19)], closed=True, r=r)),
            detail(circle(12, 13.5, 2.6)),
            dot(12, 8, 1), dot(6.5, 17, 1), dot(17.5, 17, 1)]


@icon("toner-cartridge", CAT, "Long boxy printer cartridge with a handle grip and a drum edge along the bottom",
      tags=["laser toner", "printer cartridge", "copier toner", "ink supply", "printer supplies", "refill"])
def _(S):
    return [shell(poly([(2.5, 9), (16, 9), (21.5, 13), (21.5, 20), (2.5, 20)], closed=True, r=S.r)),
            line(poly([(6, 9), (6, 4.5), (12, 4.5), (12, 9)], r=S.r * 0.6)),
            detail(seg(2.5, 16.5, 21.5, 16.5))]


@icon("ink-cartridge", CAT, "Small boxy printer cartridge with a label area and a nozzle tip at its base",
      tags=["printer ink", "inkjet cartridge", "ink tank", "printer supplies", "refill", "color ink"])
def _(S):
    return [shell(poly([(4, 3), (20, 3), (20, 16), (15, 16), (15, 21), (9, 21), (9, 16), (4, 16)], closed=True, r=S.r)),
            detail(rect(7.5, 6.5, 9, 5, rr(S, 1)))]


@icon("paper-jam", CAT, "Printer with a creased sheet stuck half out of its output slot",
      tags=["printer error", "stuck paper", "jammed printer", "crumpled paper", "printer problem", "troubleshooting"])
def _(S):
    return [shell(rect(3, 12, 18, 9, rr(S, 2.5))),
            detail(seg(6, 16.5, 18, 16.5)),
            line(poly([(7.5, 12), (7.5, 3.5), (16.5, 3.5), (16.5, 12)], r=S.r * 0.4)),
            line(poly([(7.5, 8), (10.5, 6), (13.5, 9), (16.5, 7)], r=0))]


@icon("banknote-counter", CAT, "Desk machine with a hopper of notes on top and a digit display on the front",
      tags=["money counter", "cash counter", "bill counter", "currency counting", "bank machine", "till"])
def _(S):
    return [shell(rect(3, 11, 18, 10, rr(S, 2.5))),
            line(poly([(6.5, 11), (7.5, 4.5), (16.5, 4.5), (17.5, 11)], r=S.r * 0.5)),
            detail(seg(9.5, 7.5, 14.5, 7.5)),
            detail(rect(5.5, 14, 13, 4.5, 1)),
            dot(9, 16.25, 0.9), dot(12, 16.25, 0.9), dot(15, 16.25, 0.9)]


@icon("pneumatic-tube-carrier", CAT, "Capsule with rounded end caps and a rolled document inside",
      tags=["tube capsule", "message carrier", "bank tube", "vacuum tube", "document capsule", "drive-through"])
def _(S):
    return [shell(rect(2.5, 6.5, 19, 11, L(S, 2, 5.5))),
            detail(seg(6.5, 6.5, 6.5, 17.5)), detail(seg(17.5, 6.5, 17.5, 17.5)),
            detail(rect(9.5, 9.5, 5, 5, L(S, 1, 2.5)))]


@icon("stenotype-machine", CAT, "Small compact keyboard with few keys mounted on a short tripod stand",
      tags=["steno machine", "court reporter", "shorthand", "stenograph", "transcription", "captioning"])
def _(S):
    return [shell(rect(3, 3, 18, 9.5, rr(S, 3))),
            dot(7, 6.5, 1.2), dot(10.5, 6.5, 1.2), dot(14, 6.5, 1.2), dot(17.5, 6.5, 1.2),
            dot(8.5, 9.5, 1.2), dot(12, 9.5, 1.2), dot(15.5, 9.5, 1.2),
            line(seg(12, 12.5, 12, 17)), line(poly([(5.5, 21.5), (12, 17), (18.5, 21.5)], r=S.r * 0.5))]


@icon("printing-press", CAT, "Hand press with a large screw and bar handle above a flat bed platen",
      tags=["letterpress", "gutenberg", "print shop", "printmaking", "typesetting", "old printer"])
def _(S):
    return [shell(rect(3, 15.5, 18, 5.5, rr(S, 2.5))),
            line(poly([(5, 15.5), (5, 8), (19, 8), (19, 15.5)], r=S.r)),
            shell(rect(10.5, 4.5, 3, 8.5, rr(S, 1))),
            line(seg(3, 3.5, 21, 3.5))]
