"""Vector colouring-page generators (mandalas, snowflakes, ornaments) for reportlab.

Each draw_* function draws black line art centred at (cx, cy) inside radius R
on a reportlab canvas. All shapes are stroked, with white fills only to hide
lines behind them, so every region stays closed and colourable.
"""
import math
import random

from reportlab.lib.colors import black, white


def _setup(c, lw):
    c.setStrokeColor(black)
    c.setFillColor(white)
    c.setLineWidth(lw)
    c.setLineJoin(1)
    c.setLineCap(1)


def _petal(c, cx, cy, ang, r0, r1, width, shape):
    """Closed petal from radius r0 to r1 along angle ang."""
    ca, sa = math.cos(ang), math.sin(ang)
    px, py = -sa, ca

    def pt(r, off):
        return cx + ca * r + px * off, cy + sa * r + py * off

    p = c.beginPath()
    x0, y0 = pt(r0, 0)
    x1, y1 = pt(r1, 0)
    p.moveTo(x0, y0)
    if shape == "round":
        a1 = pt(r0 + (r1 - r0) * 0.3, width)
        a2 = pt(r1 + (r1 - r0) * 0.1, width * 0.9)
        b1 = pt(r1 + (r1 - r0) * 0.1, -width * 0.9)
        b2 = pt(r0 + (r1 - r0) * 0.3, -width)
    elif shape == "pointed":
        a1 = pt(r0 + (r1 - r0) * 0.25, width)
        a2 = pt(r0 + (r1 - r0) * 0.7, width * 0.7)
        b1 = pt(r0 + (r1 - r0) * 0.7, -width * 0.7)
        b2 = pt(r0 + (r1 - r0) * 0.25, -width)
    else:  # heart / tulip
        a1 = pt(r0 + (r1 - r0) * 0.6, width * 1.2)
        a2 = pt(r1 + (r1 - r0) * 0.15, width * 0.2)
        b1 = pt(r1 + (r1 - r0) * 0.15, -width * 0.2)
        b2 = pt(r0 + (r1 - r0) * 0.6, -width * 1.2)
    p.curveTo(*a1, *a2, x1, y1)
    p.curveTo(*b1, *b2, x0, y0)
    p.close()
    c.drawPath(p, stroke=1, fill=1)
    return pt


def draw_mandala(c, cx, cy, R, seed, lw=3.2):
    rng = random.Random(seed)
    _setup(c, lw)
    n_layers = rng.randint(5, 7)
    radii = sorted(rng.uniform(0.12, 1.0) for _ in range(n_layers - 1)) + [1.0]
    # Draw outer layers first so inner ones sit on top.
    bounds = [0.08] + radii
    layers = list(zip(bounds[:-1], bounds[1:]))
    for i, (a, b) in reversed(list(enumerate(layers))):
        r0, r1 = a * R, b * R
        if r1 - r0 < R * 0.06:
            r1 = r0 + R * 0.06
        n = rng.choice([8, 10, 12, 12, 16, 16, 20, 24])
        kind = rng.choice(["petal", "petal", "petal", "ring_dots", "scallop", "spike"])
        shape = rng.choice(["round", "pointed", "heart"])
        if kind == "petal":
            width = min((r1 + r0) / 2 * math.pi / n * 0.95, (r1 - r0) * 0.6)
            off = rng.choice([0, 0.5])
            for k in range(n):
                ang = 2 * math.pi * (k + off) / n
                _petal(c, cx, cy, ang, r0, r1, width, shape)
                # inner detail petal
                if r1 - r0 > R * 0.12 and rng.random() < 0.8:
                    _petal(c, cx, cy, ang, r0 + (r1 - r0) * 0.2, r0 + (r1 - r0) * 0.75,
                           width * 0.45, shape)
        elif kind == "scallop":
            c.circle(cx, cy, r1, stroke=1, fill=1)
            for k in range(n):
                ang = 2 * math.pi * k / n
                rr = r1 * math.sin(math.pi / n) * 0.95
                x = cx + math.cos(ang) * (r1 - rr * 0.2)
                y = cy + math.sin(ang) * (r1 - rr * 0.2)
                c.circle(x, y, rr, stroke=1, fill=1)
            c.circle(cx, cy, r0 + (r1 - r0) * 0.55, stroke=1, fill=1)
        elif kind == "spike":
            p = c.beginPath()
            for k in range(2 * n + 1):
                ang = math.pi * k / n
                r = r1 if k % 2 == 0 else r0 + (r1 - r0) * 0.25
                x, y = cx + math.cos(ang) * r, cy + math.sin(ang) * r
                (p.moveTo if k == 0 else p.lineTo)(x, y)
            p.close()
            c.drawPath(p, stroke=1, fill=1)
        else:  # ring with dots
            c.circle(cx, cy, r1, stroke=1, fill=1)
            mid = (r0 + r1) / 2
            dr = min((r1 - r0) * 0.32, mid * math.pi / n * 0.4)
            for k in range(n):
                ang = 2 * math.pi * k / n
                c.circle(cx + math.cos(ang) * mid, cy + math.sin(ang) * mid, dr, stroke=1, fill=1)
        c.circle(cx, cy, r0, stroke=1, fill=1)
    # centre flower
    rc = bounds[0] * R
    for k in range(8):
        _petal(c, cx, cy, 2 * math.pi * k / 8, rc * 0.25, rc, rc * 0.35, "round")
    c.circle(cx, cy, rc * 0.3, stroke=1, fill=1)


def _branch(c, cx, cy, ang, R, rng, params):
    ca, sa = math.cos(ang), math.sin(ang)

    def P(r, off):
        return cx + ca * r - sa * off, cy + sa * r + ca * off

    w = R * params["arm_w"]
    # arm as a closed thin shape
    p = c.beginPath()
    p.moveTo(*P(R * 0.12, w))
    p.lineTo(*P(R * 0.88, w))
    p.lineTo(*P(R * 0.97, 0))
    p.lineTo(*P(R * 0.88, -w))
    p.lineTo(*P(R * 0.12, -w))
    p.close()
    c.drawPath(p, stroke=1, fill=1)
    # side branches
    for (t, L, a) in params["sides"]:
        for s in (1, -1):
            bx, by = P(R * t, s * w)
            ba = ang + s * a
            ex = bx + math.cos(ba) * R * L
            ey = by + math.sin(ba) * R * L
            bw = w * 0.8
            nx, ny = -math.sin(ba) * bw, math.cos(ba) * bw
            q = c.beginPath()
            q.moveTo(bx + nx, by + ny)
            q.lineTo(ex + nx, ey + ny)
            q.lineTo(ex + math.cos(ba) * bw * 2, ey + math.sin(ba) * bw * 2)
            q.lineTo(ex - nx, ey - ny)
            q.lineTo(bx - nx, by - ny)
            q.close()
            c.drawPath(q, stroke=1, fill=1)
    # diamonds along the arm
    for t in params["diamonds"]:
        x, y = P(R * t, 0)
        d = R * params["dia"]
        q = c.beginPath()
        q.moveTo(*P(R * t + d, 0))
        q.lineTo(*P(R * t, d * 0.7))
        q.lineTo(*P(R * t - d, 0))
        q.lineTo(*P(R * t, -d * 0.7))
        q.close()
        c.drawPath(q, stroke=1, fill=1)
    # tip
    tx, ty = P(R * 0.97, 0)
    c.circle(tx, ty, R * 0.035, stroke=1, fill=1)


def draw_snowflake(c, cx, cy, R, seed, lw=3.2):
    rng = random.Random(seed)
    _setup(c, lw)
    params = {
        "arm_w": rng.uniform(0.018, 0.03),
        "sides": [(rng.uniform(0.3, 0.42), rng.uniform(0.18, 0.28), math.radians(rng.choice([45, 55, 60]))),
                  (rng.uniform(0.55, 0.68), rng.uniform(0.13, 0.2), math.radians(rng.choice([40, 50, 60])))],
        "diamonds": [rng.uniform(0.2, 0.26), rng.uniform(0.75, 0.82)],
        "dia": rng.uniform(0.05, 0.075),
    }
    for k in range(6):
        _branch(c, cx, cy, math.pi / 2 + k * math.pi / 3, R, rng, params)
    # hexagon core
    for rr in (0.18, 0.11):
        p = c.beginPath()
        for k in range(7):
            ang = math.pi / 2 + k * math.pi / 3 + math.pi / 6
            x, y = cx + math.cos(ang) * R * rr, cy + math.sin(ang) * R * rr
            (p.moveTo if k == 0 else p.lineTo)(x, y)
        p.close()
        c.drawPath(p, stroke=1, fill=1)
    # six-petal star in the middle
    for k in range(6):
        _petal(c, cx, cy, math.pi / 2 + k * math.pi / 3, R * 0.01, R * 0.09, R * 0.025, "pointed")
    # small satellite flakes
    for k in range(rng.randint(3, 5)):
        ang = rng.uniform(0, 2 * math.pi)
        dist = R * rng.uniform(1.05, 1.25)
        sx, sy = cx + math.cos(ang) * dist, cy + math.sin(ang) * dist
        _mini_flake(c, sx, sy, R * rng.uniform(0.08, 0.13))


def _mini_flake(c, x, y, r):
    for k in range(6):
        _petal(c, x, y, k * math.pi / 3, r * 0.15, r, r * 0.18, "pointed")
    c.circle(x, y, r * 0.18, stroke=1, fill=1)


def draw_ornament(c, cx, cy, R, seed, lw=3.2):
    """A big Christmas bauble filled with pattern bands."""
    rng = random.Random(seed)
    _setup(c, lw)
    r = R * 0.82
    ocy = cy - R * 0.12
    # hanging string and cap
    c.line(cx, ocy + r + R * 0.12, cx, cy + R * 1.05)
    c.circle(cx, ocy + r + R * 0.16, R * 0.05, stroke=1, fill=1)
    c.roundRect(cx - R * 0.14, ocy + r - R * 0.02, R * 0.28, R * 0.14, R * 0.03, stroke=1, fill=1)
    for k in range(1, 4):
        x = cx - R * 0.14 + R * 0.07 * k
        c.line(x, ocy + r - R * 0.02, x, ocy + r + R * 0.12)
    c.circle(cx, ocy, r, stroke=1, fill=1)
    # clip to ball
    c.saveState()
    p = c.beginPath()
    p.circle(cx, ocy, r)
    c.clipPath(p, stroke=0, fill=0)
    n_bands = rng.choice([5, 6, 7])
    edges = [ocy - r + 2 * r * k / n_bands for k in range(n_bands + 1)]
    for i in range(n_bands):
        y0, y1 = edges[i], edges[i + 1]
        c.line(cx - r, y1, cx + r, y1)
        kind = rng.choice(["zig", "dots", "hearts", "stars", "scallop", "diamonds"])
        h = y1 - y0
        mid = (y0 + y1) / 2
        step = h * rng.uniform(0.9, 1.3)
        x = cx - r
        while x < cx + r + step:
            if kind == "zig":
                c.line(x, y0 + h * 0.2, x + step / 2, y1 - h * 0.2)
                c.line(x + step / 2, y1 - h * 0.2, x + step, y0 + h * 0.2)
            elif kind == "dots":
                c.circle(x, mid, h * 0.25, stroke=1, fill=1)
            elif kind == "hearts":
                _heart(c, x, mid, h * 0.32)
            elif kind == "stars":
                _star(c, x, mid, h * 0.36, h * 0.16)
            elif kind == "scallop":
                c.arc(x, y0 + h * 0.15, x + step, y1 + h * 0.3, 180, 180)
            else:
                q = c.beginPath()
                q.moveTo(x, mid + h * 0.34)
                q.lineTo(x + step * 0.3, mid)
                q.lineTo(x, mid - h * 0.34)
                q.lineTo(x - step * 0.3, mid)
                q.close()
                c.drawPath(q, stroke=1, fill=1)
            x += step
    c.restoreState()
    c.circle(cx, ocy, r, stroke=1, fill=0)
    # holly sprig decoration
    for k, s in enumerate((-1, 1)):
        _leaf(c, cx + s * R * 0.2, ocy + r + R * 0.05, math.radians(90 - s * 60), R * 0.22)
    for dx in (-0.05, 0.05, 0.0):
        c.circle(cx + R * dx, ocy + r + R * (0.02 if dx else 0.08), R * 0.04, stroke=1, fill=1)
    # little stars around
    for k in range(rng.randint(4, 6)):
        ang = rng.uniform(0, 2 * math.pi)
        d = R * rng.uniform(1.02, 1.2)
        _star(c, cx + math.cos(ang) * d, ocy + math.sin(ang) * d, R * 0.07, R * 0.03)


def _heart(c, x, y, s):
    p = c.beginPath()
    p.moveTo(x, y - s)
    p.curveTo(x - s * 1.6, y - s * 0.1, x - s * 0.6, y + s * 1.1, x, y + s * 0.35)
    p.curveTo(x + s * 0.6, y + s * 1.1, x + s * 1.6, y - s * 0.1, x, y - s)
    p.close()
    c.drawPath(p, stroke=1, fill=1)


def _star(c, x, y, ro, ri, n=5):
    p = c.beginPath()
    for k in range(2 * n + 1):
        ang = math.pi / 2 + math.pi * k / n
        r = ro if k % 2 == 0 else ri
        px, py = x + math.cos(ang) * r, y + math.sin(ang) * r
        (p.moveTo if k == 0 else p.lineTo)(px, py)
    p.close()
    c.drawPath(p, stroke=1, fill=1)


def _leaf(c, x, y, ang, L):
    ca, sa = math.cos(ang), math.sin(ang)

    def P(t, off):
        return x + ca * L * t - sa * off * L, y + sa * L * t + ca * off * L

    p = c.beginPath()
    p.moveTo(*P(0, 0))
    pts = [(0.2, 0.18), (0.4, 0.12), (0.6, 0.2), (0.8, 0.1), (1, 0)]
    prev = (0, 0)
    for t, o in pts:
        p.curveTo(*P(prev[0] + 0.05, prev[1] + 0.08), *P(t - 0.05, o + 0.08), *P(t, o))
        prev = (t, o)
    for t, o in reversed([(0, 0)] + pts[:-1]):
        p.curveTo(*P(prev[0] - 0.05, -prev[1] - 0.08), *P(t + 0.05, -o - 0.08), *P(t, -o))
        prev = (t, o)
    p.close()
    c.drawPath(p, stroke=1, fill=1)
    c.line(*P(0.05, 0), *P(0.9, 0))


GENERATORS = {"mandala": draw_mandala, "snowflake": draw_snowflake, "ornament": draw_ornament}
