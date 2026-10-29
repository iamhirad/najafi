# Web edition of the notes

An HTML edition of the course notes (sessions 3–22), with no PDF typesetting step.

- `build.py` builds `dist/` (one page per session plus `index.html`).
- Content comes from `../jozve/chapters/*.tex`: pandoc reads its structure, and `convert.py` turns it into styled HTML (boxes, solutions, Persian digits).
- `mathrender.js` (MathJax, Node) draws every formula as SVG. Persian text inside formulas is measured with HarfBuzz.
- `figs.py` / `figlib.py` redraw every figure as SVG that follows the page's light or dark theme.
- `template.py` holds the page layout, styles and the small script for the theme, solutions toggle and table of contents.

Build:

```
cd web && npm install && python3 build.py
```

Requires Python 3 (beautifulsoup4, numpy, scipy), pandoc, Node 18+ and the Vazirmatn TTF fonts.

PDF (same pages printed by Chromium, with cover, table of contents with page numbers and bookmarks):

```
cd web && python3 print.py     # -> pdf/Jozve-Amar-Ehtemal-Najafi.pdf
```
