# jSpider 🕷️

Web scraper for [Investing.com](https://www.investing.com/) commodity data, using Playwright + stealth plugins to bypass bot detection.

## Features

- Scrape real-time commodity prices from Investing.com
- Category filtering: energy, metals, agriculture, or all
- Stealth mode with browser fingerprint randomization
- Auto-wait for Cloudflare challenge resolution
- Output as JSON and CSV

## Quick Start

```bash
pip install playwright playwright-stealth
playwright install chromium

python scrape_commodities.py          # All commodities
python scrape_commodities.py --metals  # Only metals
python scrape_commodities.py --energy  # Only energy
python scrape_commodities.py --agriculture  # Only agriculture
python scrape_commodities.py --visible  # Show browser
python scrape_commodities.py --output my_data.csv  # Custom output
```

## Requirements

- Python 3.8+
- Playwright Chromium browser
- Must run from a residential/office IP (Investing.com blocks datacenter IPs)

## Output

Data saved to `output/` in JSON and CSV.

| Field      | Description        |
|------------|--------------------|
| name       | Commodity name     |
| last       | Last price         |
| high       | Daily high         |
| low        | Daily low          |
| change     | Price change       |
| change_pct | Change percentage  |
| time       | Last update time   |

## License

MIT
