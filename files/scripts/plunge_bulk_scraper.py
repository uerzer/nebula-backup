#!/usr/bin/env python3
"""Bulk scraper for plungesaunafinder.com venue pages.
Scrapes first 500 URLs from the venue URL list.
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
OUT_JSON = "/home/user/files/data/plunge_venues_batch1.json"
OUT_CSV = "/home/user/files/data/plunge_venues_batch1.csv"
OUT_FAILED = "/home/user/files/data/plunge_failed_batch1.txt"
BATCH_SIZE = 500
CONCURRENCY = 25
TIMEOUT = 15
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
    idx: int,
    total: int,
) -> tuple[int, str, str | None, int]:
    """Fetch one URL. Returns (index, url, html_or_None, status_code)."""
    async with semaphore:
        for attempt in range(2):  # 1 initial + 1 retry
            try:
                resp = await client.get(url, timeout=TIMEOUT)
                if resp.status_code == 404:
                    return (idx, url, None, 404)
                resp.raise_for_status()
                return (idx, url, resp.text, resp.status_code)
            except Exception as e:
                if attempt == 0:
                    await asyncio.sleep(RETRY_DELAY)
                else:
                    return (idx, url, None, -1)  # -1 = network/timeout error


async def main():
    t0 = time.time()

    # Step 1: Read URLs
    raw_urls = Path(URL_FILE).read_text().strip().splitlines()
    print(f"Loaded {len(raw_urls)} total URLs from file.")

    # Step 2: Fix URLs and take first BATCH_SIZE
    urls = [fix_url(u.strip()) for u in raw_urls[:BATCH_SIZE]]
    print(f"Processing first {len(urls)} URLs (with /wellness/ -> / fix applied).")
    print(f"Sample fixed URL: {urls[0]}")
    print()

    # Step 3: Scrape
    semaphore = asyncio.Semaphore(CONCURRENCY)
    results = []
    failed = []
    completed = 0

    headers = {"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"}

    async with httpx.AsyncClient(
        headers=headers,
        follow_redirects=True,
        http2=False,
        limits=httpx.Limits(max_connections=CONCURRENCY + 5, max_keepalive_connections=CONCURRENCY),
    ) as client:
        tasks = [
            fetch_one(client, url, semaphore, i, len(urls))
            for i, url in enumerate(urls)
        ]

        for coro in asyncio.as_completed(tasks):
            idx, url, html, status = await coro
            completed += 1

            if html:
                venue = extract_venue(html, url)
                if venue.get("name"):  # only keep if we got real data
                    results.append(venue)
                else:
                    failed.append((url, "no_data_extracted"))
            else:
                if status != 404:  # skip 404s silently
                    failed.append((url, f"status_{status}"))
                # else: silently skip 404s

            if completed % 100 == 0 or completed == len(urls):
                elapsed = time.time() - t0
                rate = completed / elapsed if elapsed > 0 else 0
                print(
                    f"  Progress: {completed}/{len(urls)} "
                    f"({len(results)} success, {len(failed)} failed) "
                    f"[{elapsed:.1f}s, {rate:.1f} req/s]"
                )

    elapsed_total = time.time() - t0
    print(f"\nScraping complete in {elapsed_total:.1f}s.")

    # Step 5: Save results
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)

    # JSON
    with open(OUT_JSON, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Saved {len(results)} venues to JSON: {OUT_JSON}")

    # CSV
    with open(OUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for venue in results:
            # Flatten opening_hours_raw if present
            row = {k: venue.get(k, "") for k in CSV_COLUMNS}
            writer.writerow(row)
    print(f"Saved {len(results)} venues to CSV: {OUT_CSV}")

    # Failed
    with open(OUT_FAILED, "w") as f:
        for url, reason in failed:
            f.write(f"{url}\t{reason}\n")
    print(f"Saved {len(failed)} failed URLs to: {OUT_FAILED}")

    # Step 6: Stats
    with_rating = sum(1 for v in results if v.get("rating_value"))
    with_phone = sum(1 for v in results if v.get("phone"))
    with_services = sum(1 for v in results if v.get("services"))
    with_place_id = sum(1 for v in results if v.get("google_place_id"))
    with_coords = sum(1 for v in results if v.get("latitude") and v.get("longitude"))
    with_website = sum(1 for v in results if v.get("website"))

    print("\n" + "=" * 55)
    print("  SCRAPE RESULTS -- BATCH 1 (first 500 URLs)")
    print("=" * 55)
    print(f"  Total URLs processed:    {len(urls)}")
    print(f"  Successful extractions:  {len(results)}")
    print(f"  Failed / no data:        {len(failed)}")
    print(f"  Silent 404 skips:        {len(urls) - len(results) - len(failed)}")
    print(f"  ---")
    print(f"  With ratings:            {with_rating}  ({with_rating/max(len(results),1)*100:.1f}%)")
    print(f"  With phone:              {with_phone}  ({with_phone/max(len(results),1)*100:.1f}%)")
    print(f"  With services:           {with_services}  ({with_services/max(len(results),1)*100:.1f}%)")
    print(f"  With Google Place ID:    {with_place_id}  ({with_place_id/max(len(results),1)*100:.1f}%)")
    print(f"  With coordinates:        {with_coords}  ({with_coords/max(len(results),1)*100:.1f}%)")
    print(f"  With website URL:        {with_website}  ({with_website/max(len(results),1)*100:.1f}%)")
    print(f"  ---")
    print(f"  Avg time per request:    {elapsed_total/len(urls)*1000:.0f}ms")
    print(f"  Throughput:              {len(urls)/elapsed_total:.1f} req/s")
    print("=" * 55)

    # Show sample record
    if results:
        print("\nSample venue record:")
        sample = results[0]
        for k, v in sample.items():
            val = str(v)[:100] if v else ""
            print(f"  {k}: {val}")


if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())
