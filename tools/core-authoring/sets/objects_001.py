"""TypeIcon Core: objects (batch 001): household vessels, bags, umbrellas, candles, fire tools, batteries and lights."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path  # noqa: F401

CAT = "objects"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def mark(d):
    """Small solid mark: solid in stroke styles, knocked out of a Filled body."""
    return Part("dot", d)


# ============================================================================ vessels and jars

@icon("gratitude-jar", CAT, "Glass jar with a lid filled with small folded paper notes.",
      tags=["thankful", "notes jar", "memory jar", "appreciation", "wishes", "keepsake"])
def _(S):
    return [shell(rect(7, 2.5, 10, 3, L(S, 0.5, 1.5))),
            shell(rect(5.5, 8, 13, 13, S.R)),
            detail(poly([(9.5, 15), (12, 12), (15, 13.5), (12.5, 17)], closed=True, r=S.r * 0.3)),
            mark(circle(15.5, 17.5, 1.2))]


@icon("clay-water-pot", CAT, "Round clay water pot with a short neck, resting on a ring stand.",
      tags=["matka", "earthen pot", "terracotta", "water jug", "pitcher", "pottery"])
def _(S):
    return [shell("M9 3h6v3.2c3.5 1 5 3.8 5 6.8 0 2.5-1.5 4.3-4 5H8c-2.5-.7-4-2.5-4-5 0-3 1.5-5.8 5-6.8z"),
            line("M8 19.5l1 2h6l1-2")]


@icon("surahi", CAT, "Round clay water carafe with a very long narrow neck and a flared mouth.",
      tags=["carafe", "water pitcher", "clay jug", "decanter", "long neck", "earthenware"])
def _(S):
    return [shell("M8 3h8l-2 4v4.4A5.5 5.5 0 1 1 10 11.4V7z")]


@icon("lota", CAT, "Small round-bodied metal water vessel with a short flared neck and no handle.",
      tags=["water vessel", "brass pot", "kalash", "ritual pot", "ewer", "washing pot"])
def _(S):
    return [shell("M8 3.5h8l-2 3.8A7 7 0 1 1 10 7.3z"),
            detail("M7.3 15.5h9.4")]


@icon("well-bucket", CAT, "Wooden bucket with metal bands hanging from a rope under a small well pulley.",
      tags=["pail", "draw water", "well", "rope", "pulley", "village"])
def _(S):
    return [shell(circle(12, 5.5, 2.5)),
            line("M12 8v3"),
            shell(poly([(6.5, 11), (17.5, 11), (16.5, 21), (7.5, 21)], closed=True, r=S.r)),
            detail("M6.8 14.5h10.4"), detail("M7.2 18h9.6")]


@icon("ash-bucket", CAT, "Metal bucket with a lid and a handle, a little shovel leaning against it.",
      tags=["fireplace", "coal scuttle", "ash pail", "hearth", "fire cleanup", "shovel"])
def _(S):
    return [shell(poly([(3, 11), (15, 11), (13.5, 21), (4.5, 21)], closed=True, r=S.r)),
            line("M5 11a4 4 0 0 1 8 0"),
            detail("M3.4 14.5h11.2"),
            line("M20.5 3v11"),
            solid(poly([(18.3, 14), (22.7, 14), (21.6, 20), (19.4, 20)], closed=True))]


@icon("sake-bottle", CAT, "Slender ceramic flask with a bulbous base and narrow neck, beside a small cup.",
      tags=["tokkuri", "japanese", "rice wine", "flask", "ochoko", "drink"])
def _(S):
    return [shell("M7 3h4v7.9A5.5 5.5 0 1 1 7 10.9z"),
            shell(poly([(15.5, 15), (21.5, 15), (20.5, 20.5), (16.5, 20.5)], closed=True, r=S.r * 0.6))]


@icon("genie-bottle", CAT, "Squat round bottle with a long narrow neck and flared lip, smoke curling from it.",
      tags=["magic lamp", "wish", "fantasy", "smoke", "aladdin", "potion"])
def _(S):
    return [shell("M9 7.5h6l-1 2v2.9A5 5 0 1 1 10 12.4V9.5z"),
            line("M12 5c-2.6-1.3 2.6-2.2 0-3.6")]


@icon("crushed-can", CAT, "Drink can crumpled and bent in the middle with its pull tab still on top.",
      tags=["soda can", "recycling", "empty can", "litter", "aluminium", "trash"])
def _(S):
    return [shell(poly([(7, 3), (17, 3), (17, 9), (15.5, 12), (17.5, 15), (17, 21), (7, 21), (7, 16.5), (9.5, 14), (6.5, 11.5), (7, 8)], closed=True, r=S.r)),
            mark(circle(12, 6, 1.2))]


@icon("sardine-tin", CAT, "Flat rectangular tin with its lid rolled back on a key, showing fish lying side by side.",
      tags=["canned fish", "tinned fish", "can opener", "preserved", "pantry", "seafood"])
def _(S):
    return [shell(rect(3, 9, 18, 12, L(S, 1, 3))),
            shell(circle(17, 5, 2.5)),
            mark(ellipse(10, 13, 4, 1.3)), mark(poly([(14, 13), (17.5, 11.4), (17.5, 14.6)], closed=True)),
            mark(ellipse(10, 17.5, 4, 1.3)), mark(poly([(14, 17.5), (17.5, 15.9), (17.5, 19.1)], closed=True))]


@icon("lavender-sachet", CAT, "Small fabric pouch tied with a ribbon and a sprig of lavender tucked in the knot.",
      tags=["scented bag", "potpourri", "drawer freshener", "herbal", "aroma", "pouch"])
def _(S):
    return [shell("M8 3.5l2.5 5.500C6 11 4 14.500 5 18c.4 2 2 3 4 3h6c2 0 3.600-1 4-3 1-3.500-1-7-5.500-9L16 3.500z"),
            detail("M10.500 9h3"),
            detail("M12 18v-4"),
            mark(circle(12, 12.3, 1.2)), mark(circle(10, 14.2, 1.1)), mark(circle(14, 14.2, 1.1))]


@icon("charcoal-bag", CAT, "Paper sack with a folded top and lumps of charcoal shown on the front.",
      tags=["barbecue", "bbq fuel", "briquettes", "grill", "coal", "sack"])
def _(S):
    return [shell(poly([(5, 3), (19, 3), (19, 21), (5, 21)], closed=True, r=S.r)),
            detail("M5.400 8h13.200"),
            mark(poly([(8, 16), (10.5, 12), (13, 15.5)], closed=True, r=0.5)),
            mark(poly([(13, 18), (15.5, 13), (17.500, 17)], closed=True, r=0.5))]


@icon("vacuum-storage-bag", CAT, "Flat storage bag squeezed tight around folded clothes with a round valve on the front.",
      tags=["space saver", "compression bag", "packing", "closet", "travel", "seal bag"])
def _(S):
    return [shell(poly([(5, 3), (19, 3), (18, 12), (19, 21), (5, 21), (6, 12)], closed=True, r=S.r)),
            mark(circle(12, 12, 1.6)),
            detail("M7.500 7.500h9"), detail("M7.500 16.500h9")]


@icon("bindle", CAT, "Cloth bundle tied at the end of a stick carried over the shoulder.",
      tags=["hobo bundle", "wanderer", "traveler", "knapsack", "runaway", "stick bag"])
def _(S):
    return [line("M3 20L17.500 6.500"),
            shell("M17 8.500l1.500 3c2.500 1 3.500 2.500 3.500 4.500 0 2.500-2 4.500-5 4.500s-5-2-5-4.500c0-2 1-3.500 3.500-4.500z"),
            detail("M13 16.500h8")]


# ============================================================================ bags, cases and keys

@icon("bowling-bag", CAT, "Rounded barrel-shaped bag with two short handles and a zipper along the top.",
      tags=["duffel", "gym bag", "sports bag", "retro bag", "barrel bag", "travel bag"])
def _(S):
    return [line("M8 9C8 3.500 16 3.500 16 9"),
            shell(rect(2.5, 9, 19, 11.5, L(S, 4, 5.5))),
            detail("M3 13h18"),
            mark(rect(10.500, 14.500, 3, 3, 0.5))]


@icon("shoe-bag", CAT, "Drawstring pouch with a shoe outline printed on the front.",
      tags=["footwear bag", "sneaker bag", "gym", "travel packing", "drawstring", "laundry"])
def _(S):
    return [shell(poly([(7, 7), (17, 7), (19.5, 21), (4.5, 21)], closed=True, r=S.r)),
            line("M8.500 3L12 7l3.500-4"),
            mark(poly([(8, 12.5), (10.500, 12.5), (11.500, 15), (16, 16), (16, 18), (8, 18)], closed=True, r=0.4))]


@icon("clutch-bag", CAT, "Slim rectangular handbag with a fold-over flap and a clasp, no handle.",
      tags=["evening bag", "purse", "envelope bag", "party bag", "fashion", "accessory"])
def _(S):
    return [shell(rect(2.5, 6.5, 19, 12, S.R)),
            detail("M3 8.500c2 5 5 6.500 9 6.500s7-1.500 9-6.500"),
            mark(circle(12, 15, 1.3))]


@icon("laptop-sleeve", CAT, "Padded zippered sleeve with a laptop edge showing at the partly open zip.",
      tags=["notebook case", "computer bag", "protective cover", "macbook sleeve", "zipper", "tech"])
def _(S):
    return [line("M6 9.500V5.500a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v4"),
            shell(rect(3, 9.500, 18, 11.500, S.R)),
            detail("M3.500 13.500h17"),
            mark(rect(15.500, 15, 3, 3, 0.5))]


@icon("yoga-mat-bag", CAT, "Long tube-shaped bag with a drawstring end and a shoulder strap, a rolled mat peeking out.",
      tags=["pilates", "exercise mat carrier", "gym", "fitness", "stretching", "carry bag"])
def _(S):
    return [shell(circle(12, 6, 3)), mark(circle(12, 6, 0.9)),
            shell(rect(7, 10.5, 10, 10.500, S.R)),
            detail("M7.500 14h9"),
            line("M7 12C2 13 2 18 7 19.500")]


@icon("hydration-pack", CAT, "Slim backpack with a drinking tube looping over the shoulder to a bite valve.",
      tags=["camelbak", "water bladder", "running vest", "hiking", "cycling", "trail"])
def _(S):
    return [shell(rect(4, 7, 12, 14.500, S.R)),
            detail("M4.500 14.500h11"),
            line("M13 7V4.500a3.500 3.500 0 0 1 7 0V11"),
            solid(rect(18.700, 11, 2.600, 3.400, 0.6))]


@icon("keepsake-box", CAT, "Square lidded box with the lid propped open and a ribbon running down the front.",
      tags=["memory box", "treasure box", "jewelry box", "trinket", "gift box", "souvenir"])
def _(S):
    return [shell(poly([(6, 3), (18, 3), (19.500, 10), (4.500, 10)], closed=True, r=S.r)),
            shell(rect(4, 12.500, 16, 8.500, S.R)),
            detail("M12 13v7.500"),
            mark(circle(15.500, 7, 1.2))]


@icon("watch-box", CAT, "Box with a glass-window lid showing a watch resting inside.",
      tags=["watch case", "timepiece", "display box", "jewelry", "gift", "collector"])
def _(S):
    return [shell(rect(3, 4.500, 18, 15.500, S.R)),
            detail(rect(6.500, 8, 11, 8.500, L(S, 0.5, 2))),
            mark(circle(12, 12.250, 2.200)), mark(rect(11, 9.500, 2, 5.500))]


@icon("phone-case", CAT, "Rear view of a phone case with a camera cut-out in the corner and raised edges.",
      tags=["cover", "smartphone", "protective case", "mobile accessory", "bumper", "camera cutout"])
def _(S):
    return [shell(rect(5.500, 2.500, 13, 19, S.R + 1)),
            detail(rect(8.500, 5.500, 4.500, 4.500, L(S, 0.5, 1.500))),
            mark(circle(10.750, 7.750, 1.1))]


@icon("passport-holder", CAT, "Folding cover wrapped around a passport with a card slot on the front flap.",
      tags=["travel wallet", "document holder", "passport cover", "travel", "id holder", "trip"])
def _(S):
    return [shell(rect(5, 3, 14, 18, S.R)),
            detail("M8.500 3.500v17"),
            detail(circle(14, 9.500, 2.200)),
            detail("M11.500 16h5")]


@icon("key-under-mat", CAT, "Doormat with a key resting just below its front edge.",
      tags=["spare key", "hidden key", "welcome mat", "doormat", "front door", "emergency key"])
def _(S):
    return [shell(poly([(5, 4), (19, 4), (22, 12), (2, 12)], closed=True, r=S.r * 0.6)),
            detail("M6.500 8h11"),
            shell(circle(6.500, 18, 2)),
            line("M8.500 18H21"),
            line("M16 18v2.500"), line("M19.500 18v2.500")]


@icon("double-bit-key", CAT, "Long key with a round bow and identical bits on both sides of the tip.",
      tags=["skeleton key", "antique key", "old key", "lock", "vintage", "access"])
def _(S):
    return [shell(circle(5.500, 12, 3.300)),
            line("M9 12h13"),
            solid(rect(14.500, 8.500, 3, 3.500)), solid(rect(14.500, 12, 3, 3.500)),
            solid(rect(19, 8.500, 3, 3.500)), solid(rect(19, 12, 3, 3.500))]


@icon("key-organizer", CAT, "Compact holder with several keys folded inside like a pocket knife, one key swung out.",
      tags=["key holder", "smart key", "folding keys", "keychain", "compact", "pocket"])
def _(S):
    return [shell(rect(2.500, 11.500, 13.500, 8, L(S, 3, 4))),
            mark(circle(7, 15.500, 1.300)),
            line("M8 13.500L16.500 8.500"),
            shell(circle(19, 6, 2.500))]


@icon("garage-door-remote", CAT, "Small remote with two large buttons below a house-with-garage symbol.",
      tags=["opener", "clicker", "car remote", "gate remote", "transmitter", "driveway"])
def _(S):
    return [shell(rect(5, 2, 14, 20, S.R)),
            detail(poly([(8, 11), (8, 8), (12, 5), (16, 8), (16, 11)], r=S.r * 0.4)),
            mark(circle(9, 16.500, 2.300)), mark(circle(15, 16.500, 2.300))]


# ============================================================================ umbrellas and parasols

@icon("folding-umbrella", CAT, "Short collapsed umbrella in its sleeve above a straight grip with a wrist strap.",
      tags=["compact umbrella", "travel umbrella", "pocket umbrella", "telescopic", "rain", "collapsible"])
def _(S):
    return [shell("M12 3C15.500 5 16.500 9 16.500 13h-9c0-4 1-8 4.500-10z"),
            detail("M8.500 9.500h7"),
            shell(rect(10, 13, 4, 8, L(S, 0.5, 2))),
            line("M10 18H7.500a2 2 0 0 0 0 4H10")]


@icon("closed-umbrella", CAT, "Tall umbrella closed and furled with a strap, a hooked handle and a pointed tip.",
      tags=["furled", "rolled up", "rain gear", "walking umbrella", "hook handle", "weather"])
def _(S):
    return [shell("M12 2C15 6 15.500 10.500 15 14H9c-.5-3.500 0-8 3-12z"),
            detail("M9.200 10h5.600"),
            line("M12 14v4.500a2.500 2.500 0 0 0 5 0V17")]


@icon("paper-umbrella", CAT, "Oil-paper parasol with thin bamboo ribs fanning out to the edge and a straight handle.",
      tags=["japanese umbrella", "wagasa", "oriental", "bamboo", "parasol", "chinese umbrella"])
def _(S):
    return [shell("M2.500 13C2.500 7 7 3 12 3s9.500 4 9.500 10z"),
            detail("M12 3.500V12.500"),
            detail("M11.500 4C9 6.500 8 9.500 7.500 12.500"),
            detail("M12.500 4C15 6.500 16 9.500 16.500 12.500"),
            line("M12 13v8")]


@icon("bubble-umbrella", CAT, "Deep dome umbrella that curves down almost to the shoulders, with a straight handle.",
      tags=["dome umbrella", "clear umbrella", "transparent", "rain", "wedding", "deep canopy"])
def _(S):
    return [shell("M3.500 16C2.500 8 7 3 12 3s9.500 5 8.500 13c-2-1.500-4.500-2-8.500-2S5.500 14.500 3.500 16z"),
            line("M12 14.500V20"),
            detail("M12 3.500C10 6 9.500 10 9.500 14"), detail("M12 3.500C14 6 14.500 10 14.500 14")]


@icon("broken-umbrella", CAT, "Umbrella with a ragged torn edge and a bent rib poking out of the canopy.",
      tags=["damaged", "windy", "storm", "wrecked umbrella", "gale", "snapped rib"])
def _(S):
    return [shell("M2.500 13C2.500 7 7 3 12 3s9.500 4 9.500 10l-3.500-2-3 2.500-3-2.500-3 2.500-3.500-2z"),
            detail("M12 3.500V9"),
            line("M20 7l2.500 4"),
            line("M12 13v6a2.500 2.500 0 0 1-5 0")]


@icon("umbrella-hat", CAT, "Small umbrella canopy held over a head by a headband.",
      tags=["rain hat", "novelty hat", "funny hat", "hands free umbrella", "headgear", "comic"])
def _(S):
    return [shell(L(S, "M3 9C3 5 7 2.500 12 2.500S21 5 21 9z", "M3 9C3 5 7 2.500 12 2.500S21 5 21 9c-2-1.300-4.500-1.500-9-1.500S5 7.700 3 9z")),
            line("M12 9v4.500"),
            shell(circle(12, 17.500, 4)),
            detail("M8 16.500h8")]


@icon("lace-parasol", CAT, "Small handheld sun parasol with a scalloped frilled edge and a long slim shaft.",
      tags=["sunshade", "victorian", "bridal", "wedding", "frilly", "vintage", "garden party"])
def _(S):
    return [shell("M2.500 12C2.500 6.500 7 3 12 3s9.500 3.500 9.500 9a2.375 2.375 0 0 1-4.750 0 2.375 2.375 0 0 1-4.750 0 2.375 2.375 0 0 1-4.750 0 2.375 2.375 0 0 1-4.750 0z"),
            line("M12 14.500v6a2 2 0 0 1-4 0")]


# ============================================================================ candles, matches and lighters

def flame(cx, top, bot, w=1.7):
    """Small teardrop flame as a path string."""
    h = bot - top
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + w * .3)} {fmt(top + h * .28)} {fmt(cx + w)} {fmt(bot - w * 2.2)} {fmt(cx + w)} {fmt(bot - w)}"
            f"A{fmt(w)} {fmt(w)} 0 0 1 {fmt(cx - w)} {fmt(bot - w)}"
            f"C{fmt(cx - w)} {fmt(bot - w * 2.2)} {fmt(cx - w * .3)} {fmt(top + h * .28)} {fmt(cx)} {fmt(top)}Z")


@icon("taper-candle", CAT, "Tall thin candle tapering to the top with a flame, standing in a simple holder.",
      tags=["dinner candle", "candlestick", "romantic", "dining table", "formal", "elegant"])
def _(S):
    return [solid(flame(12, 2, 6)),
            shell(rect(10, 7.500, 4, 9.500)),
            shell(poly([(7, 17), (17, 17), (15.500, 21.500), (8.500, 21.500)], closed=True, r=S.r * 0.6))]


@icon("jar-candle", CAT, "Candle poured into a glass jar with a flame and a lid set down beside it.",
      tags=["scented candle", "soy candle", "glass candle", "aromatherapy", "home fragrance", "cozy"])
def _(S):
    return [solid(flame(8.500, 2.500, 7.500)),
            shell(rect(3, 10, 11, 11, S.R)),
            detail("M3.500 14h10"),
            shell(rect(16.500, 17, 5, 4, L(S, 0.5, 1.500)))]


@icon("floating-candle", CAT, "Flat round candle floating on a wavy water line with a small flame.",
      tags=["water candle", "pool candle", "wedding centerpiece", "ritual", "diya", "tea light"])
def _(S):
    return [solid(flame(12, 2.500, 8.500)),
            shell(rect(6.500, 10.500, 11, 4, L(S, 0.5, 2))),
            line("M2 18.500q2.500-2.500 5 0t5 0t5 0t5 0")]


@icon("spiral-candle", CAT, "Tall candle with a twisted spiral body and a flame on top.",
      tags=["twisted candle", "decorative candle", "taper", "holiday candle", "swirl", "home decor"])
def _(S):
    return [solid(flame(12, 2, 6.500)),
            shell(rect(8, 8, 8, 13, L(S, 0.5, 2))),
            detail("M8 13.500l8-3.500"), detail("M8 19l8-3.500")]


@icon("melting-candle", CAT, "Short candle with wax drips running down its sides and a pool of wax at the base.",
      tags=["dripping wax", "burning candle", "gothic", "melted", "wax", "halloween"])
def _(S):
    return [solid(flame(12, 2, 6.500)),
            shell(rect(7.500, 8.500, 9, 10, L(S, 0.5, 1.500))),
            detail("M10.500 9v4.500"), detail("M14 9v6.500"),
            shell(rect(4, 17.500, 16, 4, L(S, 1, 2)))]


@icon("birthday-candle", CAT, "Thin striped candle with a flame standing in a small holder.",
      tags=["cake candle", "party", "celebration", "wish", "age", "anniversary"])
def _(S):
    return [solid(flame(12, 2, 6.500)),
            shell(rect(9.500, 7.500, 5, 10.500)),
            detail("M9.500 12l5-2.500"), detail("M9.500 17l5-2.500"),
            shell(poly([(8, 18), (16, 18), (15, 21.500), (9, 21.500)], closed=True, r=S.r * 0.5))]


@icon("chamberstick", CAT, "Short candle in a saucer-shaped holder with a finger loop handle.",
      tags=["candle holder", "bedtime candle", "victorian", "saucer", "antique", "handheld"])
def _(S):
    return [solid(flame(9.500, 2, 6.500)),
            shell(rect(7.500, 8, 4, 8)),
            shell(poly([(3, 16.500), (16, 16.500), (14.500, 21), (4.500, 21)], closed=True, r=S.r * 0.6)),
            line("M16 17.500h3a2 2 0 0 1 0 4h-3.500")]


@icon("multi-wick-candle", CAT, "Wide candle in a bowl with three flames across the top.",
      tags=["three wick", "large candle", "scented candle", "spa", "bowl candle", "home fragrance"])
def _(S):
    return [solid(flame(6.500, 2.500, 8)), solid(flame(12, 2.500, 8)), solid(flame(17.500, 2.500, 8)),
            shell(L(S, "M2.500 11h19v3l-3.500 7h-12l-3.500-7z", "M2.500 11h19v2.500a7.500 7.500 0 0 1-7.500 7.500h-4A7.500 7.500 0 0 1 2.500 13.500z"))]


@icon("extinguished-candle", CAT, "Candle with no flame and a curl of smoke rising from the blown-out wick.",
      tags=["blown out", "put out", "snuffed", "smoke", "end", "night"])
def _(S):
    return [line("M12 7.500c-2.700-1.500 2.700-3 0-5.500"),
            shell(rect(8.500, 10, 7, 11.500, L(S, 0.5, 2))),
            mark(circle(12, 13.5, 1.1))]


@icon("wax-melt", CAT, "Snap-apart tray of scented wax cubes with one cube broken off.",
      tags=["wax tart", "scented wax", "wax warmer", "fragrance", "home scent", "cubes"])
def _(S):
    return [shell(rect(2.500, 4, 14, 10, L(S, 0.5, 2))),
            detail("M7.200 4.500v9"), detail("M11.800 4.500v9"), detail("M3 9h13"),
            shell(rect(14.500, 15.500, 6, 5.500, L(S, 0.5, 1.500)))]


@icon("candle-sconce", CAT, "Wall bracket with a back plate holding a single arm, candle and flame.",
      tags=["wall candle holder", "wall mount", "castle", "medieval", "hallway", "rustic lighting"])
def _(S):
    return [solid(flame(16, 2, 6.500)),
            shell(rect(3, 4.500, 4, 15.500, L(S, 0.5, 2))),
            line("M7 17.500h6"),
            shell(rect(14, 8, 4, 7.500)),
            shell(poly([(12.500, 16), (19.500, 16), (18.500, 19.500), (13.500, 19.500)], closed=True, r=S.r * 0.5))]


@icon("bottle-candle", CAT, "Candle standing in the neck of a round bottle.",
      tags=["wine bottle candle", "bistro", "romantic", "restaurant table", "recycled glass", "dripping wax"])
def _(S):
    return [solid(flame(12, 2, 5.500, 1.5)),
            solid(rect(10.500, 6, 3, 3.500)),
            shell("M10 12.200V9.500h4v2.700A5 5 0 1 1 10 12.200z")]


@icon("matchstick", CAT, "Single wooden match with a rounded head.",
      tags=["match", "light", "ignite", "strike", "fire starter", "safety match"])
def _(S):
    return [line("M5.500 20.500L15.500 10.500"),
            solid(circle(17.800, 8.200, 3))]


@icon("matchbook", CAT, "Folded card matchbook showing a row of paper matches above the striking strip.",
      tags=["matches", "restaurant matches", "souvenir", "strike", "fire", "light"])
def _(S):
    return [line("M8 9.500V6.500"), line("M12 9.500V6.500"), line("M16 9.500V6.500"),
            mark(circle(8, 5, 1.400)), mark(circle(12, 5, 1.400)), mark(circle(16, 5, 1.400)),
            shell(rect(4, 10, 16, 11, S.R)),
            detail("M4.500 14h15"),
            mark(rect(6.500, 16.500, 11, 2.500))]


@icon("lighter", CAT, "Pocket lighter with a rectangular body, a thumb wheel and a flame on top.",
      tags=["cigarette lighter", "zippo style", "flint", "ignite", "smoker", "camping"])
def _(S):
    return [solid(flame(11.500, 2, 6.500, 1.500)),
            shell(rect(7.500, 8, 8, 4, L(S, 0.5, 1.500))),
            shell(rect(6.500, 12, 10, 9.500, L(S, 1, 2))),
            detail("M7 16.500h9"),
            solid(circle(19.300, 10, 1.800))]


@icon("firelighter", CAT, "Small fire-starter cube with a flame on one corner.",
      tags=["fire starter", "kindling block", "barbecue", "wood stove", "camping", "tinder"])
def _(S):
    return [solid(flame(18, 3, 13, 2.800)),
            shell(rect(2.500, 10, 13, 11.500, L(S, 1, 3))),
            detail("M3 15.500h12")]


# ============================================================================ fire tools and firewood

@icon("kindling", CAT, "Small pile of thin split sticks crossed over each other.",
      tags=["sticks", "twigs", "fire starter", "campfire", "tinder", "woodpile"])
def _(S):
    return [line("M3 19L21 14"), line("M3 13.500L21 19.500"), line("M6 5L19 16"), line("M12 3.500L21.500 10.500")]


@icon("fire-poker", CAT, "Long metal rod with a hooked point and a looped handle.",
      tags=["fireplace tool", "hearth", "stoke", "iron rod", "wood stove", "fire iron"])
def _(S):
    return [shell(circle(5.500, 18.500, 2.800)),
            line("M7.500 16.500L17.500 6.500a2.500 2.500 0 0 1 3.500 3.500")]


@icon("fire-tongs", CAT, "Long hinged tongs with curved gripping ends holding a small log.",
      tags=["fireplace tool", "log grabber", "hearth", "campfire", "pincers", "wood stove"])
def _(S):
    return [line("M7.500 3L16.500 16.500q.3 1.600-1.500 2.500"), line("M16.500 3L7.500 16.500q-.3 1.600 1.500 2.500"),
            mark(circle(12, 9.750, 1.200)),
            shell(circle(12, 19, 1.800))]


@icon("fire-grate", CAT, "Iron basket grate on short legs holding two logs.",
      tags=["fireplace grate", "log holder", "hearth", "andiron", "fire basket", "wood stove"])
def _(S):
    return [shell(rect(6, 2.500, 12, 4.500, 2.200)), shell(rect(4, 8.500, 16, 4.500, 2.200)),
            shell(rect(3, 14.500, 18, 4.500, L(S, 0.5, 1.500))),
            detail("M8 15v3.500"), detail("M12 15v3.500"), detail("M16 15v3.500"),
            line("M5 19v3"), line("M19 19v3")]


@icon("firewood-bundle", CAT, "Several split logs stacked and tied together with a strap.",
      tags=["logs", "campfire wood", "wood pile", "fuel", "fireplace", "stacked wood"])
def _(S):
    pts = [(7.500, 16), (16.500, 16), (12, 8.500)]
    return [shell(circle(x, y, 3.300) if S.name == "rounded" else poly(regular(x, y, 3.600, 6), closed=True)) for x, y in pts] + \
           [mark(circle(x, y, 0.9)) for x, y in pts]


@icon("lantern-battery", CAT, "Square block battery with two round terminals on top.",
      tags=["6v battery", "spring terminal", "dry cell", "power", "camping lantern", "block battery"])
def _(S):
    return [line("M8.500 9V6"), line("M15.500 9V6"),
            solid(circle(8.500, 4.300, 1.800)), solid(circle(15.500, 4.300, 1.800)),
            shell(rect(4.500, 9, 15, 12, L(S, 0.5, 2))),
            detail("M5 13.500h14")]


@icon("battery-organizer", CAT, "Wall case with rows of cylindrical batteries in slots.",
      tags=["battery storage", "battery case", "tester", "drawer organizer", "aa aaa", "spares"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)),
            detail("M3.500 12h17"),
            mark(rect(6, 5.300, 3, 4.600, 0.6)), mark(rect(10.500, 5.300, 3, 4.600, 0.6)), mark(rect(15, 5.300, 3, 4.600, 0.6)),
            mark(rect(6, 14.300, 3, 4.600, 0.6)), mark(rect(10.500, 14.300, 3, 4.600, 0.6)), mark(rect(15, 14.300, 3, 4.600, 0.6))]


@icon("replacing-battery", CAT, "Cylindrical battery sliding into an open battery compartment, with an arrow showing the direction.",
      tags=["change batteries", "insert battery", "swap", "remote control", "power", "install"])
def _(S):
    return [line("M12 3.500H3.500v12H12"),
            shell(rect(8, 6.500, 12, 6.500, L(S, 0.5, 3))),
            solid(rect(20, 8.300, 1.800, 3)),
            line("M20 19.500H9.500"), line("M12.500 16.500l-3 3 3 3")]


@icon("leaking-battery", CAT, "Cylindrical battery with fluid running from the terminal and dripping below.",
      tags=["corroded", "acid", "damaged", "hazard", "old battery", "spill"])
def _(S):
    return [shell(rect(3, 9, 10.500, 12, L(S, 0.5, 2))),
            solid(rect(6, 5.800, 4.500, 3)),
            line("M11 7h5a2 2 0 0 1 2 2v4.500"),
            solid(flame(18, 14.500, 21, 1.900))]


@icon("swollen-battery", CAT, "Flat rectangular battery pack bulging outward in the middle.",
      tags=["bloated", "puffed", "lithium", "spudger", "hazard", "phone battery"])
def _(S):
    return [shell("M2.500 9C7 4 15 4 19.500 9v6c-4.500 5-12.500 5-17 0z"),
            solid(rect(19.500, 10.500, 2, 3)),
            detail("M8 12h6")]


@icon("globe-bulb", CAT, "Large spherical light bulb on a short screw base.",
      tags=["vanity bulb", "round bulb", "g25", "decorative lighting", "edison", "lamp"])
def _(S):
    return [shell("M9 16.900A7.500 7.500 0 1 1 15 16.900z"),
            detail("M9.500 13.500l2.500-3.500 2.500 3.500"),
            shell(rect(9, 18.500, 6, 3, L(S, 0.3, 1)))]


@icon("corn-led-bulb", CAT, "Tall cylindrical bulb covered in rows of small square LED chips on a screw base.",
      tags=["led lamp", "high output", "garage light", "e27", "retrofit", "energy saving"])
def _(S):
    return [shell("M7 16V7.500a5 5 0 0 1 10 0V16z"),
            mark(rect(9.500, 6, 2, 2)), mark(rect(12.500, 6, 2, 2)),
            mark(rect(9.500, 9.500, 2, 2)), mark(rect(12.500, 9.500, 2, 2)),
            mark(rect(9.500, 13, 2, 2)), mark(rect(12.500, 13, 2, 2)),
            shell(rect(8.500, 17.500, 7, 4, L(S, 0.3, 1)))]


@icon("circular-fluorescent-tube", CAT, "Ring-shaped fluorescent tube with a small plug connector at the top.",
      tags=["circline", "ring light", "ceiling lamp", "t9", "lighting", "old lamp"])
def _(S):
    return [line(circle(12, 13, 7.500)),
            shell(rect(9.500, 2, 5, 3.500, L(S, 0.3, 1)))]


@icon("broken-bulb", CAT, "Light bulb with a jagged crack across the glass.",
      tags=["burnt out", "shattered", "dead bulb", "blown", "cracked glass", "replace"])
def _(S):
    return [shell("M9 16.900A7.500 7.500 0 1 1 15 16.900z"),
            detail("M4 9l4 3 2.500-4 2.500 5 2.500-4.500 4 3"),
            shell(rect(9, 18.500, 6, 3, L(S, 0.3, 1)))]


@icon("bulb-changer", CAT, "Long pole with a cup-shaped grip holding a light bulb at the top.",
      tags=["light bulb puller", "extension pole", "high ceiling", "replace bulb", "reach", "maintenance"])
def _(S):
    return [shell(circle(12, 6.500, 3.500)),
            shell(poly([(8.500, 11.500), (15.500, 11.500), (14, 14.500), (10, 14.500)], closed=True, r=S.r * 0.4)),
            line("M12 14.500V21.500"),
            solid(rect(10.700, 17, 2.600, 4.500, 1))]


# ============================================================================ lamps, switches and adhesives

@icon("pendant-bulb", CAT, "Bare bulb hanging from a long cord with a small ceiling canopy.",
      tags=["hanging lamp", "edison bulb", "ceiling light", "cord light", "industrial", "cafe lighting"])
def _(S):
    return [shell(rect(8, 2, 8, 2.500, L(S, 0.3, 1))),
            line("M12 4.500V10"),
            shell(rect(10.300, 10.500, 3.400, 3)),
            shell(circle(12, 17.500, 4.200))]


def _tube_ring():
    return path_to_d(ST(arc(12, 12, 6.500, 40, 330), 5, "butt", "round"))


@icon("rope-light", CAT, "Flexible clear tube with tiny bulbs inside, coiled in a loose loop.",
      tags=["led strip", "string light", "outdoor lighting", "tube light", "decoration", "flexible light"])
def _(S):
    dots = [Part("dot", circle(12 + 6.5 * math.cos(math.radians(a)), 12 + 6.5 * math.sin(math.radians(a)), 1.100))
            for a in (75, 125, 175, 225, 275)]
    return [shell(_tube_ring())] + dots


@icon("puck-light", CAT, "Flat round light mounted under a shelf with a cone of light below.",
      tags=["under cabinet light", "spotlight", "led puck", "closet light", "shelf lighting", "downlight"])
def _(S):
    return [line("M3 3.500h18"),
            shell(rect(7.500, 5.500, 9, 3.500, L(S, 0.5, 1.700))),
            line("M9.500 12L6 19.500"), line("M12 12v8"), line("M14.500 12L18 19.500")]


@icon("cable-clip", CAT, "Small clip stuck to a desk edge holding three cables in slots.",
      tags=["cable organizer", "cord holder", "desk cable management", "wire clip", "tidy cables", "adhesive clip"])
def _(S):
    return [line("M2.500 3.500h19"),
            shell(rect(4, 6, 16, 9, L(S, 1, 3))),
            mark(circle(8, 10.500, 1.600)), mark(circle(12, 10.500, 1.600)), mark(circle(16, 10.500, 1.600)),
            line("M8 15v6"), line("M12 15v6"), line("M16 15v6")]


@icon("motion-sensor-light", CAT, "Wall light with a dome sensor below and radiating detection arcs.",
      tags=["security light", "pir sensor", "floodlight", "outdoor light", "detector", "automatic light"])
def _(S):
    return [shell(rect(4, 2.500, 16, 3.500, L(S, 0.5, 1.700))),
            shell("M8.500 6a3.500 3.500 0 0 0 7 0z"),
            line(arc(12, 6, 8.500, 50, 130)), line(arc(12, 6, 13.500, 50, 130))]


@icon("emergency-radio", CAT, "Compact radio with a hand crank on the side, a small solar panel and an antenna.",
      tags=["hand crank radio", "weather radio", "disaster kit", "survival", "solar radio", "power outage"])
def _(S):
    return [line("M6.500 8.500L4 2.500"),
            shell(rect(3, 8.500, 15, 12, L(S, 1, 2.500))),
            detail(rect(5.500, 11, 6, 3.500, 0.3)),
            mark(circle(14.800, 12.500, 1.300)),
            detail("M6 17.500h9"),
            line("M18 14h2.500v4"), solid(rect(19.200, 17.500, 2.600, 3.500, 0.6))]


@icon("inline-switch", CAT, "Section of cord with a small oval switch in the middle.",
      tags=["cord switch", "lamp switch", "rocker", "power cable", "wire", "on off"])
def _(S):
    return [line("M2 15c2.500 0 3-3 5-3"), line("M17 12c2 0 2.500 3 5 3"),
            shell(rect(7, 8, 10, 8, 4)),
            mark(rect(9.500, 10.700, 5, 2.600, 1.300))]


@icon("festoon-lights", CAT, "Row of round bulbs hanging in a sagging curve from a cable between two posts.",
      tags=["string lights", "party lights", "garden lights", "patio", "outdoor lighting", "bunting lights"])
def _(S):
    return [line("M3 3v18"), line("M21 3v18"),
            line("M3 5Q12 13 21 5"),
            line("M7.500 7.300v2"), line("M12 9v2"), line("M16.500 7.300v2"),
            solid(circle(7.500, 11, 2)), solid(circle(12, 13, 2)), solid(circle(16.500, 11, 2))]


@icon("sticky-tack", CAT, "Blob of reusable adhesive putty with a poster corner stuck to it.",
      tags=["blu tack", "poster putty", "reusable adhesive", "wall hanging", "craft", "removable"])
def _(S):
    return [line("M9 9V3.500h12.500V16h-5.500"),
            shell("M3.500 15.500c0-2.800 2.200-4.500 4.800-4.200 2.800.3 4.200 2 4.200 4.200s-1.700 5-4.800 5-4.200-2.200-4.200-5z")]


@icon("glue-dots", CAT, "Strip of backing paper with a row of round adhesive dots.",
      tags=["adhesive dots", "craft glue", "double sided", "sticky dots", "scrapbook", "paper strip"])
def _(S):
    return [shell(rect(2.500, 7.500, 19, 9, L(S, 1, 3))),
            mark(circle(7.500, 12, 2.100)), mark(circle(12, 12, 2.100)), mark(circle(16.500, 12, 2.100))]
