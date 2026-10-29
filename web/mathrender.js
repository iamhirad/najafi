// Converts TeX formulas to SVG with MathJax (one shared glyph cache per page).
// stdin:  {"items": [{"tex": "...", "display": false}, ...]}
// stdout: {"svgs": [...], "errors": [[index, message], ...], "defs": "<svg>...</svg>"}
// Persian text inside \text{} is drawn with the page font (Vazirmatn); its width
// is measured with HarfBuzz so the surrounding symbols are placed correctly.
const fs = require('fs');
const path = require('path');
const {mathjax} = require('mathjax-full/js/mathjax.js');
const {TeX} = require('mathjax-full/js/input/tex.js');
const {SVG} = require('mathjax-full/js/output/svg.js');
const {liteAdaptor} = require('mathjax-full/js/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler} = require('mathjax-full/js/handlers/html.js');
const {AllPackages} = require('mathjax-full/js/input/tex/AllPackages.js');

const FONT_DIR = '/usr/share/fonts/truetype/vazirmatn';

const MACROS = {
  Prob: '\\mathbb{P}', E: '\\mathbb{E}', Var: '\\operatorname{Var}', Cov: '\\operatorname{Cov}',
  R: '\\mathbb{R}', N: '\\mathbb{N}', Z: '\\mathbb{Z}', F: '\\mathcal{F}',
  ind: '\\mathbf{1}', given: '\\,|\\,', iid: '\\text{i.i.d.}', indep: '\\perp\\!\\!\\!\\perp',
  dd: '\\,\\mathrm{d}', ML: '\\mathrm{ML}',
  argmax: '\\mathop{\\mathrm{arg\\,max}}\\limits', argmin: '\\mathop{\\mathrm{arg\\,min}}\\limits',
  lr: ['#1', 1], en: ['#1', 1], mtxt: ['\\text{#1}', 1], bm: ['\\boldsymbol{#1}', 1],
  mbox: ['\\text{#1}', 1], textsc: ['\\text{#1}', 1],
};

async function main() {
  const hb = await require('harfbuzzjs');
  const fonts = {};
  for (const [w, file] of [['normal', 'Vazirmatn-Regular.ttf'], ['bold', 'Vazirmatn-Bold.ttf']]) {
    const blob = hb.createBlob(fs.readFileSync(path.join(FONT_DIR, file)));
    const face = hb.createFace(blob, 0);
    fonts[w] = {font: hb.createFont(face), upem: face.upem};
  }
  function advance(text, weight) {
    const f = fonts[weight === 'bold' ? 'bold' : 'normal'];
    const buf = hb.createBuffer();
    buf.addText(text);
    buf.guessSegmentProperties();
    hb.shape(f.font, buf);
    let sum = 0;
    for (const g of buf.json()) sum += g.ax;
    buf.destroy();
    return sum / f.upem;
  }

  const input = JSON.parse(fs.readFileSync(0, 'utf8'));
  const adaptor = liteAdaptor();
  RegisterHTMLHandler(adaptor);
  const tex = new TeX({
    packages: AllPackages.filter(p => p !== 'bussproofs'),
    macros: MACROS,
    formatError: (jax, err) => { throw err; },
  });
  const svg = new SVG({fontCache: 'global', mtextFont: 'Vazirmatn'});
  svg.measureTextNode = function (textNode) {
    const s = adaptor.textContent(textNode);
    const size = parseFloat(adaptor.getAttribute(textNode, 'font-size')) || 884;
    const weight = adaptor.getAttribute(textNode, 'font-weight');
    return {w: advance(s, weight) * size / 1000, h: .75, d: .2};
  };
  const html = mathjax.document('', {InputJax: tex, OutputJax: svg});

  const out = {svgs: [], errors: []};
  input.items.forEach((it, i) => {
    try {
      const node = html.convert(it.tex, {display: !!it.display, em: 16, ex: 8, containerWidth: 1280});
      out.svgs.push(adaptor.outerHTML(node));
    } catch (e) {
      out.errors.push([i, String(e.message || e)]);
      out.svgs.push(null);
    }
  });
  const cache = svg.fontCache.getCache();
  out.defs = '<svg class="mjx-defs" aria-hidden="true" style="position:absolute;width:0;height:0;overflow:hidden" xmlns="http://www.w3.org/2000/svg">'
    + adaptor.outerHTML(cache) + '</svg>';
  process.stdout.write(JSON.stringify(out));
}
main().catch(e => { console.error(e); process.exit(1); });
