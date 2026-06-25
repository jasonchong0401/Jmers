#!/usr/bin/env python3
"""Investing.com Commodities Scraper"""
import asyncio, json, csv, sys, argparse
from datetime import datetime
from pathlib import Path

CATEGORY_URLS = {
    "all": "https://www.investing.com/commodities/",
    "energy": "https://www.investing.com/commodities/energies",
    "metals": "https://www.investing.com/commodities/metals",
    "agriculture": "https://www.investing.com/commodities/agricultural",
}
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

def parse_args():
    parser = argparse.ArgumentParser(description="Investing.com Commodities Scraper")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--all", action="store_true", default=True)
    group.add_argument("--energy", action="store_true")
    group.add_argument("--metals", action="store_true")
    group.add_argument("--agriculture", action="store_true")
    parser.add_argument("--output", type=str)
    parser.add_argument("--headless", action="store_true", default=True)
    parser.add_argument("--visible", action="store_true")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--retries", type=int, default=2)
    return parser.parse_args()

def get_url(args):
    if args.energy:
        return CATEGORY_URLS["energy"], "energy"
    elif args.metals:
        return CATEGORY_URLS["metals"], "metals"
    elif args.agriculture:
        return CATEGORY_URLS["agriculture"], "agriculture"
    return CATEGORY_URLS["all"], "all"

def extract_commodity_data(page):
    return page.evaluate("""() => {
        const results = [];
        const seen = new Set();
        const table = document.querySelector('table[class*="datatable"], table.genTbl');
        const rows = table ? table.querySelectorAll('tbody tr') : document.querySelectorAll('table tbody tr');
        for (const row of rows) {
            const cells = row.querySelectorAll('td');
            if (!cells.length) continue;
            const texts = [];
            cells.forEach(c => texts.push((c.innerText || '').trim().replace(/\\s+/g, ' ')));
            const first = texts[0] || '';
            if (!first || first.length > 120) continue;
            if (/Name|Symbol|Instrument|Sort/i.test(first)) continue;
            const key = first.substring(0, 40).toLowerCase();
            if (seen.has(key)) continue;
            seen.add(key);
            results.push({
                name: first, last: texts[1] || '', high: texts[2] || '',
                low: texts[3] || '', change: texts[4] || '',
                change_pct: texts[5] || '', time: texts[6] || '',
            });
        }
        return results;
    }""")

async def scrape_once(browser, url, timeout):
    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1080},
        locale="en-US", timezone_id="America/New_York",
    )
    page = await context.new_page()
    await page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => false });
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
        window.chrome = { runtime: {}, loadTimes: function(){}, csi: function(){}, app: {} };
    """)
    try:
        await page.goto(url, timeout=timeout * 1000, wait_until="domcontentloaded")
        title = await page.title()
        if "Just a moment" in title or "Cloudflare" in title:
            for i in range(20):
                await page.wait_for_timeout(3000)
                title = await page.title()
                if "Just a moment" not in title and "Cloudflare" not in title:
                    break
        try:
            await page.wait_for_selector('table', timeout=15000)
        except:
            pass
        await page.wait_for_timeout(3000)
        await page.evaluate("window.scrollTo(0, 600)")
        await page.wait_for_timeout(2000)
        data = await extract_commodity_data(page)
        return data, await page.title()
    finally:
        await context.close()

async def main():
    args = parse_args()
    url, category = get_url(args)
    headless = not args.visible
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=headless,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
        )
        data = []
        for attempt in range(args.retries + 1):
            if attempt > 0:
                await asyncio.sleep(3)
            try:
                data, title = await scrape_once(browser, url, args.timeout)
                if data:
                    break
            except Exception as e:
                if attempt < args.retries:
                    continue
        await browser.close()
    if not data:
        print("No data extracted.")
        return 1
    for item in data:
        print(f"{item['name']:25} {item['last']:>12} {item.get('change', ''):>10} {item.get('change_pct', ''):>8}")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outpath = Path(args.output) if args.output else OUTPUT_DIR / f"commodities_{category}_{ts}.json"
    outpath.parent.mkdir(parents=True, exist_ok=True)
    json_path = outpath.with_suffix(".json")
    json_path.write_text(json.dumps({"source": url, "scraped_at": datetime.now().isoformat(), "count": len(data), "data": data}, indent=2, ensure_ascii=False), encoding="utf-8")
    csv_path = outpath.with_suffix(".csv")
    if data:
        with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "last", "high", "low", "change", "change_pct", "time"])
            writer.writeheader()
            writer.writerows(data)
    print(f"Saved: {json_path}, {csv_path}")
    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
