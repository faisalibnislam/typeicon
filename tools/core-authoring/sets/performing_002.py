"""TypeIcon Core: performing arts, batch 002 (stagecraft, puppetry, costume, circus and dance)."""
from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401

CAT = "performing"


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle (knocked out of a Filled shell)."""
    return Part("dot", rect(x, y, w, h, rx))


# ---------------------------------------------------------------------------- chunk 1

@icon("soliloquy-skull", CAT, "A skull held on an open palm with a small head in profile looking at it",
      tags=["hamlet", "skull", "soliloquy", "shakespeare", "monologue", "tragedy", "theatre"])
def _(S):
    return [shell("M12.5 15.5V13.9A5.5 5.5 0 1 1 17.5 13.9V15.5Z"),
            dot(13, 9.5, 1.25), dot(17, 9.5, 1.25),
            line("M9 19Q15 22 21 18.5"), line("M9 19L4 21"),
            dot(5.5, 7, 2.25), line("M5.5 11V16")]


@icon("elizabethan-playhouse", CAT, "Round timber playhouse with a ring roof and a small flag on top",
      tags=["globe", "playhouse", "shakespeare", "theatre", "building", "elizabethan", "open air"])
def _(S):
    return [shell(poly([(3, 10), (6, 6), (18, 6), (21, 10)], closed=True, r=S.r)),
            shell(rect(5, 10, 14, 11, min(S.R, 2))),
            line("M12 6V2.5"), solid(poly([(12, 2.5), (16, 3.75), (12, 5)], closed=True)),
            detail("M10 21V17.5A2 2 0 0 1 14 17.5V21")]


@icon("noh-stage", CAT, "Square wooden stage under a temple roof on pillars with a pine on the back wall",
      tags=["noh", "japanese", "theatre", "stage", "roof", "pine", "traditional"])
def _(S):
    return [shell(poly([(2, 9), (6, 4), (18, 4), (22, 9)], closed=True, r=S.r)),
            line("M5 9V18"), line("M19 9V18"),
            shell(rect(3, 18, 18, 3, min(S.R, 1.5))),
            detail(poly([(12, 9), (9, 13.5), (15, 13.5)], closed=True)), line("M12 13.5V16")]


@icon("kamishibai", CAT, "Small box theater with open doors on the back of a bicycle",
      tags=["kamishibai", "paper theatre", "storyteller", "japanese", "bicycle", "picture cards", "street"])
def _(S):
    return [shell(rect(10, 3, 8, 10, min(S.R, 1.5))), dot(14, 8, 1.5),
            line("M10 4L6 5.5V11L10 13"), line("M18 4L22 5.5V11L18 13"),
            shell(circle(6, 19, 3)), shell(circle(18, 19, 3)),
            line("M6 19L9 14H18"), line("M9 14L8 11H5")]


@icon("stagehand", CAT, "Figure carrying a tall flat of scenery on one shoulder",
      tags=["stagehand", "crew", "scenery", "flat", "backstage", "set", "carry"])
def _(S):
    return [dot(8, 5.5, 2.25), line("M8 9V15"), line("M8 15L5.5 21"), line("M8 15L10.5 21"),
            line("M8 10.5L14 8"),
            shell(rect(14, 3, 7, 16, min(S.R, 1.5))), detail(poly([(17.5, 14), (17.5, 9)]))]


@icon("playwright", CAT, "Figure at a desk writing with a quill",
      tags=["playwright", "writer", "author", "script", "quill", "dramatist", "writing"])
def _(S):
    return [dot(7, 6.5, 2.25), line("M7 10V17"), line("M7 12L12 14"),
            line("M3 17H21"), line("M5 17V21"), line("M19 17V21"),
            shell(rect(13, 13, 7, 3, 0)),
            line("M12 14L18 6"), solid(poly([(18, 6), (21.5, 3), (20, 8)], closed=True))]


@icon("choreographer", CAT, "Figure clapping out the count beside a small dancer and footstep marks",
      tags=["choreographer", "dance director", "counting", "clap", "rehearsal", "dance", "coach"])
def _(S):
    return [dot(7, 9, 2.25), line("M7 12.5V17"), line("M7 17L4.5 21.5"), line("M7 17L9.5 21.5"),
            line("M7 13L3.5 9L7 4.5L10.5 9L7 13"),
            dot(18, 7, 1.75), line("M18 9.5V14"), line("M18 14L15.5 17.5"), line("M18 14L21 16"),
            line("M18 10.5L21 8.5"), line("M18 10.5L15.5 12.5"),
            dot(14, 20.5, 1), dot(18, 20, 1), dot(21, 20.5, 1)]


@icon("stage-fright", CAT, "Small figure with knocking knees alone in a spotlight cone with sweat drops",
      tags=["stage fright", "nervous", "anxiety", "performance anxiety", "spotlight", "shaking", "scared"])
def _(S):
    return [shell(poly([(9, 2), (15, 2), (21, 21), (3, 21)], closed=True, r=S.r * 0.5)),
            dot(12, 11, 2), line("M12 13.5V17"),
            line("M12 17L10.5 19L11 21"), line("M12 17L13.5 19L13 21"),
            line("M8.5 14L10 13.5"), line("M15.5 14L14 13.5")]


@icon("audition", CAT, "Performer holding a number card facing two judges seated at a table",
      tags=["audition", "casting", "tryout", "judges", "number card", "talent show", "interview"])
def _(S):
    return [dot(5.5, 6, 2.25), line("M5.5 9.5V15"), line("M5.5 15L3.5 21"), line("M5.5 15L7.5 21"),
            line("M5.5 11L9 12"), shell(rect(9, 9, 4, 4)),
            dot(16.5, 9, 1.75), dot(20.5, 9, 1.75),
            line("M14.5 15H22"), line("M15.5 15V21"), line("M21 15V21")]


@icon("actor-headshot", CAT, "Portrait photo of a head and shoulders with a resume sheet behind it",
      tags=["headshot", "portrait", "actor", "casting", "resume", "photo", "profile picture", "cv"])
def _(S):
    return [shell(rect(3, 7, 13, 14, min(S.R, 2))), dot(9.5, 12, 2.25),
            line("M6 18C6 15.5 13 15.5 13 18"),
            line("M8 7V3H21V16H16")]


@icon("table-read", CAT, "Table seen from above with four people holding scripts around it",
      tags=["table read", "script reading", "cast", "read through", "rehearsal", "meeting", "script"])
def _(S):
    return [shell(rect(3, 7.5, 18, 9, S.R)),
            dot(7.5, 4, 2), dot(16.5, 4, 2), dot(7.5, 20, 2), dot(16.5, 20, 2),
            sq(5.5, 9.5, 4, 2), sq(14.5, 9.5, 4, 2), sq(5.5, 12.5, 4, 2), sq(14.5, 12.5, 4, 2)]


@icon("thrust-stage", CAT, "Top view of a stage jutting out into curved seating on three sides",
      tags=["thrust stage", "theatre in the round", "seating", "audience", "stage layout", "auditorium", "plan"])
def _(S):
    return [shell(rect(9, 3, 6, 6, min(S.R, 1))),
            line("M5 4V9A7 7 0 0 0 19 9V4"),
            line(arc(12, 9, 11, 25, 155))]


@icon("pageant-wagon", CAT, "Medieval wheeled wagon carrying a small curtained stage with a figure",
      tags=["pageant wagon", "medieval", "mystery play", "cart", "travelling theatre", "wagon", "stage"])
def _(S):
    return [shell(rect(3, 13, 18, 3, 0)),
            line("M5 13V5H19V13"),
            line("M5 5Q9 8 9 13"), line("M19 5Q15 8 15 13"),
            dot(12, 8, 1.75), line("M12 10V13"),
            shell(circle(7, 19.5, 2)), shell(circle(17, 19.5, 2))]


@icon("periaktos", CAT, "Tall triangular prism of scenery turning on a pivot base",
      tags=["periaktos", "revolving scenery", "greek theatre", "scene change", "prism", "set piece", "ancient"])
def _(S):
    return [shell(poly([(4, 4), (12, 3), (12, 16), (4, 15)], closed=True, r=S.r * 0.4)),
            shell(poly([(12, 3), (20, 5), (20, 17), (12, 16)], closed=True, r=S.r * 0.4)),
            detail(poly([(6, 13), (8, 9), (10, 13)])), dot(16, 11, 1.5),
            line("M12 16V19"), shell(rect(7, 19, 10, 2.5, 0.5))]


@icon("prop-table", CAT, "Table covered in paper with taped outlines of a cup and a dagger",
      tags=["prop table", "props", "backstage", "tape outline", "stage management", "cup", "dagger"])
def _(S):
    return [shell(rect(3, 4, 18, 16, min(S.R, 3))),
            detail(circle(9, 9.5, 2.25)),
            detail("M14 17L18 8"), detail("M14.5 11.5L19 13.5")]


# ---------------------------------------------------------------------------- chunk 2
from dsl import pt_on  # noqa: E402
from geometry import path_to_d  # noqa: E402


@icon("stage-blocking", CAT, "Stage floor plan with X marks and a dashed arrow showing an actor's path",
      tags=["blocking", "stage plan", "floor plan", "movement", "rehearsal", "marks", "direction"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)),
            detail("M5.5 7.5L8.5 10.5M8.5 7.5L5.5 10.5"),
            detail("M11 9H16V12.5"), detail("M14.5 11L16 12.5L17.5 11"),
            detail("M15.5 15.5L18.5 18.5M18.5 15.5L15.5 18.5")]


@icon("coconut-hoof-shells", CAT, "Two coconut half shells clapped together with hoofprint marks below",
      tags=["coconut", "horse sound", "foley", "clip clop", "sound effect", "hooves", "shells"])
def _(S):
    return [shell("M3 13A4 4 0 0 1 11 13Z"), shell("M13 13A4 4 0 0 1 21 13Z"),
            line("M12 4V6"), line("M7 3.5L8 5"), line("M17 3.5L16 5"),
            line(arc(8, 20, 2, 180, 360)), line(arc(16, 20, 2, 180, 360))]


@icon("stage-barricade", CAT, "Row of crowd barrier panels in front of a raised stage edge",
      tags=["barricade", "crowd barrier", "front of stage", "concert", "security", "fence", "festival"])
def _(S):
    return [shell(rect(2, 3, 20, 4, 0)),
            shell(rect(2, 11, 20, 9, S.R)),
            detail("M7 11V20"), detail("M12 11V20"), detail("M17 11V20")]


@icon("stage-dive", CAT, "Figure lying flat on the raised hands of a crowd",
      tags=["stage dive", "crowd surfing", "concert", "mosh", "rock", "gig", "fans"])
def _(S):
    return [dot(5, 7.5, 2), line("M9 8H20"), line("M20 8L21 12"), line("M10 8L8 4.5"),
            line("M6 21V14.5"), dot(6, 13, 1.5), line("M12 21V14.5"), dot(12, 13, 1.5),
            line("M18 21V14.5"), dot(18, 13, 1.5)]


@icon("safety-curtain", CAT, "Iron safety curtain half lowered across a stage opening with warning stripes",
      tags=["safety curtain", "fire curtain", "iron curtain", "theatre safety", "proscenium", "stage", "fireproof"])
def _(S):
    return [line("M3 21V3H21V21"),
            shell(rect(7, 6, 10, 7, 0)), detail("M7 9.5H17"),
            Part("dot", poly([(7, 17.5), (9.5, 15), (12, 15), (9.5, 17.5)], closed=True)),
            Part("dot", poly([(12, 17.5), (14.5, 15), (17, 15), (14.5, 17.5)], closed=True))]


@icon("green-room", CAT, "Backstage lounge with a sofa and a round mirror beside a door marked with a star",
      tags=["green room", "backstage", "lounge", "dressing room", "waiting room", "performers", "star"])
def _(S):
    return [shell(rect(15, 3, 6, 18, min(S.R, 1.5))), solid(poly(regular(18, 9, 1.8, 5), closed=True)),
            shell(circle(7.5, 6.5, 3)),
            shell(rect(3, 13, 10, 5, min(S.R, 2))), line("M4.5 18V21"), line("M11.5 18V21")]


@icon("bunraku-puppet", CAT, "Large kimono puppet held up by a hooded operator standing behind it",
      tags=["bunraku", "japanese puppet", "puppeteer", "puppet theatre", "kimono", "operator", "doll"])
def _(S):
    return [dot(6, 5.5, 2.5), line("M6 9V21"), line("M6 11L12 12.5"),
            shell(circle(17, 7.5, 2.25)),
            shell(poly([(17, 10.5), (21.5, 21), (12.5, 21)], closed=True, r=S.r * 0.5)),
            detail("M14.5 15.5H19.5")]


@icon("rod-puppet", CAT, "Puppet with thin rods on both hands and a central rod held from below",
      tags=["rod puppet", "puppet", "puppeteer", "marionette", "rods", "puppetry", "glove"])
def _(S):
    return [shell(circle(12, 5.5, 2.5)), shell(rect(9.5, 9, 5, 6, min(S.R, 1.5))),
            line("M9.5 10.5L6 13"), line("M14.5 10.5L18 13"),
            line("M6 13L3.5 5"), line("M18 13L20.5 5"),
            line("M12 15V19"), shell(rect(9.5, 19, 5, 3, 0.5))]


@icon("water-puppet", CAT, "Small puppet rising from water ripples in front of a pavilion with a curtain",
      tags=["water puppet", "vietnamese", "puppet show", "pavilion", "ripples", "folk theatre", "puppetry"])
def _(S):
    return [shell(poly([(3, 9.5), (7.5, 4), (12, 9.5)], closed=True, r=S.r * 0.5)),
            line("M4.5 9.5V14"), line("M10.5 9.5V14"), line("M7.5 9.5V14"),
            dot(17.5, 9, 2), line("M17.5 11.5V16"), line("M17.5 13L15 10.5"), line("M17.5 13L20 10.5"),
            line("M3 17.5Q5 16 7 17.5T11 17.5T15 17.5T19 17.5T21 17.5"), line("M6 20.5Q7.5 19.5 9 20.5T12 20.5T15 20.5")]


@icon("parade-puppet", CAT, "Giant puppet with a big head and long robe carried above tiny people",
      tags=["giant puppet", "parade", "procession", "street theatre", "carnival", "festival", "puppetry"])
def _(S):
    return [shell(circle(12, 6.5, 3.75)),
            shell(poly([(12, 10.5), (19, 17.5), (5, 17.5)], closed=True, r=S.r * 0.5)),
            dot(6, 20.5, 1.25), dot(12, 20.5, 1.25), dot(18, 20.5, 1.25)]


@icon("toy-theater", CAT, "Miniature paper stage with a frame, a painted backdrop and a cardboard figure on a slide",
      tags=["toy theatre", "paper theatre", "miniature", "model stage", "cardboard", "proscenium", "puppet show"])
def _(S):
    return [line("M3 21V5M21 21V5"), shell(rect(3, 3, 18, 4, 0)),
            detail(poly([(6, 17), (9.5, 12.5), (13, 17)])),
            dot(17, 12, 1.5), line("M17 14V19"), line("M5 21H19")]


@icon("half-face-mask", CAT, "Face with a half mask over one side that has an eye hole",
      tags=["half mask", "masquerade", "phantom", "opera mask", "costume", "venetian", "eye mask"])
def _(S):
    eye = (poly([(6.5, 10), (8, 8.5), (9.5, 10), (8, 11.5)], closed=True) if S.name == "line" else circle(8, 10, 1.5))
    return [shell("M12 3A9 9 0 0 0 12 21Z"), line("M12 3A9 9 0 0 1 12 21"),
            Part("dot", eye), dot(16, 10, 1.25), line("M14.5 16H18")]


@icon("animal-onesie", CAT, "One-piece hooded animal costume with ears on the hood and a tail",
      tags=["onesie", "animal costume", "kigurumi", "pyjamas", "mascot", "dress up", "costume"])
def _(S):
    return [shell(circle(7.5, 4, 1.8)), shell(circle(16.5, 4, 1.8)),
            shell(circle(12, 7.5, 4.5)), dot(10.3, 7.5, 1), dot(13.7, 7.5, 1),
            shell(rect(8, 13, 8, 6, min(S.R, 2))),
            line("M8 14L4.5 17.5"), line("M16 14L19.5 17.5"),
            line("M10 19V21.5"), line("M14 19V21.5"), line("M16 18Q21 18 21 13")]


@icon("doublet", CAT, "Fitted jacket with puffed sleeves, a collar and a row of buttons",
      tags=["doublet", "renaissance", "jacket", "tudor", "period costume", "puffed sleeves", "shakespeare"])
def _(S):
    return [shell("M8.5 4C4 4 2 7 2.5 11C3 13 5 14 7 13.5L7.5 21H16.5L17 13.5C19 14 21 13 21.5 11C22 7 20 4 15.5 4Z"),
            detail("M9.5 4L12 7.5L14.5 4"), dot(12, 11, 1), dot(12, 14.5, 1), dot(12, 18, 1)]


@icon("face-changing-opera", CAT, "Painted face split into two patterns beside a fan sweeping across",
      tags=["face changing", "sichuan opera", "bian lian", "chinese opera", "fan", "mask", "transformation"])
def _(S):
    A = pt_on(21, 21, 10, 205)
    B = pt_on(21, 21, 10, 245)
    fan = f"M21 21L{A[0]:.2f} {A[1]:.2f}A10 10 0 0 1 {B[0]:.2f} {B[1]:.2f}Z"
    return [shell(circle(8.5, 8.5, 6.5)), detail("M8.5 2V15"),
            dot(6, 7.5, 1), dot(11, 7.5, 1), line("M10.5 12H12.5"),
            shell(fan)]


# ---------------------------------------------------------------------------- chunk 3

@icon("greek-chorus", CAT, "Row of three identical robed figures standing together",
      tags=["greek chorus", "chorus", "ancient theatre", "robes", "choir", "tragedy", "ensemble"])
def _(S):
    out = []
    for x in (4.5, 12, 19.5):
        out += [dot(x, 5.5, 2.25),
                shell(poly([(x, 9.5), (x + 2.4, 21), (x - 2.4, 21)], closed=True, r=S.r * 0.4))]
    return out


@icon("living-statue", CAT, "Figure frozen in a pose on a crate with a hat of coins beside it",
      tags=["living statue", "street performer", "busker", "mime", "statue", "coins", "busking"])
def _(S):
    return [dot(9, 4.5, 2.25), line("M9 8V13"), line("M9 9L14 5.5"), line("M9 9L5 11"),
            line("M9 13L7 16"), line("M9 13L11.5 16"),
            shell(rect(4, 16, 10, 5, min(S.R, 1.5))),
            solid(rect(18, 18, 3.5, 2.5, 0.5)), line("M16.5 21H22"),
            dot(18.5, 15, 1), dot(21, 13.5, 1)]


@icon("one-man-band", CAT, "Figure playing a drum, cymbals and guitar all at once",
      tags=["one man band", "busker", "street musician", "drum", "guitar", "cymbals", "solo"])
def _(S):
    return [dot(12, 7, 2.25), line("M8 3Q12 1.5 16 3"),
            line("M12 10.5V16"), line("M12 16L10 21"), line("M12 16L14 21"),
            shell(circle(4.5, 14, 2.5)), line("M12 12L7 13.5"),
            shell(ellipse(18.5, 15, 2.5, 3)), line("M18.5 12L21 6"), line("M12 12L17 13.5")]


@icon("funhouse-mirror", CAT, "Tall wavy-edged mirror showing a stretched, wobbly figure",
      tags=["funhouse mirror", "carnival", "distorted", "fairground", "reflection", "warped", "fun mirror"])
def _(S):
    return [shell("M8 3C10 7 6 11 8 15C9 18 9 20 8 21H16C15 20 15 18 16 15C18 11 14 7 16 3Z"),
            dot(12, 7, 1.5), line("M12 9.5Q14 12 12 14.5T12 19")]


@icon("hall-of-mirrors", CAT, "Mirror frames repeating into the distance around a single figure",
      tags=["hall of mirrors", "infinity mirror", "reflections", "carnival", "mirror maze", "fairground", "repeat"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(rect(7.5, 7.5, 9, 9, min(S.R, 1.5))),
            detail("M4 4L7.5 7.5"), detail("M20 4L16.5 7.5"), detail("M4 20L7.5 16.5"), detail("M20 20L16.5 16.5"),
            dot(12, 12, 1.5)]


@icon("clown-tiny-bike", CAT, "Clown with a bow tie pedalling a tiny bicycle with knees up",
      tags=["clown", "circus", "tiny bike", "bicycle", "comedy", "funny", "unicycle"])
def _(S):
    return [dot(11, 4, 2.25), solid(poly([(8.5, 8), (11, 9.25), (8.5, 10.5)], closed=True)),
            solid(poly([(13.5, 8), (11, 9.25), (13.5, 10.5)], closed=True)),
            line("M11 10V14"), line("M11 14L7.5 11.5"), line("M11 14L13 17.5"), line("M11 11L15 14"),
            shell(circle(6, 19, 2.5)), shell(circle(18, 19, 2.5)), line("M6 19L11 17H18"), line("M18 19L16.5 14.5")]


@icon("trick-roping", CAT, "Figure standing inside a large spinning rope loop with one arm raised",
      tags=["trick roping", "lasso", "rope", "cowboy", "rodeo", "spinning rope", "western show"])
def _(S):
    return [line("M11 2.5C4 2.5 3 21.5 11 21.5S19 2.5 11 2.5"),
            dot(11, 7, 2), line("M11 9.5V15"), line("M11 15L9 20"), line("M11 15L13 20"),
            line("M11 11L16 7"), line("M16 7L21.5 3.5")]


@icon("russian-bar", CAT, "Two carriers holding a flexible bar on their shoulders with an acrobat flipping above",
      tags=["russian bar", "acrobat", "circus", "flip", "acrobatics", "gymnast", "balance"])
def _(S):
    return [dot(4.5, 13.5, 2), line("M4.5 16V21"), dot(19.5, 13.5, 2), line("M19.5 16V21"),
            line("M3 17Q12 10 21 17"), dot(14, 4.5, 1.75), shell(circle(10.5, 7, 2.5)),
            line(arc(10.5, 7, 6, 170, 250))]


@icon("floating-ball-trick", CAT, "Silver ball hovering over a draped cloth with small lines beneath",
      tags=["floating ball", "magic trick", "levitation", "magician", "illusion", "cloth", "levitate"])
def _(S):
    return [shell(circle(12, 6, 3)), detail("M10.2 5.2A2 2 0 0 1 11.5 4"),
            shell("M3.5 13H20.5Q19 17 17.5 21H6.5Q5 17 3.5 13Z"),
            line("M10 10V11M14 10V11") if False else line("M8 8.5V9.5M16 8.5V9.5")]


@icon("contact-juggling", CAT, "Clear ball balanced on the back of an open hand with a roll arc",
      tags=["contact juggling", "juggler", "ball", "crystal ball", "hand", "balance", "circus"])
def _(S):
    return [shell(circle(11, 9.5, 3.5)), shell(rect(3, 15, 17, 5, min(S.R, 2.5))),
            line("M20 17.5H22"), line(arc(11, 9.5, 8, -40, 30))]


@icon("carnival-barker", CAT, "Figure in a straw hat and striped vest calling out through a megaphone",
      tags=["barker", "carnival", "fairground", "showman", "megaphone", "ringmaster", "straw hat"])
def _(S):
    return [dot(9, 7.5, 2.25), line("M5.5 5H12.5"), solid(rect(7.5, 2.5, 3, 2.5)),
            shell(rect(6.5, 11, 5, 6, 0.5)), detail("M9 11V17"),
            line("M9 17V21"), line("M8 17L6 21"),
            shell(poly([(13, 6), (17.5, 4), (17.5, 9.5), (13, 8)], closed=True)),
            line("M11.5 12.5L20 14")]


@icon("scenic-painter", CAT, "Figure with a long brush painting a hilly backdrop laid on the floor",
      tags=["scenic painter", "set painter", "backdrop", "scenery", "brush", "theatre craft", "painting"])
def _(S):
    return [dot(5, 5, 2.25), line("M5 8.5V15"), line("M5 15L3 21"), line("M5 15L7 21"),
            line("M5 10.5L9 11.5"), line("M8 10L15 16"),
            shell(rect(9, 16, 13, 5, 0)),
            Part("dot", poly([(11, 20), (14, 17.5), (17, 20)], closed=True)),
            Part("dot", poly([(16, 20), (18.5, 18), (21, 20)], closed=True))]


@icon("costume-fitting", CAT, "Performer on a box in a long costume while a second figure pins the hem",
      tags=["costume fitting", "tailor", "wardrobe", "hem", "seamstress", "dressmaker", "pins"])
def _(S):
    return [dot(8, 4, 2.25), shell(poly([(8, 7), (12.5, 16), (3.5, 16)], closed=True, r=S.r * 0.5)),
            shell(rect(3, 17, 10, 4, 0)),
            dot(19, 11.5, 2), line("M19 14V18.5H16"), line("M19 15.5L14.5 15.5"), dot(14, 15.5, 0.9)]


@icon("prompt-desk", CAT, "Stage manager's desk with an open script, a hooded lamp and cue buttons",
      tags=["prompt desk", "stage manager", "cue", "calling script", "prompt corner", "backstage", "show control"])
def _(S):
    return [shell(rect(2, 14, 20, 7, min(S.R, 2))), dot(7, 17.5, 1.2), dot(12, 17.5, 1.2), dot(17, 17.5, 1.2),
            line("M3 14V8Q5.5 6.5 8 8.5Q10.5 6.5 13 8V14"),
            shell(poly([(16, 5.5), (20, 3.5), (22, 8)], closed=True)), line("M19 8V14")]


@icon("kabuki-curtain", CAT, "Wide stage curtain with bold vertical bands of alternating stripes",
      tags=["kabuki", "curtain", "japanese theatre", "striped curtain", "jokimaku", "stage curtain", "drape"])
def _(S):
    return [line("M2 4H22"), shell(rect(3, 6, 18, 14, 0)),
            Part("dot", rect(5.5, 8.5, 3, 9)), Part("dot", rect(15.5, 8.5, 3, 9))]


@icon("cabaret", CAT, "Small table with a shaded lamp facing a tiny stage with a performer on a stool",
      tags=["cabaret", "nightclub", "variety show", "stage", "intimate venue", "performer", "lounge"])
def _(S):
    return [shell(poly([(4, 4), (8, 4), (9.5, 9), (2.5, 9)], closed=True)),
            line("M6 9V16"), line("M2 16H10"), line("M6 16V21"), line("M3.5 21H8.5"),
            dot(18, 6.5, 2), line("M18 9V13"), line("M18 13L15.5 15"), line("M15.5 15H20.5"),
            line("M16 15V17"), line("M20 15V17"), shell(rect(13, 18, 9, 3, 0))]


@icon("melodrama-villain", CAT, "Figure in a top hat and long cape twirling a curled mustache",
      tags=["villain", "melodrama", "top hat", "cape", "mustache", "baddie", "pantomime"])
def _(S):
    return [shell(rect(8, 2.5, 5, 3.5, 0)), line("M6.5 6.5H14.5"),
            shell(circle(10.5, 10, 2.5)), line("M8.5 12.5Q10.5 14 12.5 12.5"),
            shell(poly([(8, 14), (13, 14), (20, 21.5), (3, 21.5)], closed=True, r=S.r * 0.5)),
            line("M14 15L15.5 12"), line("M15.5 12Q16.5 10 14.5 11")]


# ---------------------------------------------------------------------------- chunk 4


@icon("tree-costume", CAT, "Child in a tree costume with a leafy crown, a round face hole and leaf-tipped arms",
      tags=["tree costume", "school play", "nativity", "dress up", "forest", "costume", "kids"])
def _(S):
    crown = U(P(circle(12, 6, 3.5)), P(circle(7.5, 8, 2.5)), P(circle(16.5, 8, 2.5)))
    return [shell(path_to_d(crown)), shell(rect(9, 11, 6, 10, min(S.R, 1.5))), detail(circle(12, 15, 1.5)),
            line("M9 13L5 12.5"), dot(4, 12.5, 1.4), line("M15 13L19 12.5"), dot(20, 12.5, 1.4)]


@icon("dance-card", CAT, "Small booklet with a tassel cord and a pencil, lines of names inside",
      tags=["dance card", "ball", "ballroom", "regency", "programme", "waltz", "pencil"])
def _(S):
    return [shell(rect(4, 3, 10, 18, min(S.R, 2))), detail("M7 8H11"), detail("M7 12H11"), detail("M7 16H10"),
            shell(poly([(18, 6), (21, 6), (21, 16.5), (19.5, 19), (18, 16.5)], closed=True, r=S.r * 0.3)),
            line("M4 5C2 5 2 9 3 10")]


@icon("grand-jete", CAT, "Ballet dancer leaping in mid air with legs in a full horizontal split",
      tags=["grand jete", "ballet", "leap", "split leap", "dance", "jump", "dancer"])
def _(S):
    return [dot(12, 5, 2.25), line("M12 8.5V13"), line("M12 9.5L5 7"), line("M12 9.5L19 7"),
            line("M12 13L3 15.5"), line("M12 13L21 12")]


@icon("hip-hop-dance", CAT, "Figure in a cap in a low crouch with one arm across the chest and one pointing down",
      tags=["hip hop", "street dance", "breakdance", "dancer", "cap", "crouch", "urban dance"])
def _(S):
    return [dot(12, 6, 2.25), line("M13.5 4.5H17"), line("M12 9L11 14"), line("M10 10.5L15 12"),
            line("M13 10L18 16"), line("M11 14L6 16.5L7 21"), line("M11 14L16 16.5L17 21")]


@icon("gumboot-dance", CAT, "Figure bent forward in tall boots slapping one boot with a hand, one knee raised",
      tags=["gumboot dance", "boot dance", "south african", "stomping", "rubber boots", "folk dance", "rhythm"])
def _(S):
    return [dot(6, 5.5, 2.25), line("M7.5 8.5L11 13"), line("M11 13V17"), solid(rect(9.5, 15.5, 3.5, 6)),
            line("M11 13L18 13V17"), solid(rect(16.5, 15, 3.5, 6)),
            line("M8.5 9.5L14 9L18 13") if False else line("M9 9.5L16 15")]


@icon("water-sleeve-dance", CAT, "Dancer flinging very long flowing sleeves in a wide arc overhead",
      tags=["water sleeve", "chinese dance", "sleeves", "silk", "flowing", "classical dance", "opera dance"])
def _(S):
    return [dot(12, 8, 2), shell(poly([(12, 10.5), (16, 21), (8, 21)], closed=True, r=S.r * 0.5)),
            line("M10.5 12C3 12 2 5 6.5 3"), line("M13.5 12C21 12 22 5 17.5 3")]


@icon("bon-odori", CAT, "Tall tower strung with round lanterns and small dancers circling its base",
      tags=["bon odori", "obon", "japanese festival", "lanterns", "yagura", "summer festival", "folk dance"])
def _(S):
    return [shell(poly([(9, 3), (15, 3), (17, 16), (7, 16)], closed=True, r=S.r * 0.3)),
            line("M9 5.5L3 12"), line("M15 5.5L21 12"),
            shell(circle(5.5, 10, 1.5)), shell(circle(18.5, 10, 1.5)),
            dot(4.5, 20, 1.3), dot(9.5, 20, 1.3), dot(14.5, 20, 1.3), dot(19.5, 20, 1.3)]


@icon("wheelchair-dance", CAT, "Dancer in a wheelchair holding hands with a standing partner mid spin",
      tags=["wheelchair dance", "inclusive dance", "para dance", "partner dance", "disability", "dancing", "accessible"])
def _(S):
    return [dot(7, 5.5, 2.25), line("M7 9V14H11"), line("M7 10.5L11.5 5.5"), shell(circle(7, 17, 4)),
            dot(18, 5.5, 2.25), line("M18 9V15"), line("M18 15L16 21"), line("M18 15L20.5 21"), line("M18 10.5L13.5 5.5")]


@icon("headbanging", CAT, "Figure with long hair whipping around, motion arcs and a raised fist",
      tags=["headbanging", "metal", "rock", "concert", "hair", "mosh", "fist"])
def _(S):
    return [dot(13, 9, 2.5), line("M8 8C5 8 3.5 11 3.5 14"), line("M8 11C6 12 5 15 5.5 18"),
            line("M13 12.5V20"), line("M13 14L17.5 10.5V6.5"), dot(17.5, 4.5, 1.5)]


@icon("pheasant-feather-headdress", CAT, "Ornate opera crown with two long pheasant tail feathers curving back",
      tags=["pheasant feather", "opera headdress", "chinese opera", "crown", "feathers", "costume", "warrior"])
def _(S):
    return [shell(poly([(6, 20), (6.5, 14), (9, 16), (11, 12), (13, 16), (15.5, 14), (16, 20)], closed=True, r=S.r * 0.5)),
            line("M10 12C8 5 14 2 21.5 5"), line("M13.5 14C13.5 9 17 7 21.5 9")]


@icon("khon-mask", CAT, "Masked face with a tall tiered pointed crown and ornate ear flaps",
      tags=["khon", "thai mask", "ramakien", "masked dance", "crown", "thailand", "traditional"])
def _(S):
    return [shell(poly([(12, 3.5), (14.5, 7), (13.5, 7), (16.5, 11), (7.5, 11), (10.5, 7), (9.5, 7)], closed=True)),
            shell("M8.5 12.5H15.5V15Q15.5 21 12 21Q8.5 21 8.5 15Z"),
            dot(10.5, 15, 1), dot(13.5, 15, 1), line("M8.5 13L5 13.5L5.5 17"), line("M15.5 13L19 13.5L18.5 17")]


@icon("wayang-puppet", CAT, "Flat ornate puppet in profile with a long nose, a stick below and thin arm rods",
      tags=["wayang", "shadow puppet", "indonesian", "kulit", "leather puppet", "javanese", "puppetry"])
def _(S):
    return [shell(circle(11, 5, 2.25)), line("M8.75 5.5L5 7"),
            shell(poly([(8.5, 8.5), (14, 8.5), (15, 15), (8, 15)], closed=True, r=S.r * 0.5)),
            line("M11.5 15V22"), line("M13.5 10L18.5 13L19 16"), line("M18.5 13L21 6")]


@icon("bucket-door-prank", CAT, "Door left ajar with a bucket balanced on top and water dripping from its lip",
      tags=["bucket prank", "door prank", "practical joke", "slapstick", "water", "gag", "comedy"])
def _(S):
    return [line("M4 21V10H20V21"), shell(poly([(12, 12), (17, 11), (17, 21), (12, 21)], closed=True)),
            shell(poly([(9, 3), (16, 3), (15, 7.5), (10, 7.5)], closed=True, r=S.r * 0.3)),
            dot(7.5, 6, 0.9), dot(6.5, 8.7, 0.9)]


@icon("dance-studio", CAT, "Mirror wall with a barre and a dancer standing at it",
      tags=["dance studio", "ballet barre", "mirror", "rehearsal room", "practice", "dancer", "class"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), dot(12, 7, 1.75), line("M12 9.5V14"), line("M12 14L10 18"), line("M12 14L14 18"),
            detail("M12 10.5L8.5 11.5"), detail("M6 11.5H9.5"), detail("M17 6L19 8")]


@icon("applause-meter", CAT, "Semicircular dial with a needle swinging to high and clapping hands below",
      tags=["applause meter", "clap-o-meter", "gauge", "audience", "reaction", "talent show", "volume"])
def _(S):
    return [line("M3 13A9 9 0 0 1 21 13"), line("M12 13L17 7.5"), dot(12, 13, 1.25),
            solid(path_to_d(U(ST("M6 20.5L10.5 16.5", 3.2, "round", "round")))),
            solid(path_to_d(U(ST("M18 20.5L13.5 16.5", 3.2, "round", "round"))))]


@icon("flaming-hoop", CAT, "Large hoop on a stand ringed with small flames",
      tags=["flaming hoop", "fire hoop", "circus", "ring of fire", "acrobat", "stunt", "leap"])
def _(S):
    import math
    out = [line(circle(12, 9.5, 4.5))]
    for deg in (-90, -45, 0, 45, 135, 180, 225):
        a = math.radians(deg)
        out.append(line(f"M{12 + 6.6 * math.cos(a):.2f} {9.5 + 6.6 * math.sin(a):.2f}L{12 + 8.6 * math.cos(a):.2f} {9.5 + 8.6 * math.sin(a):.2f}"))
    return out + [line("M12 14V21"), line("M8 21H16")]


@icon("sword-balancing", CAT, "Dancer with a curved sword balanced flat on the head and arms curved out",
      tags=["sword dance", "balancing", "sword balancing", "dancer", "folk dance", "belly dance", "head balance"])
def _(S):
    return [line("M4 5.5Q12 3 20 5.5"), dot(12, 9, 2.25), shell(poly([(12, 12.5), (17, 21), (7, 21)], closed=True, r=S.r * 0.5)),
            line("M10.5 14Q5 13 4.5 17"), line("M13.5 14Q19 13 19.5 17")]
