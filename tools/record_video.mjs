import { chromium } from 'playwright-core';
const browser = await chromium.launch({
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  headless: true,
  args: ['--no-sandbox', '--enable-webgl', '--use-angle=metal', '--hide-scrollbars'],
});
const t0 = Date.now();
const ctx = await browser.newContext({
  viewport: { width: 2560, height: 1440 },
  recordVideo: { dir: 'renders/video_raw', size: { width: 2560, height: 1440 } },
});
const page = await ctx.newPage();
const errors = [];
page.on('pageerror', (e) => errors.push(e.message));
await page.goto('http://127.0.0.1:4178/', { waitUntil: 'domcontentloaded' });
await page.waitForFunction(() => window.__VILLA__?.loaded === true, null, { timeout: 120000 });
await page.evaluate(() => { try { localStorage.removeItem('lanai-house-lang'); } catch (e) {} });
await page.selectOption('#langSelect', 'zh');
await page.waitForTimeout(1600);
const startOffset = (Date.now() - t0) / 1000;
await page.evaluate(() => {
  const v = window.__VILLA__;
  v.startCinema();
  v.env.setMode('morning');
});
setTimeout(() => page.evaluate(() => window.__VILLA__.env.setMode('day')).catch(() => {}), 14000);
setTimeout(() => page.evaluate(() => window.__VILLA__.env.setMode('dusk')).catch(() => {}), 28000);
setTimeout(() => page.evaluate(() => window.__VILLA__.env.setMode('night')).catch(() => {}), 39000);
setTimeout(() => page.evaluate(() => window.__VILLA__.showCinemaTitle(true)).catch(() => {}), 44000);
await page.waitForTimeout(47000);
const video = page.video();
await ctx.close();
await video.saveAs('renders/video_raw/lanai-house-raw.webm');
console.log(JSON.stringify({ startOffset, errors }));
await browser.close();
