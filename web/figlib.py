"""Small SVG drawing library for the notes' figures.

Colors are CSS variables (theme-aware). Math labels are emitted as
<g class="fm" data-tex=...> markers; build.render_math swaps them for
MathJax SVG. Titles and legends are HTML around the SVG.
"""
import html
import math

import numpy as np

SERIES = {f'c{i}': f'var(--c{i})' for i in range(1, 8)}


def col(c):
    if c is None:
        return 'none'
    if c in SERIES:
        return SERIES[c]
    return c


def esc(s):
    return html.escape(str(s), quote=True)


def num(v):
    return ('%.2f' % v).rstrip('0').rstrip('.') if abs(v - round(v)) > 1e-9 else str(int(round(v)))


def fmt_tick(v):
    if abs(v) < 1e-12:
        return '0'
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    s = ('%.4f' % v).rstrip('0').rstrip('.')
    return s


def nice_ticks(lo, hi, n=5):
    span = hi - lo
    if span <= 0:
        return [lo]
    raw = span / n
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        step = m * mag
        if span / step <= n + 0.5:
            break
    start = math.ceil(lo / step - 1e-9) * step
    out = []
    v = start
    while v <= hi + 1e-9 * span:
        out.append(round(v, 10))
        v += step
    return out


class Fig:
    """Canvas in px units (y down)."""

    def __init__(self, w, h, fid):
        self.w, self.h, self.fid = w, h, fid
        self.el = []
        self.defs = []

    def add(self, s):
        self.el.append(s)

    def path(self, d, stroke='var(--fig-ink)', fill='none', sw=2, dash=None, op=None, fop=None,
             cap='round', join='round', clip=None, extra=''):
        st = 'fill:%s;stroke:%s;stroke-width:%s;stroke-linecap:%s;stroke-linejoin:%s' % (
            col(fill), col(stroke), num(sw), cap, join)
        if dash:
            st += ';stroke-dasharray:%s' % dash
        if op is not None:
            st += ';opacity:%s' % op
        if fop is not None:
            st += ';fill-opacity:%s' % fop
        cp = ' clip-path="url(#%s)"' % clip if clip else ''
        self.add('<path d="%s" style="%s"%s%s/>' % (d, st, cp, extra))

    def poly(self, pts, close=False, **kw):
        if len(pts) < 2:
            return
        d = 'M' + ' L'.join('%.1f,%.1f' % p for p in pts) + (' Z' if close else '')
        self.path(d, **kw)

    def circle_px(self, x, y, r, stroke='var(--fig-ink)', fill='none', sw=1.5, fop=None, dash=None):
        st = 'fill:%s;stroke:%s;stroke-width:%s' % (col(fill), col(stroke), num(sw))
        if fop is not None:
            st += ';fill-opacity:%s' % fop
        if dash:
            st += ';stroke-dasharray:%s' % dash
        self.add('<circle cx="%.1f" cy="%.1f" r="%.1f" style="%s"/>' % (x, y, r, st))

    def text_px(self, x, y, s, anchor='middle', size=13, color='var(--ink-2)', weight=None, rtl=False):
        st = 'fill:%s;font-size:%spx' % (col(color), num(size))
        if weight:
            st += ';font-weight:%s' % weight
        d = ''
        if rtl:
            d = ' direction="rtl"'
            anchor = {'start': 'end', 'end': 'start'}.get(anchor, anchor)
        self.add('<text x="%.1f" y="%.1f" text-anchor="%s" dominant-baseline="central" style="%s"%s>%s</text>' % (
            x, y, anchor, st, d, esc(s)))

    def math_px(self, x, y, tex, anchor='c', size=15, color='var(--ink)'):
        self.add('<g class="fm" data-tex="%s" data-x="%.1f" data-y="%.1f" data-anchor="%s" data-size="%s" data-color="%s"></g>' % (
            esc(tex), x, y, anchor, num(size), esc(col(color))))

    def arrowhead(self, x, y, ang, color='var(--fig-ink)', size=9):
        """Filled arrowhead with tip at (x, y) pointing along angle ang (radians, px space)."""
        a1, a2 = ang + math.radians(155), ang - math.radians(155)
        p1 = (x + size * math.cos(a1), y + size * math.sin(a1))
        p2 = (x + size * math.cos(a2), y + size * math.sin(a2))
        self.path('M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z' % (x, y, p1[0], p1[1], p2[0], p2[1]),
                  stroke=color, fill=color, sw=1)

    def svg(self, label=''):
        defs = ('<defs>%s</defs>' % ''.join(self.defs)) if self.defs else ''
        return ('<svg class="plot" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="%s" '
                'xmlns="http://www.w3.org/2000/svg">%s%s</svg>') % (
            self.w, self.h, self.w, self.h, esc(label), defs, ''.join(self.el))


class Plot(Fig):
    """Cartesian plot. Data coords -> px."""

    def __init__(self, fid, w=500, h=280, x=(0, 1), y=(0, 1), axes='left', xticks='auto', yticks='auto',
                 xticklabels=None, yticklabels=None, grid=False, xlabel=None, ylabel=None,
                 margins=None, equal=False, frame=False, tick_size=12.5):
        super().__init__(w, h, fid)
        self.x0, self.x1 = x
        self.y0, self.y1 = y
        self.axes = axes
        self.tick_size = tick_size
        if xticks == 'auto':
            xticks = nice_ticks(self.x0, self.x1)
        if yticks == 'auto':
            yticks = nice_ticks(self.y0, self.y1, 4)
        self.xticks, self.yticks = xticks or [], yticks or []
        self.xticklabels, self.yticklabels = xticklabels, yticklabels
        ml = 14
        if self.yticks and axes != 'middle':
            if yticklabels:
                ml = 44
            else:
                ml = 12 + 7.2 * max(len(fmt_tick(v)) for v in self.yticks) + 8
        mb = 30 if self.xticks else 12
        if xticklabels and any('frac' in t for t in xticklabels):
            mb = 40
        mt = 30 if ylabel else 12
        mr = 30 if xlabel else 14
        if margins:
            ml, mr, mt, mb = [m if m is not None else d for m, d in zip(margins, (ml, mr, mt, mb))]
        self.ml, self.mr, self.mt, self.mb = ml, mr, mt, mb
        self.pw, self.ph = w - ml - mr, h - mt - mb
        if equal:
            sx = self.pw / (self.x1 - self.x0)
            sy = self.ph / (self.y1 - self.y0)
            s = min(sx, sy)
            self.pw, self.ph = s * (self.x1 - self.x0), s * (self.y1 - self.y0)
            self.ml += (w - ml - mr - self.pw) / 2
            self.mt += (h - mt - mb - self.ph) / 2
        self.clip_id = fid + '-clip'
        self.defs.append('<clipPath id="%s"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></clipPath>' % (
            self.clip_id, self.ml - 1, self.mt - 4, self.pw + 2, self.ph + 5))
        self.grid, self.xlabel, self.ylabel, self.frame = grid, xlabel, ylabel, frame
        self.front = []

    # coordinate transforms
    def X(self, x):
        return self.ml + (x - self.x0) / (self.x1 - self.x0) * self.pw

    def Y(self, y):
        return self.mt + (self.y1 - y) / (self.y1 - self.y0) * self.ph

    def P(self, x, y):
        return (self.X(x), self.Y(y))

    def _axes(self):
        out = []
        ink = 'var(--fig-ink)'
        if self.grid:
            for v in self.xticks:
                out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" style="stroke:var(--fig-grid);stroke-width:1"/>' % (
                    self.X(v), self.mt, self.X(v), self.mt + self.ph))
            for v in self.yticks:
                out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" style="stroke:var(--fig-grid);stroke-width:1"/>' % (
                    self.ml, self.Y(v), self.ml + self.pw, self.Y(v)))
        self.el = out + self.el
        # axis lines
        if self.axes == 'middle':
            ya = self.Y(0) if self.y0 <= 0 <= self.y1 else self.Y(self.y0)
            xa = self.X(0) if self.x0 <= 0 <= self.x1 else self.X(self.x0)
        else:
            ya, xa = self.Y(self.y0), self.X(self.x0)
        self.xa_y, self.ya_x = ya, xa
        if self.axes in ('left', 'middle'):
            self.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" style="stroke:%s;stroke-width:1.2"/>' % (
                self.ml, ya, self.ml + self.pw + 6, ya, ink))
            self.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" style="stroke:%s;stroke-width:1.2"/>' % (
                xa, self.mt + self.ph, xa, self.mt - 6, ink))
            self.arrowhead(self.ml + self.pw + 8, ya, 0, size=6)
            self.arrowhead(xa, self.mt - 8, -math.pi / 2, size=6)
        elif self.axes in ('box', 'frame'):
            self.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" style="fill:none;stroke:var(--fig-ink);stroke-width:1;stroke-opacity:.55"/>' % (
                self.ml, self.mt, self.pw, self.ph))
        # ticks
        ts = self.tick_size
        for i, v in enumerate(self.xticks):
            px = self.X(v)
            ybase = ya if self.axes == 'middle' else self.mt + self.ph
            self.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" style="stroke:%s;stroke-width:1"/>' % (
                px, ybase, px, ybase + 4, ink))
            if self.xticklabels:
                self.math_px(px, ybase + 7, self.xticklabels[i], anchor='n', size=ts + 1.5, color='var(--ink-2)')
            else:
                self.text_px(px, ybase + 15, fmt_tick(v), size=ts, color='var(--ink-2)')
        for i, v in enumerate(self.yticks):
            py = self.Y(v)
            xbase = xa if self.axes == 'middle' else self.ml
            self.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" style="stroke:%s;stroke-width:1"/>' % (
                xbase - 4, py, xbase, py, ink))
            if self.yticklabels:
                self.math_px(xbase - 7, py, self.yticklabels[i], anchor='e', size=ts + 1.5, color='var(--ink-2)')
            else:
                self.text_px(xbase - 7, py, fmt_tick(v), anchor='end', size=ts, color='var(--ink-2)')
        if self.xlabel:
            self.label_px(self.ml + self.pw + 12, (ya if self.axes == 'middle' else self.mt + self.ph), self.xlabel, 'w')
        if self.ylabel:
            self.label_px(xa, self.mt - 14, self.ylabel, 's' if self.axes == 'middle' else 'sw')

    def label_px(self, x, y, s, anchor, size=15, color='var(--ink)'):
        """Math if it looks like TeX ($...$), else plain text."""
        if s.startswith('$'):
            self.math_px(x, y, s.strip('$'), anchor=anchor, size=size, color=color)
        else:
            a = {'w': 'start', 'e': 'end', 'sw': 'start', 'se': 'end'}.get(anchor, 'middle')
            dy = {'s': -8, 'sw': -8, 'se': -8, 'n': 8}.get(anchor, 0)
            self.text_px(x, y + dy, s, anchor=a, size=size - 1.5, color=color)

    # marks
    def fn(self, f, a=None, b=None, n=240, color='c1', sw=2.2, dash=None, front=False):
        a = self.x0 if a is None else a
        b = self.x1 if b is None else b
        xs = np.linspace(a, b, n)
        with np.errstate(all='ignore'):
            ys = np.array([f(x) for x in xs], dtype=float)
        self.curve(xs, ys, color=color, sw=sw, dash=dash)

    def curve(self, xs, ys, color='c1', sw=2.2, dash=None, close=False):
        segs = []
        cur = []
        lim = (self.y1 - self.y0) * 4
        for x, y in zip(xs, ys):
            if not np.isfinite(y):
                if cur:
                    segs.append(cur)
                cur = []
                continue
            y = max(min(y, self.y1 + lim), self.y0 - lim)
            cur.append(self.P(x, y))
        if cur:
            segs.append(cur)
        d = ' '.join('M' + ' L'.join('%.1f,%.1f' % p for p in s) for s in segs if len(s) > 1)
        if d:
            self.path(d, stroke=color, sw=sw, dash=dash, clip=self.clip_id)

    def area(self, f, a, b, color='c1', op=None, n=160, base=0.0):
        xs = np.linspace(a, b, n)
        with np.errstate(all='ignore'):
            ys = [min(f(x), self.y1 * 3) for x in xs]
        pts = [self.P(a, base)] + [self.P(x, y) for x, y in zip(xs, ys)] + [self.P(b, base)]
        self.path('M' + ' L'.join('%.1f,%.1f' % p for p in pts) + ' Z', stroke='none', fill=color,
                  fop=('var(--fig-fill)' if op is None else op), clip=self.clip_id)

    def polyfill(self, pts, color='c1', op=None, stroke=None, sw=1.5):
        P = [self.P(*p) for p in pts]
        self.path('M' + ' L'.join('%.1f,%.1f' % p for p in P) + ' Z', stroke=stroke or 'none', fill=color,
                  fop=('var(--fig-fill)' if op is None else op), sw=sw, clip=self.clip_id)

    def line(self, pts, color='var(--fig-ink)', sw=2, dash=None, clip=True):
        P = [self.P(*p) for p in pts]
        self.path('M' + ' L'.join('%.1f,%.1f' % p for p in P), stroke=color, sw=sw, dash=dash,
                  clip=self.clip_id if clip else None)

    def stems(self, xs, ys, color='c1', r=3.6, sw=1.8, marker='o', shift=0.0):
        for x, y in zip(xs, ys):
            px = self.X(x) + shift
            self.path('M%.1f,%.1f L%.1f,%.1f' % (px, self.Y(0), px, self.Y(y)), stroke=color, sw=sw)
        if marker:
            self.points(xs, ys, color=color, r=r, mark=marker, shift=shift)

    def points(self, xs, ys, color='c1', r=3.6, mark='o', hollow=False, shift=0.0, sw=1.6):
        for x, y in zip(xs, ys):
            px, py = self.X(x) + shift, self.Y(y)
            if mark == 'o':
                self.add('<circle cx="%.1f" cy="%.1f" r="%.1f" style="fill:%s;stroke:%s;stroke-width:%s"/>' % (
                    px, py, r, 'var(--fig-bg)' if hollow else col(color), col(color), num(sw)))
            elif mark == 's':
                self.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" style="fill:%s;stroke:%s;stroke-width:1"/>' % (
                    px - r, py - r, 2 * r, 2 * r, col(color), col(color)))
            elif mark == 'x':
                self.path('M%.1f,%.1f L%.1f,%.1f M%.1f,%.1f L%.1f,%.1f' % (
                    px - r, py - r, px + r, py + r, px - r, py + r, px + r, py - r), stroke=color, sw=2)

    def bars(self, xs, ys, width, color='c1', op=0.75, gap=1.5):
        for x, y in zip(xs, ys):
            x0, x1 = self.X(x - width / 2), self.X(x + width / 2)
            y0, y1 = self.Y(0), self.Y(y)
            r = min(3, (x1 - x0) / 3)
            h = y0 - y1
            if h <= 0:
                continue
            # rounded data-end, square baseline
            d = ('M%.1f,%.1f L%.1f,%.1f Q%.1f,%.1f %.1f,%.1f L%.1f,%.1f Q%.1f,%.1f %.1f,%.1f L%.1f,%.1f Z' % (
                x0, y0, x0, y1 + r, x0, y1, x0 + r, y1, x1 - r, y1, x1, y1, x1, y1 + r, x1, y0))
            self.path(d, stroke='var(--fig-bg)', fill=color, sw=gap, fop=op)

    def arrow(self, p0, p1, color='var(--fig-ink)', sw=1.6, both=False, size=8, dash=None):
        (x0, y0), (x1, y1) = self.P(*p0), self.P(*p1)
        ang = math.atan2(y1 - y0, x1 - x0)
        sh = size * 0.8
        xa0, ya0 = (x0 + sh * math.cos(ang), y0 + sh * math.sin(ang)) if both else (x0, y0)
        xa1, ya1 = x1 - sh * math.cos(ang), y1 - sh * math.sin(ang)
        self.path('M%.1f,%.1f L%.1f,%.1f' % (xa0, ya0, xa1, ya1), stroke=color, sw=sw, dash=dash)
        self.arrowhead(x1, y1, ang, color=color, size=size)
        if both:
            self.arrowhead(x0, y0, ang + math.pi, color=color, size=size)

    def math(self, x, y, tex, anchor='c', size=15, color='var(--ink)'):
        self.math_px(self.X(x), self.Y(y), tex, anchor, size, color)

    def text(self, x, y, s, anchor='middle', size=13, color='var(--ink-2)', rtl=False):
        self.text_px(self.X(x), self.Y(y), s, anchor=anchor, size=size, color=color, rtl=rtl)

    def svg(self, label=''):
        body = self.el
        self.el = []
        self._axes()
        axes_el = self.el
        self.el = axes_el[:0]
        # grid first, then marks, then axes on top
        grid = [e for e in axes_el if 'fig-grid' in e]
        rest = [e for e in axes_el if 'fig-grid' not in e]
        self.el = grid + body + rest
        return Fig.svg(self, label)


class Diagram(Fig):
    """TikZ-like coordinates (y up, units) scaled to px."""

    def __init__(self, fid, x=(0, 1), y=(0, 1), scale=60, pad=10):
        self.sx0, self.sx1 = x
        self.sy0, self.sy1 = y
        self.s = scale
        self.pad = pad
        w = int(round((x[1] - x[0]) * scale + 2 * pad))
        h = int(round((y[1] - y[0]) * scale + 2 * pad))
        super().__init__(w, h, fid)

    def X(self, x):
        return self.pad + (x - self.sx0) * self.s

    def Y(self, y):
        return self.pad + (self.sy1 - y) * self.s

    def P(self, x, y):
        return (self.X(x), self.Y(y))

    def circle(self, cx, cy, r, stroke='var(--fig-ink)', fill='none', sw=1.8, fop=None, dash=None):
        self.circle_px(self.X(cx), self.Y(cy), r * self.s, stroke=stroke, fill=fill, sw=sw, fop=fop, dash=dash)

    def ellipse(self, cx, cy, rx, ry, rot=0, stroke='var(--fig-ink)', fill='none', sw=1.8, fop=None, dash=None):
        st = 'fill:%s;stroke:%s;stroke-width:%s' % (col(fill), col(stroke), num(sw))
        if fop is not None:
            st += ';fill-opacity:%s' % fop
        if dash:
            st += ';stroke-dasharray:%s' % dash
        px, py = self.P(cx, cy)
        self.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" transform="rotate(%.1f %.1f %.1f)" style="%s"/>' % (
            px, py, rx * self.s, ry * self.s, -rot, px, py, st))

    def rect(self, x0, y0, x1, y1, stroke='var(--fig-ink)', fill='none', sw=1.8, fop=None, rx=0, dash=None):
        st = 'fill:%s;stroke:%s;stroke-width:%s' % (col(fill), col(stroke), num(sw))
        if fop is not None:
            st += ';fill-opacity:%s' % fop
        if dash:
            st += ';stroke-dasharray:%s' % dash
        X0, Y1 = self.P(min(x0, x1), max(y0, y1))
        self.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" style="%s"/>' % (
            X0, Y1, abs(x1 - x0) * self.s, abs(y1 - y0) * self.s, num(rx), st))

    def line(self, pts, color='var(--fig-ink)', sw=1.8, dash=None, fill='none', close=False, fop=None):
        P = [self.P(*p) for p in pts]
        self.path('M' + ' L'.join('%.1f,%.1f' % p for p in P) + (' Z' if close else ''), stroke=color, sw=sw,
                  dash=dash, fill=fill, fop=fop)

    def arrow(self, p0, p1, color='var(--fig-ink)', sw=1.8, bend=0, size=9, both=False, shorten=(0, 0)):
        """bend in degrees: positive = to the left of travel (TikZ 'bend left')."""
        x0, y0 = p0
        x1, y1 = p1
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        x0, y0 = x0 + ux * shorten[0], y0 + uy * shorten[0]
        x1, y1 = x1 - ux * shorten[1], y1 - uy * shorten[1]
        if bend:
            L2 = math.hypot(x1 - x0, y1 - y0)
            h = math.tan(math.radians(bend)) * L2 / 2
            nx, ny = -uy, ux
            cx, cy = (x0 + x1) / 2 + nx * h, (y0 + y1) / 2 + ny * h
        else:
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        P0, C, P1 = self.P(x0, y0), self.P(cx, cy), self.P(x1, y1)
        ang = math.atan2(P1[1] - C[1], P1[0] - C[0])
        sh = size * 0.75
        E = (P1[0] - sh * math.cos(ang), P1[1] - sh * math.sin(ang))
        S = P0
        if both:
            ang0 = math.atan2(P0[1] - C[1], P0[0] - C[0])
            S = (P0[0] - sh * math.cos(ang0), P0[1] - sh * math.sin(ang0))
            self.arrowhead(P0[0], P0[1], ang0, color=color, size=size)
        self.path('M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f' % (S[0], S[1], C[0], C[1], E[0], E[1]), stroke=color, sw=sw)
        self.arrowhead(P1[0], P1[1], ang, color=color, size=size)
        return C

    def math(self, x, y, tex, anchor='c', size=16, color='var(--ink)'):
        self.math_px(self.X(x), self.Y(y), tex, anchor, size, color)

    def text(self, x, y, s, anchor='middle', size=14, color='var(--ink-2)', weight=None, rtl=True):
        self.text_px(self.X(x), self.Y(y), s, anchor=anchor, size=size, color=color, weight=weight, rtl=rtl)


# ---------------------------------------------------------------- HTML wrappers
def mspan(tex):
    return '<span class="math inline">\\(%s\\)</span>' % html.escape(tex, quote=False)


def rich(s):
    """'$..$' segments -> math spans, rest escaped."""
    out = []
    parts = s.split('$')
    for i, p in enumerate(parts):
        if i % 2:
            out.append(mspan(p))
        else:
            out.append(html.escape(p, quote=False))
    return ''.join(out)


def legend(items):
    """items: list of (label, color, kind) kind in line|dash|dot|box|mark."""
    li = []
    for label, color, kind in items:
        c = col(color)
        if kind == 'box':
            sw = '<svg width="16" height="12" aria-hidden="true"><rect x="1" y="1" width="14" height="10" rx="2" style="fill:%s;fill-opacity:.6;stroke:%s"/></svg>' % (c, c)
        elif kind == 'mark':
            sw = '<svg width="16" height="12" aria-hidden="true"><circle cx="8" cy="6" r="4" style="fill:%s"/></svg>' % c
        elif kind == 'square':
            sw = '<svg width="16" height="12" aria-hidden="true"><rect x="4" y="2" width="8" height="8" style="fill:%s"/></svg>' % c
        else:
            dash = {'dash': '5 3', 'dot': '1.5 3'}.get(kind)
            sw = '<svg width="22" height="12" aria-hidden="true"><line x1="1" y1="6" x2="21" y2="6" style="stroke:%s;stroke-width:2.4;stroke-linecap:round%s"/></svg>' % (
                c, (';stroke-dasharray:' + dash) if dash else '')
        li.append('<li>%s<span>%s</span></li>' % (sw, rich(label)))
    return '<ul class="fig-legend">%s</ul>' % ''.join(li)


def wrap(svg, title=None, leg=None, cls=''):
    out = '<div class="subfig%s">' % ((' ' + cls) if cls else '')
    if title:
        out += '<div class="subfig-t">%s</div>' % rich(title)
    out += svg
    if leg:
        out += leg
    out += '</div>'
    return out


def flow(nodes, edges, cls=''):
    """Horizontal flow of boxes with labelled arrows; stacks vertically on phones.
    nodes: list of (main_rich, sub_text, tone); edges: list of (above_rich, below_rich)."""
    parts = []
    for i, (main, sub, tone) in enumerate(nodes):
        parts.append('<div class="flow-node tone-%s"><div class="fn-main">%s</div>%s</div>' % (
            tone, rich(main), ('<div class="fn-sub">%s</div>' % rich(sub)) if sub else ''))
        if i < len(edges):
            a, b = edges[i]
            parts.append('<div class="flow-edge"><span class="fe-a">%s</span><span class="fe-line" aria-hidden="true"></span><span class="fe-b">%s</span></div>' % (
                rich(a) if a else '', rich(b) if b else ''))
    return '<div class="flow %s">%s</div>' % (cls, ''.join(parts))


def place_math(mjx, x, y, anchor, size, color):
    """Turn MathJax output into a positioned nested <svg>."""
    import re
    if mjx is None:
        return ''
    m = re.search(r'<svg[^>]*viewBox="([^"]+)"[^>]*>(.*)</svg>', mjx, re.S)
    if not m:
        return ''
    vb = [float(v) for v in m.group(1).split()]
    inner = m.group(2)
    w = vb[2] / 1000 * size
    h = vb[3] / 1000 * size
    ax = {'c': .5, 'n': .5, 's': .5, 'w': 0, 'e': 1, 'nw': 0, 'ne': 1, 'sw': 0, 'se': 1}[anchor]
    ay = {'c': .5, 'w': .5, 'e': .5, 'n': 0, 'nw': 0, 'ne': 0, 's': 1, 'sw': 1, 'se': 1}[anchor]
    x0 = x - ax * w
    y0 = y - ay * h
    return ('<svg x="%.1f" y="%.1f" width="%.1f" height="%.1f" viewBox="%s" overflow="visible" style="color:%s">%s</svg>' % (
        x0, y0, w, h, m.group(1), color or 'var(--ink)', inner))
