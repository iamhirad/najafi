"""Build the web edition of the notes into web/dist.

python3 build.py            # all pages
python3 build.py 21 22      # only these chapters (plus index)
"""
import glob
import html as htmllib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import convert  # noqa: E402
import template  # noqa: E402
import figs  # noqa: E402

SRC = os.path.join(HERE, '..', 'jozve', 'chapters')
DIST = os.path.join(HERE, 'dist')
FA = convert.fa

ORDINAL = {3: 'سوم', 4: 'چهارم', 5: 'پنجم', 6: 'ششم', 7: 'هفتم', 8: 'هشتم', 9: 'نهم', 10: 'دهم',
           11: 'یازدهم', 12: 'دوازدهم', 13: 'سیزدهم', 14: 'چهاردهم', 15: 'پانزدهم', 16: 'شانزدهم',
           17: 'هفدهم', 18: 'هجدهم', 19: 'نوزدهم', 20: 'بیستم', 21: 'بیست‌ویکم', 22: 'بیست‌ودوم'}

PARTS = [
    ('مبانی احتمال', 'فضای احتمال، احتمال شرطی و استقلال', [0, 3, 4, 5]),
    ('متغیر تصادفی', 'توزیع‌ها، میانگین، گشتاورها و تبدیل‌ها', [6, 7, 8, 9, 10, 11, 12]),
    ('چند متغیر تصادفی', 'توزیع مشترک، همبستگی، جمع و قضایای حدی', [13, 14, 15, 16, 17]),
    ('آمار و تخمین', 'نامساوی‌ها، آمار، تخمین و درست‌نمایی', [18, 19, 20, 21, 22]),
]


# ---------------------------------------------------------------- math
MATH_SPAN = re.compile(r'<span class="math (inline|display)">(.*?)</span>', re.S)
FIG_MATH = re.compile(r'<g class="fm"([^>]*)></g>')


def attr(s, name):
    m = re.search(r'\b%s="([^"]*)"' % name, s)
    return htmllib.unescape(m.group(1)) if m else None


def render_math(page):
    items = []
    for m in MATH_SPAN.finditer(page):
        tex = htmllib.unescape(m.group(2)).strip()
        if m.group(1) == 'inline':
            tex = re.sub(r'^\\\(|\\\)$', '', tex)
        else:
            tex = re.sub(r'^\\\[|\\\]$', '', tex)
        items.append({'tex': tex.strip(), 'display': m.group(1) == 'display'})
    for m in FIG_MATH.finditer(page):
        items.append({'tex': attr(m.group(1), 'data-tex'), 'display': False})
    if not items:
        return page, ''
    r = subprocess.run(['node', os.path.join(HERE, 'mathrender.js')], input=json.dumps({'items': items}).encode(),
                       capture_output=True, cwd=HERE)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode()[:2000])
    out = json.loads(r.stdout)
    for i, err in out['errors']:
        print('  MATH ERROR:', err, '|', items[i]['tex'][:120])
    svgs = out['svgs']
    k = 0

    def rep(m):
        nonlocal k
        s = svgs[k]
        it = items[k]
        k += 1
        if s is None:
            return '<span class="merr">%s</span>' % htmllib.escape(it['tex'])
        if it['display']:
            return '<span class="dm">%s</span>' % s
        return s
    page = MATH_SPAN.sub(rep, page)

    def frep(m):
        nonlocal k
        s = svgs[k]
        k += 1
        a = m.group(1)
        return figs.place_math(s, float(attr(a, 'data-x')), float(attr(a, 'data-y')),
                               attr(a, 'data-anchor'), float(attr(a, 'data-size')), attr(a, 'data-color'))
    page = FIG_MATH.sub(frep, page)
    return page, out['defs']


# ---------------------------------------------------------------- chapters
def load_chapters(only=None):
    labels = {}
    chapters = []
    for f in sorted(glob.glob(os.path.join(SRC, 'ch*.tex'))):
        chap = int(re.search(r'ch(\d+)\.tex', f).group(1))
        tex, figsrc = convert.preprocess(open(f, encoding='utf-8').read(), chap)
        html, warn = convert.run_pandoc(tex)
        if warn:
            print('pandoc', f, warn[:300])
        res = convert.restructure(html, chap, labels, lambda fid: '<figslot data-id="%s"></figslot>' % fid)
        title_html = res['title']
        if chap == 0:
            title_html = 'مرور پیش‌نیازها'
            label = 'پیش‌درآمد'
            eyebrow = 'پیش‌درآمد · جلسات اول و دوم'
        else:
            label = 'جلسه %s' % FA(chap)
            eyebrow = 'جلسه %s' % ORDINAL[chap]
        soup = res['soup']
        counts = {
            'ex': len(soup.select('section.box-ex')),
            'exr': len(soup.select('section.box-exr')),
            'q': len(soup.select('section.box-q')),
            'fig': len(soup.select('figure.fig')),
            'thm': len(soup.select('section.box-thm')),
            'def': len(soup.select('section.box-def')),
        }
        from bs4 import BeautifulSoup
        chapters.append({
            'num': chap, 'file': convert.page_name(chap), 'label': label, 'eyebrow': eyebrow,
            'title_html': title_html,
            'title_text': BeautifulSoup(title_html, 'html.parser').get_text().strip(),
            'sections': res['sections'], 'soup': soup, 'counts': counts,
        })
    return chapters, labels


def toc_html(ch):
    out = ['<ol>']
    for s in ch['sections']:
        out.append('<li class="l%d"><a href="#%s"><span class="n">%s</span><span>%s</span></a></li>' % (
            s['level'], s['id'], s['num'], re.sub(r'<span class="en"[^>]*>(.*?)</span>', r'\1', s['html'])))
    out.append('</ol>')
    return ''.join(out)


def chapter_head(ch):
    c = ch['counts']
    meta = []
    for key, word in (('def', 'تعریف'), ('thm', 'قضیه'), ('ex', 'مثال'), ('exr', 'تمرین'), ('fig', 'شکل')):
        if c[key]:
            meta.append('<span><b>%s</b> %s</span>' % (FA(c[key]), word))
    num = '' if ch['num'] == 0 else '<span class="ch-num">%s</span>' % FA(ch['num'])
    return ('<header class="ch-head"><div class="ch-eyebrow">%s<span>%s</span></div>'
            '<h1 class="ch-title">%s</h1><div class="ch-meta">%s</div></header>') % (
        num, ch['eyebrow'], ch['title_html'], ''.join(meta))


def build_chapter(ch, prev, nxt, labels):
    body = convert.resolve_refs(str(ch['soup']), ch['num'], labels)
    body = re.sub(r'<figslot data-id="([^"]+)"></figslot>', lambda m: figs.render(m.group(1)), body)
    page = template.chapter_page(ch, prev, nxt, body, toc_html(ch), '@@DEFS@@', chapter_head(ch))
    page, defs = render_math(page)
    page = page.replace('@@DEFS@@', defs, 1)
    with open(os.path.join(DIST, ch['file']), 'w', encoding='utf-8') as fh:
        fh.write(page)
    return len(page)


def build_index(chapters):
    tot = {k: sum(c['counts'][k] for c in chapters) for k in ('ex', 'exr', 'fig', 'thm', 'def')}
    by = {c['num']: c for c in chapters}
    parts = []
    for name, sub, nums in PARTS:
        items = []
        for n in nums:
            c = by[n]
            secs = '، '.join(re.sub(r'<span class="en"[^>]*>.*?</span>', '', s['html']).strip()
                            for s in c['sections'] if s['level'] == 2)
            k = c['counts']
            pills = ''
            if k['ex']:
                pills += '<span class="pill ex">%s مثال</span>' % FA(k['ex'])
            if k['exr']:
                pills += '<span class="pill exr">%s تمرین</span>' % FA(k['exr'])
            if k['fig']:
                pills += '<span class="pill fig">%s شکل</span>' % FA(k['fig'])
            numtxt = 'پیش' if n == 0 else FA(n)
            small = 'جلسات ۱ و ۲' if n == 0 else 'جلسه'
            items.append(
                '<li><a class="chap" href="%s"><div class="chap-n">%s<small>%s</small></div>'
                '<div class="chap-b"><div class="chap-t">%s</div><div class="chap-s">%s</div>'
                '<div class="chap-c">%s</div></div></a></li>' % (
                    c['file'], numtxt, small, c['title_html'], secs, pills))
        parts.append('<section class="part"><div class="part-h"><h2>%s</h2><span>%s</span></div>'
                     '<ol class="chap-list">%s</ol></section>' % (name, sub, ''.join(items)))
    hero_fig = figs.hero_binomial()
    body = (
        '<div class="page" dir="rtl" lang="fa">' + template.topbar('جزوه کامل درس', show_toc=False, show_quiz=False) +
        '<div class="home"><section class="hero"><div>'
        '<div class="hero-k">دانشکده مهندسی کامپیوتر · دانشگاه صنعتی شریف</div>'
        '<h1>آمار و احتمال مهندسی</h1>'
        '<p>جزوه کامل درس بر اساس اسلایدهای جلسات سوم تا بیست‌ودوم: توضیح کامل هر مبحث، همه مثال‌ها و پرسش‌های اسلایدها با حل قدم‌به‌قدم، و تمرین‌های تکمیلی حل‌شده.</p>'
        '<p class="who">مدرس: دکتر امیر نجفی · زمستان ۱۴۰۴ و بهار ۱۴۰۵</p>'
        '</div><figure class="hero-fig">%s<figcaption>توزیع دوجمله‌ای: احتمال \\(k\\) شیر در \\(n=20\\) پرتاب سکه سالم، و منحنی گاوسی که قضیه حد مرکزی پیش‌بینی می‌کند</figcaption></figure></section>'
        '<div class="stats">'
        '<div class="stat"><b>%s</b><span>فصل</span></div><div class="stat"><b>%s</b><span>تعریف و قضیه</span></div>'
        '<div class="stat"><b>%s</b><span>مثال حل‌شده</span></div><div class="stat"><b>%s</b><span>تمرین با حل کامل</span></div>'
        '<div class="stat"><b>%s</b><span>شکل و نمودار</span></div></div>'
        '<div class="resume" id="resume" hidden><span>ادامه مطالعه از</span><a href="#">—</a></div>'
        '%s'
        '<section class="howto"><h2>راهنمای استفاده</h2><ul>'
        '<li>هر جلسه یک صفحه است؛ فهرست بخش‌ها در کنار صفحه (یا با دکمه «فهرست» در گوشی) در دسترس است.</li>'
        '<li>حل هر مثال و تمرین زیر آن آمده است. با دکمه «حل‌ها» همه حل‌ها را پنهان کنید تا خودتان را بسنجید؛ هر حل با یک ضربه دوباره باز می‌شود.</li>'
        '<li>رنگ هر کادر نوع آن را نشان می‌دهد: <span class="tc-blue">تعریف</span>، <span class="tc-red">قضیه</span>، <span class="tc-green">مثال</span>، <span class="tc-orange">تمرین</span>.</li>'
        '</ul></section>'
        '<p class="foot">نسخه وب جزوه · فرمول‌ها و شکل‌ها به صورت برداری رسم شده‌اند و در حالت روشن و تیره خوانا هستند.</p>'
        '</div></div>') % (
        hero_fig, FA(len(chapters)), FA(tot['def'] + tot['thm']), FA(tot['ex']), FA(tot['exr']), FA(tot['fig']),
        ''.join(parts))
    body = convert.BeautifulSoup(body, 'html.parser')
    body = str(body)
    # note: the publish skeleton supplies <html>/<head>/<body>; our wrapper carries dir/lang
    page = ('<title>جزوه آمار و احتمال مهندسی</title>'
            '<meta name="claude:viewport-fit-sides" content="cover">' + template.FONTS +
            '<style>%s .page{min-height:100%%}</style>' % template.CSS + '@@DEFS@@' + body +
            '<script>document.body.setAttribute("data-page","index");document.documentElement.setAttribute("lang","fa");</script>'
            '<script>%s</script>' % template.JS)
    page = page.replace('\\(k\\)', '<span class="math inline">\\(k\\)</span>').replace(
        '\\(n=20\\)', '<span class="math inline">\\(n=20\\)</span>')
    page, defs = render_math(page)
    page = page.replace('@@DEFS@@', defs, 1)
    with open(os.path.join(DIST, 'index.html'), 'w', encoding='utf-8') as fh:
        fh.write(page)


def main():
    only = [int(a) for a in sys.argv[1:]]
    os.makedirs(DIST, exist_ok=True)
    chapters, labels = load_chapters()
    for i, ch in enumerate(chapters):
        if only and ch['num'] not in only:
            continue
        prev = chapters[i - 1] if i > 0 else None
        nxt = chapters[i + 1] if i + 1 < len(chapters) else None
        n = build_chapter(ch, prev, nxt, labels)
        print('built', ch['file'], '%.0f KB' % (n / 1024))
    build_index(chapters)
    print('built index.html')


if __name__ == '__main__':
    main()
