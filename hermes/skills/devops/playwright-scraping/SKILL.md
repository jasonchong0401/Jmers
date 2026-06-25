# Playwright Scraping Skill

Skill for web scraping with Playwright, including anti-detection techniques.

## Problem: Investing.com Cloudflare Protection

Investing.com uses aggressive Cloudflare WAF that blocks datacenter IPs.

### Attempts

1. Playwright headless + stealth → Cloudflare JS Challenge → IP blocked
2. Browserbase → blocked (no residential proxy)
3. curl with various User-Agents → 403
4. Internal TradingView API → 403

### Solution

Must run from a residential/office IP:

```bash
pip install playwright playwright-stealth
playwright install chromium
python scrape_commodities.py
```
