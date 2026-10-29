"""Build a single print-ready PDF of the web edition (Chromium, no LaTeX).

python3 print.py            -> web/pdf/Jozve-Amar-Ehtemal-Najafi.pdf

Pass 1 renders the PDF and reads where every chapter/section landed;
pass 2 writes those page numbers into the table of contents.
"""
import os
import re
import subprocess
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build  # noqa: E402
import convert  # noqa: E402
import figs  # noqa: E402
import template  # noqa: E402

OUT_DIR = os.path.join(HERE, 'pdf')
FA = convert.fa

PRINT_CSS = r"""
@page {
  size: A4; margin: 17mm 16mm 19mm 16mm;
  @bottom-center { content: counter(page, persian); font-family: "Vazirmatn", sans-serif; font-size: 9pt; color: #687285; }
  @top-center { content: "آمار و احتمال مهندسی · جزوه کامل درس"; font-family: "Vazirmatn", sans-serif; font-size: 7.5pt; color: #9AA2B0; }
}
@page :first { @bottom-center { content: none; } @top-center { content: none; } }
@page cover { @bottom-center { content: none; } @top-center { content: none; } }
:root { padding: 0 !important; --paper: #FFFFFF; --shadow: none; }
html { scroll-behavior: auto; }
body { background: #FFFFFF; font-size: 10.6pt; line-height: 1.85; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body::before { display: none; }
.print-main { padding: 0; }

/* cover */
.cover { page: cover; height: 255mm; display: flex; flex-direction: column; justify-content: space-between; break-after: page; }
.cover-top { padding-top: 18mm; }
.cover .k { color: var(--accent); font-weight: 600; font-size: 12pt; }
.cover h1 { font-family: var(--font-display); font-weight: 700; font-size: 44pt; line-height: 1.15; margin: 6mm 0 4mm; color: var(--ink); }
.cover .sub { font-size: 13pt; color: var(--ink-2); max-width: 140mm; line-height: 1.9; }
.cover-fig { text-align: center; }
.cover-fig > svg { width: 120mm; height: auto; }
.cover-fig figcaption { font-size: 9pt; }
.cover-meta { display: flex; justify-content: space-between; align-items: flex-end; border-top: 1px solid var(--rule); padding-top: 5mm; font-size: 11pt; color: var(--ink-2); }
.cover-meta b { display: block; font-size: 12.5pt; color: var(--ink); }
.cover-stats { display: flex; gap: 9mm; }
.cover-stats div { text-align: center; }
.cover-stats b { font-family: var(--font-display); font-size: 20pt; line-height: 1.1; }
.cover-stats span { font-size: 9pt; color: var(--muted); }

/* table of contents */
.ptoc { break-after: page; }
.ptoc h2 { font-family: var(--font-display); font-size: 26pt; margin: 0 0 6mm; }
.ptoc-ch { margin: 0 0 3.2mm; break-inside: avoid; }
.ptoc-row { display: flex; align-items: baseline; gap: 2.5mm; text-decoration: none; color: var(--ink); }
.ptoc-row .n { flex: none; min-width: 11mm; color: var(--accent); font-weight: 700; font-variant-numeric: tabular-nums; }
.ptoc-row .t { flex: 0 1 auto; }
.ptoc-row .dots { flex: 1 1 auto; border-bottom: 1px dotted var(--muted); transform: translateY(-1.2mm); min-width: 6mm; }
.ptoc-row .p { flex: none; min-width: 8mm; text-align: left; font-variant-numeric: tabular-nums; color: var(--ink-2); }
.ptoc-ch > .ptoc-row { font-weight: 700; font-size: 11.5pt; }
.ptoc-sec .ptoc-row { font-size: 9.6pt; color: var(--ink-2); padding-inline-start: 13.5mm; line-height: 1.75; }
.ptoc-sec .ptoc-row .n { color: var(--muted); font-weight: 500; min-width: 10mm; }

/* chapters */
.chapter { break-before: page; }
.ch-head { padding-block: 0 4mm; margin-bottom: 5mm; }
.ch-title { font-size: 25pt; }
main h2 { font-size: 17pt; margin: 8mm 0 3mm; break-after: avoid; }
main h3 { font-size: 12.2pt; margin: 6mm 0 2mm; break-after: avoid; }
main h4 { break-after: avoid; }
.box { box-shadow: none; margin: 4.5mm 0; break-inside: auto; }
.box-head { break-after: avoid; break-inside: avoid; }
figure.fig, .table-wrap, .callout, .flow { break-inside: avoid; }
.dm { overflow: visible; break-inside: avoid; }
.dm mjx-container > svg { max-width: 100%; height: auto; }
p, li { orphans: 3; widows: 3; }
details.sol > summary { cursor: default; }
details.sol > summary::before, details.sol > summary::after { display: none; content: none; }
details.sol > summary::marker { content: ""; }
.table-wrap { overflow: visible; }
a.xref { color: var(--accent); }
.fig-row > svg, .subfig > svg { max-width: 100%; height: auto; }
.fig-row > .subfig > svg { max-height: 62mm; width: auto; }
"""


def rewrite_ids(body, n):
    pat = r'(s\d[^"]*|b\d+|fig-[^"]*)'
    body = re.sub(r'id="%s"' % pat, lambda m: 'id="c%d-%s"' % (n, m.group(1)), body)
    body = re.sub(r'href="#%s"' % pat, lambda m: 'href="#c%d-%s"' % (n, m.group(1)), body)
    body = re.sub(r'href="ch(\d\d)\.html#([^"]+)"', lambda m: 'href="#c%d-%s"' % (int(m.group(1)), m.group(2)), body)
    return body


def toc_html(chapters, pages):
    def pg(key):
        p = pages.get(key)
        return FA(p) if p else '<span style="visibility:hidden">۰۰۰</span>'
    out = ['<section class="ptoc"><h2>فهرست مطالب</h2>']
    for ch in chapters:
        n = ch['num']
        label = 'پیش‌درآمد' if n == 0 else 'جلسه %s' % FA(n)
        out.append('<div class="ptoc-ch"><a class="ptoc-row" href="#c%d"><span class="n">%s</span>'
                   '<span class="t">%s</span><span class="dots"></span><span class="p">%s</span></a>' % (
                       n, '' if n == 0 else FA(n), ch['title_html'] if n else label + ': ' + ch['title_html'],
                       pg('c%d' % n)))
        out.append('<div class="ptoc-sec">')
        for s in ch['sections']:
            if s['level'] != 2:
                continue
            title = re.sub(r'<span class="en"[^>]*>.*?</span>', '', s['html']).strip()
            key = 'c%d-%s' % (n, s['id'])
            out.append('<a class="ptoc-row" href="#%s"><span class="n">%s</span><span class="t">%s</span>'
                       '<span class="dots"></span><span class="p">%s</span></a>' % (key, s['num'], title, pg(key)))
        out.append('</div></div>')
    out.append('</section>')
    return ''.join(out)


def cover_html(chapters):
    tot = {k: sum(c['counts'][k] for c in chapters) for k in ('ex', 'exr', 'fig', 'thm', 'def')}
    return (
        '<section class="cover"><div class="cover-top">'
        '<div class="k">دانشکده مهندسی کامپیوتر · دانشگاه صنعتی شریف</div>'
        '<h1>آمار و احتمال مهندسی</h1>'
        '<p class="sub">جزوه کامل درس بر اساس اسلایدهای جلسات سوم تا بیست‌ودوم: توضیح کامل هر مبحث، همه مثال‌ها و پرسش‌های اسلایدها با حل قدم‌به‌قدم، و تمرین‌های تکمیلی حل‌شده.</p>'
        '</div>'
        '<figure class="cover-fig">%s<figcaption>توزیع دوجمله‌ای: احتمال <span class="math inline">\\(k\\)</span> شیر در '
        '<span class="math inline">\\(n=20\\)</span> پرتاب سکه سالم، و منحنی گاوسی که قضیه حد مرکزی پیش‌بینی می‌کند</figcaption></figure>'
        '<div class="cover-meta"><div><b>مدرس: دکتر امیر نجفی</b>زمستان ۱۴۰۴ و بهار ۱۴۰۵</div>'
        '<div class="cover-stats"><div><b>%s</b><br><span>جلسه</span></div><div><b>%s</b><br><span>مثال حل‌شده</span></div>'
        '<div><b>%s</b><br><span>تمرین با حل</span></div><div><b>%s</b><br><span>شکل</span></div></div></div>'
        '</section>') % (figs.hero_binomial(), FA(len(chapters)), FA(tot['ex']), FA(tot['exr']), FA(tot['fig']))


def assemble(chapters, labels, pages):
    parts = []
    for ch in chapters:
        body = convert.resolve_refs(str(ch['soup']), ch['num'], labels)
        body = re.sub(r'<figslot data-id="([^"]+)"></figslot>', lambda m: figs.render(m.group(1)), body)
        body = rewrite_ids(body, ch['num'])
        parts.append('<section class="chapter" id="c%d">%s%s</section>' % (ch['num'], build.chapter_head(ch), body))
    html = ('<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><title>جزوه آمار و احتمال مهندسی</title>%s'
            '<style>%s%s</style></head><body>@@DEFS@@<main class="print-main">%s%s%s</main></body></html>') % (
        template.FONTS, template.CSS, PRINT_CSS, cover_html(chapters), toc_html(chapters, pages), ''.join(parts))
    return html


def render_pdf(html_path, pdf_path):
    js = os.path.join(HERE, 'pdfrender.js')
    r = subprocess.run(['node', js, html_path, pdf_path], capture_output=True, cwd=HERE)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode()[-2000:])
    print(r.stdout.decode().strip())


def page_map(pdf_path):
    from pypdf import PdfReader
    rd = PdfReader(pdf_path)
    out = {}
    for name, dest in rd.named_destinations.items():
        try:
            out[str(name).lstrip('/')] = rd.get_destination_page_number(dest) + 1
        except Exception:
            pass
    return out, len(rd.pages)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    chapters, labels = build.load_chapters()
    html_path = os.path.join(OUT_DIR, 'jozve.html')
    pdf_path = os.path.join(OUT_DIR, 'Jozve-Amar-Ehtemal-Najafi.pdf')
    pages = {}
    for p in (1, 2):
        html = assemble(chapters, labels, pages)
        html, defs = build.render_math(html)
        html = html.replace('@@DEFS@@', defs, 1)
        with open(html_path, 'w', encoding='utf-8') as fh:
            fh.write(html)
        render_pdf(html_path, pdf_path)
        new, total = page_map(pdf_path)
        print('pass %d: %d pages, %d destinations' % (p, total, len(new)))
        if p == 2 and new != pages:
            print('warning: page numbers moved between passes')
        pages = new
    print('wrote', pdf_path)


if __name__ == '__main__':
    main()
