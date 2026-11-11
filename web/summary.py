"""Formula & concept summary: jozve/summary.md -> summary.html (+ PDF).

python3 summary.py          # summary.html into dist/ and, with --site, into site/
python3 summary.py --pdf    # also pdf/Kholaseh-Formulha-Amar-Ehtemal.pdf
"""
import os
import re
import subprocess
import sys

from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build  # noqa: E402
import convert  # noqa: E402
import template  # noqa: E402
from figlib import rich  # noqa: E402

SRC = os.path.join(HERE, '..', 'jozve', 'summary.md')
SITE_URL = 'https://iamhirad.github.io/najafi/'
PDF_NAME = 'Kholaseh-Formulha-Amar-Ehtemal.pdf'
FA = convert.fa
TITLE = 'خلاصه فرمول‌ها و مفاهیم'


def ref_chips(ref, absolute):
    seen = []
    for r in (ref or '').split():
        ch, sid = r.split(':')
        ch = int(ch)
        if ch in [c for c, _ in seen]:
            continue
        seen.append((ch, sid))
    out = []
    for ch, sid in seen:
        href = '%s#%s' % (convert.page_name(ch), sid)
        if absolute:
            href = SITE_URL + href
        label = 'پیش‌درآمد' if ch == 0 else 'جلسه %s' % FA(ch)
        out.append('<a class="fref" href="%s">%s</a>' % (href, label))
    return '<span class="frefs">%s</span>' % ''.join(out) if out else ''


def load(absolute=False):
    """Return (body_html, toc_entries, counts)."""
    r = subprocess.run(['pandoc', '-f', 'markdown', '-t', 'html', '--mathjax', '--wrap=none', SRC],
                       capture_output=True, check=True)
    soup = BeautifulSoup(r.stdout.decode(), 'html.parser')
    for sp in soup.find_all('span', class_='en'):
        sp['dir'] = 'ltr'
    out = []
    grid = []
    toc = []
    pi = ti = 0
    ncards = 0

    def flush():
        if grid:
            out.append('<div class="fgrid">%s</div>' % ''.join(grid))
            grid.clear()

    for node in list(soup.children):
        if getattr(node, 'name', None) is None:
            continue
        cls = node.get('class') or []
        if node.name == 'h2':
            flush()
            title = node.decode_contents()
            appendix = title.strip().startswith('پیوست')
            pi += 1
            ti = 0
            hid = 'p%d' % pi
            num = 'پیوست' if appendix else 'بخش %s' % FA(pi)
            out.append('<h2 id="%s" class="part-title"><span class="h-num">%s</span><span class="h-text">%s</span></h2>' % (
                hid, num, re.sub(r'^\s*پیوست:\s*', '', title)))
            toc.append({'id': hid, 'level': 2, 'num': '' if appendix else FA(pi), 'html': re.sub(r'^\s*پیوست:\s*', 'پیوست: ', title)})
        elif node.name == 'h3':
            flush()
            ti += 1
            hid = 'p%d-%d' % (pi, ti)
            out.append('<h3 id="%s"><span class="h-text">%s</span></h3>' % (hid, node.decode_contents()))
            toc.append({'id': hid, 'level': 3, 'num': '', 'html': node.decode_contents()})
        elif node.name == 'div' and 'card' in cls:
            ncards += 1
            grid.append('<article class="fcard"><header class="fcard-h"><h4>%s</h4>%s</header>'
                        '<div class="fcard-b">%s</div></article>' % (
                            rich(node.get('data-t', '')), ref_chips(node.get('data-ref'), absolute), node.decode_contents()))
        elif node.name == 'div' and 'wide' in cls:
            flush()
            ncards += 1
            inner = BeautifulSoup(node.decode_contents(), 'html.parser')
            for tb in inner.find_all('table'):
                for el in tb.find_all(['th', 'td', 'tr', 'col', 'colgroup']):
                    el.attrs.pop('style', None)
                    el.attrs.pop('class', None)
                for cg in tb.find_all('colgroup'):
                    cg.decompose()
                tb.wrap(inner.new_tag('div', attrs={'class': 'table-wrap'}))
            out.append('<section class="fcard fwide"><header class="fcard-h"><h4>%s</h4>%s</header>'
                       '<div class="fcard-b">%s</div></section>' % (
                           rich(node.get('data-t', '')), ref_chips(node.get('data-ref'), absolute), str(inner)))
        else:
            flush()
            out.append(str(node))
    flush()
    body = BeautifulSoup(''.join(out), 'html.parser')
    convert.convert_digits(body)
    return str(body), toc, ncards


def toc_html(toc):
    items = []
    for s in toc:
        items.append('<li class="l%d"><a href="#%s"><span class="n">%s</span><span>%s</span></a></li>' % (
            s['level'], s['id'], s['num'], re.sub(r'<span class="en"[^>]*>(.*?)</span>', r'\1', s['html'])))
    return '<ol>%s</ol>' % ''.join(items)


def head_html(ncards, pdf_link=None):
    dl = ''
    if pdf_link:
        dl = ('<p class="dl-row"><a class="dl" href="%s" download>%s<span>دانلود PDF خلاصه</span></a></p>' % (
            pdf_link, template.ICONS['download']))
    return ('<header class="ch-head"><div class="ch-eyebrow"><span class="ch-num">∑</span><span>پیوست جزوه · جلسات ۱ تا ۲۷</span></div>'
            '<h1 class="ch-title">%s</h1><div class="ch-meta"><span><b>%s</b> کارت فرمول و جدول</span>'
            '<span>هر کارت به جلسه مربوطش پیوند دارد</span></div>%s</header>') % (TITLE, FA(ncards), dl)


def build_page(dest_dir, site=False):
    body, toc, n = load()
    ch = {'label': 'خلاصه فرمول‌ها', 'title_text': TITLE, 'file': 'summary.html'}
    page = template.summary_page(ch, body, toc_html(toc), '@@DEFS@@',
                                 head_html(n, PDF_NAME if site else None))
    page, defs = build.render_math(page)
    page = page.replace('@@DEFS@@', defs, 1)
    with open(os.path.join(dest_dir, 'summary.html'), 'w', encoding='utf-8') as fh:
        fh.write(page)
    return len(page)


# ---------------------------------------------------------------- PDF
PRINT_CSS = r"""
@page {
  size: A4; margin: 15mm 13mm 16mm 13mm;
  @bottom-center { content: counter(page, persian); font-family: "Vazirmatn", sans-serif; font-size: 8.5pt; color: #687285; }
  @top-center { content: "خلاصه فرمول‌ها و مفاهیم · آمار و احتمال مهندسی"; font-family: "Vazirmatn", sans-serif; font-size: 7.5pt; color: #9AA2B0; }
}
@page :first { @top-center { content: none; } }
:root { padding: 0 !important; --paper: #FFFFFF; --shadow: none; }
body { background: #FFFFFF; font-size: 9.3pt; line-height: 1.7; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body::before { display: none; }
.sum-title { display: flex; justify-content: space-between; align-items: flex-end; gap: 6mm; border-bottom: 1.5px solid var(--accent); padding-bottom: 3mm; margin-bottom: 4mm; }
.sum-title h1 { font-family: var(--font-display); font-size: 26pt; line-height: 1.15; margin: 0; }
.sum-title .k { color: var(--accent); font-weight: 600; font-size: 10pt; }
.sum-title .meta { color: var(--muted); font-size: 8.8pt; text-align: left; }
.sum-intro { font-size: 9pt; color: var(--ink-2); margin: 0 0 3mm; }
.ptoc { column-count: 2; column-gap: 8mm; font-size: 8.6pt; margin-bottom: 4mm; }
.ptoc-row { display: flex; gap: 2mm; text-decoration: none; color: var(--ink-2); line-height: 1.7; break-inside: avoid; }
.ptoc-row .dots { flex: 1; border-bottom: 1px dotted var(--rule); transform: translateY(-1mm); }
.ptoc-row .p { min-width: 6mm; text-align: left; }
.ptoc-row.l2 { font-weight: 800; color: var(--accent); margin-top: 1.2mm; }
.sum-main h2.part-title { break-after: avoid; font-size: 15pt; margin: 4mm 0 2mm; }
.sum-main h2.part-title:first-of-type { break-before: auto; }
.sum-main h3 { font-size: 10.6pt; margin: 3.5mm 0 1.5mm; break-after: avoid; }
.fgrid { display: block; column-count: 2; column-gap: 4mm; margin: 0; }
.fcard { break-inside: avoid; margin: 0 0 3mm; display: block; padding: 2mm 3mm; border-radius: 8px; }
.fcard-h h4 { font-size: 9.4pt; }
.fref { font-size: 6.8pt; }
.fcard-b { font-size: 8.9pt; line-height: 1.7; }
.fwide { break-inside: avoid; margin: 1mm 0 3.5mm; }
.fwide .table-wrap table { font-size: 8.2pt; }
.fwide .table-wrap th, .fwide .table-wrap td { padding: .25rem .45rem; min-width: 0; }
.fcard-b .dm { overflow: visible; margin: .2rem 0; }
.dm > mjx-container[jax="SVG"][display="true"] { width: auto; min-width: 0; }
"""


def pdf_html(pages):
    body, toc, n = load(absolute=True)
    # mini table of contents with page numbers
    rows = []
    for s in toc:
        p = pages.get(s['id'])
        num = FA(p) if p else '<span style="visibility:hidden">۰۰</span>'
        rows.append('<a class="ptoc-row l%d" href="#%s"><span>%s</span><span class="dots"></span><span class="p">%s</span></a>' % (
            s['level'], s['id'], re.sub(r'<span class="en"[^>]*>(.*?)</span>', r'\1', s['html']), num))
    intro_m = re.match(r'\s*(<p>.*?</p>)', body, re.S)
    intro = intro_m.group(1) if intro_m else ''
    body = body[intro_m.end():] if intro_m else body
    head = ('<div class="sum-title"><div><div class="k">آمار و احتمال مهندسی · دکتر امیر نجفی · دانشگاه صنعتی شریف</div>'
            '<h1>%s</h1></div><div class="meta">%s کارت فرمول و جدول<br>جزوه کامل: iamhirad.github.io/najafi</div></div>'
            '<div class="sum-intro">%s</div><nav class="ptoc">%s</nav>') % (TITLE, FA(n), intro.replace('<p>', '<p style="margin:0">'), ''.join(rows))
    return ('<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><title>%s</title>%s'
            '<style>%s%s</style></head><body>@@DEFS@@<main class="sum-main summary">%s%s</main></body></html>') % (
        TITLE, template.FONTS, template.CSS, PRINT_CSS, head, body)


def build_pdf():
    import print as pr
    out_dir = os.path.join(HERE, 'pdf')
    os.makedirs(out_dir, exist_ok=True)
    html_path = os.path.join(out_dir, 'summary.html')
    pdf_path = os.path.join(out_dir, PDF_NAME)
    pages = {}
    for p in (1, 2):
        html, defs = build.render_math(pdf_html(pages))
        html = html.replace('@@DEFS@@', defs, 1)
        with open(html_path, 'w', encoding='utf-8') as fh:
            fh.write(html)
        pr.render_pdf(html_path, pdf_path)
        new, total = pr.page_map(pdf_path)
        print('summary pdf pass %d: %d pages' % (p, total))
        if p == 2 and new != pages:
            print('warning: page numbers moved between passes')
        pages = new
    return pdf_path


def main():
    dest = os.path.join(HERE, 'dist')
    os.makedirs(dest, exist_ok=True)
    n = build_page(dest)
    print('built summary.html %.0f KB' % (n / 1024))
    if '--pdf' in sys.argv:
        print('wrote', build_pdf())


if __name__ == '__main__':
    main()
