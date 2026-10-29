// node pdfrender.js in.html out.pdf  -- print an HTML file to PDF with Chromium
const { chromium } = require('playwright');
(async () => {
  const [inp, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ colorScheme: 'light' });
  await page.goto('file://' + inp, { waitUntil: 'networkidle', timeout: 120000 });
  await page.evaluate(() => document.fonts.ready);
  await page.emulateMedia({ media: 'print', colorScheme: 'light' });
  await page.pdf({
    path: out, format: 'A4', printBackground: true, preferCSSPageSize: true,
    outline: true, tagged: true, displayHeaderFooter: false,
  });
  await browser.close();
  console.log('pdf ok');
})().catch(e => { console.error(e); process.exit(1); });
