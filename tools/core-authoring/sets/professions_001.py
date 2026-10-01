"""TypeIcon Core: professions and roles (batch professions_001).

Clinical, protective-service, legal, civic, office and technical roles. Each icon is a head-and-shoulders
figure (head r 3, shoulders 9 wide) on the left or centre with one identifying prop, hat or garment mark.
Small solid marks use `dot` parts so they are knocked out of the Filled shell.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import I, P, U, fmt, path_to_d, polar  # noqa: F401

CAT = "professions"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def u(*ds):
    """Union of closed shapes as one outline (d-string)."""
    return path_to_d(U(*[P(d) for d in ds]))


def clip(a, b):
    """Intersection of two closed shapes as a d-string."""
    return path_to_d(I(P(a), P(b)))


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def cross(cx, cy, arm=1.6, w=1.4):
    return u(rect(cx - w / 2, cy - arm, w, 2 * arm), rect(cx - arm, cy - w / 2, 2 * arm, w))


def bust_d(S, cx, top, hw, bottom=21.0):
    """Open-bottom shoulders; Line has squarer shoulders than Rounded."""
    r = min(hw - L(S, 2.0, 1.0), bottom - top)
    x0, x1 = cx - hw, cx + hw
    return (f"M{fmt(x0)} {fmt(bottom)}V{fmt(top + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x0 + r)} {fmt(top)}"
            f"H{fmt(x1 - r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(top + r)}V{fmt(bottom)}")


def person(S, cx=12.0, hy=9.0, hr=3.0, top=15.0, hw=4.5, bottom=21.0):
    return [shell(circle(cx, hy, hr)), shell(bust_d(S, cx, top, hw, bottom))]


def lp(S, hy=9.0):
    """Person on the left, leaving the right third free for a prop."""
    return person(S, 7.5, hy, 3.0, hy + 6.0, 4.5)


def cp(S, hy=10.0):
    """Centred person with room above for a hat."""
    return person(S, 12, hy, 3.0, hy + 6.0, 6.5)


def dome(cx, y, w, h):
    return f"M{fmt(cx - w)} {fmt(y)}A{fmt(w)} {fmt(h)} 0 0 1 {fmt(cx + w)} {fmt(y)}Z"


def mask_mark(cx, hy, hr=3.0):
    """Face mask: the lower part of the head, solid."""
    return mark(clip(circle(cx, hy, hr - 0.4), rect(cx - hr, hy + 0.4, 2 * hr, hr)))


def peaked_cap(S, cx, hy):
    """Peaked cap sitting on a head of r 3 centred at (cx, hy)."""
    return poly([(cx - 5.5, hy - 4.7), (cx, hy - 7.7), (cx + 5.5, hy - 4.7), (cx + 4, hy - 2), (cx - 4, hy - 2)], closed=True, r=S.r * 0.5)


def sunburst(cx, cy, r0, r1, n):
    return [line(seg(*polar(cx, cy, r0, a), *polar(cx, cy, r1, a))) for a in [360 * i / n for i in range(n)]]


# ============================================================================ medical roles

@icon("surgeon", CAT, "Figure in a surgical cap and face mask beside a raised scalpel",
      tags=["surgeon", "surgery", "operating room", "doctor", "scalpel", "mask", "theatre"])
def _(S):
    cx, hy = 7.5, 10.5
    blade = "M16.3 11C15.8 8 16.8 5.5 19.4 3.8C19.6 6.5 19.5 9 19 11Z"
    return ([shell(dome(cx, hy - 1.2, 3.9, 4.2))] + person(S, cx, hy, 3.0, 16.5, 4.5)
            + [mask_mark(cx, hy), line(seg(17.7, 11, 17.7, 21)), solid(blade)])


@icon("dentist", CAT, "Figure in a face mask with a head mirror beside a large tooth",
      tags=["dentist", "dental", "tooth", "teeth", "head mirror", "oral health", "orthodontics"])
def _(S):
    tooth = poly([(13.5, 8), (15, 6), (17.25, 7), (19.5, 6), (21, 8), (20.5, 12.5), (19.8, 19.5), (18.6, 19.5), (17.25, 13.5),
                  (15.9, 19.5), (14.7, 19.5), (14, 12.5)], closed=True, r=S.r)
    return (person(S, 6.3, 10, 3.0, 16, 3.8) + [shell(circle(4.2, 5.2, 1.5)), mask_mark(6.3, 10), shell(tooth)])


@icon("paramedic", CAT, "Figure in a vest with a medical cross on the chest beside a boxy first aid bag",
      tags=["paramedic", "emt", "ambulance crew", "first aid", "emergency medical", "responder", "first responder"])
def _(S):
    bag = rect(12.5, 13.5, 9.5, 7.5, min(S.R, 2))
    return (person(S, 6.3, 9, 3.0, 15, 3.8) + [mark(cross(6.3, 18.6, 1.4, 1.2)), shell(bag),
            line("M15.5 13.5V11H19V13.5"), detail(seg(12.5, 16.5, 22, 16.5)), mark(cross(17.25, 18.9, 1.0, 0.9))])


@icon("pharmacist", CAT, "Figure in a white coat holding up a pill bottle",
      tags=["pharmacist", "pharmacy", "chemist", "medication", "pills", "prescription", "drugstore"])
def _(S):
    bottle = rect(15, 8.5, 6.5, 11.5, min(S.R, 2))
    return (lp(S, 8.5) + [detail(poly([(5, 15.3), (7.5, 18.5), (10, 15.3)], r=S.r * 0.3)),
            shell(rect(15.5, 4.5, 5.5, 2.5, 0.5)), shell(bottle), detail(seg(15, 13, 21.5, 13)),
            mark(cross(18.25, 16.6, 1.2, 1.1))])


@icon("midwife", CAT, "Figure in scrubs holding a swaddled newborn",
      tags=["midwife", "birth", "newborn", "baby", "delivery", "maternity", "obstetric"])
def _(S):
    swaddle = poly([(12.5, 17.5), (15.5, 13), (21.5, 16), (18.5, 21)], closed=True, r=S.r)
    return lp(S, 9) + [shell(swaddle), detail(seg(16, 18.8, 18.5, 15.2)), shell(circle(18.8, 11.8, 2))]


@icon("optometrist", CAT, "Figure beside an eye chart with rows of shrinking letters",
      tags=["optometrist", "eye doctor", "eye test", "vision", "eye chart", "optician", "eyesight"])
def _(S):
    return (lp(S, 9) + [shell(rect(14, 3.5, 8, 17, min(S.R, 2))), detail(seg(16.5, 7.5, 19.5, 7.5)),
            detail(seg(16.5, 11.5, 19, 11.5)), detail(seg(16.5, 15.5, 18, 15.5))])


@icon("radiologist", CAT, "Figure beside an x-ray film showing a spine and ribs",
      tags=["radiologist", "x-ray", "xray", "radiology", "scan", "ribs", "imaging"])
def _(S):
    return (lp(S, 9) + [shell(rect(13.5, 3.5, 9, 15, min(S.R, 2))), detail(seg(18, 6.5, 18, 15.5)),
            detail("M15.5 8.5Q18 10.5 20.5 8.5"), detail("M15.5 12.5Q18 14.5 20.5 12.5")])


@icon("physiotherapist", CAT, "Figure beside a stretched resistance band with a handle at each end",
      tags=["physiotherapist", "physical therapy", "rehab", "physio", "exercise band", "stretching", "recovery"])
def _(S):
    return (lp(S, 9) + [shell(circle(15, 19, 1.6)), shell(circle(20.5, 5, 1.6)), line(seg(15.6, 17.5, 19.9, 6.5))])


@icon("psychologist", CAT, "Figure beside a couch with a raised back",
      tags=["psychologist", "therapist", "counselling", "counseling", "therapy", "mental health", "psychiatrist"])
def _(S):
    couch = u(rect(13.5, 8.5, 8.5, 5, min(S.R, 2)), rect(13, 12.5, 9.5, 5, min(S.R, 1.5)))
    return lp(S, 9) + [shell(couch), line(seg(14.5, 17.5, 14.5, 20.5)), line(seg(21, 17.5, 21, 20.5))]


@icon("pediatrician", CAT, "Figure with a stethoscope beside a small child",
      tags=["pediatrician", "paediatrician", "children's doctor", "child health", "kids", "stethoscope", "baby doctor"])
def _(S):
    return (person(S, 7, 7.5, 3.0, 13.5, 4.5) + [line("M5 15.5V17.5A2 2 0 0 0 9 17.5V15.5")]
            + person(S, 17.5, 13.5, 2.0, 17.5, 3.5))


@icon("phlebotomist", CAT, "Figure beside a blood collection tube with a cap",
      tags=["phlebotomist", "blood draw", "blood test", "blood sample", "lab technician", "vial", "venipuncture"])
def _(S):
    tube = "M16 7V17A2.5 2.5 0 0 0 21 17V7Z"
    return (lp(S, 9) + [shell(tube), detail(seg(15, 7, 22, 7)), line(seg(16.5, 4, 20.5, 4)),
            mark("M16.2 13H20.8V17A2.3 2.3 0 0 1 16.2 17Z")])


@icon("sonographer", CAT, "Figure beside an ultrasound screen showing a scan fan and a probe",
      tags=["sonographer", "ultrasound", "sonogram", "scan", "pregnancy scan", "imaging", "probe"])
def _(S):
    return (lp(S, 9) + [shell(rect(13.5, 3.5, 9, 8.5, min(S.R, 2))), mark("M18 5.5L15.6 10A5.2 5.2 0 0 0 20.4 10Z"),
            shell(rect(16, 14.5, 4, 3, 1)), line(seg(18, 17.5, 18, 21))])


@icon("dietitian", CAT, "Figure holding a clipboard with an apple on top",
      tags=["dietitian", "dietician", "nutritionist", "nutrition", "diet plan", "healthy eating", "apple"])
def _(S):
    apple = ("M18 5C17.2 3.6 14.8 4 14.8 6.4C14.8 8.4 16.2 9.6 18 9.6C19.8 9.6 21.2 8.4 21.2 6.4C21.2 4 18.8 3.6 18 5Z")
    return (lp(S, 9) + [shell(rect(13.5, 13, 9, 8, min(S.R, 2))), detail(seg(16, 17, 20, 17)),
            shell(apple), line(seg(18, 4.8, 18.8, 2.4))])


@icon("speech-therapist", CAT, "Figure pointing at a speech bubble with an open mouth",
      tags=["speech therapist", "speech therapy", "speech pathologist", "language", "talking", "pronunciation", "communication"])
def _(S):
    bubble = u(rect(12.5, 3, 10, 8, min(S.R, 2)), poly([(14.5, 10), (14.5, 13.5), (18, 10)], closed=True))
    return lp(S, 10) + [shell(bubble), mark(ellipse(17.5, 7, 2.3, 1.3)), line(seg(11.8, 16.5, 13.5, 14.5))]


@icon("orthodontist", CAT, "Figure in a face mask beside a wide smile with braces on the teeth",
      tags=["orthodontist", "braces", "teeth straightening", "smile", "dental", "brackets", "aligners"])
def _(S):
    smile = "M12.5 7H22.5A5 5 0 0 1 12.5 7Z"
    return lp(S, 9) + [mask_mark(7.5, 9), shell(smile), detail(seg(14.5, 10.3, 20.5, 10.3))]


@icon("chiropractor", CAT, "Figure beside a spine of stacked vertebrae",
      tags=["chiropractor", "spine", "back pain", "vertebrae", "backbone", "spinal adjustment", "posture"])
def _(S):
    v = [solid(rect(cx - w / 2, y, w, 3, 1.3)) for cx, y, w in ((17.5, 3.2, 4.4), (19, 7.7, 5.4), (17.5, 12.2, 6.2), (19, 16.7, 6.6))]
    return lp(S, 9) + v


@icon("massage-therapist", CAT, "Figure pressing both hands onto the back of a person lying on a massage table",
      tags=["massage therapist", "massage", "spa", "bodywork", "relaxation", "masseuse", "masseur"])
def _(S):
    return (person(S, 6, 8, 3.0, 14, 3.5) + [line(seg(9.6, 16.5, 13.5, 12.6)), shell(rect(11.5, 13.5, 8, 3.5, 1.7)),
            solid(circle(21.2, 14.8, 1.7)), line(seg(11, 19.5, 22.5, 19.5))])


@icon("acupuncturist", CAT, "Figure beside a hand with fine needles inserted",
      tags=["acupuncturist", "acupuncture", "needles", "traditional medicine", "alternative medicine", "pressure points", "holistic"])
def _(S):
    return (lp(S, 9) + [shell(rect(13.5, 14, 9, 7, 3)), line(seg(15.2, 14, 14.2, 8)), line(seg(18, 14, 18, 7)), line(seg(20.8, 14, 21.8, 8)),
            solid(circle(14, 6.6, 1.3)), solid(circle(18, 5.6, 1.3)), solid(circle(22, 6.6, 1.3))])


@icon("anesthesiologist", CAT, "Figure in a surgical cap beside an anesthesia mask with a hose",
      tags=["anesthesiologist", "anaesthetist", "anesthesia", "anaesthesia", "sedation", "gas mask", "operating room"])
def _(S):
    cx, hy = 7.5, 10.5
    mask = poly([(14.5, 19), (18, 10), (21.5, 19)], closed=True, r=max(S.r, 1.5) + L(S, 0, 1))
    return ([shell(dome(cx, hy - 1.2, 3.9, 4.2))] + person(S, cx, hy, 3.0, 16.5, 4.5)
            + [shell(mask), line("M18 10V7A2.5 2.5 0 0 0 15.5 4.5H13")])


@icon("army-medic", CAT, "Figure in a helmet with a cross armband beside a stretcher",
      tags=["army medic", "combat medic", "field medic", "military medic", "stretcher", "casualty", "battlefield"])
def _(S):
    cx, hy = 7.5, 10.5
    helmet = "M3.5 9.5H11.5A4 4.5 0 0 0 3.5 9.5Z"
    return ([shell(helmet)] + person(S, cx, hy, 3.0, 16.5, 4.5)
            + [mark(cross(4.6, 19, 1.3, 1.1)), shell(rect(13.5, 13, 8.5, 3.5, min(S.R, 1.2))), line(seg(11.5, 14.75, 13.5, 14.75)),
               line(seg(15.5, 16.5, 15.5, 20)), line(seg(20.5, 16.5, 20.5, 20))])


@icon("pharmacy-delivery-rider", CAT, "Rider on a scooter with a delivery box carrying a medical cross",
      tags=["pharmacy delivery", "medicine delivery", "scooter", "courier", "rider", "prescription delivery", "moped"])
def _(S):
    return [shell(circle(5.5, 18.5, 2.5)), shell(circle(18.5, 18.5, 2.5)), line(seg(8, 17, 16, 17)),
            line(poly([(18.5, 18.5), (16.5, 9), (14.5, 8)], r=S.r)),
            solid(circle(10, 5, 2)), line(poly([(10, 8), (10.5, 12), (9.5, 17)], r=S.r)), line(seg(10.3, 10, 15, 8.8)),
            shell(rect(2.5, 8.5, 5.5, 6, min(S.R, 1.5))), mark(cross(5.25, 11.5, 1.3, 1.0))]


@icon("blood-donor", CAT, "Figure with a tube running from the arm up to a bag of blood",
      tags=["blood donor", "blood donation", "transfusion", "blood bag", "donate blood", "red cross", "give blood"])
def _(S):
    return (lp(S, 9) + [shell(rect(14.5, 3, 7, 9, min(S.R, 2.5))), mark("M18 5.3C16.6 7 16.2 7.8 16.2 8.6A1.8 1.8 0 0 0 19.8 8.6C19.8 7.8 19.4 7 18 5.3Z"),
            line("M18 12V16A2 2 0 0 1 16 18H12.5")])


@icon("organ-donor", CAT, "Figure beside a heart held in a cupped hand",
      tags=["organ donor", "organ donation", "transplant", "donor card", "heart", "give life", "donate"])
def _(S):
    heart = "M18 14C14.4 11.6 14 8.6 15.8 7.3C17 6.6 18 7.4 18 8.3C18 7.4 19 6.6 20.2 7.3C22 8.6 21.6 11.6 18 14Z"
    return lp(S, 9) + [shell(heart), line("M12.5 17.5C15 20.5 19.5 20.5 22 17.5")]


@icon("bodyguard", CAT, "Figure in dark sunglasses and a suit with a coiled earpiece wire",
      tags=["bodyguard", "security guard", "close protection", "sunglasses", "earpiece", "secret service", "protector"])
def _(S):
    return (cp(S, 9.5) + [mark(rect(9.2, 8.8, 5.6, 1.8, 0.6)), line("M9 10.5Q6.5 13 8 15.5"),
            detail(poly([(9.5, 16.5), (12, 20), (14.5, 16.5)], r=S.r * 0.3))])


@icon("park-ranger", CAT, "Figure in a flat-brimmed campaign hat with a pine tree patch on the shoulder",
      tags=["park ranger", "forest ranger", "national park", "ranger hat", "wildlife", "warden", "outdoors"])
def _(S):
    hat = u(rect(8.5, 3, 7, 5.5, 1.5), rect(4, 7.3, 16, 1.8, 0.9))
    return (cp(S, 11.5) + [shell(hat), mark(poly([(16.5, 16.8), (18.6, 19.6), (14.4, 19.6)], closed=True))])


@icon("traffic-police-officer", CAT, "Figure in a peaked cap with one white-gloved arm raised to stop traffic",
      tags=["traffic police", "traffic officer", "traffic cop", "stop", "road safety", "whistle", "point duty"])
def _(S):
    cap = poly([(3.5, 6.3), (9, 3.3), (14.5, 6.3), (13, 9), (5, 9)], closed=True, r=S.r * 0.5)
    return (person(S, 9, 11, 3.0, 17, 5.5) + [shell(cap), line(seg(14.5, 18, 19, 8.5)), solid(circle(19.3, 5.8, 2.1))])


@icon("mountain-rescuer", CAT, "Figure in a helmet with a coil of rope on the shoulder and a cross on the jacket",
      tags=["mountain rescuer", "mountain rescue", "alpine rescue", "climbing", "rope", "search and rescue", "helmet"])
def _(S):
    cx, hy = 8, 10.5
    helmet = "M3.8 9.3H12.2A4.2 4.6 0 0 0 3.8 9.3Z"
    return ([shell(helmet)] + person(S, cx, hy, 3.0, 16.5, 4.8) + [mark(cross(cx, 19, 1.3, 1.1)),
            shell(circle(18, 16.8, 3.2)), line("M18 13.6V11Q18 8.5 21 8.5")])


@icon("ski-patroller", CAT, "Figure in a ski helmet and goggles with a cross on the jacket and skis resting on the shoulder",
      tags=["ski patrol", "ski patroller", "ski rescue", "skis", "goggles", "snow", "slope safety"])
def _(S):
    cx, hy = 7.5, 10.5
    return ([shell(dome(cx, hy - 1.2, 3.9, 4.2))] + person(S, cx, hy, 3.0, 16.5, 4.5)
            + [mark(rect(4.8, 9.6, 5.4, 1.8, 0.8)), mark(cross(cx, 19, 1.2, 1.0)),
               line("M14.5 20.5L20 5.5A1.2 1.2 0 0 1 22 4.8"), line("M18 21L22.2 10")])




@icon("bomb-disposal-technician", CAT, "Bulky figure in a padded bomb suit with a large visored helmet and thick collar",
      tags=["bomb disposal", "bomb squad", "explosives", "eod", "bomb suit", "ordnance", "demolition"])
def _(S):
    return [shell(rect(6, 2.5, 12, 9.5, L(S, 3, 5))), mark(rect(8, 6, 8, 2.6, 1.0)),
            shell(bust_d(S, 12, 15, 9, 21)), detail(seg(12, 15.5, 12, 21))]


@icon("hazmat-worker", CAT, "Figure in a hooded protective suit with a face window, respirator and hazard mark on the chest",
      tags=["hazmat", "hazardous materials", "protective suit", "biohazard", "respirator", "decontamination", "chemical"])
def _(S):
    return [shell(circle(12, 8, 5.5)), mark(rect(8.5, 5.5, 7, 3.2, 1.4)), mark(circle(12, 11.2, 1.2)),
            shell(bust_d(S, 12, 15, 7.5, 21)), mark(poly([(12, 16.8), (14.2, 20.2), (9.8, 20.2)], closed=True))]


@icon("wildland-firefighter", CAT, "Figure in a brimmed hard hat with a long-handled axe over the shoulder",
      tags=["wildland firefighter", "forest fire", "wildfire", "firefighter", "hotshot", "fire line", "axe"])
def _(S):
    cx, hy = 7.5, 10.5
    return ([shell(dome(cx, hy - 1.2, 3.9, 4.2)), line(seg(2.8, hy - 1.2, 12.2, hy - 1.2))] + person(S, cx, hy, 3.0, 16.5, 4.5)
            + [line(seg(16.4, 21, 17.6, 5)), solid("M18 4.2C22 3.6 23 8 22.6 9.6C21.2 9 19.8 9 18 9Z"), solid(rect(14.8, 4.2, 3.2, 4.8, 0.6))])


@icon("prison-guard", CAT, "Figure in a peaked cap with a large key ring hanging at the belt",
      tags=["prison guard", "correctional officer", "jailer", "warden", "keys", "jail", "custody"])
def _(S):
    return (person(S, 7, 11, 3.0, 17, 4.5) + [shell(peaked_cap(S, 7, 11)), shell(circle(17, 12.5, 2.5)),
            line(seg(17, 15, 17, 21)), line(seg(17, 18.5, 20.5, 18.5))])


@icon("forensic-scientist", CAT, "Figure beside a magnifying glass held over a sealed evidence bag",
      tags=["forensic scientist", "forensics", "crime scene", "evidence", "csi", "investigation", "criminalist"])
def _(S):
    return (lp(S, 9) + [shell(circle(17, 7, 3.3)), line(seg(19.5, 9.5, 22, 12)), shell(rect(13.5, 14.5, 9, 6.5, min(S.R, 1.5))),
            detail(seg(13.5, 17.5, 22.5, 17.5))])


@icon("police-dog-handler", CAT, "Figure in a police cap beside a sitting police dog with pointed ears",
      tags=["police dog handler", "k9", "canine unit", "police dog", "sniffer dog", "german shepherd", "dog handler"])
def _(S):
    dog = poly([(13.5, 4.5), (16, 8), (19, 8), (21.5, 4.5), (20.8, 13.5), (18.6, 19), (15.9, 19), (14, 13.5)], closed=True, r=max(S.r, 1.0))
    return (person(S, 7.2, 11, 3.0, 17, 4) + [shell(peaked_cap(S, 7.2, 11)), shell(dog), mark(circle(15.7, 11.5, 0.9)),
            mark(circle(18.8, 11.5, 0.9)), mark(circle(17.25, 16.8, 1.1))])


@icon("mounted-police-officer", CAT, "Officer in a helmet riding a horse seen from the side",
      tags=["mounted police", "horse patrol", "police horse", "cavalry", "riding", "equestrian officer", "horseback"])
def _(S):
    body = rect(6.5, 12, 13, 5, 2.4)
    head = poly([(8, 12.5), (5, 6.5), (3, 8.5), (3.2, 10.5), (6.5, 11.5)], closed=True, r=S.r * 0.3)
    return [shell(body), shell(head), line(seg(9, 17, 9, 21)), line(seg(12, 17, 12, 21)), line(seg(16, 17, 16, 21)), line(seg(19, 17, 19, 21)),
            line("M19.5 13C21.5 13.5 22 16 21.5 18"), solid(circle(14, 5.2, 2.1)), line(seg(14, 8, 13.5, 12))]


@icon("emergency-dispatcher", CAT, "Figure in a headset with a boom microphone beside a map screen with a location pin",
      tags=["emergency dispatcher", "911 operator", "call handler", "headset", "dispatch", "control room", "operator"])
def _(S):
    return (person(S, 7.5, 10, 3.0, 16, 4.5) + [line(arc(7.5, 9.8, 4.4, 180, 360)), solid(rect(2.4, 8.5, 1.8, 3.2, 0.8)),
            line("M3.3 12Q3.3 14.3 6 14.3"), shell(rect(13.5, 3.5, 9, 9, min(S.R, 2))),
            mark("M18 11C16.2 9.4 15.4 8.4 15.4 7.4A2.6 2.6 0 0 1 20.6 7.4C20.6 8.4 19.8 9.4 18 11Z"), line(seg(18, 12.5, 18, 15.5)),
            line(seg(15, 16, 21, 16))])


@icon("customs-officer", CAT, "Figure in a peaked cap beside an open suitcase being inspected",
      tags=["customs officer", "customs", "baggage check", "luggage inspection", "border control", "airport security", "suitcase"])
def _(S):
    lid = poly([(14.5, 10), (16, 3.5), (22.5, 3.5), (22.5, 10)], closed=True, r=S.r * 0.6)
    return (person(S, 7, 11, 3.0, 17, 4.5) + [shell(peaked_cap(S, 7, 11)), shell(lid),
            shell(rect(13, 12.5, 10, 8.5, min(S.R, 1.5))), detail(seg(13, 16.5, 23, 16.5))])


@icon("border-guard", CAT, "Figure in a peaked cap beside a striped barrier arm on a post",
      tags=["border guard", "border patrol", "checkpoint", "boom barrier", "frontier", "gate", "passport control"])
def _(S):
    return (person(S, 7, 11, 3.0, 17, 4.5) + [shell(peaked_cap(S, 7, 11)), shell(rect(12.5, 7, 10, 4, min(S.R, 1.5))),
            mark(rect(15, 8.2, 1.6, 1.6)),
            mark(rect(18.4, 8.2, 1.6, 1.6)), shell(rect(17, 13, 5, 8, min(S.R, 1.5)))])


@icon("lawyer", CAT, "Figure in a suit with a briefcase and a small balance scale of justice",
      tags=["lawyer", "attorney", "solicitor", "counsel", "legal", "law", "advocate"])
def _(S):
    return (person(S, 7, 10, 3.0, 16, 4.5) + [detail(poly([(5.5, 16.5), (7, 19.5), (8.5, 16.5)], r=S.r * 0.3)),
            line(seg(18, 3.5, 18, 11)), line(seg(14.5, 5, 21.5, 5)), solid("M12.7 8.8A1.8 1.8 0 0 0 16.3 8.8Z"), solid("M18.7 8.8A1.8 1.8 0 0 0 22.3 8.8Z"),
            shell(rect(14, 14, 8, 6.5, min(S.R, 1.5))), line("M16.5 14V12.5H19.5V14")])


@icon("barrister-in-wig", CAT, "Figure in a short curled court wig with white collar tabs at the neck",
      tags=["barrister", "wig", "advocate", "court", "legal", "judge's wig", "lawyer"])
def _(S):
    wig = u(circle(12, 6.8, 4), circle(7.4, 10.6, 1.9), circle(16.6, 10.6, 1.9))
    return [shell(wig), shell(circle(12, 10, 2.3)), shell(bust_d(S, 12, 16, 6.5, 21)), mark(rect(10.3, 16.8, 1.4, 4)), mark(rect(12.3, 16.8, 1.4, 4))]


@icon("bailiff", CAT, "Figure in a cap and uniform with a badge beside a courtroom rail",
      tags=["bailiff", "court officer", "courtroom", "usher", "marshal", "court security", "badge"])
def _(S):
    star = poly([polar(7, 19, 1.7 if k % 2 == 0 else 0.8, -90 + k * 36) for k in range(10)], closed=True)
    return (person(S, 7, 11, 3.0, 17, 4.5) + [shell(peaked_cap(S, 7, 11)), mark(star), line(seg(13, 12.5, 22.5, 12.5)),
            line(seg(14.5, 12.5, 14.5, 21)), line(seg(18, 12.5, 18, 21)), line(seg(21.5, 12.5, 21.5, 21))])


@icon("court-stenographer", CAT, "Figure typing on a small stenotype machine on a stand",
      tags=["court stenographer", "court reporter", "stenotype", "transcription", "shorthand", "transcript", "typing"])
def _(S):
    return (lp(S, 8.5) + [shell(poly([(13, 11.5), (22, 9.5), (22, 14.5), (13, 14.5)], closed=True, r=S.r * 0.4)),
            mark(circle(15, 13, 0.7)), mark(circle(17.5, 12.6, 0.7)), mark(circle(20, 12.2, 0.7)),
            line(seg(17.5, 14.5, 17.5, 21)), line(seg(14.5, 21, 20.5, 21))])


@icon("notary", CAT, "Figure pressing a round rubber stamp onto a document",
      tags=["notary", "notary public", "stamp", "seal", "attest", "certify", "document signing"])
def _(S):
    stamp = u(rect(16.5, 3, 4, 3.5, 1.2), rect(17.5, 6, 2, 3), rect(14, 9, 8, 2.5, 0.8))
    return lp(S, 9) + [shell(stamp), shell(rect(13, 14.5, 9, 6.5, min(S.R, 1.5))), detail(seg(15.5, 18, 19.5, 18))]


@icon("mayor", CAT, "Figure wearing a heavy chain of office with a round medallion across the chest",
      tags=["mayor", "chain of office", "medallion", "town leader", "city hall", "civic", "councillor"])
def _(S):
    return person(S, 12, 8.5, 3.0, 14.5, 6.5) + [detail("M7 15.5Q8 19 12 19.2Q16 19 17 15.5"), solid(circle(12, 19.4, 1.7))]


@icon("diplomat", CAT, "Figure in a suit beside a table with two small flags on poles",
      tags=["diplomat", "ambassador", "embassy", "negotiation", "international", "flags", "foreign affairs"])
def _(S):
    return (person(S, 7, 9, 3.0, 15, 4.5) + [line(seg(15.3, 20, 15.3, 4)), line(seg(20, 20, 20, 4)),
            solid("M15.3 4L18.5 5.6L15.3 7.2Z"), solid("M20 4L22.8 5.6L20 7.2Z"), line(seg(13, 20.5, 22, 20.5))])


@icon("public-speaker", CAT, "Figure behind a podium with a microphone on a bendy stalk",
      tags=["public speaker", "speech", "podium", "lectern", "keynote", "talk", "orator"])
def _(S):
    return [shell(circle(11, 6, 3)), shell(poly([(4.5, 12.5), (17.5, 12.5), (16.5, 21), (5.5, 21)], closed=True, r=S.r * 0.4)),
            line("M19.5 12.5V9.5"), solid(ellipse(19.5, 7.5, 1.4, 2))]


@icon("juror", CAT, "Figure holding up a numbered card in a jury box",
      tags=["juror", "jury", "jury duty", "verdict", "court", "panel", "numbered card"])
def _(S):
    return lp(S, 9) + [shell(rect(13.5, 5, 9, 12, min(S.R, 2))), detail(poly([(16.5, 9.5), (18.2, 8.5), (18.2, 13.5)], r=S.r * 0.2))]


@icon("witness-oath", CAT, "Figure with the right hand raised and the left hand resting on a closed book",
      tags=["witness", "oath", "swearing in", "testimony", "court", "affirmation", "sworn"])
def _(S):
    return (person(S, 7, 9, 3.0, 15, 4.5) + [line(seg(11.5, 17, 15.5, 11)), solid(circle(16.5, 8.5, 2.1)),
            shell(rect(13.5, 17, 9, 4, 1))])


@icon("prisoner", CAT, "Figure in a flat cap and a horizontally striped uniform",
      tags=["prisoner", "inmate", "convict", "jail", "prison", "striped uniform", "detainee"])
def _(S):
    return ([shell(rect(7.5, 3, 9, 3.5, 1.7))] + person(S, 12, 9.5, 3.0, 15, 7.5) + [detail(seg(4, 18, 20, 18)), detail(seg(4, 20.8, 20, 20.8))])


@icon("census-taker", CAT, "Figure with a clipboard knocking at a door",
      tags=["census taker", "enumerator", "survey", "door to door", "canvasser", "household survey", "knock"])
def _(S):
    return (lp(S, 9) + [shell(rect(14, 3.5, 8, 17.5, min(S.R, 1.5))), mark(circle(19.5, 13, 1.1)),
            line("M12.5 8Q13.4 9.5 12.5 11"), ])


@icon("election-official", CAT, "Figure beside a ballot box with a folded paper dropping through the slot",
      tags=["election official", "poll worker", "ballot box", "voting", "election", "polling station", "ballot"])
def _(S):
    return (lp(S, 9) + [shell(rect(13, 13, 9.5, 8, min(S.R, 1.5))), detail(seg(15.5, 16, 20, 16)), line("M16 12V5H19.5V12")])


@icon("town-crier", CAT, "Figure in a tricorn hat ringing a hand bell",
      tags=["town crier", "bell ringer", "herald", "announcement", "hand bell", "tricorn hat", "proclamation"])
def _(S):
    hat = poly([(2.5, 9), (7.5, 3.5), (12.5, 9), (10, 10), (5, 10)], closed=True, r=S.r * 0.4)
    return (person(S, 7.5, 11.5, 3.0, 17, 4.5) + [shell(hat), shell("M14 18C14 13 15.4 10 18 10C20.6 10 22 13 22 18Z"),
            line(seg(18, 10, 18, 7.5)), solid(circle(18, 20, 1.2))])


@icon("receptionist", CAT, "Figure in a headset behind a front desk with a service bell",
      tags=["receptionist", "front desk", "reception", "headset", "service bell", "check-in", "concierge"])
def _(S):
    return [shell(circle(12, 6.5, 3)), line(arc(12, 6.8, 4.4, 180, 360)), solid(rect(6.2, 5.6, 1.8, 3.2, 0.8)), solid(rect(16, 5.6, 1.8, 3.2, 0.8)),
            line("M7 9Q7 11 9.5 11.2"), shell(rect(3, 13.5, 18, 7.5, L(S, 1.5, 3))), mark(dome(16.5, 18, 2, 2)), mark(rect(14, 18, 5, 1))]


@icon("accountant", CAT, "Figure beside a calculator with a display and number keys",
      tags=["accountant", "bookkeeper", "calculator", "accounting", "finance", "tax", "numbers"])
def _(S):
    keys = [mark(circle(x, y, 0.9)) for x in (16, 18.25, 20.5) for y in (13, 16, 19)]
    return lp(S, 9) + [shell(rect(13.5, 3.5, 9, 17.5, min(S.R, 2))), mark(rect(15.5, 6, 5, 3, 0.6))] + keys


@icon("banker", CAT, "Figure in a suit and tie beside a classical bank building with columns",
      tags=["banker", "bank manager", "bank", "finance", "columns", "financier", "investment"])
def _(S):
    return (person(S, 7, 10, 3.0, 16, 4.5) + [detail(poly([(5.8, 16.5), (7, 19.5), (8.2, 16.5)], r=S.r * 0.3)),
            shell(poly([(13, 9), (17.5, 5), (22, 9)], closed=True, r=max(S.r * 0.5, 0.7))),
            line(seg(14.5, 11.5, 14.5, 17.5)), line(seg(17.5, 11.5, 17.5, 17.5)), line(seg(20.5, 11.5, 20.5, 17.5)), line(seg(13, 20.5, 22, 20.5))])


@icon("bank-teller", CAT, "Figure behind a counter window passing a banknote through the slot",
      tags=["bank teller", "cashier", "counter", "teller window", "banknote", "deposit", "withdrawal"])
def _(S):
    return (lp(S, 9) + [shell(rect(13, 3.5, 9.5, 8.5, min(S.R, 2))), line(seg(12, 14.5, 23, 14.5)),
            shell(rect(14.5, 16.5, 7, 4.5, 1)), mark(circle(18, 18.75, 0.9))])


@icon("stock-trader", CAT, "Figure with a phone at the ear beside a rising zigzag chart",
      tags=["stock trader", "broker", "trading", "stock market", "shares", "phone call", "investor"])
def _(S):
    return (lp(S, 9) + [solid(rect(11.6, 7, 2, 4.5, 0.8)), line(poly([(14.5, 20), (17, 14.5), (19, 17), (22, 9)], r=S.r)),
            line(poly([(19.5, 9), (22, 9), (22, 11.5)]))])


@icon("recruiter", CAT, "Figure with a magnifying glass over a small person on a candidate card",
      tags=["recruiter", "headhunter", "talent search", "hiring", "candidate", "hr", "job search"])
def _(S):
    return (lp(S, 9) + [shell(rect(13, 10.5, 9.5, 10.5, min(S.R, 1.5))), solid(circle(17.75, 14.3, 1.5)),
            detail("M15.4 19A2.4 2.4 0 0 1 20.1 19"), shell(circle(17.5, 5.5, 2.4)), line(seg(19.4, 7.4, 21.5, 9.5))])


@icon("salesperson", CAT, "Figure in a tie holding out a price tag",
      tags=["salesperson", "sales", "salesman", "seller", "retail", "price tag", "pitch"])
def _(S):
    tag = poly([(14, 6.5), (19, 6.5), (22.5, 10.5), (19, 14.5), (14, 14.5)], closed=True, r=S.r)
    return (person(S, 7, 10, 3.0, 16, 4.5) + [detail(poly([(5.8, 16.5), (7, 19.5), (8.2, 16.5)], r=S.r * 0.3)),
            shell(tag), mark(circle(16.5, 10.5, 1.0))])


@icon("real-estate-agent", CAT, "Figure holding a house key beside a for sale sign on a post",
      tags=["real estate agent", "realtor", "estate agent", "property", "house key", "for sale", "housing"])
def _(S):
    return (lp(S, 9) + [shell(rect(13.5, 3, 9, 7.5, min(S.R, 1.5))), detail(poly([(15.5, 8), (18, 5.5), (20.5, 8)], r=S.r * 0.2)),
            shell(circle(16, 16, 1.8)), line(seg(17.8, 16, 22, 16)), line(seg(21, 16, 21, 18.5))])


@icon("insurance-agent", CAT, "Figure holding an umbrella over a small house",
      tags=["insurance agent", "insurance", "cover", "protection", "umbrella", "home insurance", "broker"])
def _(S):
    return (lp(S, 9) + [shell("M13 8.5A4.75 5 0 0 1 22.5 8.5Z"), line(seg(17.75, 8.5, 17.75, 13)),
            shell(poly([(14.5, 21), (14.5, 16.5), (17.75, 13.5), (21, 16.5), (21, 21)], closed=True, r=S.r * 0.3))])


@icon("auditor", CAT, "Figure beside a ledger page with rows, checked with a magnifying glass",
      tags=["auditor", "audit", "inspection", "ledger", "accounts review", "compliance", "magnifying glass"])
def _(S):
    return (lp(S, 9) + [shell(rect(13, 3.5, 8, 12, min(S.R, 1.5))), detail(seg(15.5, 7.5, 18.5, 7.5)), detail(seg(15.5, 11.5, 18.5, 11.5)),
            shell(circle(19, 16.8, 2.6)), line(seg(20.9, 18.7, 22.5, 20.3))])


@icon("data-analyst", CAT, "Figure pointing at a screen showing a bar chart",
      tags=["data analyst", "analytics", "bar chart", "statistics", "insights", "reporting", "dashboard"])
def _(S):
    return (lp(S, 9) + [shell(rect(12.5, 3.5, 10, 10, min(S.R, 2))), mark(rect(14.8, 8.5, 1.7, 2.6)), mark(rect(17.5, 6, 1.7, 5.1)),
            mark(rect(20.2, 9.5, 1.5, 1.6)), line(seg(17.5, 13.5, 17.5, 17)), line(seg(14.5, 17.5, 20.5, 17.5))])


@icon("project-manager", CAT, "Figure beside a clipboard with a gantt chart of offset bars",
      tags=["project manager", "gantt chart", "schedule", "timeline", "planning", "milestones", "clipboard"])
def _(S):
    return (lp(S, 9) + [shell(rect(13, 4.5, 9.5, 16.5, min(S.R, 1.5))), solid(rect(15.5, 3, 4.5, 2.6, 0.8)),
            mark(rect(14.8, 8.5, 3.5, 1.5)), mark(rect(16.8, 12, 3.5, 1.5)), mark(rect(18.3, 15.5, 2.8, 1.5))])


@icon("presenter", CAT, "Figure pointing a stick at a board on an easel showing a rising chart",
      tags=["presenter", "presentation", "easel", "pointer", "lecture", "briefing", "meeting"])
def _(S):
    return (person(S, 6, 9, 3.0, 15, 3.8) + [shell(rect(11.5, 3.5, 11, 9, min(S.R, 1.5))),
            line(poly([(14, 10.2), (16.5, 8), (18.5, 9.2), (21, 6)], r=S.r * 0.3)), line(seg(14, 12.5, 13, 21)), line(seg(20, 12.5, 21, 21)),
            line(seg(9.8, 16.5, 13, 13.5))])


@icon("intern", CAT, "Young figure with a lanyard badge carrying a folder",
      tags=["intern", "trainee", "apprentice", "work experience", "junior", "lanyard", "folder"])
def _(S):
    return (lp(S, 9) + [detail(poly([(5, 15.5), (7.5, 19), (10, 15.5)], r=S.r * 0.3)), mark(rect(6.3, 19, 2.4, 1.8, 0.4)),
            shell("M13 21V8H17L18.2 9.8H22.5V21Z"), detail(seg(13, 13.5, 22.5, 13.5))])


@icon("job-seeker", CAT, "Figure holding out a resume sheet with a photo square and text lines",
      tags=["job seeker", "resume", "cv", "applicant", "job hunt", "unemployed", "application"])
def _(S):
    return (lp(S, 9) + [shell(rect(13, 3.5, 9.5, 17, min(S.R, 1.5))), mark(rect(15, 6, 3.2, 3.2, 0.5)), detail(seg(15, 12.5, 20.5, 12.5)),
            detail(seg(15, 16.5, 20.5, 16.5))])


@icon("employee-badge-holder", CAT, "Figure wearing a lanyard with a photo ID card on the chest",
      tags=["employee badge", "id card", "lanyard", "staff pass", "photo id", "access card", "worker"])
def _(S):
    return ([shell(circle(12, 6.5, 2.7)), line("M7 11.5L12 16L17 11.5"), shell(rect(8.5, 14.5, 7, 7, min(S.R, 1.5))),
             mark(circle(12, 17.2, 1.0)), mark(rect(10.3, 19, 3.4, 1))])


@icon("remote-worker", CAT, "Figure working at a laptop under a house roof",
      tags=["remote worker", "work from home", "telecommute", "home office", "wfh", "freelancer", "laptop"])
def _(S):
    return [line(poly([(3, 10), (12, 3.5), (21, 10)], r=S.r)), shell(circle(12, 11, 2.5)), shell(rect(6.5, 15.5, 11, 5.5, min(S.R, 1.5)))]


@icon("entrepreneur", CAT, "Figure in a blazer beside a rocket rising upward",
      tags=["entrepreneur", "startup", "founder", "launch", "rocket", "business owner", "innovation"])
def _(S):
    return (person(S, 7, 10, 3.0, 16, 4.5) + [detail(poly([(5.5, 16.5), (7, 19.5), (8.5, 16.5)], r=S.r * 0.3)),
            shell("M18 2.8C20.6 5.5 20.8 10 20.2 13.5H15.8C15.2 10 15.4 5.5 18 2.8Z"), mark(circle(18, 8, 1.2)),
            solid("M16.6 15.5L18 20.5L19.4 15.5Z")])


@icon("secretary", CAT, "Figure beside a notepad and a desk telephone",
      tags=["secretary", "personal assistant", "admin", "notes", "telephone", "office assistant", "receptionist"])
def _(S):
    return (lp(S, 9) + [shell(rect(13.5, 3.5, 9, 7, min(S.R, 1.5))), detail(seg(15.5, 7, 20.5, 7)),
            line("M14 15.5V14H22V15.5"), shell(rect(13.5, 16, 9, 5, min(S.R, 1.5)))])


@icon("architect", CAT, "Figure with a rolled blueprint and a set square",
      tags=["architect", "blueprint", "set square", "drafting", "building design", "plans", "draughtsman"])
def _(S):
    return (lp(S, 9) + [shell(rect(13, 4, 4, 16, 2)), detail(seg(13, 8, 17, 8)),
            shell(poly([(19.5, 8), (19.5, 20), (22.5, 20)], closed=True, r=S.r * 0.3))])


@icon("civil-engineer", CAT, "Figure in a hard hat beside a small suspension bridge",
      tags=["civil engineer", "engineer", "bridge", "infrastructure", "hard hat", "construction design", "structural"])
def _(S):
    cx, hy = 7.5, 10.5
    return ([shell(dome(cx, hy - 1.2, 3.9, 4.2)), line(seg(2.8, hy - 1.2, 12.2, hy - 1.2))] + person(S, cx, hy, 3.0, 16.5, 4.5)
            + [line(seg(14, 6.5, 14, 21)), line(seg(21, 6.5, 21, 21)), line("M14 6.5Q17.5 20 21 6.5"), line(seg(12.5, 18.5, 22.5, 18.5))])


@icon("surveyor", CAT, "Figure looking through a surveying instrument on a three-legged tripod",
      tags=["surveyor", "land surveying", "theodolite", "tripod", "mapping", "total station", "measurement"])
def _(S):
    return (lp(S, 9) + [shell(rect(13, 3.5, 9.5, 4.5, min(S.R, 2))), shell(rect(15.5, 8, 4.5, 3.5, 0.5)),
            line(seg(17.75, 11.5, 14, 21)), line(seg(17.75, 11.5, 17.75, 21)), line(seg(17.75, 11.5, 21.5, 21))])


@icon("interior-designer", CAT, "Figure holding a fan of color swatches",
      tags=["interior designer", "decorator", "color swatches", "palette", "home design", "decor", "paint chips"])
def _(S):
    ends = [polar(13, 20, 9.5, a) for a in (-75, -45, -15)]
    return (lp(S, 9) + [line(seg(13, 20, *e)) for e in ends] + [solid(circle(e[0], e[1], 1.5)) for e in ends])


@icon("fashion-designer", CAT, "Figure with a measuring tape around the neck beside a dress form on a stand",
      tags=["fashion designer", "tailor", "dress form", "mannequin", "measuring tape", "couture", "seamstress"])
def _(S):
    form = poly([(15.5, 6), (20.5, 6), (19.5, 11), (21.5, 16), (14.5, 16), (16.5, 11)], closed=True, r=S.r * 0.5)
    return (lp(S, 9) + [line("M4.5 15.2Q7.5 19.5 10.5 15.2"), shell(form), line(seg(18, 16, 18, 21)), line(seg(15, 21, 21, 21)),
            solid(circle(18, 4, 1.0))])


@icon("hacker-in-hoodie", CAT, "Hooded figure with a shadowed face working at a laptop",
      tags=["hacker", "hoodie", "cybersecurity", "coder", "anonymous", "laptop", "dark web"])
def _(S):
    hood = poly([(5.5, 15), (6.3, 7.5), (12, 3.2), (17.7, 7.5), (18.5, 15)], closed=True, r=L(S, 0, 3))
    return [shell(hood), mark(ellipse(12, 9.5, 3, 3.6)), shell(rect(6.5, 14.5, 11, 6.5, L(S, 0.5, 2.2)))]


@icon("system-administrator", CAT, "Figure beside a server rack with rows of status lights",
      tags=["system administrator", "sysadmin", "server room", "server rack", "it admin", "infrastructure", "data center"])
def _(S):
    leds = [mark(circle(15.7, y, 0.8)) for y in (8.2, 12.5, 16.8)]
    return (lp(S, 9) + [shell(rect(13, 3.5, 9.5, 17.5, min(S.R, 1.5))), detail(seg(13, 10.3, 22.5, 10.3)), detail(seg(13, 14.7, 22.5, 14.7))] + leds)


@icon("it-support-technician", CAT, "Figure in a headset beside a laptop with a wrench",
      tags=["it support", "help desk", "technician", "tech support", "wrench", "repair", "headset"])
def _(S):
    return (person(S, 7.5, 10, 3.0, 16, 4.5) + [line(arc(7.5, 9.8, 4.4, 180, 360)), solid(rect(2.4, 8.5, 1.8, 3.2, 0.8)),
            shell(rect(13.5, 3.5, 9, 7, min(S.R, 1.5))), line(seg(12.5, 12.5, 23, 12.5)), line(arc(19.5, 17, 2.2, 0, 270)),
            line(seg(17.9, 18.6, 14, 21))])
