#!/usr/bin/env python3
"""Full scraper for plungesaunafinder.com -- scrapes ALL remaining URLs,
skips the first 500 already processed, and combines with batch 1 results.
"""

import asyncio
import csv
import json
import os
import re
import time
from pathlib import Path

import httpx

# --- Config ---
URL_FILE = "/home/user/files/data/plunge_venue_urls.txt"
BATCH1_JSON = "/home/user/files/data/plunge_venues_batch1.json"
OUT_JSON = "/home/user/files/data/plunge_venues_all.json"
OUT_CSV = "/home/user/files/data/plunge_venues_all.csv"
SKIP_FIRST = 500  # Already processed first 500 URLs
CONCURRENCY = 15
TIMEOUT = 20
RETRY_DELAY = 1
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

CSV_COLUMNS = [
    "name", "street_address", "city", "state", "postal_code",
    "latitude", "longitude", "phone", "website", "rating_value",
    "review_count", "services", "google_place_id", "description",
    "source_url", "canonical_url",
]


# --- Extraction ---
def extract_venue(html_text: str, source_url: str = "") -> dict:
    result = {"source_url": source_url}
    jsonld_pattern = re.compile(
        r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>', re.DOTALL
    )
    for block_text in jsonld_pattern.findall(html_text):
        try:
            data = json.loads(block_text)
            if data.get("@type") == "LocalBusiness":
                addr = data.get("address", {})
                if addr.get("streetAddress"):
                    geo = data.get("geo", {})
                    rating = data.get("aggregateRating", {})
                    result.update(
                        {
                            "name": data.get("name"),
                            "street_address": addr.get("streetAddress"),
                            "city": addr.get("addressLocality"),
                            "state": addr.get("addressRegion"),
                            "postal_code": addr.get("postalCode"),
                            "country": addr.get("addressCountry"),
                            "latitude": geo.get("latitude"),
                            "longitude": geo.get("longitude"),
                            "phone": data.get("telephone"),
                            "website": data.get("url"),
                            "description": data.get("description"),
                            "rating_value": rating.get("ratingValue"),
                            "review_count": rating.get("reviewCount"),
                            "opening_hours_raw": data.get("openingHours"),
                        }
                    )
        except Exception:
            continue

    svc = re.search(r"Services:</strong>\s*(?:<!--\s*-->)?\s*([^<]+)", html_text)
    if svc:
        result["services"] = svc.group(1).strip()

    place = re.search(r"place_id:([A-Za-z0-9_-]+)", html_text)
    if place:
        result["google_place_id"] = place.group(1)

    canon = re.search(r'rel="canonical"\s+href="([^"]+)"', html_text)
    if canon:
        result["canonical_url"] = canon.group(1)

    return result


def fix_url(url: str) -> str:
    """Replace /wellness/ with / since the site 307-redirects."""
    return url.replace("/wellness/", "/")


# --- Async fetch ---
async def fetch_one(
    client: httpx.AsyncClient,
    url: str,
    semaphore: asyncio.Semaphore,
) -> tuple[str, str | None, int]:
    """Fetch one URL. Returns (url, html_or_None, status_code)."""
    async with semaphore:
        for attempt in range(2):  # 1 initial + 1 retry
            try:
                resp = await client.get(url, timeout=TIMEOUT)
                if resp.status_code == 404:
                    return (url, None, 404)
                resp.raise_for_status()
                return (url, resp.text, resp.status_code)
            except Exception:
                if attempt == 0:
                    await asyncio.sleep(RETRY_DELAY)
                else:
                    return (url, None, -1)  # -1 = network/timeout error


async def main():
    t0 = time.time()

    # ── Step 1: Load batch 1 results ──
    batch1 = json.loads(Path(BATCH1_JSON).read_text())
    batch1_urls = {v["source_url"] for v in batch1}
    print(f"Loaded {len(batch1)} venues from batch 1 ({len(batch1_urls)} unique source URLs)")

    # ── Step 2: Load ALL URLs and skip first 500 ──
    raw_urls = Path(URL_FILE).read_text().strip().splitlines()
    print(f"Total URLs in file: {len(raw_urls)}")

    remaining_raw = raw_urls[SKIP_FIRST:]  # Skip first 500
    urls = [fix_url(u.strip()) for u in remaining_raw]
    print(f"Remaining URLs to process: {len(urls)} (skipped first {SKIP_FIRST})")
    
    # Double-check: also skip any URL already in batch1 results (belt and suspenders)
    urls_to_scrape = [u for u in urls if u not in batch1_urls]
    skipped_dupes = len(urls) - len(urls_to_scrape)
    if skipped_dupes > 0:
        print(f"  Also skipped {skipped_dupes} URLs already in batch 1 results")
    urls = urls_to_scrape
    print(f"Final URLs to scrape: {len(urls)}")
    print(f"Sample: {urls[0]}")
    print()

    # ── Step 3: Scrape all remaining ──
    semaphore = asyncio.Semaphore(CONCURRENCY)
    new_results = []
    failed = []
    skipped_404 = 0
    completed = 0

    headers = {"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"}

    async with httpx.AsyncClient(
        headers=headers,
        follow_redirects=True,
        http2=False,
        limits=httpx.Limits(max_connections=CONCURRENCY + 5, max_keepalive_connections=CONCURRENCY),
    ) as client:
        tasks = [
            fetch_one(client, url, semaphore)
            for url in urls
        ]

        for coro in asyncio.as_completed(tasks):
            url, html, status = await coro
            completed += 1

            if html:
                venue = extract_venue(html, url)
                if venue.get("name"):  # only keep if we got real data
                    new_results.append(venue)
                else:
                    failed.append((url, "no_data_extracted"))
            else:
                if status == 404:
                    skipped_404 += 1
                else:
                    failed.append((url, f"status_{status}"))

            if completed % 500 == 0 or completed == len(urls):
                elapsed = time.time() - t0
                rate = completed / elapsed if elapsed > 0 else 0
                print(
                    f"  Progress: {completed}/{len(urls)} "
                    f"({len(new_results)} extracted, {skipped_404} 404s, {len(failed)} failed) "
                    f"[{elapsed:.1f}s, {rate:.1f} req/s]"
                )

    elapsed_total = time.time() - t0
    print(f"\nScraping complete in {elapsed_total:.1f}s.")
    print(f"  New venues extracted: {len(new_results)}")
    print(f"  404 skips: {skipped_404}")
    print(f"  Failures: {len(failed)}")
    if failed:
        print(f"  Failed URLs sample: {failed[:5]}")
    print()

    # ── Step 4: Combine batch 1 + new results ──
    all_venues = batch1 + new_results
    print(f"Combined total: {len(batch1)} (batch 1) + {len(new_results)} (new) = {len(all_venues)} venues")

    # Deduplicate by source_url (just in case)
    seen_urls = set()
    deduped = []
    for v in all_venues:
        su = v.get("source_url", "")
        if su not in seen_urls:
            seen_urls.add(su)
            deduped.append(v)
    if len(deduped) < len(all_venues):
        print(f"  Removed {len(all_venues) - len(deduped)} duplicates")
    all_venues = deduped
    print(f"Final dataset: {len(all_venues)} unique venues")

    # ── Step 5: Save combined results ──
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)

    # JSON
    with open(OUT_JSON, "w") as f:
        json.dump(all_venues, f, indent=2, default=str)
    json_size = os.path.getsize(OUT_JSON) / (1024 * 1024)
    print(f"\nSaved {len(all_venues)} venues to JSON: {OUT_JSON} ({json_size:.1f} MB)")

    # CSV
    with open(OUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for venue in all_venues:
            row = {k: venue.get(k, "") for k in CSV_COLUMNS}
            writer.writerow(row)
    csv_size = os.path.getsize(OUT_CSV) / (1024 * 1024)
    print(f"Saved {len(all_venues)} venues to CSV: {OUT_CSV} ({csv_size:.1f} MB)")

    # ── Step 6: Final stats ──
    total_urls_processed = SKIP_FIRST + len(urls)
    total_404s = skipped_404 + (SKIP_FIRST - len(batch1))  # batch 1 had 500 - 332 = 168 404s

    with_rating = sum(1 for v in all_venues if v.get("rating_value"))
    with_phone = sum(1 for v in all_venues if v.get("phone"))
    with_services = sum(1 for v in all_venues if v.get("services"))
    with_place_id = sum(1 for v in all_venues if v.get("google_place_id"))
    with_coords = sum(1 for v in all_venues if v.get("latitude") and v.get("longitude"))
    with_website = sum(1 for v in all_venues if v.get("website"))
    n = max(len(all_venues), 1)

    print("\n" + "=" * 60)
    print("  COMPLETE SCRAPE RESULTS -- ALL VENUES")
    print("=" * 60)
    print(f"  Total URLs in sitemap:       {len(raw_urls)}")
    print(f"  Total URLs processed:        {total_urls_processed}")
    print(f"  Total live venues extracted: {len(all_venues)}")
    print(f"    - From batch 1:           {len(batch1)}")
    print(f"    - From remaining scrape:  {len(new_results)}")
    print(f"  Total 404s (dead links):     {total_404s}")
    print(f"  Total failures:              {len(failed)}")
    print(f"  ---")
    print(f"  DATA QUALITY (of {len(all_venues)} venues):")
    print(f"    Ratings:         {with_rating:>5}  ({with_rating/n*100:.1f}%)")
    print(f"    Phone numbers:   {with_phone:>5}  ({with_phone/n*100:.1f}%)")
    print(f"    Services:        {with_services:>5}  ({with_services/n*100:.1f}%)")
    print(f"    Google Place ID: {with_place_id:>5}  ({with_place_id/n*100:.1f}%)")
    print(f"    Coordinates:     {with_coords:>5}  ({with_coords/n*100:.1f}%)")
    print(f"    Website URL:     {with_website:>5}  ({with_website/n*100:.1f}%)")
    print(f"  ---")
    print(f"  Scrape time (remaining):     {elapsed_total:.1f}s")
    print(f"  Throughput:                  {len(urls)/elapsed_total:.1f} req/s")
    print("=" * 60)


if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())
