"""Page template: tokens, CSS, JS and page assembly for the notes."""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Markazi+Text:wght@500;600;700&family=Vazirmatn:wght@400;500;600;700;800&display=swap">')

CSS = r"""
/* Layout: one reading column (~46rem) with a sticky section index on the start (right) side on wide screens.
   Boxes are coded by hue: definition / theorem / example / exercise / question. */
:root {
  --paper: #F5F6F8;
  --surface: #FFFFFF;
  --ink: #17202D;
  --ink-2: #3D4757;
  --muted: #687285;
  --rule: #DFE3EA;
  --rule-2: #EEF0F4;
  --accent: #1C39BB;          /* Persian blue */
  --accent-soft: #E8ECFA;
  --def: #1C39BB;
  --thm: #A1232B;
  --ex: #00796B;
  --exr: #A85A12;
  --q: #0C6F8A;
  --note: #5E44A6;
  --warn: #B83226;
  --sum: #4B5567;
  --c1: #2451C9; --c2: #C8362F; --c3: #13896F; --c4: #D9821E; --c5: #7A4CC2; --c6: #1A93B0; --c7: #8A93A3;
  --fig-ink: #303845; --fig-grid: #E6E9EF; --fig-bg: #FFFFFF; --fig-fill: .22;
  --font-body: "Vazirmatn", "Noto Sans Arabic", Tahoma, "Segoe UI", sans-serif;
  --font-display: "Markazi Text", "Noto Naskh Arabic", "Vazirmatn", serif;
  --radius: 12px;
  --shadow: 0 1px 2px rgba(23, 32, 45, .05), 0 4px 18px rgba(23, 32, 45, .04);
  --measure: 46rem;
  --head-h: 3.5rem;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --paper: #0E1116; --surface: #151A22; --ink: #E6E9EF; --ink-2: #C5CBD6; --muted: #929BAC;
    --rule: #283041; --rule-2: #1D2330; --accent: #93A6FF; --accent-soft: #1D2647;
    --def: #93A6FF; --thm: #FF8D93; --ex: #4CD2B4; --exr: #F2A660; --q: #5FCAE4; --note: #BCA6F7; --warn: #FF7F72; --sum: #AEB6C4;
    --c1: #7E9CFF; --c2: #FF7A72; --c3: #49CFA9; --c4: #F5AA55; --c5: #B994FF; --c6: #5BCDE6; --c7: #8F98A8;
    --fig-ink: #C9CFDA; --fig-grid: #232A37; --fig-bg: #151A22; --fig-fill: .28;
    --shadow: 0 1px 2px rgba(0,0,0,.4);
    color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --paper: #0E1116; --surface: #151A22; --ink: #E6E9EF; --ink-2: #C5CBD6; --muted: #929BAC;
  --rule: #283041; --rule-2: #1D2330; --accent: #93A6FF; --accent-soft: #1D2647;
  --def: #93A6FF; --thm: #FF8D93; --ex: #4CD2B4; --exr: #F2A660; --q: #5FCAE4; --note: #BCA6F7; --warn: #FF7F72; --sum: #AEB6C4;
  --c1: #7E9CFF; --c2: #FF7A72; --c3: #49CFA9; --c4: #F5AA55; --c5: #B994FF; --c6: #5BCDE6; --c7: #8F98A8;
  --fig-ink: #C9CFDA; --fig-grid: #232A37; --fig-bg: #151A22; --fig-fill: .28;
  --shadow: 0 1px 2px rgba(0,0,0,.4);
  color-scheme: dark;
}

* { box-sizing: border-box; }
[hidden] { display: none !important; }
html { -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
body {
  margin: 0; background: var(--paper); color: var(--ink);
  font-family: var(--font-body); font-size: 16.5px; line-height: 1.95;
  text-rendering: optimizeLegibility;
}
body::before {
  content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px);
  z-index: 30; background: var(--surface);
}
a { color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 3px; }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 4px; }
.en { font-family: var(--font-body); unicode-bidi: isolate; }
strong { font-weight: 700; color: var(--ink); }
.tc-red { color: var(--thm); } .tc-blue { color: var(--def); } .tc-green { color: var(--ex); }
.tc-orange { color: var(--exr); } .tc-accent { color: var(--note); }

/* ---------- top bar ---------- */
.topbar {
  position: sticky; top: env(safe-area-inset-top, 0px); z-index: 20;
  background: color-mix(in srgb, var(--surface) 92%, transparent);
  -webkit-backdrop-filter: saturate(1.4) blur(10px); backdrop-filter: saturate(1.4) blur(10px);
  border-bottom: 1px solid var(--rule);
}
.topbar-in {
  height: var(--head-h); display: flex; align-items: center; gap: .75rem;
  max-width: 76rem; margin: 0 auto;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
}
.brand { display: flex; align-items: center; gap: .55rem; text-decoration: none; color: var(--ink); min-width: 0; }
.brand-mark {
  width: 2rem; height: 2rem; border-radius: 8px; background: var(--accent); color: var(--surface);
  display: grid; place-items: center; font-family: var(--font-display); font-weight: 700; font-size: 1.25rem; flex: none;
}
.brand-text { font-size: .9rem; line-height: 1.3; min-width: 0; }
.brand-text b { display: block; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.brand-text span { color: var(--muted); font-size: .78rem; white-space: nowrap; }
.spacer { flex: 1; }
.tb-btn {
  display: inline-flex; align-items: center; gap: .4rem; height: 2.25rem; padding: 0 .7rem;
  border: 1px solid var(--rule); border-radius: 999px; background: var(--surface); color: var(--ink-2);
  font: inherit; font-size: .84rem; cursor: pointer; white-space: nowrap;
}
.tb-btn:hover { border-color: var(--accent); color: var(--accent); }
.tb-btn svg { width: 1.05rem; height: 1.05rem; flex: none; }
.tb-btn[aria-pressed="true"] { background: var(--accent-soft); color: var(--accent); border-color: transparent; }
.toc-btn { display: none; }
@media (max-width: 1179px) { .toc-btn { display: inline-flex; } }
@media (max-width: 560px) { .tb-btn .lbl { display: none; } .tb-btn { padding: 0 .6rem; } .brand-text span { display: none; } }

/* ---------- chapter layout ---------- */
.layout {
  max-width: 76rem; margin: 0 auto; display: grid; grid-template-columns: minmax(0, 1fr); gap: 3rem;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  padding-block: 0 4rem;
}
@media (min-width: 1180px) { .layout { grid-template-columns: 16rem minmax(0, var(--measure)); justify-content: center; } }
main { min-width: 0; }
.toc {
  font-size: .86rem; line-height: 1.6;
}
@media (min-width: 1180px) {
  .toc { position: sticky; top: calc(var(--head-h) + env(safe-area-inset-top, 0px) + 1.5rem); align-self: start;
         max-height: calc(100vh - var(--head-h) - 3rem); overflow: auto; padding-block: 2.5rem 1rem; }
}
@media (max-width: 1179px) {
  .toc { position: fixed; z-index: 25; inset: 0 auto 0 0; width: min(22rem, 88vw);
         background: var(--surface); border-inline-end: 1px solid var(--rule); box-shadow: var(--shadow);
         padding: calc(1.25rem + env(safe-area-inset-top, 0px)) 1.25rem calc(1.25rem + env(safe-area-inset-bottom, 0px));
         padding-right: max(1.25rem, env(safe-area-inset-right, 0px));
         overflow: auto; transform: translateX(100%); visibility: hidden; transition: transform .25s ease, visibility .25s; right: 0; left: auto; }
  .toc.open { transform: none; visibility: visible; }
  .scrim { position: fixed; inset: 0; z-index: 24; background: rgba(10, 14, 20, .35); }
}
.toc-title { font-weight: 700; color: var(--muted); font-size: .78rem; letter-spacing: .02em; margin: 0 0 .6rem; }
.toc ol { list-style: none; margin: 0; padding: 0; }
.toc li a { display: flex; gap: .5rem; padding: .28rem .6rem; border-radius: 8px; color: var(--ink-2); text-decoration: none; }
.toc li a:hover { background: var(--rule-2); color: var(--ink); }
.toc li a.active { background: var(--accent-soft); color: var(--accent); font-weight: 600; }
.toc li.l3 a { padding-right: 1.9rem; font-size: .82rem; color: var(--muted); }
.toc .n { font-variant-numeric: tabular-nums; color: var(--muted); flex: none; }
.toc li a.active .n { color: inherit; }
.toc-close { display: none; }
@media (max-width: 1179px) { .toc-close { display: inline-flex; margin-bottom: 1rem; } }

/* ---------- chapter head ---------- */
.ch-head { padding-block: 2.6rem 1.6rem; border-bottom: 1px solid var(--rule); margin-bottom: 1.8rem; }
.ch-eyebrow { display: flex; align-items: center; gap: .6rem; color: var(--accent); font-weight: 600; font-size: .92rem; }
.ch-num {
  font-family: var(--font-display); font-weight: 700; font-size: 1.35rem; line-height: 1;
  border: 1.5px solid currentColor; border-radius: 10px; padding: .35rem .55rem .25rem;
}
.ch-title {
  font-family: var(--font-display); font-weight: 700; font-size: clamp(2rem, 1.4rem + 2.4vw, 2.9rem);
  line-height: 1.35; margin: .8rem 0 .6rem; text-wrap: balance; color: var(--ink);
}
.ch-meta { color: var(--muted); font-size: .9rem; display: flex; flex-wrap: wrap; gap: .3rem 1.2rem; }
.ch-meta b { color: var(--ink-2); font-weight: 600; font-variant-numeric: tabular-nums; }

/* ---------- prose ---------- */
main p { margin: .8rem 0; }
main ul, main ol { padding-inline-start: 1.4rem; margin: .7rem 0; }
main li { margin: .3rem 0; }
main li > p { margin: .2rem 0; }
main li::marker { color: var(--muted); }
h2, h3, h4 { scroll-margin-top: calc(var(--head-h) + 1.2rem); }
main h2 {
  font-family: var(--font-display); font-weight: 700; font-size: 1.85rem; line-height: 1.4;
  margin: 3.2rem 0 1rem; text-wrap: balance; display: flex; flex-wrap: wrap; align-items: baseline; gap: .2rem .7rem;
}
main h3 { font-size: 1.17rem; font-weight: 700; margin: 2.2rem 0 .6rem; display: flex; flex-wrap: wrap; align-items: baseline; gap: .2rem .6rem; text-wrap: balance; }
main h4 { font-size: 1.02rem; font-weight: 700; margin: 1.6rem 0 .4rem; color: var(--ink-2); }
main h2 .en, .ch-title .en { font-family: var(--font-body); font-size: .62em; font-weight: 600; color: var(--muted); }
main h3 .en { font-weight: 600; color: var(--muted); font-size: .9em; }
.h-num { font-family: var(--font-body); font-size: .62em; font-weight: 600; color: var(--accent); font-variant-numeric: tabular-nums; }
main h3 .h-num { font-size: .82em; }
.h-sub { flex-basis: 100%; font-family: var(--font-body); font-size: .58em; font-weight: 500; color: var(--muted); line-height: 1.5; }
main h3 .h-sub { font-size: .8em; }

/* math */
mjx-container[jax="SVG"] { direction: ltr; }
mjx-container[jax="SVG"] > svg { overflow: visible; min-height: 1px; min-width: 1px; }
mjx-container[jax="SVG"][display="true"] { display: block; text-align: center; margin: 0; }
mjx-container[jax="SVG"]:not([display]) { unicode-bidi: isolate; }
main mjx-container[jax="SVG"]:not([display]) > svg { max-width: 100%; height: auto; }
.dm { display: block; overflow-x: auto; overflow-y: hidden; margin: .9rem 0; padding: .35rem 0; -webkit-overflow-scrolling: touch; }
.dm::-webkit-scrollbar { height: 6px; } .dm::-webkit-scrollbar-thumb { background: var(--rule); border-radius: 3px; }
.merr { color: var(--warn); font-family: monospace; direction: ltr; unicode-bidi: isolate; }

/* ---------- boxes ---------- */
.box {
  --k: var(--def);
  margin: 1.6rem 0; border-radius: var(--radius); background: var(--surface);
  border: 1px solid color-mix(in srgb, var(--k) 26%, var(--rule)); box-shadow: var(--shadow);
  scroll-margin-top: calc(var(--head-h) + 1rem); overflow: hidden;
}
.box-def { --k: var(--def); } .box-thm { --k: var(--thm); } .box-ex { --k: var(--ex); }
.box-exr { --k: var(--exr); } .box-q { --k: var(--q); } .box-sum { --k: var(--sum); }
.box-head {
  display: flex; flex-wrap: wrap; align-items: baseline; gap: .15rem .7rem; padding: .7rem 1.15rem .6rem;
  background: color-mix(in srgb, var(--k) 9%, var(--surface));
  border-bottom: 1px solid color-mix(in srgb, var(--k) 18%, var(--rule));
}
.box-kind { color: var(--k); font-weight: 800; font-size: .86rem; letter-spacing: .01em; white-space: nowrap; font-variant-numeric: tabular-nums; }
.box-title { font-weight: 700; font-size: .98rem; color: var(--ink); line-height: 1.7; }
.box-sum .box-title { color: var(--ink-2); }
.box-body { padding: .35rem 1.15rem .55rem; }
.box-body > :first-child { margin-top: .6rem; }
.box-thm .box-body, .box-def .box-body { background: color-mix(in srgb, var(--k) 2.5%, var(--surface)); }

/* solutions */
details.sol { margin: .9rem -1.15rem -.55rem; border-top: 1px dashed color-mix(in srgb, var(--k, var(--ex)) 35%, var(--rule)); background: color-mix(in srgb, var(--paper) 55%, var(--surface)); }
main > details.sol, .callout details.sol { margin: 1rem 0; border: 1px dashed var(--rule); border-radius: var(--radius); }
details.sol > summary {
  list-style: none; cursor: pointer; padding: .55rem 1.15rem; display: flex; align-items: center; gap: .5rem;
  font-weight: 700; font-size: .9rem; color: var(--k, var(--ex)); user-select: none;
}
details.sol > summary::-webkit-details-marker { display: none; }
details.sol > summary::before {
  content: ""; width: .5rem; height: .5rem; border-inline-start: 2px solid currentColor; border-bottom: 2px solid currentColor;
  transform: rotate(45deg); transition: transform .2s; margin-top: -.2rem;
}
details.sol:not([open]) > summary::before { transform: rotate(-45deg); margin-top: 0; }
details.sol:not([open]) > summary::after { content: "نمایش"; font-weight: 500; font-size: .8rem; color: var(--muted); margin-inline-start: auto; }
.sol-body { padding: 0 1.15rem .7rem; }
.sol-body > :first-child { margin-top: 0; }

.proof { margin: .9rem 0; }
.proof-kind { font-weight: 700; color: var(--ink-2); margin-inline-end: .35rem; }
.proof > p:first-of-type { display: inline; }
.qed { display: block; width: .62rem; height: .62rem; border: 1.5px solid var(--muted); margin-inline-start: auto; margin-top: .2rem; }

/* callouts */
.callout {
  --k: var(--note); margin: 1.3rem 0; padding: .7rem 1.1rem; border-radius: var(--radius);
  background: color-mix(in srgb, var(--k) 7%, var(--surface)); font-size: .97rem;
}
.callout-warning { --k: var(--warn); }
.callout-kind {
  display: inline-block; font-weight: 800; font-size: .76rem; color: var(--surface); background: var(--k);
  border-radius: 6px; padding: 0 .5rem; margin-inline-end: .45rem; line-height: 1.75; vertical-align: .08em;
}
.callout > p:first-of-type { display: inline; }
.callout > .callout-kind + p { display: inline; }
.callout > p { margin: .5rem 0; }

/* figures */
figure.fig { margin: 1.8rem 0; text-align: center; }
.fig-row { display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: .6rem 1rem; }
.fig-row > svg { max-width: 100%; height: auto; flex: 0 1 auto; }
.fig-op { font-size: 1.6rem; color: var(--muted); }
.fig-eq { direction: ltr; }
.fig-row > .flow { flex: 1 1 100%; }
figcaption { color: var(--muted); font-size: .88rem; line-height: 1.8; margin-top: .6rem; max-width: 38rem; margin-inline: auto; text-wrap: pretty; }
svg.plot { direction: ltr; overflow: visible; }
svg.plot text { font-family: var(--font-body); }
.subfig { display: flex; flex-direction: column; align-items: center; gap: .3rem; max-width: 100%; min-width: 0; }
.subfig > svg { max-width: 100%; height: auto; }
.subfig-t { font-size: .9rem; font-weight: 600; color: var(--ink-2); line-height: 1.7; }
.fig-legend { list-style: none; margin: .2rem 0 0; padding: 0; display: flex; flex-wrap: wrap; justify-content: center; gap: .2rem 1.1rem; font-size: .85rem; color: var(--ink-2); }
.fig-legend li { display: inline-flex; align-items: center; gap: .4rem; }
.fig-legend svg { flex: none; }
.flow { display: flex; align-items: stretch; justify-content: center; gap: 0; flex-wrap: nowrap; margin: .4rem auto; max-width: 40rem; direction: ltr; }
.flow-node { flex: 0 1 11rem; min-width: 0; border: 1.6px solid var(--k, var(--rule)); border-radius: 12px; padding: .7rem .8rem; text-align: center; direction: rtl;
  background: color-mix(in srgb, var(--k, var(--rule)) 8%, var(--surface)); display: flex; flex-direction: column; justify-content: center; }
.flow-node.tone-blue { --k: var(--def); } .flow-node.tone-red { --k: var(--thm); } .flow-node.tone-green { --k: var(--ex); }
.fn-main { font-size: 1.1rem; }
.fn-sub { font-size: .82rem; color: var(--muted); line-height: 1.6; }
.flow-edge { flex: 1 1 7rem; min-width: 5.5rem; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 0 .4rem; font-size: .9rem; direction: rtl; }
.fe-line { display: block; width: 100%; height: 2px; background: var(--fig-ink); position: relative; margin: .3rem 0; }
.fe-line::after { content: ""; position: absolute; right: -2px; top: -5px; border: 6px solid transparent; border-left: 9px solid var(--fig-ink); border-right: 0; }
.fe-b { color: var(--muted); font-size: .82rem; }
@media (max-width: 560px) {
  .flow { flex-direction: column; align-items: center; }
  .flow-node { flex: none; width: min(16rem, 100%); }
  .flow-edge { flex: none; min-width: 0; flex-direction: row; gap: .6rem; padding: .3rem 0; }
  .fe-line { width: 2px; height: 2.2rem; margin: 0; }
  .fe-line::after { right: -5px; top: auto; bottom: -2px; border: 6px solid transparent; border-top: 9px solid var(--fig-ink); border-bottom: 0; }
}
.figph { padding: 2rem; border: 1px dashed var(--rule); color: var(--muted); }

/* tables */
.table-wrap { overflow-x: auto; margin: 1.1rem 0; -webkit-overflow-scrolling: touch; }
.table-wrap table { border-collapse: collapse; margin: 0 auto; font-size: .93rem; font-variant-numeric: tabular-nums; min-width: min(100%, 22rem); }
.table-wrap th, .table-wrap td { min-width: 4.5rem; padding: .45rem .8rem; border-bottom: 1px solid var(--rule); text-align: center; vertical-align: middle; }
.table-wrap thead th { background: var(--rule-2); font-weight: 700; color: var(--ink-2); border-bottom: 1px solid var(--rule); }
.table-wrap tbody tr:last-child td { border-bottom: none; }
.table-wrap table { border: 1px solid var(--rule); border-radius: 10px; border-collapse: separate; border-spacing: 0; overflow: hidden; }

a.xref { text-decoration: none; border-bottom: 1px dotted currentColor; }

/* chapter nav */
.pager { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 4rem; }
.pager a {
  display: flex; flex-direction: column; gap: .2rem; padding: 1rem 1.2rem; border: 1px solid var(--rule); border-radius: var(--radius);
  background: var(--surface); text-decoration: none; color: var(--ink); min-width: 0;
}
.pager a:hover { border-color: var(--accent); }
.pager .dir { font-size: .8rem; color: var(--muted); }
.pager .t { font-weight: 700; line-height: 1.6; }
.pager .next { text-align: left; grid-column: 2; }
@media (max-width: 560px) { .pager { grid-template-columns: 1fr; } .pager .next { grid-column: 1; } }

/* self-test mode: hide solutions */
body.quiz details.sol:not([open]) { background: var(--rule-2); }

/* ---------- index ---------- */
.home { max-width: 64rem; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 0 4rem; }
.hero { display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); gap: 2rem; align-items: end; padding-block: 3.2rem 2.4rem; border-bottom: 1px solid var(--rule); }
@media (max-width: 760px) { .hero { grid-template-columns: minmax(0, 1fr); padding-block: 2.2rem 1.8rem; } }
.hero-k { color: var(--accent); font-weight: 600; font-size: .92rem; }
.hero h1 { font-family: var(--font-display); font-weight: 700; font-size: clamp(2.6rem, 1.6rem + 4vw, 4.2rem); line-height: 1.2; margin: .5rem 0 .7rem; text-wrap: balance; }
.hero p { margin: .3rem 0; color: var(--ink-2); }
.hero .who { color: var(--muted); font-size: .93rem; }
.hero-fig { text-align: center; }
.hero-fig > svg { width: 100%; max-width: 26rem; height: auto; }
.hero-fig mjx-container > svg { max-width: 100%; height: auto; }
.hero-fig figcaption { margin-top: .2rem; }
.stats { display: flex; flex-wrap: wrap; gap: .6rem 2.2rem; padding-block: 1.4rem; border-bottom: 1px solid var(--rule); }
.stat b { display: block; font-family: var(--font-display); font-size: 2rem; line-height: 1.1; color: var(--ink); font-variant-numeric: tabular-nums; }
.stat span { color: var(--muted); font-size: .85rem; }
.resume { display: flex; flex-wrap: wrap; align-items: center; gap: .5rem 1rem; margin-top: 1.4rem; padding: .8rem 1.1rem; border-radius: var(--radius); background: var(--accent-soft); }
.resume a { font-weight: 700; text-decoration: none; }
.part { margin-top: 2.6rem; }
.part-h { display: flex; align-items: baseline; gap: .8rem; margin-bottom: .8rem; }
.part-h h2 { font-family: var(--font-display); font-size: 1.7rem; margin: 0; }
.part-h span { color: var(--muted); font-size: .88rem; }
.chap-list { list-style: none; margin: 0; padding: 0; display: grid; gap: .7rem; }
.chap {
  display: grid; grid-template-columns: 4.2rem minmax(0, 1fr); gap: 1rem; align-items: start;
  padding: 1rem 1.2rem; background: var(--surface); border: 1px solid var(--rule); border-radius: var(--radius);
  text-decoration: none; color: var(--ink); transition: border-color .15s, transform .15s;
}
.chap:hover { border-color: var(--accent); }
.chap-n { font-family: var(--font-display); font-weight: 700; font-size: 2.3rem; line-height: 1; color: var(--accent); text-align: center; padding-top: .25rem; }
.chap-n small { display: block; font-family: var(--font-body); font-size: .68rem; font-weight: 600; color: var(--muted); margin-top: .35rem; }
.chap-b { min-width: 0; }
.chap-t { font-weight: 700; font-size: 1.06rem; line-height: 1.7; }
.chap-s { color: var(--muted); font-size: .86rem; line-height: 1.8; margin-top: .15rem; }
.chap-c { display: flex; flex-wrap: wrap; gap: .4rem; margin-top: .5rem; }
.pill { font-size: .76rem; padding: .05rem .55rem; border-radius: 999px; background: var(--rule-2); color: var(--ink-2); font-variant-numeric: tabular-nums; white-space: nowrap; }
.pill.ex { color: var(--ex); background: color-mix(in srgb, var(--ex) 10%, var(--surface)); }
.pill.exr { color: var(--exr); background: color-mix(in srgb, var(--exr) 10%, var(--surface)); }
.pill.fig { color: var(--def); background: color-mix(in srgb, var(--def) 9%, var(--surface)); }
.legend-boxes { display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1rem; }
.howto { margin-top: 2.8rem; padding: 1.2rem 1.4rem; border: 1px solid var(--rule); border-radius: var(--radius); background: var(--surface); font-size: .93rem; }
.howto h2 { font-family: var(--font-display); font-size: 1.4rem; margin: 0 0 .4rem; }
.howto ul { margin: .3rem 0; padding-inline-start: 1.2rem; }
.foot { margin-top: 3rem; color: var(--muted); font-size: .82rem; text-align: center; }
"""

JS = r"""
(function () {
  var root = document.documentElement;
  function get(k, d) { try { var v = localStorage.getItem(k); return v === null ? d : v; } catch (e) { return d; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  // theme: system -> light -> dark
  var themeBtn = document.getElementById('theme-btn');
  var labels = { system: 'خودکار', light: 'روشن', dark: 'تیره' };
  function applyTheme(t) {
    if (t === 'system') root.removeAttribute('data-theme'); else root.setAttribute('data-theme', t);
    if (themeBtn) { var l = themeBtn.querySelector('.lbl'); if (l) l.textContent = 'پوسته: ' + labels[t]; themeBtn.setAttribute('aria-label', 'پوسته: ' + labels[t]); }
  }
  var theme = get('jz-theme', 'system');
  applyTheme(theme);
  if (themeBtn) themeBtn.addEventListener('click', function () {
    theme = theme === 'system' ? 'light' : theme === 'light' ? 'dark' : 'system';
    set('jz-theme', theme); applyTheme(theme);
  });

  // self-test mode: collapse every solution
  var quizBtn = document.getElementById('quiz-btn');
  function applyQuiz(on) {
    document.body.classList.toggle('quiz', on);
    document.querySelectorAll('details.sol').forEach(function (d) { d.open = !on; });
    if (quizBtn) {
      quizBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
      var l = quizBtn.querySelector('.lbl'); if (l) l.textContent = on ? 'حل‌ها پنهان' : 'حل‌ها نمایان';
    }
  }
  var quiz = get('jz-quiz', '0') === '1';
  if (document.querySelector('details.sol')) applyQuiz(quiz);
  if (quizBtn) quizBtn.addEventListener('click', function () { quiz = !quiz; set('jz-quiz', quiz ? '1' : '0'); applyQuiz(quiz); });

  // table of contents drawer (narrow screens)
  var toc = document.getElementById('toc'), tocBtn = document.getElementById('toc-btn'), scrim = null;
  function closeToc() { if (!toc) return; toc.classList.remove('open'); if (scrim) { scrim.remove(); scrim = null; } if (tocBtn) tocBtn.setAttribute('aria-expanded', 'false'); }
  function openToc() {
    toc.classList.add('open'); tocBtn.setAttribute('aria-expanded', 'true');
    scrim = document.createElement('div'); scrim.className = 'scrim'; scrim.addEventListener('click', closeToc); document.body.appendChild(scrim);
  }
  if (tocBtn && toc) tocBtn.addEventListener('click', function () { toc.classList.contains('open') ? closeToc() : openToc(); });
  var tocClose = document.getElementById('toc-close'); if (tocClose) tocClose.addEventListener('click', closeToc);
  if (toc) toc.addEventListener('click', function (e) { if (e.target.closest('a') && window.matchMedia('(max-width: 1179px)').matches) closeToc(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeToc(); });

  // highlight the section being read
  var links = toc ? Array.prototype.slice.call(toc.querySelectorAll('a[href^="#"]')) : [];
  var map = {}; links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
  var heads = Array.prototype.slice.call(document.querySelectorAll('main h2[id], main h3[id]')).filter(function (h) { return map[h.id]; });
  function spy() {
    var y = window.scrollY + 120, cur = null;
    for (var i = 0; i < heads.length; i++) { if (heads[i].offsetTop <= y) cur = heads[i]; else break; }
    links.forEach(function (a) { a.classList.remove('active'); });
    if (cur) { map[cur.id].classList.add('active'); }
  }
  if (heads.length) { window.addEventListener('scroll', function () { window.requestAnimationFrame(spy); }, { passive: true }); spy(); }

  // remember the last chapter read; show it on the home page
  var page = document.body.getAttribute('data-page');
  if (page && page !== 'index') set('jz-last', page + '|' + document.body.getAttribute('data-label'));
  var resume = document.getElementById('resume');
  if (resume) {
    var last = get('jz-last', '');
    if (last) { var parts = last.split('|'); var a = resume.querySelector('a'); a.href = parts[0] + '.html'; a.textContent = parts[1]; resume.hidden = false; }
  }
})();
"""

ICONS = {
    'list': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M9 6h11M9 12h11M9 18h11"/><circle cx="4.5" cy="6" r="1" fill="currentColor"/><circle cx="4.5" cy="12" r="1" fill="currentColor"/><circle cx="4.5" cy="18" r="1" fill="currentColor"/></svg>',
    'eye': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg>',
    'theme': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="8.5"/><path d="M12 3.5v17A8.5 8.5 0 0 0 12 3.5z" fill="currentColor"/></svg>',
    'close': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>',
}


def topbar(page_label, show_toc=True, show_quiz=True):
    b = ['<header class="topbar"><div class="topbar-in">',
         '<a class="brand" href="index.html"><span class="brand-mark">آ</span>'
         '<span class="brand-text"><b>آمار و احتمال مهندسی</b><span>%s</span></span></a>' % page_label,
         '<span class="spacer"></span>']
    if show_toc:
        b.append('<button class="tb-btn toc-btn" id="toc-btn" type="button" aria-expanded="false" aria-controls="toc">%s<span class="lbl">فهرست</span></button>' % ICONS['list'])
    if show_quiz:
        b.append('<button class="tb-btn" id="quiz-btn" type="button" aria-pressed="false" title="پنهان یا نمایان کردن همه حل‌ها">%s<span class="lbl">حل‌ها نمایان</span></button>' % ICONS['eye'])
    b.append('<button class="tb-btn" id="theme-btn" type="button">%s<span class="lbl">پوسته</span></button>' % ICONS['theme'])
    b.append('</div></header>')
    return ''.join(b)


def chapter_page(ch, prev, nxt, body, toc_html, defs, head_html):
    title = '%s · %s' % (ch['label'], ch['title_text'])
    pager = '<nav class="pager" aria-label="جلسه قبل و بعد">'
    if prev:
        pager += '<a class="prev" href="%s"><span class="dir">→ %s</span><span class="t">%s</span></a>' % (prev['file'], prev['label'], prev['title_html'])
    if nxt:
        pager += '<a class="next" href="%s"><span class="dir">%s ←</span><span class="t">%s</span></a>' % (nxt['file'], nxt['label'], nxt['title_html'])
    pager += '</nav>'
    return ('<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
            '<meta name="claude:viewport-fit-sides" content="cover">'
            '<title>%s</title>%s<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}%s</style></head>'
            '<body data-page="%s" data-label="%s">%s%s'
            '<div class="layout"><nav class="toc" id="toc" aria-label="فهرست این جلسه">'
            '<button class="tb-btn toc-close" id="toc-close" type="button">%s<span>بستن</span></button>'
            '<p class="toc-title">در این جلسه</p>%s</nav>'
            '<main>%s%s%s</main></div><script>%s</script></body></html>') % (
        title, FONTS, CSS, ch['file'][:-5], ch['label'], defs, topbar(ch['label']), ICONS['close'], toc_html,
        head_html, body, pager, JS)
