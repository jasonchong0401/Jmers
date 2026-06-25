const { chromium } = require('playwright-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');

chromium.use(StealthPlugin());

(async () => {
  const browser = await chromium.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--disable-dev-shm-usage',
      '--disable-gpu',
    ]
  });

  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    viewport: { width: 1920, height: 1080 },
    locale: 'en-US',
    timezoneId: 'America/New_York',
    bypassCSP: true,
    ignoreHTTPSErrors: true,
  });

  const page = await context.newPage();

  await page.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => false });
    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
    window.chrome = { runtime: {}, loadTimes: function(){}, csi: function(){}, app: {} };
  });

  await page.route('**/*', (route) => {
    const type = route.request().resourceType();
    if (['image', 'media', 'font', 'stylesheet'].includes(type)) {
      route.abort();
    } else {
      route.continue();
    }
  });

  try {
    await page.goto('https://www.investing.com/commodities/', {
      timeout: 120000,
      waitUntil: 'domcontentloaded'
    });

    const title = await page.title();
    if (title.includes('Just a moment') || title.includes('Cloudflare')) {
      for (let i = 0; i < 30; i++) {
        await page.waitForTimeout(3000);
        const t = await page.title();
        if (!t.includes('Just a moment') && !t.includes('Cloudflare')) break;
      }
    }

    await page.waitForTimeout(5000);
    await page.evaluate(() => window.scrollTo(0, 800));
    await page.waitForTimeout(3000);

    const data = await page.evaluate(() => {
      const results = [];
      const seen = new Set();
      const allTrs = document.querySelectorAll('tr');
      const rows = [];
      allTrs.forEach(tr => {
        const cells = tr.querySelectorAll('td');
        if (cells.length >= 3) {
          const texts = [];
          cells.forEach(c => { texts.push((c.innerText || c.textContent || '').trim()); });
          rows.push(texts);
        }
      });
      rows.forEach(texts => {
        if (texts.length < 3) return;
        const name = texts[0];
        if (!name || name.length > 100 || name.includes('Name') || name.includes('Symbol')) return;
        if (name.includes('Sponsored') || name.includes('Advertisement') || name === '') return;
        const key = name.substring(0, 30);
        if (seen.has(key)) return;
        seen.add(key);
        results.push({
          name: name, last: texts[1] || '', high: texts[2] || '',
          low: texts[3] || '', change: texts[4] || '',
          changePct: texts[5] || '', time: texts[6] || ''
        });
      });
      return results;
    });

    if (data.length > 0) {
      data.forEach((item, i) => {
        console.log(`[${i+1}] ${item.name} | Last: ${item.last} | Chg: ${item.change}`);
      });
    }

    const ts = new Date().toISOString().replace(/[:.]/g, '-');
    fs.writeFileSync('commodities-' + ts + '.json', JSON.stringify(data, null, 2));
  } catch (err) {
    console.error('Error:', err.message);
  }

  await browser.close();
})();
