---
name: web-scraping-pipelines
description: Best practices and patterns for web scraping pipelines, data extraction workflows, and HTML parsing. Use when building scrapers, designing extraction pipelines, or processing raw web data.
created_at: 2026-03-08T14:34:05.436888+00:00
updated_at: 2026-03-08T14:34:05.436888+00:00
---

# Web Scraping Pipeline Patterns

## Tool Selection
- Static HTML (no JS): use fetch + BeautifulSoup (Python) or cheerio (Node)
- JS-rendered pages: use Playwright or Puppeteer via the browser automation toolkit
- APIs behind UI: inspect Network tab, replicate JSON API calls directly

## Python Scraper Template
```python
import httpx
import time
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; research-bot/1.0)",
    "Accept-Language": "en-US,en;q=0.9",
}

def scrape_page(url: str) -> BeautifulSoup:
    resp = httpx.get(url, headers=HEADERS, timeout=15, follow_redirects=True)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def scrape_all(base_url: str, delay: float = 1.5):
    results = []
    page = 1
    while True:
        soup = scrape_page(f"{base_url}?page={page}")
        items = parse_items(soup)
        if not items:
            break
        results.extend(items)
        page += 1
        time.sleep(delay)
    return results
```

## Data Normalization
- Strip and lowercase text fields before comparison
- Normalize phone numbers to E.164: +1XXXXXXXXXX
- Geocode addresses using a free API (nominatim.openstreetmap.org) when lat/lng missing
- Validate URLs: ensure they start with http/https

## Error Handling
- Wrap each page scrape in try/except; log errors but continue pipeline
- Retry on 429/503 with exponential backoff (2s, 4s, 8s)
- On 404, mark venue as inactive rather than deleting

## Output Formats
- Intermediate: JSONL (one JSON object per line) for streaming large datasets
- Final: upsert to Supabase or write to CSV/Parquet for archival
- Always include source_url and scraped_at timestamp

## Politeness
- Respect robots.txt
- Default crawl delay: 1.5s between requests
- Max concurrency: 3 parallel requests for same domain
