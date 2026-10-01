"""TypeIcon Core: tech (cloud, data, networking and operations), batch 002."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from dsl import filled_region
from geometry import LINE, fmt, path_to_d, transform_path

CAT = "tech"

_CLOUD_LINE = "M4.5 19H19.5A3.8 3.8 0 0 0 18 11.7A6 6 0 0 0 6.5 10A4.7 4.7 0 0 0 4.5 19Z"
_CLOUD_ROUND = "M7 19H17.5A4.5 4.5 0 0 0 18 10.03A6 6 0 0 0 6.34 9.1A5 5 0 0 0 7 19Z"
_CB: dict = {}


def pk(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap):
    return min(S.R, cap)


def cloud(S, x, y, w, h):
    """Cloud outline whose centreline box is x, y, w, h."""
    d0 = pk(S, _CLOUD_LINE, _CLOUD_ROUND)
    if d0 not in _CB:
        b = P(d0).bounds
        _CB[d0] = tuple(v / 100 for v in b)
    l, t, r, b = _CB[d0]
    sx, sy = w / (r - l), h / (b - t)
    return path_to_d(transform_path(P(d0), (sx, 0, 0, sy, x - l * sx, y - t * sy)))


def behind(back, *fronts, gap=1.0, w=2.0):
    """Stroke of `back` with a clear gap around every `front` shape (a part drawn behind another)."""
    reg = ST(back, w, "round", "round")
    cut = U(*[U(P(f), ST(f, 2 + 2 * gap, "round", "round")) for f in fronts])
    return solid(path_to_d(D(reg, cut)))


def _cut_region(fronts, gap):
    return U(*[U(P(f), ST(f, 2 + 2 * gap, "round", "round")) for f in fronts])


def occlude(S, back, fronts, gap=1.0):
    """Back parts re-emitted as solid regions with a clear gap around the closed front shapes."""
    cut = _cut_region(fronts, gap)
    out = []
    for p in back:
        reg = P(p.d) if p.kind in ("dot", "solid") else ST(p.d, 2.0, S.cap, S.join)
        out.append(solid(path_to_d(D(reg, cut))))
    return out


def layered_filled(back, front, fronts, gap=1.0):
    """Filled override for a back drawing partly hidden behind a front drawing."""
    def f():
        return U(D(filled_region(back(LINE)), _cut_region(fronts, gap)), filled_region(front(LINE)))
    return f


def lens_d(c1, r1, c2, r2):
    from geometry import I, circle_d
    return path_to_d(I(P(circle_d(*c1, r1)), P(circle_d(*c2, r2))))


def corners(S, x, y, w, h, n=3.5, r=0.0):
    """Dashed-looking enclosure: four corner brackets of leg n."""
    x2, y2 = x + w, y + h
    out = []
    for (cx, cy, dx, dy) in ((x, y, 1, 1), (x2, y, -1, 1), (x2, y2, -1, -1), (x, y2, 1, -1)):
        out.append(line(poly([(cx + dx * n, cy), (cx, cy), (cx, cy + dy * n)], r=r)))
    return out


def db_d(S, x, y, w, h, ry=2.5):
    half = w / 2
    rx = half * pk(S, 1.3, 1.0)
    return f"M{fmt(x)} {fmt(y + ry)}A{fmt(rx)} {fmt(ry)} 0 0 1 {fmt(x + w)} {fmt(y + ry)}V{fmt(y + h - ry)}A{fmt(rx)} {fmt(ry)} 0 0 1 {fmt(x)} {fmt(y + h - ry)}Z"


def db_ring(S, x, y, w, ry=2.5):
    rx = w / 2 * pk(S, 1.3, 1.0)
    return f"M{fmt(x)} {fmt(y)}A{fmt(rx)} {fmt(ry)} 0 0 0 {fmt(x + w)} {fmt(y)}"


def database(S, x, y, w, h, ry=2.5, rings=1):
    parts = [shell(db_d(S, x, y, w, h, ry)), detail(db_ring(S, x, y + ry, w, ry))]
    for i in range(1, rings):
        parts.append(detail(db_ring(S, x, y + ry + (h - 2 * ry) * i / rings, w, ry)))
    return parts


def arrow_head(tip, direction, size=3.0, r=0.0):
    """Open chevron arrowhead pointing in `direction` degrees (0 = right, 90 = down)."""
    a = math.radians(direction)
    x, y = tip
    p1 = (x - size * math.cos(a - math.pi / 4), y - size * math.sin(a - math.pi / 4))
    p2 = (x - size * math.cos(a + math.pi / 4), y - size * math.sin(a + math.pi / 4))
    return line(poly([p1, tip, p2], r=r))


# ============================================================================ cloud and compute

@icon("cloud-server", CAT, "A cloud sitting on top of a server box",
      tags=["cloud hosting", "server", "hosting", "saas", "infrastructure", "iaas", "remote server"])
def _(S):
    return [shell(cloud(S, 5, 2.5, 14, 8.5)),
            shell(rect(4.5, 13.5, 15, 7.5, rr(S, 2))),
            dot(8.5, 17.25, 1), detail(seg(12.5, 17.25, 16, 17.25))]


@icon("cloud-backup", CAT, "A cloud holding a counter-clockwise history arrow with clock hands",
      tags=["backup", "restore", "cloud storage", "snapshot", "history", "recovery", "versions"])
def _(S):
    cx, cy, r = 12, 13.4, 3.6
    a0 = math.radians(130)
    return [shell(cloud(S, 2, 3, 20, 17.5)),
            detail(arc(cx, cy, r, 130, 400)),
            detail(poly([(cx + r * math.cos(a0) - 2.2, cy + r * math.sin(a0) - 0.6), (cx + r * math.cos(a0), cy + r * math.sin(a0)),
                         (cx + r * math.cos(a0) + 0.4, cy + r * math.sin(a0) - 2.4)])),
            detail(poly([(cx, cy - 1.5), (cx, cy), (cx + 1.5, cy + 1)]))]


@icon("multi-cloud", CAT, "Three overlapping clouds of different sizes",
      tags=["multicloud", "cloud providers", "clouds", "vendor", "cross cloud", "cloud strategy"])
def _(S):
    big = cloud(S, 2.5, 3.5, 12.5, 9.5)
    small = cloud(S, 13.5, 3, 8, 6.5)
    front = cloud(S, 7, 11.5, 14.5, 9)
    return [behind(big, front, gap=1.0), behind(small, front, gap=1.0), shell(front)]


@icon("hybrid-cloud", CAT, "A cloud linked by a line to a small office building",
      tags=["on premises", "on-prem", "hybrid", "cloud and datacenter", "enterprise", "private and public cloud"])
def _(S):
    return [shell(cloud(S, 2, 3, 13.5, 9.5)),
            shell(rect(16, 9, 5.5, 12, rr(S, 1.5))),
            dot(18.75, 12.5, 1), dot(18.75, 16, 1),
            line(poly([(8.5, 12.5), (8.5, 18.5), (16, 18.5)], r=S.r))]


@icon("private-cloud", CAT, "A cloud enclosed by a bracketed fence",
      tags=["secure cloud", "private", "dedicated", "walled", "enclosed", "virtual private cloud", "vpc"])
def _(S):
    return [*corners(S, 2.5, 3.5, 19, 17, 4.5, S.r),
            shell(cloud(S, 6, 7.5, 12, 9))]


@icon("cloud-region", CAT, "A map pin standing on a cloud",
      tags=["region", "data center location", "geo", "location", "datacenter", "availability", "cloud map"])
def _(S):
    pin = "M12 14.5C10 12.5 7.2 9.5 7.2 6.2A4.8 4.8 0 0 1 16.8 6.2C16.8 9.5 14 12.5 12 14.5Z"
    base = cloud(S, 2.5, 12, 19, 8.5)
    return [behind(pin, base, gap=1.0), shell(base), dot(12, 6.2, 1.5)]


@icon("availability-zone", CAT, "Three tall separate zone boxes side by side, each marked with a server slot",
      tags=["az", "zone", "redundancy", "fault tolerance", "data center", "failure domain", "isolated"])
def _(S):
    parts = []
    for x in (3, 10.2, 17.4):
        parts.append(shell(rect(x, 4, 3.6, 16, pk(S, 0.6, 1.8))))
        parts.append(detail(seg(x, 12, x + 3.6, 12)))
    return parts


@icon("virtual-machine", CAT, "A dashed monitor outline with a smaller solid monitor inside",
      tags=["vm", "guest", "virtual", "emulation", "virtualization", "instance"])
def _(S):
    return [*corners(S, 2.5, 3, 19, 14.5, 4, S.r * 0.6),
            shell(rect(7.5, 7, 9, 6, rr(S, 1.5))),
            line(seg(12, 17.5, 12, 20.5)), line(seg(8, 20.5, 16, 20.5))]


@icon("hypervisor", CAT, "A thick layer bar supporting three small windows",
      tags=["virtualization layer", "vm host", "host machine", "virtual machine monitor", "vmm"])
def _(S):
    parts = [shell(rect(2.5, 15.5, 19, 5.5, rr(S, 3)))]
    for x in (2.5, 9.25, 16):
        parts.append(solid(rect(x, 4, 5.5, 8.5, pk(S, 0.5, 2))))
    return parts


@icon("container-registry", CAT, "Two stacked shipping containers with a label tag beside them",
      tags=["image registry", "images", "container images", "repository", "devops", "artifact store"])
def _(S):
    return [shell(rect(2.5, 3.5, 9.5, 15, rr(S, 2))),
            detail(seg(2.5, 11, 12, 11)),
            detail(seg(7.25, 6, 7.25, 8.5)), detail(seg(7.25, 13.5, 7.25, 16)),
            line(seg(2, 21.5, 13, 21.5)),
            shell(poly([(18.25, 3.5), (21.5, 7), (21.5, 20.5), (15, 20.5), (15, 7)], closed=True, r=S.r * 0.4)),
            dot(18.25, 8.5, 1.1), detail(seg(17, 13, 19.5, 13)), detail(seg(17, 16.5, 19.5, 16.5))]


@icon("autoscaling", CAT, "Three bars of growing height under an upward growth arrow",
      tags=["auto scaling", "scale out", "elastic", "capacity", "load", "grow", "elasticity"])
def _(S):
    parts = [solid(rect(2.5, 15, 4.5, 5.5, rr(S, 1))), solid(rect(9.75, 11, 4.5, 9.5, rr(S, 1))),
             solid(rect(17, 6.5, 4.5, 14, rr(S, 1)))]
    parts += [line(poly([(3.5, 9.5), (9.5, 3.5)])), arrow_head((9.5, 3.5), -45 + 0, 3.5, 0)]
    return parts


@icon("horizontal-scaling", CAT, "Two identical server boxes with a plus sign adding another",
      tags=["scale out", "add nodes", "more servers", "cluster", "scale horizontally", "replicas", "capacity"])
def _(S):
    parts = []
    for x in (3, 11):
        parts += [shell(rect(x, 6, 4, 12, rr(S, 1.5))), detail(seg(x, 12, x + 4, 12))]
    parts += [line(seg(19.5, 9.5, 19.5, 14.5)), line(seg(17, 12, 22, 12))]
    return parts


@icon("vertical-scaling", CAT, "A server box growing taller with a stretch arrow beside it",
      tags=["scale up", "bigger server", "resize", "more resources", "upgrade instance", "scale vertically"])
def _(S):
    return [shell(rect(3, 8.5, 12, 12.5, rr(S, 2))),
            detail(seg(3, 13, 15, 13)), detail(seg(3, 17, 15, 17)),
            dot(6.5, 10.75, 0.9), dot(6.5, 15, 0.9), dot(6.5, 19, 0.9),
            line(seg(19, 21, 19, 4)), arrow_head((19, 3.5), -90, 3.2, S.r * 0.3)]


@icon("high-availability", CAT, "Two server boxes joined by a heartbeat line",
      tags=["ha", "uptime", "redundancy", "heartbeat", "cluster", "always on", "resilience"])
def _(S):
    return [shell(rect(4, 3, 16, 5, rr(S, 1.5))), shell(rect(4, 16, 16, 5, rr(S, 1.5))),
            dot(7.5, 5.5, 0.9), dot(7.5, 18.5, 0.9),
            line(poly([(2, 12), (7.5, 12), (10, 9.5), (13, 14.5), (15.5, 12), (22, 12)], r=S.r * 0.5))]


@icon("failover", CAT, "A server with a crossed status light and an arrow jumping to a second server",
      tags=["switchover", "standby", "backup server", "redundancy", "outage", "disaster", "secondary"])
def _(S):
    return [shell(rect(2.5, 11, 8, 10, rr(S, 2))), shell(rect(13.5, 11, 8, 10, rr(S, 2))),
            line(seg(5.5, 14, 7.5, 18)), line(seg(7.5, 14, 5.5, 18)),
            dot(17.5, 16, 1.2),
            line("M6.5 8A5.5 4 0 0 1 17.5 8"), arrow_head((17.5, 8.5), 90, 3, S.r * 0.3)]


# ============================================================================ databases and data

@icon("data-replication", CAT, "A database cylinder with a copy arrow pointing to an identical cylinder",
      tags=["replica", "copy data", "mirror", "sync", "standby database", "read replica", "duplicate"])
def _(S):
    return [*database(S, 2.5, 2.5, 9.5, 9.5, 2.2), *database(S, 12, 12, 9.5, 9.5, 2.2),
            line(poly([(14.5, 6), (18.5, 6), (18.5, 9.5)], r=S.r)), arrow_head((18.5, 10), 90, 3, S.r * 0.3)]


def _shard_slices(S):
    ry = pk(S, 2.0, 2.4)
    out = []
    for y in (2.5, 9.6, 16.7):
        out.append(f"M3 {fmt(y + ry)}A9 {fmt(ry)} 0 0 1 21 {fmt(y + ry)}V{fmt(y + 4.8 - ry)}A9 {fmt(ry)} 0 0 1 3 {fmt(y + 4.8 - ry)}Z")
    return out


def _shard_filled():
    parts = [P(d) for d in _shard_slices(LINE)]
    top_ring = ST(f"M3 {fmt(2.5 + 2.0)}A9 2 0 0 0 21 {fmt(2.5 + 2.0)}", 1.2, "butt", "miter")
    return U(D(parts[0], top_ring), parts[1], parts[2])


@icon("database-shard", CAT, "A database cylinder cut into three separated flat slices",
      tags=["sharding", "partition", "horizontal partition", "split database", "slices", "distributed data"],
      filled=_shard_filled)
def _(S):
    return [solid(d) for d in _shard_slices(S)]


@icon("database-index", CAT, "A database cylinder with a bookmark tab sticking out beside it",
      tags=["index", "lookup", "b-tree", "fast query", "bookmark", "sql index", "search key"])
def _(S):
    return [*database(S, 2.5, 3, 11, 18, 2.5, rings=2),
            shell(poly([(16.5, 6), (21.5, 6), (21.5, 17), (19, 14.5), (16.5, 17)], closed=True, r=S.r * 0.4))]


@icon("database-transaction", CAT, "A database cylinder with two opposite exchange arrows on its front",
      tags=["commit", "rollback", "acid", "transfer", "sql transaction", "exchange", "atomic"])
def _(S):
    return [shell(db_d(S, 3, 3, 18, 18, 2.8)), detail(db_ring(S, 3, 5.8, 18, 2.8)),
            detail(seg(7, 11.5, 16.5, 11.5)), detail(poly([(14, 9.5), (16.5, 11.5), (14, 13.5)])),
            detail(seg(7.5, 16.5, 17, 16.5)), detail(poly([(10, 14.5), (7.5, 16.5), (10, 18.5)]))]


@icon("primary-key", CAT, "A key with the number one on its round bow",
      tags=["pk", "unique id", "identifier", "table key", "sql", "record id", "unique key"])
def _(S):
    return [shell(circle(8, 8, 5.5)),
            detail(poly([(6.2, 7), (8.2, 5.5), (8.2, 10.5)])),
            line(seg(12, 12, 21, 21)), line(seg(15.5, 15.5, 13.5, 17.5)), line(seg(19, 19, 17, 21))]


@icon("sql-join", CAT, "Two overlapping circles with only the shared lens area filled",
      tags=["inner join", "intersection", "overlap", "venn", "sql", "matching rows", "merge tables"])
def _(S):
    c1, c2, r = (8.8, 12), (15.2, 12), 7
    lens = lens_d(c1, r, c2, r)
    from geometry import circle_d
    inner = path_to_d(D(P(lens), ST(lens, 2.4, "round", "round"))) if S.name == "rounded" else lens
    return [line(circle(*c1, r)), line(circle(*c2, r)), solid(inner)]


@icon("full-outer-join", CAT, "Two overlapping circles fully filled with the overlap outlined",
      tags=["outer join", "union", "all rows", "venn", "sql", "combine tables", "merge"],
      filled=lambda: D(U(P(circle(8.8, 12, 7.5)), P(circle(15.2, 12, 7.5))), P(lens_d((8.8, 12), 7.5, (15.2, 12), 7.5))))
def _(S):
    r = pk(S, 7.5, 7)
    c1, c2 = (pk(S, 8.8, 8.6), 12), (pk(S, 15.2, 15.4), 12)
    lens = lens_d(c1, r, c2, r)
    reg = D(U(P(circle(*c1, r)), P(circle(*c2, r))), ST(lens, pk(S, 1.3, 1.9), "round", "round"))
    return [solid(path_to_d(reg))]


def _sp_back(S):
    return database(S, 2.5, 2.5, 12, 16, 2.5)


def _sp_front(S):
    return [shell(rect(10.5, 10.5, 11, 11, rr(S, 2))), detail(seg(13.5, 14.5, 18.5, 14.5)), detail(seg(13.5, 17.5, 16.5, 17.5))]


@icon("stored-procedure", CAT, "A database cylinder with a small page of code lines in front of it",
      tags=["procedure", "sql function", "routine", "trigger", "plsql", "server side code", "database script"],
      filled=layered_filled(_sp_back, _sp_front, [rect(10.5, 10.5, 11, 11, 2)]))
def _(S):
    return [*occlude(S, _sp_back(S), [rect(10.5, 10.5, 11, 11, rr(S, 2))]), *_sp_front(S)]


@icon("key-value-store", CAT, "A key above two columns of small cells, a short key cell and a wide value cell per row",
      tags=["kv store", "dictionary", "hash map", "nosql", "lookup table", "cache"])
def _(S):
    k = pk(S, 0.4, 1.2)
    return [shell(circle(5.5, 5.5, 2.75)), line(seg(8.25, 5.5, 16, 5.5)), line(seg(13, 5.5, 13, 8.5)),
            solid(rect(2.5, 12, 6, 3.5, k)), solid(rect(11, 12, 10.5, 3.5, k)),
            solid(rect(2.5, 17.5, 6, 3.5, k)), solid(rect(11, 17.5, 10.5, 3.5, k))]


@icon("document-database", CAT, "A stack of document pages resting on a database cylinder",
      tags=["nosql", "json store", "collection", "documents", "records", "object store"])
def _(S):
    return [shell(poly([(7.5, 2.5), (13, 2.5), (16.5, 6), (16.5, 10.5), (7.5, 10.5)], closed=True, r=S.r * 0.4)),
            detail(poly([(13, 2.5), (13, 6), (16.5, 6)])),
            line(seg(4.5, 5, 4.5, 11)),
            *database(S, 3.5, 13.5, 17, 8, 2.2)]


@icon("time-series-database", CAT, "A database cylinder with a zigzag line chart across its front",
      tags=["tsdb", "metrics store", "timeseries", "telemetry", "sensor data", "monitoring data"])
def _(S):
    return [shell(db_d(S, 3, 3, 18, 18, 2.8)), detail(db_ring(S, 3, 5.8, 18, 2.8)),
            detail(poly([(6.5, 17.5), (10, 13), (13, 15.5), (17.5, 10.5)], r=S.r * 0.5))]


@icon("vector-database", CAT, "A database cylinder with three arrows fanning out from one point on its front",
      tags=["embeddings", "vector store", "similarity search", "ai database", "semantic search", "rag", "nearest neighbour"])
def _(S):
    ox, oy = 7.5, 17
    return [shell(db_d(S, 3, 3, 18, 18, 2.8)), detail(db_ring(S, 3, 5.8, 18, 2.8)),
            dot(ox, oy, 1.2),
            detail(seg(ox, oy, 15, 11.5)), detail(seg(ox, oy, 17.5, 15)), detail(seg(ox, oy, 12, 10.5))]


@icon("data-lake", CAT, "A lake shape with the digits one, zero and one floating above its surface",
      tags=["raw data", "data warehouse", "storage", "big data", "bits", "binary", "object storage"])
def _(S):
    lake = pk(S, "M2 17.5L5 14L12 12.5L19 14L22 17.5L19 20.5L12 21.5L5 20.5Z",
              "M2.5 17C2.5 14.5 6.5 12.5 12 12.5S21.5 14.5 21.5 17S17.5 21.5 12 21.5S2.5 19.5 2.5 17Z")
    def one(x):
        return line(poly([(x - 1.6, 4.4), (x, 3), (x, 8.5)]))
    zero = shell(rect(10.4, 3, 3.2, 5.5, pk(S, 0.3, 1.6)))
    return [shell(lake), one(5.5), line(poly([(16.4, 4.4), (18, 3), (18, 8.5)])), zero]


@icon("data-lineage", CAT, "Three nodes chained left to right with a branch splitting from the middle node",
      tags=["data flow", "provenance", "pipeline graph", "etl", "upstream downstream", "dependency graph", "traceability"])
def _(S):
    nd = lambda x, y: shell(rect(x - 2.5, y - 2.5, 5, 5, pk(S, 0.3, 2.5)))  # noqa: E731
    return [nd(4.5, 12), nd(12, 12), nd(19.5, 6.5), nd(19.5, 17.5),
            line(seg(7, 12, 9.5, 12)),
            line(seg(14.4, 11, 17.2, 7.8)),
            line(seg(14.4, 13, 17.2, 16.2))]


def _catalog_back(S):
    return [line(poly([(5.5, 9), (5.5, 4), (18.5, 4), (18.5, 9)], r=S.r * 0.5))]


@icon("data-catalog", CAT, "A card index box holding cards, with a small database cylinder on the front card",
      tags=["metadata", "data inventory", "data discovery", "index cards", "data governance", "datasets", "data dictionary"])
def _(S):
    return [shell(rect(2.5, 8.5, 19, 12.5, rr(S, 2))), *_catalog_back(S),
            shell(db_d(S, 9, 11.5, 6, 6, 2)), detail(db_ring(S, 9, 13.5, 6, 2))]


@icon("big-data", CAT, "A database cylinder surrounded by a ring of small dots",
      tags=["massive data", "data volume", "analytics", "data science", "many records", "data deluge"])
def _(S):
    parts = [shell(db_d(S, 8, 7, 8, 10, 2)), detail(db_ring(S, 8, 9, 8, 2))]
    for i in range(8):
        a = math.radians(i * 45)
        parts.append(dot(12 + 9.4 * math.cos(a), 12 + 9.4 * math.sin(a), 1.2))
    return parts


@icon("data-mining", CAT, "A pickaxe striking a small pile of ones and zeros",
      tags=["extraction", "knowledge discovery", "pattern finding", "dig", "analytics", "pickaxe", "machine learning"])
def _(S):
    return [line(seg(10.5, 14.5, 18, 6)),
            line("M10.5 4Q20 3 20.8 12.5"),
            line(poly([(3, 17.5), (4.5, 16), (4.5, 21.5)])),
            shell(rect(8, 16, 3.5, 5.5, pk(S, 0.3, 1.7))),
            line(poly([(14.5, 17.5), (16, 16), (16, 21.5)]))]


@icon("data-cleaning", CAT, "A broom sweeping across a small table grid",
      tags=["data cleansing", "scrub", "data quality", "tidy data", "preprocessing", "wrangling", "deduplicate"])
def _(S):
    return [shell(rect(2.5, 3, 12.5, 10.5, rr(S, 2))), detail(seg(2.5, 8.25, 15, 8.25)), detail(seg(8.75, 3, 8.75, 13.5)),
            line(seg(21.5, 4, 15.5, 12.5)),
            shell(poly([(13, 12.5), (18, 16), (14.5, 21.5), (7, 19), (9.5, 15)], closed=True, r=S.r * 0.5)),
            detail(seg(11.5, 17, 14, 19.5))]


def _dns_back(S):
    return [shell(rect(2.5, 2.5, 14, 15, rr(S, 2))), detail(seg(2.5, 7.5, 16.5, 7.5)), detail(seg(2.5, 12.5, 16.5, 12.5)),
            dot(6, 5, 0.9), dot(6, 10, 0.9), dot(6, 15, 0.9)]


def _dns_front(S):
    return [shell(rect(10.5, 11.5, 11, 10, rr(S, 2))), detail(seg(14, 11.5, 14, 21.5)),
            detail(seg(16.5, 15, 19, 15)), detail(seg(16.5, 18, 19, 18))]


@icon("dns-server", CAT, "A server box with a small address book in front of it",
      tags=["name server", "domain name system", "resolver", "nameserver", "lookup", "records"],
      filled=layered_filled(_dns_back, _dns_front, [rect(10.5, 11.5, 11, 10, 2)]))
def _(S):
    return [*occlude(S, _dns_back(S), [rect(10.5, 11.5, 11, 10, rr(S, 2))]), *_dns_front(S)]


@icon("domain-name", CAT, "A globe above a web address bar with a dot in it",
      tags=["website name", "web address", "hostname", "dns", "url", "registrar", ".com"])
def _(S):
    return [shell(circle(12, 8, 5.5)), detail(ellipse(12, 8, 2.4, 5.5)), detail(seg(6.5, 8, 17.5, 8)),
            shell(rect(2.5, 16.5, 19, 5, rr(S, 2.5))), dot(6.5, 19, 1), detail(seg(10.5, 19, 18, 19))]


@icon("ip-address", CAT, "A map pin holding four dots like the parts of an address",
      tags=["ipv4", "ip", "network address", "host address", "dotted quad", "location", "geolocation"])
def _(S):
    pin = pk(S, "M12 22L5.3 14.6A8 8 0 1 1 18.7 14.6Z", "M12 22C12 22 4 14.5 4 9.5A8 8 0 0 1 20 9.5C20 14.5 12 22 12 22Z")
    return [shell(pin), dot(9, 8, 1.4), dot(15, 8, 1.4), dot(9, 12.5, 1.4), dot(15, 12.5, 1.4)]


@icon("subnet", CAT, "A large rounded box divided into four smaller boxes, each with a dot",
      tags=["subnetwork", "cidr", "network segment", "vlan", "address range", "netmask", "ip range"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, S.R)), detail(seg(12, 2.5, 12, 21.5)), detail(seg(2.5, 12, 21.5, 12)),
            dot(7.25, 7.25, 1.4), dot(16.75, 7.25, 1.4), dot(7.25, 16.75, 1.4), dot(16.75, 16.75, 1.4)]


@icon("network-gateway", CAT, "A gateway arch with an arrow of traffic passing through it",
      tags=["gateway", "router gateway", "default gateway", "entry point", "portal", "api gateway", "ingress"])
def _(S):
    return [line(poly([(3.5, 21), (3.5, 11), (5, 7), (8, 4.5), (12, 3.5), (16, 4.5), (19, 7), (20.5, 11), (20.5, 21)], r=S.r))
            if S.name == "rounded" else line("M3.5 21V11A8.5 8 0 0 1 20.5 11V21"),
            line(seg(12, 21, 12, 9.5)), line(poly([(8.5, 12.5), (12, 9), (15.5, 12.5)], r=S.r * 0.3))]


@icon("network-packet", CAT, "A small parcel box with a header strip and a row of binary dots",
      tags=["data packet", "frame", "datagram", "payload", "tcp", "ip packet", "bits"])
def _(S):
    return [shell(rect(4, 3, 16, 18, rr(S, 2.5))), detail(seg(4, 8.5, 20, 8.5)),
            dot(8, 14.5, 1.1), dot(12, 14.5, 1.1), dot(16, 14.5, 1.1)]


@icon("packet-loss", CAT, "A row of three small packets where the middle one is broken into two pieces",
      tags=["dropped packets", "lost data", "broken packet", "network error", "unreliable", "connection problem", "udp"])
def _(S):
    return [shell(rect(3, 9.5, 4, 5, rr(S, 1.5))), shell(rect(17, 9.5, 4, 5, rr(S, 1.5))),
            solid(poly([(9.5, 8), (13.5, 8), (9.5, 12.2)], closed=True, r=S.r * 0.3)),
            solid(poly([(14.5, 11.8), (14.5, 16), (10.5, 16)], closed=True, r=S.r * 0.3))]


@icon("network-latency", CAT, "Two dots joined by a line with an hourglass in the middle",
      tags=["delay", "lag", "response time", "ping time", "round trip", "slow connection", "wait"])
def _(S):
    return [dot(3.5, 12, 2.2), dot(20.5, 12, 2.2), line(seg(5.7, 12, 9.5, 12)), line(seg(14.5, 12, 18.3, 12)),
            shell(poly([(9, 5.5), (15, 5.5), (12, 12), (15, 18.5), (9, 18.5), (12, 12)], closed=True, r=S.r * 0.3))]


@icon("ping-network", CAT, "A dot sending concentric arcs toward a second dot",
      tags=["ping", "icmp", "echo request", "reachability", "connectivity test", "signal", "network test"])
def _(S):
    return [dot(3.5, 12, 2), line(arc(3.5, 12, 6, -42, 42)), line(arc(3.5, 12, 10.5, -42, 42)), dot(20.5, 12, 2)]


@icon("traceroute", CAT, "A dashed path hopping across three dots to a small flag",
      tags=["trace route", "hops", "network path", "tracert", "route trace", "diagnostics", "path"])
def _(S):
    return [dot(4, 18, 1.8), dot(8.5, 10.5, 1.8), dot(14, 17, 1.8),
            line(seg(5, 15.5, 7.4, 12.8)), line(seg(10.2, 12.4, 12.5, 14.8)), line(seg(16, 16.2, 17.5, 16)),
            line(seg(18.5, 3.5, 18.5, 19.5)), solid(poly([(18.5, 3.5), (22.5, 5.5), (18.5, 7.5)], closed=True, r=0))]


@icon("port-number", CAT, "A wall socket plate below a hash sign",
      tags=["tcp port", "udp port", "socket number", "network port", "8080", "listening port", "service port"])
def _(S):
    return [line(seg(10.4, 2, 9.2, 9)), line(seg(15.4, 2, 14.2, 9)), line(seg(7.5, 4, 17, 4)), line(seg(7, 7, 16.5, 7)),
            shell(rect(3.5, 12, 17, 9.5, rr(S, 3))), detail(seg(9, 15, 9, 18.5)), detail(seg(15, 15, 15, 18.5))]


@icon("http-request", CAT, "An arrow going from a browser window to a server box",
      tags=["request", "get request", "web request", "client server", "fetch", "rest call", "browser to server"])
def _(S):
    return [shell(rect(2.5, 3, 12, 8.5, rr(S, 2))), detail(seg(2.5, 6.5, 14.5, 6.5)),
            line(poly([(6, 11.5), (6, 17.5), (12, 17.5)], r=S.r)), arrow_head((12.5, 17.5), 0, 3, S.r * 0.3),
            shell(rect(15.5, 12.5, 6, 9, rr(S, 1.5))), dot(18.5, 15.5, 0.8), dot(18.5, 18.5, 0.8)]


# ============================================================================ networking

@icon("api-endpoint", CAT, "A line running from angle brackets to a target circle with a filled centre",
      tags=["endpoint", "api", "route", "rest endpoint", "url target", "webhook", "service address"])
def _(S):
    return [line(poly([(5.5, 8), (2.5, 12), (5.5, 16)], r=S.r * 0.4)), line(seg(7.5, 12, 12.5, 12)),
            shell(circle(17.5, 12, 4.5)), dot(17.5, 12, 1.5)]


@icon("sdk-toolkit", CAT, "A toolbox with angle code brackets on its front",
      tags=["sdk", "software development kit", "developer tools", "library", "toolkit", "programming", "dev kit"])
def _(S):
    return [shell(rect(2.5, 8, 19, 13, rr(S, 2.5))), line(poly([(8, 8), (8, 4), (16, 4), (16, 8)], r=S.r * 0.5)),
            detail(seg(2.5, 12, 21.5, 12)),
            detail(poly([(10.2, 14.2), (8.2, 16.5), (10.2, 18.8)], r=S.r * 0.3)),
            detail(poly([(13.8, 14.2), (15.8, 16.5), (13.8, 18.8)], r=S.r * 0.3))]


@icon("websocket", CAT, "Two plugs facing each other below a double headed arrow",
      tags=["ws", "realtime", "two way connection", "persistent connection", "socket", "live updates", "bidirectional"])
def _(S):
    return [line(seg(4.5, 4.5, 19.5, 4.5)), arrow_head((3.5, 4.5), 180, 2.8, S.r * 0.3), arrow_head((20.5, 4.5), 0, 2.8, S.r * 0.3),
            shell(rect(2.5, 10.5, 5, 10, rr(S, 2))), line(seg(7.5, 13.5, 11.2, 13.5)), line(seg(7.5, 17.5, 11.2, 17.5)),
            shell(rect(16.5, 10.5, 5, 10, rr(S, 2))), line(seg(16.5, 13.5, 12.8, 13.5)), line(seg(16.5, 17.5, 12.8, 17.5))]


@icon("query-string", CAT, "A chain link above a question mark and an equals sign",
      tags=["url parameters", "query params", "get parameters", "search params", "url", "key value pairs", "link"])
def _(S):
    k = pk(S, 2, 3)
    return [line(rect(2.5, 3.5, 11, 6, k)), line(rect(10.5, 3.5, 11, 6, k)),
            line("M3.5 15.2A2.4 2.4 0 1 1 7.4 17C6.4 17.7 5.9 18.2 5.9 19.2"), dot(5.9, 21.2, 0.8),
            line(seg(12.5, 16, 21, 16)), line(seg(12.5, 20, 21, 20))]


@icon("url-slug", CAT, "A slug with two antennae and a chain link floating above its back",
      tags=["slug", "permalink", "readable url", "seo url", "link", "page name", "friendly url"])
def _(S):
    body = "M2.5 20.5C4 18 5.5 16.5 9 16.5H13.5C14 13.5 15.5 12 18 12C20 12 21.5 13.5 21.5 16.5V20.5Z"
    return [shell(body), line(seg(17.2, 12, 16, 8)), line(seg(20.2, 12.3, 21.2, 8)), dot(19.4, 16, 1),
            shell(rect(4.5, 8.5, 8.5, 4.5, pk(S, 1.5, 2.25)))]


@icon("lan-network", CAT, "Three computers on a single line under a house roof",
      tags=["local area network", "office network", "home network", "ethernet", "switch", "intranet", "local network"])
def _(S):
    k = pk(S, 0.4, 1.4)
    return [line(poly([(2.5, 9), (12, 3), (21.5, 9)], r=S.r * 0.5)),
            line(seg(4.75, 12.5, 19.25, 12.5)),
            line(seg(4.75, 12.5, 4.75, 15.5)), line(seg(12, 12.5, 12, 15.5)), line(seg(19.25, 12.5, 19.25, 15.5)),
            solid(rect(2, 15.5, 5.5, 5, k)), solid(rect(9.25, 15.5, 5.5, 5, k)), solid(rect(16.5, 15.5, 5.5, 5, k))]


@icon("wan-network", CAT, "A globe linked to three small nodes around it",
      tags=["wide area network", "internet link", "global network", "remote sites", "branch offices", "carrier", "worldwide"])
def _(S):
    k = pk(S, 0.4, 1.2)
    return [shell(circle(12, 11.5, 5.5)), detail(ellipse(12, 11.5, 2.4, 5.5)), detail(seg(6.5, 11.5, 17.5, 11.5)),
            solid(rect(2, 2, 4, 4, k)), solid(rect(18, 2, 4, 4, k)), solid(rect(10, 19, 4, 4, k)),
            line(seg(6, 6, 8.2, 8.2)), line(seg(18, 6, 15.8, 8.2)), line(seg(12, 17, 12, 19))]


@icon("ring-topology", CAT, "Six nodes evenly spaced around a circular ring",
      tags=["token ring", "network topology", "loop network", "circular network", "nodes", "network layout", "daisy chain"])
def _(S):
    parts = [line(circle(12, 12, 8))]
    for i in range(6):
        x, y = 12 + 8 * math.cos(math.radians(i * 60 - 90)), 12 + 8 * math.sin(math.radians(i * 60 - 90))
        parts.append(solid(rect(x - 2.2, y - 2.2, 4.4, 4.4, pk(S, 0.3, 2.2))))
    return parts


@icon("bus-topology", CAT, "A horizontal backbone line with small nodes hanging above and below it",
      tags=["network topology", "backbone", "bus network", "linear network", "ethernet bus", "nodes", "trunk"])
def _(S):
    k = pk(S, 0.4, 1.3)
    parts = [line(seg(2, 12, 22, 12))]
    for x in (5.5, 12, 18.5):
        parts += [line(seg(x, 7.5, x, 12)), solid(rect(x - 2.4, 3, 4.8, 4.8, k))]
    for x in (8.75, 15.25):
        parts += [line(seg(x, 12, x, 16.5)), solid(rect(x - 2.4, 16.2, 4.8, 4.8, k))]
    return parts


def _osi_bars(h, S=None):
    return [rect(3, 2.75 + 3 * i, 18, h, 0.85 if S is None or S.name == "rounded" else 0) for i in range(7)]


@icon("osi-layers", CAT, "Seven thin bars stacked in a column",
      tags=["osi model", "seven layers", "network layers", "protocol layers", "networking model", "layered", "stack"],
      filled=lambda: U(*[P(rect(3, 2.35 + 3 * i, 18, 2.2, 0)) for i in range(7)]))
def _(S):
    return [solid(d) for d in _osi_bars(1.5, S)]


@icon("protocol-stack", CAT, "Four stacked bars with a small arrow running down the side",
      tags=["tcp ip stack", "network stack", "layers", "encapsulation", "protocol layers", "networking", "layer model"])
def _(S):
    k = pk(S, 0.4, 1.7)
    return [solid(rect(2.5, 2.5 + 5.2 * i, 14, 3.5, k)) for i in range(4)] + \
           [line(seg(20, 3.5, 20, 19)), arrow_head((20, 20.5), 90, 2.8, S.r * 0.3)]


@icon("patch-panel", CAT, "A long horizontal panel with two rows of small square ports",
      tags=["network patch", "cable panel", "server rack", "ethernet ports", "cabling", "wiring closet", "rj45"])
def _(S):
    parts = [shell(rect(2, 5.5, 20, 13, rr(S, 2)))]
    for y in (8.7, 12.8):
        for i in range(4):
            parts.append(Part("dot", rect(3.9 + 4.6 * i, y, 2.8, 2.6, pk(S, 0.2, 0.9))))
    return parts


@icon("wireless-access-point", CAT, "A flat round disc with wifi arcs rising above it",
      tags=["wap", "wifi router", "wireless router", "hotspot", "ap", "wi-fi", "ceiling access point"])
def _(S):
    return [shell(rect(3, 17, 18, 4.5, rr(S, 2.25))),
            dot(12, 13.2, 1.3),
            line(arc(12, 13.2, 4, -135, -45)), line(arc(12, 13.2, 7.6, -135, -45)), line(arc(12, 13.2, 11.2, -135, -45))]


@icon("fiber-optic-cable", CAT, "A cable ending in a connector tip with light rays bursting out of it",
      tags=["fibre optic", "optical fiber", "light signal", "broadband", "fiber internet", "glass cable", "laser"])
def _(S):
    return [shell(rect(2, 9.5, 8.5, 5, rr(S, 2))), shell(rect(10.5, 10.5, 3.5, 3, pk(S, 0.3, 1.2))),
            line(seg(17, 12, 22.5, 12)), line(seg(16.5, 9, 20.5, 5)), line(seg(16.5, 15, 20.5, 19))]


@icon("sfp-transceiver", CAT, "A small rectangular network module with a pull-tab loop and contact teeth",
      tags=["sfp", "optical module", "gbic", "network module", "transceiver", "switch port", "fibre module"])
def _(S):
    return [shell(rect(9, 5, 12.5, 10.5, rr(S, 2))), line(poly([(9, 8), (5.5, 8), (5.5, 12.5), (9, 12.5)], r=S.r)),
            detail(seg(9, 10.25, 21.5, 10.25)),
            *[solid(rect(11 + 2.6 * i, 17, 1.4, 3.5, 0)) for i in range(4)]]


@icon("iot-device", CAT, "A small chip with wifi arcs above it inside a house outline",
      tags=["smart home", "connected device", "internet of things", "home automation", "smart device", "wireless chip", "embedded"])
def _(S):
    return [shell(poly([(3, 10.5), (12, 2.5), (21, 10.5), (21, 21.5), (3, 21.5)], closed=True, r=S.r)),
            dot(12, 14.2, 1.1), detail(arc(12, 14.2, 3.4, -135, -45)), detail(arc(12, 14.2, 6.4, -135, -45)),
            detail(seg(10, 17.5, 14, 17.5))]


@icon("sensor-node", CAT, "A circle with a centre dot and short signal waves on both sides",
      tags=["wireless sensor", "mote", "node", "telemetry", "measurement", "iot sensor", "transmit"])
def _(S):
    return [shell(circle(12, 12, 3.6)), dot(12, 12, 1.2),
            line(arc(12, 12, 7, -32, 32)), line(arc(12, 12, 7, 148, 212)),
            line(arc(12, 12, 10.2, -32, 32)), line(arc(12, 12, 10.2, 148, 212))]


@icon("proximity-beacon", CAT, "A small round puck with signal arcs on both sides",
      tags=["bluetooth beacon", "tag", "nearby", "indoor positioning", "ble", "location tag"])
def _(S):
    return [shell(rect(7.5, 8.5, 9, 7, pk(S, 3, 3.5))), dot(12, 12, 1.1),
            line(arc(12, 12, 8.4, -30, 30)), line(arc(12, 12, 8.4, 150, 210))]


@icon("intranet", CAT, "A globe inside a building outline",
      tags=["internal network", "company network", "private network", "corporate", "internal site", "enterprise portal", "office"])
def _(S):
    return [shell(rect(3, 2.5, 18, 19, rr(S, 2))), detail(circle(12, 10.5, 4.3)), detail(seg(7.7, 10.5, 16.3, 10.5)),
            detail(seg(12, 6.2, 12, 14.8)), detail(poly([(10, 21.5), (10, 17.5), (14, 17.5), (14, 21.5)]))]


def _plane(cx, cy, k):
    up = [(21.5, 0), (14.5, -1.5), (10.5, -5), (8.5, -5), (10.5, -1.8), (6.5, -1.5), (4.5, -3.5), (3, -3.5), (4.5, 0)]
    pts = [(cx - 12 * k + x * k, cy + y * k) for x, y in up] + [(cx - 12 * k + x * k, cy - y * k) for x, y in reversed(up[1:-1])]
    return pts


@icon("offline-mode", CAT, "A cloud with a small airplane flying beneath it",
      tags=["airplane mode", "no connection", "disconnected", "work offline", "no internet", "flight mode", "unavailable"])
def _(S):
    pts = [(3 + (x - 3) * 0.8 + 1.3, 17.6 + y * 0.8) for x, y in
           [(21.5, 0), (14.5, -1.5), (10.5, -5), (8.5, -5), (10.5, -1.8), (6.5, -1.5), (4.5, -3.5), (3, -3.5), (4.5, 0),
            (3, 3.5), (4.5, 3.5), (6.5, 1.5), (10.5, 1.8), (8.5, 5), (10.5, 5), (14.5, 1.5)]]
    return [shell(cloud(S, 4, 2.5, 16, 8.5)), shell(poly(pts, closed=True, r=S.r * 0.3))]


def _fw_back(S):
    return [shell(rect(2.5, 2.5, 19, 15, rr(S, 2))), detail(seg(2.5, 7.5, 21.5, 7.5)), detail(seg(2.5, 12.5, 21.5, 12.5)),
            detail(seg(10, 2.5, 10, 7.5)), detail(seg(16, 7.5, 16, 12.5)), detail(seg(6, 7.5, 6, 12.5)), detail(seg(12, 12.5, 12, 17.5))]


def _fw_front(S):
    return [shell(rect(12, 10.5, 9.5, 11, rr(S, 1.5))), detail(seg(14.5, 14.5, 19, 14.5)), detail(seg(14.5, 17.5, 17, 17.5))]


@icon("network-firewall-rule", CAT, "A brick wall with a small list page in front of it",
      tags=["firewall rule", "acl", "allow deny", "security policy", "packet filter", "rule list", "access control list"],
      filled=layered_filled(_fw_back, _fw_front, [rect(12, 10.5, 9.5, 11, 1.5)]))
def _(S):
    return [*occlude(S, _fw_back(S), [rect(12, 10.5, 9.5, 11, rr(S, 1.5))]), *_fw_front(S)]


@icon("ddos-attack", CAT, "Many small arrows converging on a single server box",
      tags=["denial of service", "flood", "traffic spike", "botnet", "cyber attack", "overload", "distributed attack"])
def _(S):
    parts = [shell(rect(8.5, 7.5, 7, 9, rr(S, 1.5))), dot(12, 12, 1)]
    for ang in (0, 180):
        a = math.radians(ang)
        tip = (12 + 6.9 * math.cos(a), 12 + 6.9 * math.sin(a))
        tail = (12 + 10.3 * math.cos(a), 12 + 10.3 * math.sin(a))
        parts += [line(seg(*tail, *tip)), arrow_head(tip, (ang + 180) % 360, 2.2, S.r * 0.3)]
    for ang in (45, 135, 225, 315):
        a = math.radians(ang)
        tip = (12 + 7.2 * math.cos(a), 12 + 8.2 * math.sin(a))
        tail = (12 + 10.2 * math.cos(a), 12 + 10.6 * math.sin(a))
        parts += [line(seg(*tail, *tip)), arrow_head(tip, (ang + 180) % 360, 2.2, S.r * 0.3)]
    return parts


@icon("port-scan", CAT, "A row of small doors with a magnifier held below them",
      tags=["open ports", "network scan", "security scan", "probe", "vulnerability scan", "recon"])
def _(S):
    k = pk(S, 0.4, 1.4)
    return [solid(rect(2.5, 2.2, 4.5, 7.3, k)), solid(rect(9.75, 2.2, 4.5, 7.3, k)), solid(rect(17, 2.2, 4.5, 7.3, k)),
            line(circle(10.5, 15.5, 4)), line(seg(13.5, 18.5, 19, 22))]


@icon("downtime", CAT, "A server box showing flat lines with a small sleeping Z above it",
      tags=["outage", "offline server", "service down", "unavailable", "maintenance window", "server off", "sleeping"])
def _(S):
    return [line(poly([(8.5, 3), (13.5, 3), (8.5, 8), (13.5, 8)], r=S.r * 0.2)),
            line(poly([(16.5, 3), (20, 3), (16.5, 6), (20, 6)], r=0)),
            shell(rect(3, 11.5, 18, 9.5, rr(S, 2))), detail(seg(3, 16.25, 21, 16.25)),
            detail(seg(9, 13.9, 18, 13.9)), detail(seg(9, 18.6, 18, 18.6)), dot(6.2, 13.9, 0.8), dot(6.2, 18.6, 0.8)]


@icon("observability", CAT, "An eye with a small line graph drawn in its iris",
      tags=["monitoring", "telemetry", "visibility", "insight", "metrics logs traces", "watching systems", "apm"])
def _(S):
    eye = pk(S, "M1.5 12C5 6.5 8.5 4.5 12 4.5S19 6.5 22.5 12C19 17.5 15.5 19.5 12 19.5S5 17.5 1.5 12Z",
             "M2.5 12C5.5 7 8.5 5.5 12 5.5S18.5 7 21.5 12C18.5 17 15.5 18.5 12 18.5S5.5 17 2.5 12Z")
    return [shell(eye), detail(circle(12, 12, 4.4)),
            detail(poly([(9.6, 13), (11.2, 10.8), (12.8, 12.8), (14.4, 10.6)], r=S.r * 0.2))]


_TRACE_BARS = [(2.5, 14.5), (6, 17.5), (9.5, 20), (13, 21.5)]


@icon("distributed-tracing", CAT, "A waterfall of staggered bars joined by thin vertical lines",
      tags=["trace", "spans", "waterfall", "request trace", "microservices", "latency breakdown"],
      filled=lambda: U(*[P(rect(a, 2.3 + 5.3 * i, b - a, 3.4, 0)) for i, (a, b) in enumerate(_TRACE_BARS)],
                       *[ST(seg(a + 1.2, 2.3 + 5.3 * i - 3.2, a + 1.2, 2.3 + 5.3 * i + 0.5), 2.5) for i, (a, b) in enumerate(_TRACE_BARS) if i]))
def _(S):
    k = pk(S, 0.4, 1.3)
    parts = []
    for i, (a, b) in enumerate(_TRACE_BARS):
        y = 2.5 + 5.3 * i
        parts.append(solid(rect(a, y, b - a, 2.8, k)))
        if i:
            parts.append(line(seg(a + 1.2, y - 3.2, a + 1.2, y + 0.5)))
    return parts


def _flame_rows(S, h):
    rows = [[(2.5, 21.5)], [(2.5, 10), (11.5, 18)], [(4.5, 8.5), (13, 17.5)], [(5.5, 8.5), (14.5, 17)], [(14.5, 16.5)]]
    k = pk(S, 0.3, h / 2 * 0.9)
    out = []
    for i, row in enumerate(rows):
        y = 19.4 - 4.2 * i if h < 3 else 19.2 - 4.2 * i
        for a, b in row:
            out.append(rect(a, y, b - a, h, k))
    return out


@icon("flame-graph", CAT, "Stacked bars of different widths rising into the ragged shape of a flame",
      tags=["profiler", "performance profile", "cpu profile", "call stack", "stack trace chart", "hot path", "profiling"],
      filled=lambda: U(*[P(d) for d in _flame_rows(LINE, 3.0)]))
def _(S):
    return [solid(d) for d in _flame_rows(S, 2.5)]


@icon("log-aggregation", CAT, "Three log entries funnelled into a single database cylinder",
      tags=["centralized logging", "log collection", "syslog", "log pipeline", "log management", "collect logs"])
def _(S):
    k = pk(S, 0.4, 1.2)
    return [solid(rect(2.5, 2.5, 5, 2.5, k)), solid(rect(9.5, 2.5, 5, 2.5, k)), solid(rect(16.5, 2.5, 5, 2.5, k)),
            line(seg(5, 6, 9.5, 12.8)), line(seg(12, 6, 12, 12.3)), line(seg(19, 6, 14.5, 12.8)),
            *database(S, 6.5, 13, 11, 8.5, 2.2)]


@icon("metrics-dashboard", CAT, "A monitor screen showing a small bar chart beside a line graph",
      tags=["dashboard", "kpi", "monitoring screen", "charts", "statistics", "status board"])
def _(S):
    return [shell(rect(2.5, 3, 19, 14, rr(S, 2))), detail(seg(12.5, 3, 12.5, 17)),
            detail(seg(6, 14, 6, 11.5)), detail(seg(9.2, 14, 9.2, 8)),
            detail(poly([(14.5, 13.5), (16.5, 10.5), (18, 12), (20, 8)], r=S.r * 0.2)),
            line(seg(12, 17, 12, 20.5)), line(seg(8, 20.5, 16, 20.5))]


@icon("alert-rule", CAT, "A bell joined by a short line to a wide threshold bar beneath it",
      tags=["alerting", "threshold", "notification rule", "trigger", "pager", "alarm condition", "monitor alert"])
def _(S):
    bell = pk(S, "M6.5 11.5V7.5A5.5 5.5 0 0 1 17.5 7.5V11.5L19.5 14H4.5Z", "M6.5 11.5V7.5A5.5 5.5 0 0 1 17.5 7.5V11.5L18.5 13.5H5.5Z")
    return [shell(bell), line(seg(12, 14.5, 12, 18.5)),
            solid(rect(3, 18.5, 18, 3, pk(S, 0.3, 1.5)))]


def _pm_back(S):
    return [shell(rect(3.5, 3.5, 13, 17, rr(S, 2))), detail(seg(7, 9, 13, 9)),
            detail(seg(7, 12.5, 11, 12.5))]


def _pm_front(S):
    return [line(circle(15.5, 14.5, 4)), line(seg(18.5, 17.5, 22, 21)), line(seg(14, 13, 17, 16))]


@icon("postmortem", CAT, "A clipboard report with a magnifying glass examining it",
      tags=["incident review", "root cause analysis", "rca", "outage report", "retrospective", "blameless", "incident report"],
      filled=layered_filled(_pm_back, _pm_front, [circle(15.5, 14.5, 4)]))
def _(S):
    return [*occlude(S, _pm_back(S), [circle(15.5, 14.5, 4)], gap=1.2), *_pm_front(S)]


@icon("error-budget", CAT, "A pie chart with a small warning triangle in one slice",
      tags=["slo", "reliability", "allowed failures", "sre", "uptime budget", "risk budget", "service level"])
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(seg(12, 12, 12, 2.5)), detail(seg(12, 12, 20.2, 16.75)),
            detail(poly([(5.5, 18), (8.5, 12.5), (11.5, 18)], closed=True, r=S.r * 0.3))]


@icon("sla-agreement", CAT, "A document with a small clock above a wavy signature line",
      tags=["service level agreement", "contract", "uptime guarantee", "terms", "support agreement", "signed document", "commitment"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 19, rr(S, 2))), detail(circle(12, 8.8, 3.3)),
            detail(poly([(12, 7), (12, 8.8), (13.4, 9.6)])),
            detail(poly([(8, 17.8), (10, 15.5), (12, 18), (14, 16), (16, 17.5)], r=S.r * 0.5))]


def _chaos_back(S):
    ear = lambda x: shell(poly(regular(x, 7, 2.6, 4, -45), closed=True)) if S.name == "line" else shell(circle(x, 7, 1.9))  # noqa: E731
    head = shell(poly(regular(12, 7, 4.8, 8, -22.5), closed=True)) if S.name == "line" else shell(circle(12, 7, 4.4))
    return [ear(6.6), ear(17.4), head, dot(10.2, 6.5, 0.9), dot(13.8, 6.5, 0.9)]


def _chaos_front(S):
    return [shell(rect(3, 11.5, 18, 10, rr(S, 3))), detail(seg(3, 16.5, 21, 16.5)), dot(6.5, 14, 0.9), dot(6.5, 19, 0.9)]


@icon("chaos-engineering", CAT, "A server box with a monkey face peeking over its top edge",
      tags=["resilience testing", "fault injection", "random failure", "reliability testing", "sre", "stress test"],
      filled=layered_filled(_chaos_back, _chaos_front, [rect(3, 11.5, 18, 10, 2)]))
def _(S):
    return [*occlude(S, _chaos_back(S), [rect(3, 11.5, 18, 10, rr(S, 3))]), *_chaos_front(S)]


@icon("disaster-recovery", CAT, "A small server stack inside a life ring",
      tags=["dr", "business continuity", "recovery plan", "rescue", "backup site", "lifebuoy", "survive outage"])
def _(S):
    parts = [line(circle(12, 12, 9)), line(circle(12, 12, 5.3))]
    for ang in pk(S, (45, 135, 225, 315), (0, 90, 180, 270)):
        a = math.radians(ang)
        parts.append(line(seg(12 + 5.3 * math.cos(a), 12 + 5.3 * math.sin(a), 12 + 9 * math.cos(a), 12 + 9 * math.sin(a))))
    parts += [solid(rect(9.5, 9.6, 5, 2, 0.3)), solid(rect(9.5, 12.4, 5, 2, 0.3))]
    return parts
