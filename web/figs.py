"""Every figure of the notes, redrawn as SVG (see figlib)."""
import math
import os

import numpy as np

from figlib import Plot, Diagram, Fig, legend, wrap, flow, place_math, rich  # noqa: F401

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'jozve', 'data')
PI = math.pi
exp = np.exp
sqrt = np.sqrt


def data(name):
    rows = open(os.path.join(DATA, name + '.dat')).read().split('\n')
    head = rows[0].split()
    cols = {h: [] for h in head}
    for r in rows[1:]:
        if r.strip():
            for h, v in zip(head, r.split()):
                cols[h].append(float(v))
    return {h: np.array(v) for h, v in cols.items()}


def gauss(x, m=0, s=1):
    return exp(-(x - m) ** 2 / (2 * s * s)) / (sqrt(2 * PI) * s)


REG = {}


def fig(fid):
    def deco(f):
        REG[fid] = f
        return f
    return deco


# ================================================================ session 3
@fig('f03-1')
def _(fid):
    D = Diagram(fid, x=(-2.5, 2.5), y=(-1.7, 3.0), scale=62)
    for (cx, cy), c in (((0.9, 0), 'c2'), ((-0.9, 0), 'c1'), ((0, 1.4), 'c3')):
        D.circle(cx, cy, 1.4, stroke=c, fill=c, fop=.16, sw=2)
    D.math(1.75, -0.45, 'A', size=18)
    D.math(-1.75, -0.45, 'B', size=18)
    D.math(0, 2.35, 'C', size=18)
    D.math(0, -0.7, 'A\\cap B', size=13)
    D.math(0, 0.52, 'A\\cap B\\cap C', size=12)
    D.math(1.1, 1.0, 'A\\cap C', size=13)
    D.math(-1.1, 1.0, 'B\\cap C', size=13)
    return D.svg('نمودار ون سه رویداد')


@fig('f03-2')
def _(fid):
    d = data('binom100')
    P = Plot(fid, w=560, h=250, x=(0, 100), y=(0, 0.09), xticks=list(range(0, 101, 10)),
             yticks=[0, 0.02, 0.04, 0.06, 0.08], xlabel='$k$', ylabel='$\\mathbb P(k)$', grid=True)
    P.stems(d['k'], d['p'], color='c1', r=1.9, sw=1.3)
    return wrap(P.svg('توزیع دوجمله‌ای n=100'), title='$n=100$')


@fig('f03-3')
def _(fid):
    d = data('binom10')
    P = Plot(fid, w=480, h=250, x=(-0.7, 10.7), y=(0, 0.28), xticks=list(range(11)),
             yticks=[0, 0.05, 0.1, 0.15, 0.2, 0.25], xlabel='$k$', ylabel='$\\mathbb P(k)$', grid=True)
    P.bars(d['k'], d['p'], 0.72, color='c6', op=.6)
    P.line([(3.5, 0), (3.5, 0.26), (6.5, 0.26), (6.5, 0)], color='c2', sw=2.4)
    return P.svg('توزیع دوجمله‌ای n=10')


@fig('f03-4')
def _(fid):
    d = data('binom100')
    P = Plot(fid, w=560, h=250, x=(0, 100), y=(0, 0.1), xticks=list(range(0, 101, 20)), yticks=None, xlabel='$k$')
    P.stems(d['k'], d['p'], color='c1', r=1.6, sw=1.2)
    P.arrow((41, 0.09), (59, 0.09), both=True, size=7)
    P.math(50, 0.09, 'O(n^{1/2})', anchor='s', size=14)
    P.arrow((30, 0.0008), (30, 0.0796), both=True, size=7)
    P.math(29, 0.045, 'O(n^{-1/2})', anchor='e', size=14)
    return P.svg('تمرکز توزیع دوجمله‌ای')


@fig('f03-5')
def _(fid):
    panels = []
    specs = [
        ('ناسازگار: وابسته', lambda D: (D.rect(0, 0, 1.6, 1.6, sw=2.2), D.circle(2.8, 0.8, 0.8, stroke='c2', sw=2.2))),
        ('زیرمجموعه: وابسته', lambda D: (D.rect(0.2, -0.2, 2.2, 1.8, sw=2.2), D.circle(1.4, 0.7, 0.62, stroke='c2', sw=2.2))),
        ('هم‌پوشانی جزئی: باید بررسی شود', lambda D: (D.rect(0, 0, 1.6, 1.6, sw=2.2), D.circle(1.9, 0.8, 0.8, stroke='c2', sw=2.2))),
    ]
    for i, (t, draw) in enumerate(specs):
        D = Diagram('%s-%d' % (fid, i), x=(-0.3, 3.9), y=(-0.5, 2.0), scale=46)
        draw(D)
        panels.append(wrap(D.svg(t), title=t))
    return ''.join(panels)


# ================================================================ session 4
@fig('f04-1')
def _(fid):
    D = Diagram(fid, x=(-3.2, 3.2), y=(-1.8, 1.8), scale=58)
    D.ellipse(0, 0, 3, 1.6, stroke='var(--fig-ink)', fill='c2', fop=.16, sw=2)
    D.circle(0.4, 0.1, 0.75, stroke='var(--fig-ink)', fill='var(--fig-bg)', sw=2)
    D.circle(0.4, 0.1, 0.75, stroke='none', fill='c7', fop=.5, sw=0)
    D.circle(-0.4, 0.1, 0.75, stroke='var(--fig-ink)', sw=2)
    D.circle(0.4, 0.1, 0.75, stroke='var(--fig-ink)', sw=2)
    D.math(-0.8, 0.1, 'A', size=20, color='c3')
    D.math(0.82, 0.1, 'B', size=20, color='c3')
    D.math(-2.55, 1.35, '\\Omega', size=18)
    leg = legend([('ناممکن (زیرا $B$ رخ داده است)', 'c2', 'box'),
                  ('فضای نمونه جدید پس از رخ دادن $B$', 'c7', 'box')])
    return wrap(D.svg('احتمال شرطی'), leg=leg)


@fig('f04-2')
def _(fid):
    D = Diagram(fid, x=(-3.6, 3.1), y=(-2.3, 3.0), scale=56)
    rot = 35
    D.ellipse(0, 0, 3, 1.7, rot=rot, stroke='var(--fig-ink)', fill='c6', fop=.14, sw=2.2)
    D.ellipse(0, 0, 1.4, 1.0, rot=rot, stroke='c4', fill='c4', fop=.35, sw=2)
    r = math.radians(rot)
    for a in (20, 60, 110, 150, 250):
        t = math.radians(a)
        x, y = 3 * math.cos(t), 1.7 * math.sin(t)
        D.line([(0, 0), (x * math.cos(r) - y * math.sin(r), x * math.sin(r) + y * math.cos(r))], sw=1.3)
    D.math(0.95, 1.95, 'A_1')
    D.math(1.85, 1.0, 'A_2')
    D.math(1.4, -0.1, 'A_3')
    D.math(-0.25, 1.75, 'A_n')
    D.math(-1.2, -0.8, '\\cdots')
    D.math(-2.9, 1.1, '\\Omega', size=18)
    D.arrow((-3.0, 2.45), (-0.6, 0.2), bend=-30, color='c4')
    D.math(-3.0, 2.55, '\\text{رویداد }E', anchor='s', size=15, color='c4')
    return D.svg('قانون احتمال کل')


@fig('f04-3')
def _(fid):
    D = Diagram(fid, x=(-0.8, 6.8), y=(-0.9, 0.9), scale=58)
    pts = {'A': (0, 0), 'C': (3, 0), 'B': (6, 0)}
    for k, (x, y) in pts.items():
        D.circle(x, y, 0.55, sw=2.2, fill='var(--fig-bg)')
        D.math(x, y, k, size=20)
    for a, b in (('A', 'C'), ('C', 'A'), ('C', 'B'), ('B', 'C')):
        D.arrow(pts[a], pts[b], bend=25, shorten=(0.62, 0.62), sw=2)
    return D.svg('استقلال شرطی: A و B از طریق C به هم مربوط‌اند')


# ================================================================ session 5
@fig('f05-1')
def _(fid):
    D = Diagram(fid, x=(-5.2, 3.9), y=(-2.7, 3.3), scale=52)
    D.ellipse(0, 0, 3.2, 2, rot=30, stroke='var(--fig-ink)', fill='c6', fop=.14, sw=2.2)
    D.circle(0.9, 0.45, 1.45, stroke='c7', fill='c4', fop=.32, sw=1.6)
    D.circle(-0.9, 0.3, 0.9, stroke='c2', sw=2.4)
    D.circle(-0.3, -0.4, 0.85, stroke='c3', sw=2.4)
    D.math(-3, 0.4, '\\Omega', size=18)
    D.math(-2.4, 3.0, 'S_1=\\mathtt{HHTHT}', size=14, color='c2')
    D.arrow((-2.4, 2.75), (-1.0, 1.1), bend=-10, color='var(--muted)', sw=1.4, size=8)
    D.math(-4.0, 2.2, 'S_2=\\mathtt{TTHTT}', size=14, color='c3')
    D.arrow((-4.0, 1.95), (-0.6, -0.6), bend=-20, color='var(--muted)', sw=1.4, size=8)
    D.math(2.6, -2.25, 'C=C_1\\ \\text{یا}\\ C_2', size=14)
    D.arrow((2.6, -1.95), (1.5, 0.2), bend=-30, color='var(--muted)', sw=1.4, size=8)
    return D.svg('دو سکه')


@fig('f05-2')
def _(fid):
    D = Diagram(fid, x=(-1.1, 3.0), y=(-1.1, 2.9), scale=70)
    V = {'A': (0, 2.4), 'B': (2.1, 1.6), 'C': (-0.5, 0), 'D': (2.4, -0.6)}
    D.line([V['A'], V['B'], V['D']], color='c2', sw=10, close=True, fill='c2', fop=.12)
    for a, b in (('A', 'B'), ('A', 'D'), ('C', 'D'), ('B', 'D')):
        D.line([V[a], V[b]], sw=2.2)
    for a, b in (('A', 'C'), ('B', 'C')):
        D.line([V[a], V[b]], sw=2, dash='2 5')
    for k, (x, y) in V.items():
        D.circle(x, y, 0.09, stroke='var(--fig-ink)', fill='var(--fig-ink)', sw=1)
    D.math(0, 2.4, 'A', anchor='s', size=17)
    D.math(2.2, 1.7, 'B', anchor='sw', size=17)
    D.math(-0.65, 0, 'C', anchor='e', size=17)
    D.math(2.4, -0.7, 'D', anchor='n', size=17)
    D.math(0.9, -0.6, '(p,\\,1-p)', size=14, color='var(--muted)')
    return D.svg('گراف تصادفی چهار رأسی')


@fig('f05-3')
def _(fid):
    P = Plot(fid, w=500, h=280, x=(0, 1), y=(0, 1.2), xticks=[0, .2, .4, .6, .8, 1], yticks=[0, .2, .4, .6, .8, 1],
             xlabel='$p$', ylabel='احتمال', grid=True)
    P.fn(lambda p: 4 * p ** 3 - 6 * p ** 5 + 3 * p ** 6, 0, 1, color='c1', sw=2.6)
    P.fn(lambda p: 4 * p ** 3, 0, 0.67, color='c2', dash='6 4')
    leg = legend([('دقیق: $4p^3-6p^5+3p^6$', 'c1', 'line'), ('کران اجتماع: $4p^3$', 'c2', 'dash')])
    return wrap(P.svg('احتمال وجود مثلث'), leg=leg)


# ================================================================ session 6
@fig('f06-1')
def _(fid):
    return flow([('$\\Omega$', '(وضعیت کامل جو)', 'red'), ('$\\mathbb R$', '(عدد خوانده‌شده)', 'blue')],
                [('$X_1,X_2,\\ldots$', 'حسگرها')])


@fig('f06-2')
def _(fid):
    P = Plot(fid, w=300, h=210, x=(-0.5, 2.5), y=(0, 0.6), xticks=[0, 1, 2], yticks=[0.25, 0.5], xlabel='$x$')
    P.stems([0, 1, 2], [0.25, 0.5, 0.25], color='c6', r=4.5, sw=2.6)
    return wrap(P.svg('توزیع تعداد شیر در دو پرتاب'), title='$X$ = تعداد شیر در دو پرتاب')


@fig('f06-3')
def _(fid):
    P = Plot(fid, w=340, h=210, x=(0.5, 8.5), y=(0, 0.3), xticks=list(range(1, 9)),
             yticks=[0.0625, 0.125, 0.1875, 0.25], yticklabels=['\\dfrac1{16}', '\\dfrac2{16}', '\\dfrac3{16}', '\\dfrac4{16}'], margins=(40, None, None, None),
             xlabel='$x$')
    xs = [2, 3, 4, 5, 6, 7, 8]
    P.stems(xs, [1 / 16, 2 / 16, 3 / 16, 4 / 16, 3 / 16, 2 / 16, 1 / 16], color='var(--fig-ink)', r=4.2, sw=2.4)
    return wrap(P.svg('مجموع دو تاس چهاروجهی'), title='مجموع دو تاس چهاروجهی')


@fig('f06-4')
def _(fid):
    d = data('binom_p')
    P = Plot(fid, w=560, h=250, x=(-0.5, 20.5), y=(0, 0.25), xticks=list(range(0, 21, 2)),
             yticks=[0, 0.05, 0.1, 0.15, 0.2, 0.25], xlabel='$k$', ylabel='$P_X(k)$', grid=True)
    P.stems(d['k'], d['a'], color='c1', r=3.4, sw=1.8, shift=-2.5)
    P.stems(d['k'], d['b'], color='c2', r=3.1, sw=1.8, marker='s', shift=2.5)
    leg = legend([('$n=20,\\ p=0.5$', 'c1', 'mark'), ('$n=20,\\ p=0.2$', 'c2', 'square')])
    return wrap(P.svg('دوجمله‌ای با دو مقدار p'), leg=leg)


@fig('f06-5')
def _(fid):
    P = Plot(fid, w=560, h=260, x=(-0.5, 20.5), y=(0, 0.4), xticks=list(range(0, 21, 2)),
             yticks=[0, 0.1, 0.2, 0.3, 0.4], xlabel='$k$', ylabel='$P(X=k)$', grid=True)
    for nm, c in (('pois1', 'c4'), ('pois4', 'c5'), ('pois10', 'c6')):
        d = data(nm)
        P.curve(d['k'], d['p'], color=c, sw=1.8)
        P.points(d['k'], d['p'], color=c, r=3.2)
    leg = legend([('$\\lambda=1$', 'c4', 'line'), ('$\\lambda=4$', 'c5', 'line'), ('$\\lambda=10$', 'c6', 'line')])
    return wrap(P.svg('توزیع پواسون'), leg=leg)


# ================================================================ session 7
@fig('f07-1')
def _(fid):
    P = Plot(fid, w=250, h=210, x=(-1, 3.5), y=(-0.05, 1.15), axes='middle', xticks=[1, 2, 3],
             yticks=[0.25, 0.75, 1], yticklabels=['\\dfrac14', '\\dfrac34', '1'], margins=(30, None, None, None))
    for a, b, v in ((-1, 0, 0), (0, 1, .25), (1, 2, .75), (2, 3.5, 1)):
        P.line([(a, v), (b, v)], color='c1', sw=2.6)
    P.points([0, 1, 2], [.25, .75, 1], color='c1', r=4)
    P.points([0, 1, 2], [0, .25, .75], color='c1', r=4, hollow=True)
    return wrap(P.svg('CDF گسسته'), title='گسسته (پله‌ای)')


@fig('f07-2')
def _(fid):
    P = Plot(fid, w=250, h=210, x=(0, 4), y=(0, 1.1), xticks=[1, 3], xticklabels=['a', 'b'], yticks=[1])
    P.line([(0, 0), (1, 0), (3, 1), (4, 1)], color='c1', sw=2.6)
    return wrap(P.svg('CDF یکنواخت'), title='یکنواخت')


@fig('f07-3')
def _(fid):
    P = Plot(fid, w=250, h=210, x=(-3, 3), y=(0, 1.1), xticks=[-2, 0, 2], yticks=[1])
    P.fn(lambda x: 1 / (1 + exp(-1.7 * x)), color='c1', sw=2.6)
    return wrap(P.svg('CDF هموار'), title='گاوسی (هموار)')


@fig('f07-4')
def _(fid):
    f = lambda x: 0.12 * exp(-0.5 * ((x - 2) / 1.3) ** 2) + 0.16 * exp(-0.5 * ((x - 1.5) / 1.0) ** 2)
    P = Plot(fid, w=520, h=250, x=(-3, 7), y=(0, 0.32), axes='middle', xticks=[1, 3.2], xticklabels=['a', 'b'],
             yticks=None, xlabel='$x$', ylabel='$f(x)$')
    P.area(f, 1, 3.2, color='c4', op=.4)
    P.fn(f, color='c5', sw=2.6)
    P.math(2.1, 0.08, 'P(a<X\\le b)', size=14)
    return P.svg('احتمال یک بازه به صورت سطح زیر چگالی')


@fig('f07-5')
def _(fid):
    P = Plot(fid, w=400, h=220, x=(0, 5), y=(0, 0.7), xticks=[1, 4], xticklabels=['a', 'b'], yticks=[1 / 3],
             yticklabels=['\\dfrac{1}{b-a}'], xlabel='$x$', ylabel='$f(x)$', margins=(52, None, None, None))
    P.line([(0, 0), (1, 0)], color='c1', sw=2.6)
    P.line([(1, 1 / 3), (4, 1 / 3)], color='c1', sw=2.6)
    P.line([(4, 0), (5, 0)], color='c1', sw=2.6)
    P.line([(1, 0), (1, 1 / 3)], color='c1', sw=1.4, dash='4 4')
    P.line([(4, 0), (4, 1 / 3)], color='c1', sw=1.4, dash='4 4')
    return P.svg('چگالی یکنواخت')


@fig('f07-6')
def _(fid):
    P = Plot(fid, w=500, h=260, x=(0, 5), y=(0, 1.6), xticks=[0, 1, 2, 3, 4, 5], yticks=[0, .5, 1, 1.5],
             xlabel='$x$', ylabel='$f_X(x)$', grid=True)
    items = []
    for lam, c in ((0.5, 'c4'), (1, 'c5'), (1.5, 'c6')):
        P.fn(lambda x, l=lam: l * exp(-l * x), color=c)
        items.append(('$\\lambda=%s$' % lam, c, 'line'))
    return wrap(P.svg('چگالی نمایی'), leg=legend(items))


@fig('f07-7')
def _(fid):
    P = Plot(fid, w=540, h=280, x=(-5, 5), y=(0, 1), xticks=list(range(-5, 6)), yticks=[0, .2, .4, .6, .8, 1],
             xlabel='$x$', ylabel='$f_X(x)$', grid=True)
    items = []
    for m, v, c in ((0, 0.2, 'c1'), (0, 1, 'c2'), (0, 5, 'c4'), (-2, 0.5, 'c3')):
        P.fn(lambda x, m=m, v=v: gauss(x, m, math.sqrt(v)), color=c)
        items.append(('$\\mu=%s,\\ \\sigma^2=%s$' % (m, v), c, 'line'))
    return wrap(P.svg('چگالی گاوسی'), leg=legend(items))


@fig('f07-8')
def _(fid):
    P = Plot(fid, w=520, h=260, x=(-10, 10), y=(0, 0.55), xticks=list(range(-10, 11, 2)),
             yticks=[0, .1, .2, .3, .4, .5], xlabel='$x$', grid=True)
    items = []
    for m, b, c in ((0, 1, 'c2'), (0, 2, 'var(--fig-ink)'), (0, 4, 'c1'), (-5, 4, 'c3')):
        P.fn(lambda x, m=m, b=b: exp(-abs(x - m) / b) / (2 * b), color=c, n=401)
        items.append(('$\\mu=%s,\\ b=%s$' % (m, b), c, 'line'))
    return wrap(P.svg('چگالی لاپلاس'), leg=legend(items))


@fig('f07-9')
def _(fid):
    P = Plot(fid, w=520, h=280, x=(0, 1), y=(0, 2.6), xticks=[0, .2, .4, .6, .8, 1], yticks=[0, .5, 1, 1.5, 2, 2.5],
             xlabel='$x$', ylabel='PDF', grid=True)
    specs = [(lambda x: 1 / (PI * sqrt(x * (1 - x))), (0.012, 0.988), '\\alpha=\\beta=0.5', 'c2'),
             (lambda x: 5 * x ** 4, (0, 1), '\\alpha=5,\\ \\beta=1', 'c1'),
             (lambda x: 3 * (1 - x) ** 2, (0, 1), '\\alpha=1,\\ \\beta=3', 'c3'),
             (lambda x: 6 * x * (1 - x), (0, 1), '\\alpha=2,\\ \\beta=2', 'c5'),
             (lambda x: 30 * x * (1 - x) ** 4, (0, 1), '\\alpha=2,\\ \\beta=5', 'c4')]
    items = []
    for f, (a, b), lab, c in specs:
        P.fn(f, a, b, color=c)
        items.append(('$' + lab + '$', c, 'line'))
    return wrap(P.svg('چگالی بتا'), leg=legend(items))


# ================================================================ session 8
def _samp(fid, name, y0, y1):
    d = data('samp_' + name)
    P = Plot(fid, w=640, h=210, x=(1, 1000), y=(y0, y1), xticks=[1, 200, 400, 600, 800, 1000], yticks='auto',
             xlabel=None, ylabel='مقدار نمونه', grid=True, tick_size=11.5)
    xs, ys = d['i'], np.clip(d['x'], y0 - 1, y1 + 1)
    P.line([(1, 0), (1000, 0)], color='var(--muted)', sw=1)
    mask = (d['x'] >= y0) & (d['x'] <= y1)
    P.points(xs[mask], ys[mask], color='c1', r=1.5, sw=0.8)
    return P.svg('نمونه‌های ' + name)


for _nm, _a, _b in (('unif', -0.7, 1.7), ('gauss', -5, 5), ('expo', -1, 9), ('cauchy', -70, 70)):
    REG['samp-' + _nm] = (lambda fid, n=_nm, a=_a, b=_b: _samp(fid, n, a, b))


@fig('f08-1')
def _(fid):
    P = Plot(fid, w=520, h=260, x=(-5, 5), y=(0, 0.45), xticks=list(range(-5, 6)), yticks=[0, .1, .2, .3, .4],
             xlabel='$x$', grid=True)
    P.fn(lambda x: gauss(x), color='c1')
    P.fn(lambda x: 1 / (PI * (1 + x * x)), color='c2')
    leg = legend([('گاوسی $\\mathcal N(0,1)$', 'c1', 'line'), ('کوشی $(0,1)$', 'c2', 'line')])
    return wrap(P.svg('گاوسی و کوشی'), leg=leg)


@fig('f08-2')
def _(fid):
    D = Diagram(fid, x=(-4.4, 4.4), y=(-2.75, 0.6), scale=52)
    D.rect(-1.3, -0.45, 1.3, 0.45, rx=10, fill='var(--rule-2)', sw=1.6)
    D.text(0, 0, 'دماسنج', size=16, color='var(--ink)', weight=600)
    D.rect(-4.2, -2.6, -1.8, -1.8, sw=1.8, fill='var(--fig-bg)')
    D.math(-3, -2.2, '\\mathcal N(\\mu,\\sigma^2)', size=16)
    D.rect(2.4, -2.6, 3.6, -1.8, sw=1.8, fill='var(--fig-bg)')
    D.math(3, -2.2, "\\mu'", size=16)
    D.arrow((-0.6, -0.45), (-2.7, -1.8), sw=1.8)
    D.arrow((0.6, -0.45), (2.7, -1.8), sw=1.8)
    D.math(-1.85, -0.95, 'p', anchor='e', size=16)
    D.math(1.85, -0.95, '1-p', anchor='w', size=16)
    return D.svg('دماسنج خراب')


@fig('f08-3')
def _(fid):
    P = Plot(fid, w=300, h=230, x=(-2, 2), y=(0, 4.5), axes='middle', xticks=None, yticks=None)
    for w_, h_, c in ((0.5, 1, 'c1'), (0.25, 2, 'c2'), (0.125, 4, 'c3')):
        P.line([(-2, 0), (-w_, 0), (-w_, h_), (w_, h_), (w_, 0), (2, 0)], color=c, sw=2.2)
    return wrap(P.svg('پالس‌های مستطیلی'), title='پالس‌های مستطیلی')


@fig('f08-4')
def _(fid):
    P = Plot(fid, w=300, h=230, x=(-3, 3), y=(0, 1), axes='middle', xticks=None, yticks=None)
    for v, c in ((2.5, 'c1'), (0.5, 'c2'), (0.1, 'c3')):
        P.fn(lambda x, v=v: exp(-x * x / (4 * v)) / sqrt(4 * PI * v), color=c, sw=2.2, n=300)
    return wrap(P.svg('چگالی‌های گاوسی باریک‌شونده'), title='چگالی‌های گاوسی')


@fig('f08-5')
def _(fid):
    P = Plot(fid, w=500, h=240, x=(0, 10), y=(0, 0.45), xticks=[2, 6], xticklabels=["\\mu'", '\\mu'], yticks=None)
    P.fn(lambda x: 0.7 * gauss(x, 6, 1), color='c1', sw=2.6)
    P.arrow((2, 0), (2, 0.4), color='c2', sw=2.6, size=10)
    P.math(2.25, 0.4, "(1-p)\\,\\delta(x-\\mu')", anchor='w', size=14, color='c2')
    P.math(8.2, 0.25, 'p\\,\\mathcal N(\\mu,\\sigma^2)', anchor='w', size=14, color='c1')
    return P.svg('متغیر مخلوط')


# ================================================================ session 9
@fig('f09-1')
def _(fid):
    F = lambda x: 1 / (1 + exp(-1.702 * x))
    P = Plot(fid, w=520, h=280, x=(-3, 3), y=(0, 1.08), xticks=[-3, -2, -1, 0, 1, 2, 3], yticks=[0, .25, .5, .75, 1],
             xlabel='$x$', ylabel='$F$', grid=True)
    P.fn(F, color='var(--fig-ink)', sw=2.4)
    P.fn(lambda x: F(x) / F(0.7), -3, 0.7, color='c2', sw=2.4)
    P.line([(0.7, 1), (3, 1)], color='c2', sw=2.4)
    P.line([(0.7, 0), (0.7, 1)], color='var(--muted)', sw=1.3, dash='4 4')
    P.math(0.7, 0.02, 'a', anchor='s', size=15, color='var(--muted)')
    leg = legend([('$F_X(x)$', 'var(--fig-ink)', 'line'), ('$F_X(x\\,|\\,X\\le a)$', 'c2', 'line')])
    return wrap(P.svg('CDF شرطی'), leg=leg)


@fig('f09-2')
def _(fid):
    P = Plot(fid, w=500, h=250, x=(0, 3), y=(0, 1.1), xticks=[0, 1], xticklabels=['0', 'a'], yticks=None)
    P.area(lambda x: exp(-x), 0, 3, color='c1', op=.18)
    P.fn(lambda x: exp(-x), 0, 3, color='c1', sw=2.4)
    P.area(lambda x: exp(-(x - 1)), 1, 3, color='c5', op=.18)
    P.fn(lambda x: exp(-(x - 1)), 1, 3, color='c5', sw=2.4)
    for x in (1.2, 1.7, 2.3, 2.8):
        P.arrow((x, math.exp(-x) + 0.01), (x, math.exp(-(x - 1)) - 0.01), color='var(--muted)', sw=1.8, size=7)
    leg = legend([('$f_X(x)$', 'c1', 'line'), ('$f_X(x\\,|\\,X>a)$', 'c5', 'line')])
    return wrap(P.svg('بی‌حافظگی نمایی'), leg=leg)


@fig('f09-3')
def _(fid):
    comps = [(0.3, -1.5, 0.5), (0.4, 2, 1.2), (0.3, 5, 0.4)]
    P = Plot(fid, w=520, h=250, x=(-4, 8), y=(0, 0.32), xticks=None, yticks=None, xlabel='$x$')
    for w_, m, s in comps:
        P.fn(lambda x, w_=w_, m=m, s=s: w_ * gauss(x, m, s), color='c1', sw=1.6, dash='5 4', n=400)
    P.fn(lambda x: sum(w_ * gauss(x, m, s) for w_, m, s in comps), color='c2', sw=2.6, n=400)
    leg = legend([('مؤلفه‌ها', 'c1', 'dash'), ('مجموع وزن‌دار (GMM)', 'c2', 'line')])
    return wrap(P.svg('مدل مخلوط گاوسی'), leg=leg)


@fig('f09-4')
def _(fid):
    labs = ['\\mu-3\\sigma', '\\mu-2\\sigma', '\\mu-\\sigma', '\\mu', '\\mu+\\sigma', '\\mu+2\\sigma', '\\mu+3\\sigma']
    P = Plot(fid, w=580, h=260, x=(-3.6, 3.6), y=(0, 0.46), xticks=[-3, -2, -1, 0, 1, 2, 3], xticklabels=labs,
             yticks=None, tick_size=11)
    for a, b, op in ((-1, 1, .42), (-2, -1, .26), (1, 2, .26), (-3, -2, .12), (2, 3, .12)):
        P.area(gauss, a, b, color='c1', op=op)
    P.fn(gauss, color='var(--fig-ink)', sw=2.2)
    for x, y, t in ((-0.5, .15, '34.1\\%'), (0.5, .15, '34.1\\%'), (-1.5, .05, '13.6\\%'), (1.5, .05, '13.6\\%'),
                    (-2.5, .03, '2.15\\%'), (2.5, .03, '2.15\\%')):
        P.math(x, y, t, size=12)
    return P.svg('قاعده ۶۸-۹۵-۹۹٫۷')


@fig('f09-5')
def _(fid):
    P = Plot(fid, w=500, h=260, x=(-5, 5), y=(0, 0.7), xticks=list(range(-5, 6)), yticks=[0, .2, .4, .6],
             xlabel='$x$', grid=True)
    items = []
    for x0, g, c in ((0, 0.5, 'c4'), (0, 1, 'c5'), (0, 2, 'c6'), (-2, 1, 'c3')):
        P.fn(lambda x, x0=x0, g=g: 1 / (PI * g * (1 + ((x - x0) / g) ** 2)), color=c, n=400)
        items.append(('$x_0=%s,\\ \\gamma=%s$' % (x0, g), c, 'line'))
    return wrap(P.svg('چگالی کوشی'), leg=legend(items))


@fig('f09-6')
def _(fid):
    P = Plot(fid, w=500, h=260, x=(0, 1), y=(0, 9), xticks=[0, .2, .4, .6, .8, 1], yticks=[0, 2, 4, 6, 8],
             xlabel='$p$', grid=True)
    P.fn(lambda x: 1.0, color='c7', sw=1.8, dash='6 4')
    P.fn(lambda x: 11 * 120 * x ** 7 * (1 - x) ** 3, color='c1')
    P.fn(lambda x: 2.9666e27 * x ** 70 * (1 - x) ** 30, color='c2', n=400)
    leg = legend([('پیشین (یکنواخت)', 'c7', 'dash'), ('$n=10,\\ k=7$', 'c1', 'line'), ('$n=100,\\ k=70$', 'c2', 'line')])
    return wrap(P.svg('پسین بتا'), leg=leg)


# ================================================================ session 10
@fig('f10-1')
def _(fid):
    P = Plot(fid, w=520, h=240, x=(-50, 250), y=(0, 0.045), xticks=[-50, 0, 50, 100, 150, 200, 250], yticks=None,
             xlabel='$x$')
    P.area(lambda x: gauss(x, 100, 10), -50, 250, color='c2', op=.32)
    P.fn(lambda x: gauss(x, 100, 10), color='c2', sw=2)
    P.area(lambda x: gauss(x, 100, 50), -50, 250, color='c1', op=.22)
    P.fn(lambda x: gauss(x, 100, 50), color='c1', sw=2)
    P.line([(100, 0), (100, 0.045)], color='var(--muted)', sw=1.3, dash='4 4')
    P.math(104, 0.042, '\\text{میانگین}=100', anchor='w', size=13)
    leg = legend([('انحراف معیار $=10$', 'c2', 'box'), ('انحراف معیار $=50$', 'c1', 'box')])
    return wrap(P.svg('دو توزیع با میانگین برابر'), leg=leg)


@fig('f10-2')
def _(fid):
    P = Plot(fid, w=290, h=210, x=(0, 8.5), y=(0, 0.6), axes='middle', xticks=[1, 3, 7], yticks=None)
    P.stems([1, 3, 7], [0.2, 0.5, 0.3], color='c2', r=4.5, sw=2.6)
    for x, y in ((1, .2), (3, .5), (7, .3)):
        P.math(x, y + 0.03, str(y), anchor='s', size=13)
    return P.svg('PMF نمونه')


@fig('f10-3')
def _(fid):
    f = lambda x: x ** 1.5 * exp(-x / 1.3) / 2.5615
    P = Plot(fid, w=380, h=230, x=(0, 10), y=(0, 0.3), xticks=None, yticks=None, xlabel='$x$', ylabel='$f(x)$')
    P.fn(f, color='var(--fig-ink)', sw=2.2)
    for x, lab, c, dy in ((1.95, 'مد', 'c3', 0.026), (2.83, 'میانه', 'c1', 0.02), (3.25, 'میانگین', 'c2', 0.03)):
        P.line([(x, 0), (x, float(f(x)))], color=c, sw=1.6, dash='4 3')
    P.text(1.95, float(f(1.95)) + 0.025, 'مد', size=12.5, color='c3', rtl=True)
    P.text(3.0, 0.232, 'میانه', anchor='start', size=12.5, color='c1', rtl=True)
    P.text(3.45, 0.188, 'میانگین', anchor='start', size=12.5, color='c2', rtl=True)
    return P.svg('مد، میانه و میانگین')


# ================================================================ session 11
@fig('f11-1')
def _(fid):
    D = Diagram(fid, x=(-0.3, 11.6), y=(-1.9, 2.0), scale=46)
    pts = [(0, 0), (1.2, 0.9), (2.6, 0.6), (3, -0.4), (2, -1.3), (0.5, -1.1)]
    # smooth closed curve through points (Catmull-Rom)
    P_ = [D.P(*p) for p in pts]
    n = len(P_)
    d = 'M%.1f,%.1f' % P_[0]
    for i in range(n):
        p0, p1, p2, p3 = P_[i - 1], P_[i], P_[(i + 1) % n], P_[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += ' C%.1f,%.1f %.1f,%.1f %.1f,%.1f' % (c1 + c2 + p2)
    D.path(d + ' Z', stroke='var(--fig-ink)', fill='c6', fop=.1, sw=2)
    D.ellipse(1.5, -0.1, 0.75, 0.45, stroke='none', fill='c7', fop=.5)
    D.math(1.5, -0.1, 'X\\in E', size=14)
    D.math(0.45, -0.8, '\\Omega', size=16)
    D.arrow((6, -1.5), (6, 1.6), sw=1.6, size=8)
    D.math(6.32, 1.45, '\\mathbb R', anchor='w', size=15)
    D.rect(5.92, -0.3, 6.08, 0.5, stroke='none', fill='c4', fop=.9)
    D.math(6.3, 0.1, 'E', anchor='w', size=15)
    D.arrow((9.5, -1.5), (9.5, 1.6), sw=1.6, size=8)
    D.math(9.82, 1.45, '\\mathbb R', anchor='w', size=15)
    D.rect(9.42, 0.6, 9.58, 1.0, stroke='none', fill='c2', fop=.9)
    D.math(9.7, 0.8, '\\{g(x):x\\in E\\}', anchor='w', size=12.5)
    D.arrow((2.2, 0.25), (5.85, 0.2), bend=25, sw=1.6, size=8)
    D.math(4.0, 1.05, 'X', size=15)
    D.arrow((6.15, 0.3), (9.35, 0.8), bend=25, sw=1.6, size=8)
    D.math(7.8, 1.35, 'g', size=15)
    D.arrow((2.1, -0.45), (9.35, 0.55), bend=-30, sw=1.6, size=8)
    D.math(5.2, -1.3, 'Y=g(X)', size=14)
    return D.svg('تابعی از متغیر تصادفی')


# ================================================================ session 12
@fig('f12-1')
def _(fid):
    g = lambda x: 0.3171 * (x ** 3 / 3 - 3.5 * x ** 2 + 8.64 * x) + 1.6247
    D = Diagram(fid, x=(-1.5, 8.0), y=(-0.8, 4.8), scale=52)
    D.arrow((-1, 0), (7.5, 0), color='c1', sw=1.4, size=8)
    D.arrow((0, -0.6), (0, 4.5), color='c1', sw=1.4, size=8)
    D.math(7.6, 0, 'x', anchor='w', size=15)
    D.math(-0.1, 4.6, 'g(x)', anchor='se', size=15)
    xs = np.linspace(-0.6, 6.6, 140)
    D.line([(x, g(x)) for x in xs], sw=2.6)
    D.line([(1.6, -0.6), (1.6, 4.4)], color='var(--muted)', sw=1.2, dash='4 4')
    D.line([(5.4, -0.6), (5.4, 4.4)], color='var(--muted)', sw=1.2, dash='4 4')
    for (a, b), c in (((1.0, 1.6), 'c2'), ((3.2, 3.7), 'c3')):
        ga, gb = g(a), g(b)
        D.line([(a, 0), (a, ga), (-0.7, ga)], color=c, sw=2.2)
        D.line([(b, 0), (b, gb), (-0.7, gb)], color=c, sw=2.2)
        D.arrow((a, -0.35), (b, -0.35), both=True, sw=1.4, size=6)
        D.arrow((-0.95, min(ga, gb)), (-0.95, max(ga, gb)), both=True, sw=1.4, size=6)
    D.text(0.45, 4.05, 'صعودی', size=13)
    D.text(4.3, 3.2, 'نزولی', size=13)
    D.text(6.7, 0.65, 'صعودی', size=13)
    return D.svg('تابع غیریکنوا')


@fig('f12-2')
def _(fid):
    P = Plot(fid, w=280, h=220, x=(-2.5, 2.5), y=(0, 0.5), xticks=[-2, -1, 0, 1, 2], yticks=[0.25])
    P.line([(-2.5, 0), (-2, 0)], color='c1', sw=2.6)
    P.line([(-2, .25), (2, .25)], color='c1', sw=2.6)
    P.line([(2, 0), (2.5, 0)], color='c1', sw=2.6)
    return wrap(P.svg('f_X'), title='$f_X(x)$')


@fig('f12-3')
def _(fid):
    P = Plot(fid, w=280, h=220, x=(0, 4.5), y=(0, 1.6), xticks=[0, 1, 2, 3, 4], yticks=[0.5, 1, 1.5])
    P.fn(lambda x: 1 / (4 * sqrt(x)), 0.025, 4, color='c2', sw=2.6)
    P.line([(4, 0), (4.5, 0)], color='c2', sw=2.6)
    return wrap(P.svg('f_Y'), title='$f_Y(y)=\\frac{1}{4\\sqrt y}$')


@fig('f12-4')
def _(fid):
    return flow([('$X\\sim F_X$', '(هر توزیع)', 'blue'), ('$U\\sim\\mathcal U(0,1)$', '', 'green'),
                 ('$Z\\sim F_Z$', '(توزیع دلخواه)', 'red')],
                [('$U=F_X(X)$', ''), ('$Z=F_Z^{-1}(U)$', '')])


# ================================================================ session 13
@fig('f13-1')
def _(fid):
    D = Diagram(fid, x=(-2.9, 3.4), y=(-2.4, 2.8), scale=52)
    D.rect(-2.5, -2, 1.5, 1.2, stroke='none', fill='c1', fop=.16)
    D.arrow((-2.7, 0), (3.0, 0), sw=1.4, size=8)
    D.arrow((0, -2.2), (0, 2.4), sw=1.4, size=8)
    D.math(3.1, 0, 'x', anchor='w')
    D.math(0, 2.5, 'y', anchor='s')
    D.line([(1.5, -2), (1.5, 1.2), (-2.5, 1.2)], color='c1', sw=2.2)
    D.circle(1.5, 1.2, 0.07, stroke='var(--fig-ink)', fill='var(--fig-ink)')
    D.math(1.6, 1.3, '(x,y)', anchor='sw', size=15)
    D.math(-1.2, -1.1, 'F_{X,Y}(x,y)', size=15, color='c1')
    return D.svg('CDF مشترک')


@fig('f13-2')
def _(fid):
    D = Diagram(fid, x=(-2.0, 4.9), y=(-2.0, 3.8), scale=48)
    D.rect(1, -1.6, 2.2, 3.2, stroke='none', fill='c7', fop=.25)
    D.rect(-1.6, 1, 4.2, 2, stroke='none', fill='c7', fop=.25)
    D.rect(1, 1, 2.2, 2, stroke='c1', fill='c1', fop=.35, sw=2)
    D.arrow((-1.8, 0), (4.5, 0), sw=1.4, size=8)
    D.arrow((0, -1.8), (0, 3.5), sw=1.4, size=8)
    D.math(4.6, 0, 'X', anchor='w')
    D.math(0, 3.6, 'Y', anchor='s')
    for x in (1, 2.2):
        D.line([(x, -1.6), (x, 3.2)], sw=1.1, dash='4 4', color='var(--muted)')
    for y in (1, 2):
        D.line([(-1.6, y), (4.2, y)], sw=1.1, dash='4 4', color='var(--muted)')
    D.math(0.95, -0.1, 'x_1', anchor='ne', size=14)
    D.math(2.25, -0.1, 'x_2', anchor='nw', size=14)
    D.math(-0.1, 0.8, 'y_1', anchor='e', size=14)
    D.math(-0.1, 2.2, 'y_2', anchor='e', size=14)
    return D.svg('احتمال یک مستطیل')


@fig('f13-3')
def _(fid):
    return surface3d(fid)


@fig('f13-4')
def _(fid):
    D = Diagram(fid, x=(-0.25, 1.45), y=(-0.25, 1.45), scale=150)
    D.line([(0, 0), (1, 0), (1, 1)], close=True, fill='c3', fop=.2, sw=0, color='none')
    D.arrow((-0.1, 0), (1.35, 0), sw=1.4, size=8)
    D.arrow((0, -0.1), (0, 1.35), sw=1.4, size=8)
    D.math(1.38, 0, 'x', anchor='w')
    D.math(0, 1.38, 'y', anchor='s')
    D.line([(0, 0), (1, 0), (1, 1), (0, 0)], sw=2.2)
    D.line([(0, 0), (0, 1), (1, 1)], sw=1.3, dash='4 4', color='var(--muted)')
    D.math(0.68, 0.3, 'f=2', size=15)
    D.math(0.3, 0.7, 'f=0', size=15, color='var(--muted)')
    D.math(1, -0.04, '1', anchor='n', size=14)
    D.math(-0.04, 1, '1', anchor='e', size=14)
    return D.svg('چگالی روی مثلث')


def surface3d(fid):
    """Bivariate Gaussian surface (view az=35, el=40) with marginals on the walls."""
    az, el = math.radians(35), math.radians(40)
    zs = 15.0

    def proj(x, y, z):
        # pgfplots-like view: rotate around z by az, then tilt by el
        xr = x * math.cos(az) - y * math.sin(az)
        yr = x * math.sin(az) + y * math.cos(az)
        sx = xr
        sy = -(yr * math.sin(el) + z * zs * math.cos(el))
        depth = yr * math.cos(el) - z * math.sin(el)
        return sx, sy, depth

    f = lambda x, y: math.exp(-(x * x - 1.2 * x * y + 1.5 * y * y) / 1.6) / (2 * PI)
    N = 24
    g = np.linspace(-3, 3, N + 1)
    quads = []
    for i in range(N):
        for j in range(N):
            cs = [(g[i], g[j]), (g[i + 1], g[j]), (g[i + 1], g[j + 1]), (g[i], g[j + 1])]
            ps = [proj(x, y, f(x, y)) for x, y in cs]
            zc = sum(f(x, y) for x, y in cs) / 4
            quads.append((sum(p[2] for p in ps) / 4, ps, zc))
    xw = max((-3, 3), key=lambda v: proj(v, 0, 0)[2])
    yw = max((-3, 3), key=lambda v: proj(0, v, 0)[2])
    allp = [p for q in quads for p in q[1]]
    box = [proj(x, y, 0) for x in (-3, 3) for y in (-3, 3)]
    wall = [proj(x, yw, z) for x in (-3, 3) for z in (0, 0.25)] + [proj(xw, y, z) for y in (-3, 3) for z in (0, 0.25)]
    xs = [p[0] for p in allp + box + wall]
    ys = [p[1] for p in allp + box + wall]
    W, H = 460, 330
    sc = min((W - 40) / (max(xs) - min(xs)), (H - 40) / (max(ys) - min(ys)))
    ox, oy = 20 - min(xs) * sc + ((W - 40) - (max(xs) - min(xs)) * sc) / 2, 20 - min(ys) * sc

    def T(p):
        return (ox + p[0] * sc, oy + p[1] * sc)
    F = Fig(W, H, fid)
    # floor + back walls
    floor = [T(proj(x, y, 0)) for x, y in ((-3, -3), (3, -3), (3, 3), (-3, 3))]
    F.poly(floor, close=True, stroke='var(--fig-grid)', fill='var(--rule-2)', sw=1)
    F.poly([T(proj(x, yw, z)) for x, z in ((-3, 0), (3, 0), (3, 0.25), (-3, 0.25))], close=True,
           stroke='var(--fig-grid)', fill='var(--rule-2)', sw=1, fop=.6)
    F.poly([T(proj(xw, y, z)) for y, z in ((-3, 0), (3, 0), (3, 0.25), (-3, 0.25))], close=True,
           stroke='var(--fig-grid)', fill='var(--rule-2)', sw=1, fop=.6)
    # marginal curves on the walls
    t = np.linspace(-3, 3, 120)
    F.poly([T(proj(x, yw, 0.2 * math.exp(-x * x / 2.4))) for x in t], stroke='c2', sw=2.6)
    F.poly([T(proj(xw, y, 0.2 * math.exp(-y * y / 1.3))) for y in t], stroke='c1', sw=2.6)
    zmax = max(q[2] for q in quads)
    for depth, ps, zc in sorted(quads, key=lambda q: -q[0]):
        pct = 12 + 70 * (zc / zmax)
        F.poly([T(p) for p in ps], close=True, stroke='color-mix(in srgb, var(--c6) 55%%, var(--fig-bg))' % (),
               fill='color-mix(in srgb, var(--c6) %d%%, var(--fig-bg))' % pct, sw=0.6)
    lx = T(proj(0, -yw * 1.15, 0))
    ly = T(proj(-xw * 1.15, 0, 0))
    F.math_px(lx[0], lx[1], 'x_1', anchor='c', size=15)
    F.math_px(ly[0], ly[1], 'x_2', anchor='c', size=15)
    leg = legend([('چگالی مشترک $f(x_1,x_2)$', 'c6', 'box'), ('حاشیه $x_1$', 'c2', 'line'), ('حاشیه $x_2$', 'c1', 'line')])
    return wrap(F.svg('سطح چگالی مشترک'), leg=leg)


# ================================================================ session 14 / 15: contours
def contour(fid, r, levels, title, w=230):
    P = Plot(fid, w=w, h=w, x=(-3, 3), y=(-3, 3), axes='box', xticks=None, yticks=None, equal=True,
             margins=(8, 8, 8, 8))
    k = 1 - r * r
    for i, L in enumerate(sorted(levels)):
        arg = L * 2 * PI * math.sqrt(k)
        if arg >= 1:
            continue
        Q = -2 * k * math.log(arg)
        t = np.linspace(0, 2 * PI, 200)
        u = math.sqrt(Q / (1 - r)) * np.cos(t)
        v = math.sqrt(Q / (1 + r)) * np.sin(t)
        x, y = (u + v) / math.sqrt(2), (u - v) / math.sqrt(2)
        shade = 45 + 45 * i / max(1, len(levels) - 1)
        P.curve(np.append(x, x[0]), np.append(y, y[0]),
                color='color-mix(in srgb, var(--c1) %d%%, var(--fig-bg))' % shade, sw=2)
    P.line([(-3, 0), (3, 0)], color='var(--fig-grid)', sw=1)
    P.line([(0, -3), (0, 3)], color='var(--fig-grid)', sw=1)
    return wrap(P.svg('منحنی‌های تراز ' + title), title=title)


@fig('f14-1')
def _(fid):
    return contour(fid, 0.0, [0.02, 0.06, 0.1, 0.14], '$r=0$')


@fig('f14-2')
def _(fid):
    return contour(fid, 0.7, [0.02, 0.06, 0.1, 0.14, 0.2], '$r=0.7$')


@fig('f14-3')
def _(fid):
    return contour(fid, -0.9, [0.02, 0.06, 0.1, 0.2, 0.3], '$r=-0.9$')


@fig('f15-1')
def _(fid):
    return contour(fid, 0.5, [0.03, 0.08, 0.13], '$r=0.5$')


@fig('f15-2')
def _(fid):
    return contour(fid, 0.95, [0.05, 0.15, 0.3], '$r=0.95$')


@fig('f15-3')
def _(fid):
    P = Plot(fid, w=230, h=230, x=(-3, 3), y=(-3, 3), axes='box', xticks=None, yticks=None, equal=True,
             margins=(8, 8, 8, 8))
    P.line([(-3, 0), (3, 0)], color='var(--fig-grid)', sw=1)
    P.line([(0, -3), (0, 3)], color='var(--fig-grid)', sw=1)
    P.line([(-3, -3), (3, 3)], color='c2', sw=2.8)
    return wrap(P.svg('r=1 تکین'), title='$r=1$ (تکین)')


def scatter(fid, xs, ys, color, title):
    P = Plot(fid, w=210, h=210, x=(min(xs) - 0.3, max(xs) + 0.3), y=(min(ys) - 0.3, max(ys) + 0.3), axes='box',
             xticks=None, yticks=None, margins=(8, 8, 8, 8))
    P.points(xs, ys, color=color, r=2.6, sw=0.6)
    return wrap(P.svg('نمودار پراکندگی'), title=title)


@fig('f15-4')
def _(fid):
    rng = np.random.default_rng(4)
    x = np.linspace(-2, 2, 120)
    return scatter(fid, x + 0.4 * rng.uniform(-1, 1, 120), x + 0.4 * rng.uniform(-1, 1, 120), 'c1', '$\\rho\\approx0.9$')


@fig('f15-5')
def _(fid):
    rng = np.random.default_rng(5)
    x = np.linspace(-2, 2, 120)
    return scatter(fid, x + 0.6 * rng.uniform(-1, 1, 120), -x + 0.9 * rng.uniform(-1, 1, 120), 'c2', '$\\rho\\approx-0.7$')


@fig('f15-6')
def _(fid):
    rng = np.random.default_rng(6)
    return scatter(fid, 2 * rng.uniform(-1, 1, 120), 2 * rng.uniform(-1, 1, 120), 'c7', '$\\rho\\approx0$ (مستقل)')


@fig('f15-7')
def _(fid):
    rng = np.random.default_rng(7)
    x = np.linspace(-1, 1, 120)
    return scatter(fid, x, x * x + 0.05 * rng.uniform(-1, 1, 120), 'c3', '$\\rho=0$ (ولی وابسته!)')


# ================================================================ session 16
def dice_bars(fid, xs, ys, title, color, w=220, ymax=0.25, xt=None):
    P = Plot(fid, w=w, h=170, x=(min(xs) - 0.8, max(xs) + 0.8), y=(0, ymax), xticks=xt or xs, yticks=None,
             tick_size=11.5)
    P.bars(xs, ys, 0.62, color=color, op=.7)
    return wrap(P.svg(title), title=title)


@fig('f16-1')
def _(fid):
    return dice_bars(fid, list(range(1, 7)), [1 / 6] * 6, '$\\mathbb P_X$', 'c6')


@fig('f16-2')
def _(fid):
    return dice_bars(fid, list(range(1, 7)), [1 / 6] * 6, '$\\mathbb P_Y$', 'c6')


@fig('f16-3')
def _(fid):
    xs = list(range(2, 13))
    ys = [(6 - abs(k - 7)) / 36 for k in xs]
    return dice_bars(fid, xs, ys, '$\\mathbb P_{X+Y}$', 'c4', w=290, ymax=0.2, xt=[2, 4, 6, 8, 10, 12])


@fig('f16-4')
def _(fid):
    D = Diagram(fid, x=(-1.6, 3.9), y=(-1.6, 3.2), scale=56)
    D.rect(0, 0, 2, 2, stroke='none', fill='c6', fop=.25)
    pid = fid + '-hatch'
    D.defs.append('<pattern id="%s" patternUnits="userSpaceOnUse" width="6" height="6"><path d="M0,3 H6" style="stroke:var(--c3);stroke-width:1.4"/></pattern>' % pid)
    P_ = [D.P(0, 0), D.P(1.5, 0), D.P(0, 1.5)]
    D.add('<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z" style="fill:url(#%s);stroke:var(--c3);stroke-width:1.4"/>' % (
        P_[0] + P_[1] + P_[2] + (pid,)))
    D.arrow((-1.5, 0), (3.5, 0), sw=1.4, size=8)
    D.arrow((0, -1.5), (0, 3.0), sw=1.4, size=8)
    D.math(3.6, 0, 'x', anchor='w')
    D.math(0, 3.1, 'y', anchor='s')
    D.line([(-1.2, 2.7), (2.7, -1.2)], color='c4', sw=2.4)
    D.math(2.75, -1.25, 'x+y=z', anchor='nw', size=14, color='c4')
    D.math(-0.08, 1.5, 'z', anchor='e', size=14)
    D.math(1.5, -0.08, 'z', anchor='n', size=14)
    D.math(1.25, 1.45, 'f_{XY}>0', size=13)
    return D.svg('ناحیه جمع دو متغیر')


def unif_box(fid, pts, xmax, title, w=200):
    P = Plot(fid, w=w, h=170, x=(0, xmax), y=(0, 1.3), xticks=list(range(int(xmax) + 1)), yticks=[1], tick_size=11.5)
    P.polyfill(pts, color='c6', op=.45, stroke='var(--fig-ink)', sw=1.6)
    return wrap(P.svg(title), title=title)


@fig('f16-5')
def _(fid):
    return unif_box(fid, [(0, 0), (0, 1), (1, 1), (1, 0)], 1.3, '$X$')


@fig('f16-6')
def _(fid):
    return unif_box(fid, [(0, 0), (0, 1), (1, 1), (1, 0)], 1.3, '$Y$')


@fig('f16-7')
def _(fid):
    return unif_box(fid, [(0, 0), (1, 1), (2, 0)], 2.2, '$Z=X+Y$', w=250)


# ================================================================ session 17
def _ih(fid, n):
    d = data('ih%d' % n)
    P = Plot(fid, w=200, h=170, x=(-1.2, 1.2), y=(0, 1.6), xticks=None, yticks=None)
    P.curve(d['z'], d['p'], color='c1', sw=2.4)
    return wrap(P.svg('n=%d' % n), title='$n=%d$' % n)


def _bs(fid, n):
    d = data('bs%d' % n)
    ymax = float(d['p'].max()) * 1.15
    P = Plot(fid, w=200, h=170, x=(float(d['z'].min()) - 0.4, float(d['z'].max()) + 0.4), y=(0, ymax), xticks=None,
             yticks=None)
    P.stems(d['z'], d['p'], color='c4', r=(2.8 if n < 10 else 0), sw=(2.2 if n < 10 else 1.2), marker=('o' if n < 10 else None))
    return wrap(P.svg('n=%d' % n), title='$n=%d$' % n)


for _n in (1, 2, 3, 30):
    REG['ih-%d' % _n] = (lambda fid, n=_n: _ih(fid, n))
for _n in (1, 2, 3, 100):
    REG['bs-%d' % _n] = (lambda fid, n=_n: _bs(fid, n))


@fig('f17-1')
def _(fid):
    P = Plot(fid, w=500, h=260, x=(0, 12), y=(0, 0.55), xticks=[0, 2, 4, 6, 8, 10, 12], yticks=[0, .1, .2, .3, .4, .5],
             xlabel='$z$', grid=True)
    specs = [(lambda x: exp(-x / 2) / sqrt(2 * PI * x), 0.04, 'c1', 1), (lambda x: exp(-x / 2) / 2, 0, 'c2', 2),
             (lambda x: sqrt(x) * exp(-x / 2) / (2 ** 1.5 * 0.886227), 0, 'c3', 3),
             (lambda x: x ** 2 * exp(-x / 2) / 16, 0, 'c4', 6)]
    items = []
    for f, a, c, k in specs:
        P.fn(f, a, 12, color=c)
        items.append(('$k=%d$' % k, c, 'line'))
    return wrap(P.svg('چگالی خی‌دو'), leg=legend(items))


# ================================================================ session 18
@fig('f18-1')
def _(fid):
    f = lambda x: (0.1 * exp(-0.5 * ((x - 1.5) / 0.6) ** 2) + 0.15 * exp(-0.5 * ((x - 3.2) / 0.5) ** 2)
                   + 0.12 * exp(-0.5 * ((x - 2.4) / 0.6) ** 2) + 0.08 * exp(-0.5 * ((x - 5) / 0.3) ** 2)
                   + (0.04 * exp(-(x - 5) / 2.5) if x > 5 else 0))
    P = Plot(fid, w=500, h=240, x=(0, 10), y=(0, 0.32), xticks=[3.2, 6], xticklabels=['\\mu', 'a'], yticks=None,
             xlabel='$x$', ylabel='$f(x)$')
    P.area(f, 6, 10, color='c2', op=.3)
    P.fn(f, color='var(--fig-ink)', sw=2.2, n=400)
    P.line([(3.2, 0), (3.2, 0.2)], color='var(--muted)', sw=1.4, dash='2 4')
    P.math(7.6, 0.06, '\\mathbb P(X\\ge a)', size=14, color='c2')
    return P.svg('نامساوی مارکوف')


@fig('f18-2')
def _(fid):
    P = Plot(fid, w=540, h=230, x=(-4, 4), y=(0, 0.48), axes='middle', xticks=[-2, 0, 2],
             xticklabels=['\\mu-k\\sigma', '\\mu', '\\mu+k\\sigma'], yticks=None)
    P.area(gauss, -4, -2, color='c1', op=.32)
    P.area(gauss, 2, 4, color='c1', op=.32)
    P.fn(gauss, color='c5', sw=2.6)
    P.arrow((-2, 0.3), (0, 0.3), both=True, color='c1', sw=1.6, size=7)
    P.arrow((0, 0.3), (2, 0.3), both=True, color='c1', sw=1.6, size=7)
    P.math(-1, 0.31, 'k\\sigma', anchor='s', size=13, color='c1')
    P.math(1, 0.31, 'k\\sigma', anchor='s', size=13, color='c1')
    P.line([(-2, 0), (-2, 0.32)], sw=1.2)
    P.line([(2, 0), (2, 0.32)], sw=1.2)
    return P.svg('نامساوی چبیشف')


@fig('f18-3')
def _(fid):
    P = Plot(fid, w=500, h=270, x=(-3, 3), y=(0, 1.08), xticks=[-3, -2, -1, 0, 1, 2, 3], yticks=[0, .2, .4, .6, .8, 1],
             xlabel='$x$', grid=True)
    P.fn(lambda x: 1 / (1 + exp(-1.702 * x)), color='c1', sw=2.6)
    jumps = [-1.6, -1.1, -0.7, -0.35, -0.1, 0.15, 0.4, 0.9, 1.3, 2.1]
    pts = [(-3, 0)]
    for i, j in enumerate(jumps):
        pts += [(j, i / 10), (j, (i + 1) / 10)]
    pts.append((3, 1))
    P.line(pts, color='c2', sw=2)
    leg = legend([('$F_X(x)$ (آماری)', 'c1', 'line'), ('$\\hat F_X(x)$ (تجربی، $n=10$)', 'c2', 'line')])
    return wrap(P.svg('CDF تجربی'), leg=leg)


# ================================================================ session 19-22
@fig('f19-1')
def _(fid):
    D = Diagram(fid, x=(-1.9, 9.9), y=(-1.6, 1.6), scale=46)
    for x, tone, a, b in ((0, 'c1', 'مدل احتمالاتی', 'f_X(x;\\theta)'), (8, 'c4', 'داده‌ها', 'X_1,\\ldots,X_n')):
        D.rect(x - 1.7, -0.6, x + 1.7, 0.6, rx=10, stroke=tone, fill=tone, fop=.1, sw=2)
        D.text(x, 0.22, a, size=15, color='var(--ink)', weight=600)
        D.math(x, -0.25, b, size=15)
    D.arrow((1.0, 0.65), (7.0, 0.65), bend=14, color='c1', sw=2.2)
    D.text(4, 1.35, 'احتمال (قیاسی)', size=14, color='c1', weight=600)
    D.arrow((7.0, -0.65), (1.0, -0.65), bend=14, color='c4', sw=2.2)
    D.text(4, -1.35, 'آمار (استقرایی)', size=14, color='c4', weight=600)
    return D.svg('احتمال و آمار')


@fig('f20-1')
def _(fid):
    D = Diagram(fid, x=(-3.6, 3.6), y=(-1.9, 1.9), scale=56)
    D.ellipse(0, 0, 3.2, 1.5, rot=20, stroke='var(--fig-ink)', fill='c4', fop=.25, sw=1.8)
    D.ellipse(-0.7, 0.35, 0.95, 0.5, rot=-10, stroke='var(--fig-ink)', fill='c6', fop=.4, sw=1.8)
    D.circle(-0.2, 0.25, 0.06, stroke='var(--fig-ink)', fill='var(--fig-ink)')
    D.math(-0.1, 0.33, '\\beta_0', anchor='sw', size=15)
    D.math(-1.5, 0.55, '\\hat\\beta_2', size=15)
    D.math(2.4, -0.9, '\\hat\\beta_1', size=15)
    return D.svg('گرایش و واریانس')


@fig('f21-1')
def _(fid):
    P = Plot(fid, w=500, h=270, x=(0, 1), y=(0, 0.19), xticks=[0, .2, .4, .6, .8, 1], yticks=[0, .05, .1, .15],
             xlabel='$p$', ylabel='$L(p)=p^2(1-p)$', grid=True)
    P.fn(lambda x: x * x * (1 - x), color='c3', sw=2.6)
    P.line([(2 / 3, 0), (2 / 3, 4 / 27)], color='c2', sw=1.6, dash='5 4')
    P.points([2 / 3], [4 / 27], color='c2', r=5)
    P.math(2 / 3, 4 / 27 + 0.008, '\\hat p=\\tfrac23', anchor='s', size=15, color='c2')
    return P.svg('تابع درست‌نمایی')


@fig('f22-1')
def _(fid):
    P = Plot(fid, w=520, h=270, x=(0, 5), y=(0, 0.036), xticks=[0, 1, 2, 3, 4, 5], yticks=[0, .01, .02, .03],
             xlabel='$\\theta$', ylabel='$L(\\theta)$', grid=True)
    P.line([(0, 0), (2, 0)], color='c3', sw=2.6)
    P.fn(lambda x: x ** -5, 2, 5, color='c3', sw=2.6)
    P.line([(2, 0), (2, 0.03125)], color='c3', sw=1.3, dash='4 4')
    P.points([2], [0], color='c3', r=4.5, hollow=True)
    P.points([2], [0.03125], color='c2', r=5)
    P.math(2.12, 0.0322, '\\hat\\theta_{\\mathrm{ML}}=\\max_i X_i=2', anchor='w', size=14, color='c2')
    P.points([0.4, 0.7, 1.3, 1.6, 2.0], [0.0016] * 5, color='c1', r=5, mark='x')
    return P.svg('درست‌نمایی یکنواخت')


@fig('f22-2')
def _(fid):
    P = Plot(fid, w=500, h=270, x=(0, 1.05), y=(0, 10.5), xticks=[0, .2, .4, .6, .8, 1], yticks=[0, 2, 4, 6, 8, 10],
             xlabel='$x/\\theta$', ylabel='$\\theta f_{\\hat\\theta_{\\mathrm{ML}}}(x)$', grid=True)
    items = []
    for n, c in ((2, 'c1'), (5, 'c3'), (10, 'c2')):
        P.fn(lambda x, n=n: n * x ** (n - 1), 0, 1, color=c)
        items.append(('$n=%d$' % n, c, 'line'))
    return wrap(P.svg('چگالی بیشینه'), leg=legend(items))


@fig('f22-3')
def _(fid):
    D = Diagram(fid, x=(-0.9, 4.9), y=(-0.75, 2.6), scale=62)
    for x, y, t in ((0, 1.6, '0'), (0, 0, '1'), (4, 1.6, '0'), (4, 0, '1')):
        D.circle(x, y, 0.32, sw=2, fill='var(--fig-bg)')
        D.math(x, y, t, size=17)
    D.arrow((0, 1.6), (4, 1.6), shorten=(0.36, 0.36), color='c3', sw=2.2)
    D.arrow((0, 0), (4, 0), shorten=(0.36, 0.36), color='c3', sw=2.2)
    D.arrow((0, 1.6), (4, 0), shorten=(0.36, 0.36), color='c2', sw=2.2)
    D.arrow((0, 0), (4, 1.6), shorten=(0.36, 0.36), color='c2', sw=2.2)
    D.math(2, 1.68, '1-\\varepsilon', anchor='s', size=15, color='c3')
    D.math(2, -0.08, '1-\\varepsilon', anchor='n', size=15, color='c3')
    D.math(1.0, 1.32, '\\varepsilon', anchor='sw', size=15, color='c2')
    D.math(1.0, 0.28, '\\varepsilon', anchor='nw', size=15, color='c2')
    D.text(0, 2.3, 'بیت ارسالی', size=14)
    D.text(4, 2.3, 'بیت دریافتی', size=14)
    return D.svg('کانال دودویی متقارن')


# ================================================================ API
def render(fid):
    if fid not in REG:
        return '<div class="figph">%s</div>' % fid
    return REG[fid](fid)


def hero_binomial():
    from scipy.stats import binom
    ks = np.arange(0, 21)
    ps = binom.pmf(ks, 20, 0.5)
    P = Plot('hero', w=420, h=230, x=(-0.8, 20.8), y=(0, 0.19), xticks=[0, 5, 10, 15, 20], yticks=None,
             xlabel='$k$', margins=(14, None, 14, None))
    P.bars(ks, ps, 0.8, color='c1', op=.85)
    P.fn(lambda x: gauss(x, 10, math.sqrt(5)), -0.8, 20.8, color='c2', sw=2)
    return P.svg('توزیع دوجمله‌ای n=20 و تقریب گاوسی آن')
