"""Build the GitHub Pages website into web/site (full HTML documents + PDF).

python3 site.py   (run print.py first so the PDF exists)
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build  # noqa: E402

SITE = os.path.join(HERE, 'site')
URL = 'https://iamhirad.github.io/najafi/'
PDF_NAME = 'Jozve-Amar-Ehtemal-Najafi.pdf'


def main():
    from pypdf import PdfReader
    pdf_src = os.path.join(HERE, 'pdf', PDF_NAME)
    if os.path.isdir(SITE):
        shutil.rmtree(SITE)
    os.makedirs(SITE)
    build.DIST = SITE
    chapters, labels = build.load_chapters()
    for i, ch in enumerate(chapters):
        prev = chapters[i - 1] if i > 0 else None
        nxt = chapters[i + 1] if i + 1 < len(chapters) else None
        build.build_chapter(ch, prev, nxt, labels)
    shutil.copy(pdf_src, os.path.join(SITE, PDF_NAME))
    info = {'pdf': PDF_NAME, 'pages': len(PdfReader(pdf_src).pages),
            'mb': round(os.path.getsize(pdf_src) / 1e6), 'url': URL}
    build.build_index(chapters, site=info)
    open(os.path.join(SITE, '.nojekyll'), 'w').close()
    # link-preview image
    subprocess.run(['node', os.path.join(HERE, 'ogshot.js'), os.path.join(SITE, 'index.html'),
                    os.path.join(SITE, 'og.png')], check=True, cwd=HERE)
    print('site ready:', SITE, sorted(os.listdir(SITE)))


if __name__ == '__main__':
    main()
