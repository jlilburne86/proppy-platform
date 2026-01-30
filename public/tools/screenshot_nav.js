const path = require('path');
const fs = require('fs');

async function main() {
  const { chromium } = require(path.resolve(__dirname, '../../playwright-project/node_modules/playwright'));
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await context.newPage();
  const outDir = path.resolve(__dirname, '..');
  const shots = [
    ['home', 'http://localhost:8020/'],
  ];
  for (const [name, url] of shots) {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
    // Hover Solutions and Success to capture dropdowns
    try {
      await page.hover('text=Solutions');
      await page.waitForTimeout(300);
    } catch {}
    await page.screenshot({ path: path.join(outDir, `screenshot-${name}.png`), fullPage: false });
  }
  await browser.close();
  console.log('Saved screenshot(s) to', outDir);
}

main().catch(err => { console.error(err); process.exit(1); });

