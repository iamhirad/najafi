"""Chapter source -> structured HTML fragment.

Steps: preprocess the chapter source (figures, box titles, labels), run pandoc
to get an HTML skeleton, then restructure it with BeautifulSoup (boxes,
solutions, headings, Persian digits). Math is left as \\( \\) / \\[ \\] spans
for the MathJax step in build.py.
"""
import re
import subprocess
from bs4 import BeautifulSoup, NavigableString, Tag

FA_DIGITS = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')


def fa(n):
    return str(n).translate(FA_DIGITS)


# ---------------------------------------------------------------- helpers
def read_group(s, i, open_ch='{', close_ch='}'):
    """s[i] == open_ch; return (content, index after the closing char)."""
    assert s[i] == open_ch, (s[i:i + 30])
    depth = 0
    j = i
    while j < len(s):
        c = s[j]
        if c == '\\':
            j += 2
            continue
        if c == open_ch:
            depth += 1
        elif c == close_ch:
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise ValueError('unbalanced group at %d' % i)


def read_optarg(s, i):
    """s[i] == '['; bracket content with braces respected."""
    depth = 0
    j = i + 1
    while j < len(s):
        c = s[j]
        if c == '\\':
            j += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        elif c == ']' and depth == 0:
            return s[i + 1:j], j + 1
        j += 1
    raise ValueError('unbalanced optarg')


def strip_outer_braces(t):
    t = t.strip()
    if t.startswith('{'):
        try:
            inner, end = read_group(t, 0)
            if end == len(t):
                return inner
        except ValueError:
            pass
    return t


def remove_command(s, name, nargs):
    """Remove \\name{..}{..} with nargs brace groups."""
    out = []
    i = 0
    pat = re.compile(r'\\' + name + r'(?![A-Za-z])')
    while True:
        m = pat.search(s, i)
        if not m:
            out.append(s[i:])
            break
        out.append(s[i:m.start()])
        j = m.end()
        for _ in range(nargs):
            while j < len(s) and s[j] in ' \t':
                j += 1
            if j < len(s) and s[j] == '{':
                _, j = read_group(s, j)
        i = j
    return ''.join(out)


MATH_ENVS = ('align', 'align*', 'equation', 'equation*', 'gather', 'gather*', 'multline*')


def split_math(s):
    """Yield (is_math, text) segments."""
    segs = []
    i = 0
    buf_start = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c == '\\':
            if s.startswith('\\\\', i):
                i += 2
                continue
            if s.startswith('\\[', i) or s.startswith('\\(', i):
                closer = '\\]' if s[i + 1] == '[' else '\\)'
                j = s.find(closer, i + 2)
                segs.append((False, s[buf_start:i]))
                segs.append((True, s[i:j + 2]))
                i = buf_start = j + 2
                continue
            m = re.match(r'\\begin\{([a-z]+\*?)\}', s[i:])
            if m and m.group(1) in MATH_ENVS:
                end = '\\end{%s}' % m.group(1)
                j = s.find(end, i)
                segs.append((False, s[buf_start:i]))
                segs.append((True, s[i:j + len(end)]))
                i = buf_start = j + len(end)
                continue
            i += 2
            continue
        if c == '$':
            j = i + 1
            while True:
                j = s.find('$', j)
                if s[j - 1] != '\\':
                    break
                j += 1
            segs.append((False, s[buf_start:i]))
            segs.append((True, s[i:j + 1]))
            i = buf_start = j + 1
            continue
        i += 1
    segs.append((False, s[buf_start:]))
    return segs


# ---------------------------------------------------------------- figures
def extract_figures(s, chap):
    """Replace figure code by FIGTOKEN{id}; return new source and {id: code}."""
    figs = {}
    # chapter 8: \sampplot macro
    m = re.search(r'\\newcommand\{\\sampplot\}\[4\]', s)
    if m:
        _, end = read_group(s, m.end())
        s = s[:m.start()] + s[end:]
        out = []
        i = 0
        for mm in re.finditer(r'\\sampplot', s):
            pass
        pat = re.compile(r'\\sampplot(?![A-Za-z])')
        while True:
            mm = pat.search(s, i)
            if not mm:
                out.append(s[i:])
                break
            out.append(s[i:mm.start()])
            j = mm.end()
            args = []
            for _ in range(4):
                a, j = read_group(s, j)
                args.append(a)
            fid = 'samp-' + args[0]
            figs[fid] = 'sampplot %s ymin=%s ymax=%s' % tuple(args[:3])
            out.append('\\begin{figwrap}\n\nFIGPH %s\n\n%s\n\n\\end{figwrap}' % (fid, args[3]))
            i = j
        s = ''.join(out)
    # chapter 17: \foreach loops producing several pictures
    pat = re.compile(r'\\foreach \\n/\\t in ')
    while True:
        mm = pat.search(s)
        if not mm:
            break
        lst, j = read_group(s, mm.end())
        body, j = read_group(s, j)
        kind = 'ih' if 'data/ih' in body else 'bs'
        ids = []
        for item in re.findall(r'(\d+)/\{([^}]*)\}', lst):
            fid = '%s-%s' % (kind, item[0])
            figs[fid] = '%s n=%s title=%s' % (kind, item[0], item[1])
            ids.append('FIGTOKEN{%s}' % fid)
        s = s[:mm.start()] + ' '.join(ids) + s[j:]
    # every other tikzpicture
    k = 0
    def repl(mm):
        nonlocal k
        k += 1
        fid = 'f%02d-%d' % (chap, k)
        figs[fid] = mm.group(0)
        return 'FIGTOKEN{%s}' % fid
    s = re.sub(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}', repl, s, flags=re.S)
    # figure / center blocks that hold pictures
    def block_repl(mm):
        inner = mm.group(2)
        if 'FIGTOKEN' not in inner:
            return mm.group(0)
        items = []
        def tok(m2):
            items.append(m2.group(1))
            return ' '
        rest = re.sub(r'FIGTOKEN\{([^}]*)\}', tok, inner)
        # operators between pictures: \raisebox{..}{\Large $*$}
        ops = []
        def op(m2):
            return ' '
        seq = []
        pos = 0
        for m2 in re.finditer(r'FIGTOKEN\{([^}]*)\}|\\raisebox\{[^}]*\}\{\\Large\s*\$([^$]*)\$\}', inner):
            if m2.group(1):
                seq.append(m2.group(1))
            else:
                seq.append('OP:' + m2.group(2).strip())
        rest = re.sub(r'\\raisebox\{[^}]*\}\{\\Large\s*\$[^$]*\$\}', ' ', rest)
        caption = ''
        cm = re.search(r'\\caption\{', rest)
        if cm:
            caption, end = read_group(rest, cm.end() - 1)
            rest = rest[:cm.start()] + rest[end:]
        else:
            sm = re.search(r'\{\\small\s', rest)
            if sm:
                caption, end = read_group(rest, sm.start())
                caption = caption.replace('\\small', '', 1)
                rest = rest[:sm.start()] + rest[end:]
        rest = re.sub(r'\\\\(\[[^\]]*\])?', ' ', rest)
        rest = re.sub(r'\\(centering|hfill|noindent)', ' ', rest)
        rest = remove_command(rest, 'hspace', 1)
        rest = remove_command(rest, 'label', 1)
        rest = re.sub(r'\[H\]|\[h!?t?b?p?\]', ' ', rest)
        if rest.strip():
            caption = (caption + ' ' + rest.strip()).strip()
        lbl = re.search(r'\\label\{([^}]*)\}', inner)
        lbltxt = ('@@LBL:%s@@ ' % lbl.group(1)) if lbl else ''
        return '\\begin{figwrap}\n\nFIGPH %s\n\n%s%s\n\n\\end{figwrap}' % (
            ' '.join(seq), lbltxt, caption.strip())
    s = re.sub(r'\\begin\{(figure|center)\}(?:\[[^\]]*\])?(.*?)\\end\{\1\}', block_repl, s, flags=re.S)
    # center blocks with nested centers etc. are not expected; loose tokens stay
    s = re.sub(r'FIGTOKEN\{([^}]*)\}', r'\n\n\\begin{figwrap}\n\nFIGPH \1\n\n\\end{figwrap}\n\n', s)
    return s, figs


BOX_ENVS = ('definition', 'theorem', 'example', 'exercise', 'question', 'summarybox', 'solution', 'proof')


def mark_titles(s):
    out = []
    i = 0
    pat = re.compile(r'\\begin\{(%s)\}' % '|'.join(BOX_ENVS))
    while True:
        m = pat.search(s, i)
        if not m:
            out.append(s[i:])
            break
        env = m.group(1)
        out.append(s[i:m.start()])
        j = m.end()
        title = None
        if j < len(s) and s[j] == '[':
            title, j = read_optarg(s, j)
            title = strip_outer_braces(title)
        lab = re.match(r'\s*\\label\{([^}]*)\}', s[j:])
        lbl = ''
        if lab:
            lbl = '@@LBL:%s@@' % lab.group(1)
            j += lab.end()
        name = 'myproof' if env == 'proof' else env
        out.append('\\begin{%s}\n\n' % name)
        if title is not None or lbl:
            out.append('TTLSTART %s %s TTLEND\n\n' % (lbl, title or ''))
        i = j
    s = ''.join(out)
    return s.replace('\\end{proof}', '\\end{myproof}')


def preprocess(src, chap):
    s = re.sub(r'(?<!\\)%.*', '', src)
    s, figs = extract_figures(s, chap)
    s = mark_titles(s)
    segs = split_math(s)
    out = []
    for is_math, t in segs:
        if is_math:
            t = re.sub(r'\\(lr|en)\{', '{', t)
            t = t.replace('\\mtxt{', '\\text{')
            # pandoc drops \label inside math; nothing else to do
        else:
            t = re.sub(r'\\(lr|en)\{', r'\\textsc{', t)
            t = t.replace('\\notetitle', 'NOTETITLE ').replace('\\warntitle', 'WARNTITLE ')
            t = t.replace('\\checkmark', '✓')
            t = re.sub(r'\\label\{([^}]*)\}', r' @@LBL:\1@@ ', t)
            t = re.sub(r'\\ref\{([^}]*)\}', r'@@REF:\1@@', t)
            for cmd, n in (('addcontentsline', 3), ('markboth', 2), ('hspace', 1), ('vspace', 1)):
                t = remove_command(t, cmd, n)
            t = re.sub(r'\\renewcommand\{\\arraystretch\}\{[^}]*\}', '', t)
            t = re.sub(r'>\{\\raggedright\\arraybackslash\}', '', t)
            t = re.sub(r'\\(smallskip|medskip|bigskip|noindent|centering|hfill)(?![A-Za-z])', ' ', t)
        out.append(t)
    return ''.join(out), figs


def run_pandoc(tex):
    r = subprocess.run(['pandoc', '-f', 'latex', '-t', 'html', '--mathjax', '--wrap=none'],
                       input=tex.encode(), capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode())
    warn = r.stderr.decode().strip()
    return r.stdout.decode(), warn


# ---------------------------------------------------------------- restructure
KINDS = {
    'definition': ('تعریف', 'def', True),
    'theorem': ('قضیه', 'thm', True),
    'example': ('مثال', 'ex', True),
    'exercise': ('تمرین', 'exr', True),
    'question': ('پرسش', 'q', False),
    'summarybox': ('', 'sum', False),
}


def first_p_title(div):
    """Pull 'TTLSTART ... TTLEND' out of the first paragraph of div."""
    p = div.find('p', recursive=False)
    if not p:
        return None, None
    html = p.decode_contents()
    m = re.match(r'\s*TTLSTART(.*?)TTLEND\s*(.*)$', html, re.S)
    if not m:
        return None, None
    title = m.group(1).strip()
    lbl = None
    lm = re.search(r'@@LBL:([^@]*)@@', title)
    if lm:
        lbl = lm.group(1)
        title = (title[:lm.start()] + title[lm.end():]).strip()
    rest = m.group(2).strip()
    if rest:
        p.clear()
        p.append(BeautifulSoup(rest, 'html.parser'))
    else:
        p.decompose()
    return title, lbl


def frag(soup, html):
    return BeautifulSoup(html, 'html.parser')


def convert_digits(soup):
    skip_classes = {'math', 'en', 'smallcaps', 'nofa'}
    for t in list(soup.find_all(string=True)):
        if not isinstance(t, NavigableString) or not re.search(r'[0-9]', t):
            continue
        par = t.parent
        skip = False
        while par is not None:
            if isinstance(par, Tag):
                cls = set(par.get('class') or [])
                if cls & skip_classes or par.name in ('svg', 'code', 'pre', 'script', 'style'):
                    skip = True
                    break
            par = par.parent
        if skip:
            continue
        parts = re.split(r'(@@REF:[^@]*@@)', str(t))
        new = ''.join(p if p.startswith('@@REF:') else re.sub(r'(?<=\d)\.(?=\d)', '٫', p).translate(FA_DIGITS)
                      for p in parts)
        t.replace_with(new)


def restructure(html, chap, labels, fig_render):
    """Returns dict with title, sections, body html, refs to resolve."""
    soup = BeautifulSoup(html, 'html.parser')
    # chapter title
    h1 = soup.find('h1')
    title_html = h1.decode_contents() if h1 else ''
    if h1:
        h1.decompose()
    # Latin spans
    for sp in soup.find_all('span', class_='smallcaps'):
        sp['class'] = ['en']
        sp['dir'] = 'ltr'
        par = sp.parent
        if par.name == 'span' and not par.get('class') and len(par.contents) == 1:
            par.unwrap()
    # colored spans
    for sp in soup.find_all('span', style=True):
        st = sp['style']
        if 'color' in st:
            c = st.split(':', 1)[1].strip()
            if c.startswith('red') or 'warncol' in c or 'thmcol' in c:
                cls = 'tc-red'
            elif c.startswith('blue') or 'defcol' in c:
                cls = 'tc-blue'
            elif c.startswith('green') or 'excol' in c or c.startswith('teal'):
                cls = 'tc-green'
            elif c.startswith('orange') or 'exrcol' in c:
                cls = 'tc-orange'
            else:
                cls = 'tc-accent'
            del sp['style']
            sp['class'] = [cls]
    # headings
    sections = []
    si = sj = 0
    for h in soup.find_all(['h2', 'h3', 'h4']):
        h.attrs = {k: v for k, v in h.attrs.items() if k not in ('id', 'class')}
        sub = None
        br = h.find('br')
        if br:
            after = []
            for sib in list(br.next_siblings):
                after.append(sib.extract())
            br.decompose()
            sub = ''.join(str(a) for a in after).strip()
        # ch00 uses manual numbers like "۱. "
        first = h.contents[0] if h.contents else None
        if isinstance(first, NavigableString):
            first.replace_with(re.sub(r'^\s*[۰-۹0-9]+\.\s*', '', str(first)))
        main = h.decode_contents().strip()
        if h.name == 'h2':
            si += 1
            sj = 0
            hid = 's%d' % si
            num = ('%s.%s' % (fa(chap), fa(si))) if chap else fa(si)
        elif h.name == 'h3':
            sj += 1
            hid = 's%d-%d' % (si, sj)
            num = ('%s.%s.%s' % (fa(chap), fa(si), fa(sj))) if chap else '%s.%s' % (fa(si), fa(sj))
        else:
            hid = 's%d-%d-x%d' % (si, sj, len(sections))
            num = ''
        h['id'] = hid
        inner = ''
        if num:
            inner += '<span class="h-num">%s</span>' % num
        inner += '<span class="h-text">%s</span>' % main
        if sub:
            inner += '<span class="h-sub">%s</span>' % sub
        h.clear()
        h.append(frag(soup, inner))
        if h.name in ('h2', 'h3'):
            plain = BeautifulSoup(main, 'html.parser')
            sections.append({'id': hid, 'level': 2 if h.name == 'h2' else 3, 'num': num, 'html': main})
        lm = re.search(r'@@LBL:([^@]*)@@', str(h))
        if lm:
            labels[lm.group(1)] = {'chap': chap, 'id': hid, 'text': '«' + BeautifulSoup(main, 'html.parser').get_text().strip() + '»'}

    # boxes
    counter = 0
    for div in soup.find_all('div'):
        cls = (div.get('class') or [None])[0]
        if cls in KINDS:
            kind, short, numbered = KINDS[cls]
            title, lbl = first_p_title(div)
            num = ''
            bid = None
            if numbered:
                counter += 1
                num = '%s-%s' % (fa(chap), fa(counter))
                bid = 'b%d' % counter
            sec = soup.new_tag('section')
            sec['class'] = ['box', 'box-' + short]
            if bid:
                sec['id'] = bid
            head = '<header class="box-head">'
            if kind:
                head += '<span class="box-kind">%s%s</span>' % (kind, (' ' + num) if num else '')
            if title:
                head += '<span class="box-title">%s</span>' % title
            head += '</header>'
            if kind or title:
                sec.append(frag(soup, head))
            body = soup.new_tag('div')
            body['class'] = ['box-body']
            for ch in list(div.contents):
                body.append(ch.extract())
            sec.append(body)
            div.replace_with(sec)
            if lbl:
                labels[lbl] = {'chap': chap, 'id': bid, 'text': num}
        elif cls in ('note', 'warning'):
            aside = soup.new_tag('aside')
            aside['class'] = ['callout', 'callout-' + cls]
            label = 'نکته' if cls == 'note' else 'دقت کنید'
            for t in div.find_all(string=re.compile('NOTETITLE|WARNTITLE')):
                t.replace_with(re.sub(r'\s*(NOTETITLE|WARNTITLE)\s*', '', str(t)))
            aside.append(frag(soup, '<span class="callout-kind">%s</span>' % label))
            for ch in list(div.contents):
                aside.append(ch.extract())
            div.replace_with(aside)
    # solutions / answers / proofs
    for div in soup.find_all('div', class_=['solution', 'answer', 'myproof']):
        cls = div['class'][0]
        title, _ = first_p_title(div)
        if cls == 'myproof':
            box = soup.new_tag('div')
            box['class'] = ['proof']
            box.append(frag(soup, '<span class="proof-kind">%s.</span>' % (title or 'اثبات')))
            for ch in list(div.contents):
                box.append(ch.extract())
            box.append(frag(soup, '<span class="qed" aria-hidden="true"></span>'))
            div.replace_with(box)
            continue
        label = title or ('حل' if cls == 'solution' else 'پاسخ')
        det = soup.new_tag('details')
        det['class'] = ['sol']
        det['open'] = ''
        det.append(frag(soup, '<summary><span class="sol-label">%s</span></summary>' % label))
        body = soup.new_tag('div')
        body['class'] = ['sol-body']
        for ch in list(div.contents):
            body.append(ch.extract())
        det.append(body)
        div.replace_with(det)
    # exercise followed by its solution -> move inside the card
    for sec in soup.find_all('section', class_='box-exr'):
        nxt = sec.find_next_sibling()
        if nxt is not None and nxt.name == 'details' and 'sol' in (nxt.get('class') or []):
            sec.find('div', class_='box-body').append(nxt.extract())
    # figures
    for div in soup.find_all('div', class_='figwrap'):
        fig = soup.new_tag('figure')
        fig['class'] = ['fig']
        ps = div.find_all('p', recursive=False)
        has_op = any('OP:' in p.get_text() for p in ps)
        row = '<div class="fig-row%s">' % (' fig-eq' if has_op else '')
        cap_parts = []
        lbl = None
        for p in ps:
            txt = p.get_text().strip()
            if txt.startswith('FIGPH'):
                toks = txt.split()[1:]
                for t in toks:
                    if t.startswith('OP:'):
                        row += '<span class="fig-op">%s</span>' % {'*': '∗', '=': '=', '+': '+'}.get(t[3:], t[3:])
                    else:
                        row += fig_render(t)
            else:
                h = p.decode_contents()
                lm = re.search(r'@@LBL:([^@]*)@@', h)
                if lm:
                    lbl = lm.group(1)
                    h = h.replace(lm.group(0), '')
                if h.strip():
                    cap_parts.append(h.strip())
        row += '</div>'
        fig.append(frag(soup, row))
        if cap_parts:
            fig.append(frag(soup, '<figcaption>%s</figcaption>' % ' '.join(cap_parts)))
        div.replace_with(fig)
        if lbl:
            fig['id'] = 'fig-' + lbl.split(':')[-1]
            labels[lbl] = {'chap': chap, 'id': fig['id'], 'text': 'بالا'}
    # centers and tables
    for div in soup.find_all('div', class_='center'):
        div.unwrap()
    for tb in soup.find_all('table'):
        if tb.parent.name != 'div' or 'table-wrap' not in (tb.parent.get('class') or []):
            wrap = soup.new_tag('div')
            wrap['class'] = ['table-wrap']
            tb.wrap(wrap)
        for el in tb.find_all(['th', 'td', 'tr']):
            if el.get('style', '').startswith('text-align'):
                del el['style']
            if el.name == 'tr':
                el.attrs.pop('class', None)
    # stray label markers
    for t in soup.find_all(string=re.compile('@@LBL:')):
        for lm in re.finditer(r'@@LBL:([^@]*)@@', str(t)):
            # attach to nearest preceding heading
            h = t.find_previous(['h2', 'h3'])
            if h is not None and lm.group(1) not in labels:
                labels[lm.group(1)] = {'chap': chap, 'id': h['id'],
                                       'text': '«' + h.find('span', class_='h-text').get_text().strip() + '»'}
        t.replace_with(re.sub(r'\s*@@LBL:[^@]*@@\s*', ' ', str(t)))
    convert_digits(soup)
    return {'title': title_html, 'sections': sections, 'soup': soup}


def resolve_refs(html, chap, labels):
    def rep(m):
        key = m.group(1)
        lab = labels.get(key)
        if not lab:
            return '؟'
        href = ('#' + lab['id']) if lab['chap'] == chap else ('%s#%s' % (page_name(lab['chap']), lab['id']))
        return '<a class="xref" href="%s">%s</a>' % (href, lab['text'])
    return re.sub(r'@@REF:([^@]*)@@', rep, html)


def page_name(chap):
    return 'ch%02d.html' % chap
