#!/usr/bin/env python3
"""SaunaFinder v2 — Complete Static Site Generator

Reads sauna_master_database.csv and produces ~4,500 static HTML pages
with a dark-theme design, full cross-linking, JSON-LD, sitemap, etc.
"""

import csv
import html
import math
import os
import re
import time
from collections import defaultdict
from datetime import datetime, timezone

# ── paths ────────────────────────────────────────────────────────────────────
CSV_PATH = "/home/user/files/data/sauna_master_database.csv"
OUT_DIR  = "/home/user/files/code/sauna-site-v2"
BASE_URL = "https://saunafinder.com"
CLAIM_URL = "https://YOUR_SUPABASE_URL.supabase.co/functions/v1/claim"

# ── state abbreviation <-> full name ─────────────────────────────────────────
STATE_ABBR_TO_NAME = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "DC": "District of Columbia", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii",
    "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
    "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine",
    "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
    "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska",
    "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico",
    "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island",
    "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas",
    "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington",
    "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming",
}
STATE_NAME_TO_ABBR = {v: k for k, v in STATE_ABBR_TO_NAME.items()}

# ── helpers ──────────────────────────────────────────────────────────────────
def slugify(text: str) -> str:
    """Lower-case, strip non-alphanumeric except hyphens, collapse runs."""
    s = text.lower().strip()
    s = re.sub(r"[^a-z0-9-]+", "-", s)
    s = re.sub(r"-{2,}", "-", s)
    return s.strip("-")


def esc(text) -> str:
    """HTML-escape, returning empty string for None / NaN."""
    if text is None:
        return ""
    t = str(text).strip()
    if t.lower() in ("nan", ""):
        return ""
    return html.escape(t)


def star_html(rating_str: str) -> str:
    """Render star rating as HTML."""
    try:
        rating = float(rating_str)
    except (ValueError, TypeError):
        return ""
    full = int(rating)
    half = 1 if (rating - full) >= 0.3 else 0
    empty = 5 - full - half
    stars = '<span class="stars">'
    stars += '<span class="star full">&#9733;</span>' * full
    if half:
        stars += '<span class="star half">&#9733;</span>'
    stars += '<span class="star empty">&#9734;</span>' * empty
    stars += f' <span class="rating-num">{rating:.1f}</span>'
    stars += '</span>'
    return stars


def state_abbr_for(row: dict) -> str:
    """Return 2-letter abbreviation for a venue's state."""
    st = (row.get("state") or "").strip()
    if len(st) == 2:
        return st.upper()
    return STATE_NAME_TO_ABBR.get(st, st.upper()[:2])


def state_name_for(abbr: str) -> str:
    return STATE_ABBR_TO_NAME.get(abbr.upper(), abbr)


def write(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def format_phone_link(phone: str) -> str:
    digits = re.sub(r"[^0-9+]", "", phone)
    return f'<a href="tel:{digits}" class="phone-link">{esc(phone)}</a>'


def format_website_link(url: str) -> str:
    display = re.sub(r"https?://", "", url).rstrip("/")
    if len(display) > 40:
        display = display[:37] + "..."
    return f'<a href="{esc(url)}" target="_blank" rel="noopener" class="website-link">{esc(display)}</a>'


def services_tags(services_str: str) -> str:
    if not services_str:
        return ""
    tags = [s.strip() for s in services_str.split(",") if s.strip()]
    return "".join(f'<span class="service-tag">{esc(t)}</span>' for t in tags)


def category_badge(cat: str) -> str:
    if not cat:
        return ""
    return f'<span class="category-badge">{esc(cat)}</span>'


# ── HTML shell ───────────────────────────────────────────────────────────────
def page_shell(title: str, body: str, description: str = "",
               canonical: str = "", extra_head: str = "") -> str:
    desc_tag = f'<meta name="description" content="{esc(description)}">' if description else ""
    canon_tag = f'<link rel="canonical" href="{esc(canonical)}">' if canonical else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
{desc_tag}
{canon_tag}
<link rel="stylesheet" href="/styles.css">
{extra_head}
</head>
<body>
<header class="site-header">
  <div class="container header-inner">
    <a href="/" class="logo">Sauna<span class="accent">Finder</span></a>
    <nav class="main-nav">
      <a href="/">Home</a>
      <a href="/directory.html">Directory</a>
      <a href="/#browse-states">Browse by State</a>
    </nav>
    <button class="mobile-toggle" aria-label="Menu">&#9776;</button>
  </div>
</header>
<main class="container">
{body}
</main>
<footer class="site-footer">
  <div class="container">
    <p>&copy; {datetime.now().year} SaunaFinder &mdash; The #1 Sauna &amp; Cold Plunge Directory</p>
    <p>
      <a href="mailto:hello@saunafinder.com?subject=List My Business">List Your Business</a> &middot;
      <a href="mailto:hello@saunafinder.com?subject=Advertising Inquiry">Advertise</a>
    </p>
  </div>
</footer>
<script src="/script.js"></script>
</body>
</html>"""


# ── venue card snippet ───────────────────────────────────────────────────────
def venue_card(v: dict, show_city: bool = True) -> str:
    name = esc(v["name"])
    city = esc(v["city"])
    st = esc(v["state_abbr"])
    slug = v["slug"]
    rating = v.get("rating_value", "")
    review = v.get("review_count", "")
    cat = esc(v.get("category", ""))
    svcs = v.get("services", "")

    rating_html = ""
    if rating and str(rating) not in ("nan", ""):
        try:
            r = float(rating)
            rc = ""
            if review and str(review) not in ("nan", ""):
                rc = f' <span class="review-count">({int(float(review))})</span>'
            rating_html = f'{star_html(str(r))}{rc}'
        except (ValueError, TypeError):
            pass

    location = f"{city}, {st}" if show_city else ""
    cat_html = f'<span class="category-badge">{cat}</span>' if cat else ""
    svcs_html = ""
    if svcs and str(svcs) not in ("nan", ""):
        tags = [s.strip() for s in str(svcs).split(",") if s.strip()]
        svcs_html = '<div class="card-services">' + "".join(
            f'<span class="service-tag-sm">{esc(t)}</span>' for t in tags[:4]
        ) + ("" if len(tags) <= 4 else f'<span class="service-tag-sm">+{len(tags)-4} more</span>') + "</div>"

    return f"""<div class="venue-card">
  {cat_html}
  <h3 class="card-title"><a href="/listings/{slug}.html">{name}</a></h3>
  {'<p class="card-location">' + location + '</p>' if location else ''}
  {'<div class="card-rating">' + rating_html + '</div>' if rating_html else ''}
  {svcs_html}
  <a href="/listings/{slug}.html" class="btn btn-sm">View Details</a>
</div>"""


# ── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    t0 = time.time()
    print("[1/10] Reading CSV...")
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        raw = list(reader)
    print(f"       {len(raw)} rows loaded")

    # ── normalise & slug ─────────────────────────────────────────────────
    print("[2/10] Normalising data & generating slugs...")
    venues = []
    slug_counter: dict[str, int] = defaultdict(int)
    for r in raw:
        name = (r.get("name") or "").strip()
        city = (r.get("city") or "Unknown").strip()
        state = (r.get("state") or "").strip()
        if not name:
            continue
        abbr = state.upper() if len(state) == 2 else STATE_NAME_TO_ABBR.get(state, state[:2].upper())
        base_slug = slugify(f"{name}-{city}")
        slug_counter[base_slug] += 1
        if slug_counter[base_slug] > 1:
            slug = f"{base_slug}-{slug_counter[base_slug]}"
        else:
            slug = base_slug
        v = dict(r)
        v["state_abbr"] = abbr
        v["state_name"] = state_name_for(abbr)
        v["slug"] = slug
        v["city"] = city
        venues.append(v)
    print(f"       {len(venues)} venues after normalisation")

    # ── indices ──────────────────────────────────────────────────────────
    print("[3/10] Building indices...")
    by_state: dict[str, list] = defaultdict(list)
    by_city: dict[str, list] = defaultdict(list)        # key = "city|state_abbr"
    by_slug: dict[str, dict] = {}
    for v in venues:
        by_state[v["state_abbr"]].append(v)
        ckey = f"{v['city']}|{v['state_abbr']}"
        by_city[ckey].append(v)
        by_slug[v["slug"]] = v

    # city hubs: cities with 3+ venues
    city_hubs: dict[str, list] = {k: vs for k, vs in by_city.items() if len(vs) >= 3}
    city_hub_slugs: dict[str, str] = {}   # "city|state" -> slug
    for ckey in city_hubs:
        city, abbr = ckey.split("|")
        city_hub_slugs[ckey] = f"{slugify(city)}-{abbr.lower()}"

    all_states = sorted(by_state.keys())
    total_cities = len(set(f"{v['city']}|{v['state_abbr']}" for v in venues))
    print(f"       {len(all_states)} states, {total_cities} cities, {len(city_hubs)} city hubs")

    # ── CSS ──────────────────────────────────────────────────────────────
    print("[4/10] Writing CSS & JS...")
    write(os.path.join(OUT_DIR, "styles.css"), CSS_CONTENT)
    write(os.path.join(OUT_DIR, "script.js"), JS_CONTENT)

    # ── HOMEPAGE ─────────────────────────────────────────────────────────
    print("[5/10] Generating homepage...")
    top_cities = sorted(city_hubs.items(), key=lambda kv: len(kv[1]), reverse=True)[:12]
    state_cards = ""
    for abbr in all_states:
        sn = state_name_for(abbr)
        cnt = len(by_state[abbr])
        ss = slugify(sn)
        state_cards += f'<a href="/states/{ss}.html" class="state-card"><h3>{esc(sn)}</h3><span class="count">{cnt} venues</span></a>\n'

    top_city_cards = ""
    for ckey, cvs in top_cities:
        city, abbr = ckey.split("|")
        cs = city_hub_slugs[ckey]
        top_city_cards += f'<a href="/cities/{cs}.html" class="city-hub-card"><h3>{esc(city)}, {abbr}</h3><span class="count">{len(cvs)} venues</span></a>\n'

    featured = sorted([v for v in venues if v.get("rating_value") and str(v["rating_value"]) not in ("nan", "")],
                      key=lambda v: float(v["rating_value"]), reverse=True)[:6]
    featured_html = "".join(venue_card(v) for v in featured)

    home_body = f"""
<section class="hero">
  <h1>Find Sauna Studios &amp; Cold Plunge Near You</h1>
  <p class="hero-sub">The largest directory of sauna, steam room &amp; cold plunge facilities in the US</p>
  <div class="stats-bar">
    <div class="stat"><span class="stat-num">{len(venues):,}</span><span class="stat-label">Businesses</span></div>
    <div class="stat"><span class="stat-num">{total_cities:,}</span><span class="stat-label">Cities</span></div>
    <div class="stat"><span class="stat-num">{len(all_states)}</span><span class="stat-label">States</span></div>
  </div>
</section>

<section id="browse-states" class="section">
  <h2 class="section-title">Browse by State</h2>
  <div class="state-grid">
    {state_cards}
  </div>
</section>

<section class="section">
  <h2 class="section-title">Top Cities</h2>
  <div class="city-grid">
    {top_city_cards}
  </div>
</section>

<section class="section">
  <h2 class="section-title">Featured Locations</h2>
  <div class="venue-grid">
    {featured_html}
  </div>
</section>
"""
    write(os.path.join(OUT_DIR, "index.html"),
          page_shell("SaunaFinder — Find Sauna & Cold Plunge Near You", home_body,
                     description="The largest directory of sauna, steam room and cold plunge facilities in the US.",
                     canonical=BASE_URL + "/"))

    # ── DIRECTORY ────────────────────────────────────────────────────────
    print("[6/10] Generating directory page...")
    sorted_venues = sorted(venues, key=lambda v: v["name"].lower())
    dir_cards = "".join(venue_card(v) for v in sorted_venues)
    dir_body = f"""
<section class="section">
  <h1>Full Directory</h1>
  <p>{len(venues):,} sauna &amp; cold plunge businesses across the US</p>
  <div class="search-box">
    <input type="text" id="directory-search" placeholder="Search by name, city, or state..." autocomplete="off">
  </div>
  <div class="venue-grid" id="directory-grid">
    {dir_cards}
  </div>
</section>
"""
    write(os.path.join(OUT_DIR, "directory.html"),
          page_shell("All Sauna & Cold Plunge Businesses | SaunaFinder", dir_body,
                     description="Browse all sauna and cold plunge businesses in our directory.",
                     canonical=BASE_URL + "/directory.html"))

    # ── STATE PAGES ──────────────────────────────────────────────────────
    print("[7/10] Generating state pages...")
    for abbr in all_states:
        sn = state_name_for(abbr)
        ss = slugify(sn)
        svs = by_state[abbr]
        cities_in_state = defaultdict(list)
        for v in svs:
            cities_in_state[v["city"]].append(v)
        city_count = len(cities_in_state)

        # city hubs in this state
        state_city_hubs = {ckey: vs for ckey, vs in city_hubs.items()
                           if ckey.endswith(f"|{abbr}")}
        hub_section = ""
        if state_city_hubs:
            hub_cards = ""
            for ckey in sorted(state_city_hubs, key=lambda k: len(state_city_hubs[k]), reverse=True):
                city, _ = ckey.split("|")
                cs = city_hub_slugs[ckey]
                hub_cards += f'<a href="/cities/{cs}.html" class="city-hub-card"><h3>{esc(city)}</h3><span class="count">{len(state_city_hubs[ckey])} venues</span></a>\n'
            hub_section = f"""
<div class="section">
  <h2>Popular Cities in {esc(sn)}</h2>
  <div class="city-grid">{hub_cards}</div>
</div>"""

        # group venues by city
        grouped = ""
        for city_name in sorted(cities_in_state.keys()):
            cvs = cities_in_state[city_name]
            ckey = f"{city_name}|{abbr}"
            city_link = ""
            if ckey in city_hub_slugs:
                cs = city_hub_slugs[ckey]
                city_link = f' <a href="/cities/{cs}.html" class="city-hub-link">View all in {esc(city_name)} &rarr;</a>'
            grouped += f'<h3 class="city-subheading">{esc(city_name)} ({len(cvs)}){city_link}</h3>\n'
            grouped += '<div class="venue-grid">\n'
            for v in sorted(cvs, key=lambda x: x["name"].lower()):
                grouped += venue_card(v, show_city=False) + "\n"
            grouped += "</div>\n"

        body = f"""
<nav class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/#browse-states">States</a> &rsaquo; {esc(sn)}</nav>
<h1>Sauna &amp; Cold Plunge in {esc(sn)}</h1>
<div class="stats-bar">
  <div class="stat"><span class="stat-num">{len(svs)}</span><span class="stat-label">Venues</span></div>
  <div class="stat"><span class="stat-num">{city_count}</span><span class="stat-label">Cities</span></div>
</div>
{hub_section}
<section class="section">
  <h2>All Locations in {esc(sn)}</h2>
  {grouped}
</section>
"""
        write(os.path.join(OUT_DIR, "states", f"{ss}.html"),
              page_shell(f"Sauna & Cold Plunge in {sn} | SaunaFinder", body,
                         description=f"Find {len(svs)} sauna and cold plunge businesses in {sn}.",
                         canonical=f"{BASE_URL}/states/{ss}.html"))

    # ── CITY HUB PAGES ───────────────────────────────────────────────────
    print("[8/10] Generating city hub pages...")
    for ckey, cvs in city_hubs.items():
        city, abbr = ckey.split("|")
        sn = state_name_for(abbr)
        cs = city_hub_slugs[ckey]
        ss = slugify(sn)

        sorted_cvs = sorted(cvs,
                            key=lambda v: float(v["rating_value"]) if v.get("rating_value") and str(v["rating_value"]) not in ("nan", "") else 0,
                            reverse=True)
        cards = ""
        for v in sorted_cvs:
            name = esc(v["name"])
            addr = esc(v.get("street_address", ""))
            phone = v.get("phone", "")
            phone_h = format_phone_link(phone) if phone and str(phone) not in ("nan", "") else ""
            rating_h = star_html(str(v.get("rating_value", ""))) if v.get("rating_value") and str(v["rating_value"]) not in ("nan", "") else ""
            svcs_h = services_tags(str(v.get("services", "")))
            review_c = ""
            rc = v.get("review_count", "")
            if rc and str(rc) not in ("nan", ""):
                review_c = f' ({int(float(rc))} reviews)'
            cards += f"""
<div class="venue-card venue-card-detailed">
  <h3 class="card-title"><a href="/listings/{v['slug']}.html">{name}</a></h3>
  {'<p class="card-address">' + addr + '</p>' if addr else ''}
  {'<div class="card-rating">' + rating_h + review_c + '</div>' if rating_h else ''}
  <div class="card-services">{svcs_h}</div>
  <div class="card-meta">
    {phone_h}
  </div>
  <a href="/listings/{v['slug']}.html" class="btn btn-sm">View Details</a>
</div>"""

        # similar nearby: other city hubs in same state
        nearby_hubs = [(k, vs) for k, vs in city_hubs.items()
                       if k.endswith(f"|{abbr}") and k != ckey]
        nearby_hubs.sort(key=lambda kv: len(kv[1]), reverse=True)
        nearby_section = ""
        if nearby_hubs:
            nearby_links = ""
            for nk, nvs in nearby_hubs[:5]:
                nc, na = nk.split("|")
                ns = city_hub_slugs[nk]
                nearby_links += f'<a href="/cities/{ns}.html" class="nearby-link">{esc(nc)} ({len(nvs)} venues)</a>\n'
            nearby_section = f"""
<section class="nearby-section">
  <h2>Similar Nearby</h2>
  <div class="nearby-links">{nearby_links}</div>
</section>"""

        body = f"""
<nav class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/states/{ss}.html">{esc(sn)}</a> &rsaquo; {esc(city)}</nav>
<h1>Sauna &amp; Cold Plunge in {esc(city)}, {esc(sn)}</h1>
<div class="stats-bar">
  <div class="stat"><span class="stat-num">{len(cvs)}</span><span class="stat-label">Venues</span></div>
</div>
<section class="section">
  <div class="venue-grid">
    {cards}
  </div>
</section>
{nearby_section}
"""
        write(os.path.join(OUT_DIR, "cities", f"{cs}.html"),
              page_shell(f"Sauna & Cold Plunge in {city}, {sn} | SaunaFinder", body,
                         description=f"Find {len(cvs)} sauna and cold plunge businesses in {city}, {sn}.",
                         canonical=f"{BASE_URL}/cities/{cs}.html"))

    # ── LISTING PAGES ────────────────────────────────────────────────────
    print("[9/10] Generating listing pages (this may take a moment)...")
    listing_count = 0
    for v in venues:
        listing_count += 1
        name = esc(v["name"])
        city = esc(v["city"])
        abbr = v["state_abbr"]
        sn = state_name_for(abbr)
        ss = slugify(sn)
        slug = v["slug"]

        # breadcrumb city link
        ckey = f"{v['city']}|{abbr}"
        if ckey in city_hub_slugs:
            city_crumb = f'<a href="/cities/{city_hub_slugs[ckey]}.html">{city}</a>'
        else:
            city_crumb = city

        # category & chain badges
        cat = v.get("category", "")
        cat_html = f' <span class="category-badge">{esc(cat)}</span>' if cat and str(cat) not in ("nan", "") else ""
        chain_html = ""
        if str(v.get("is_chain", "")).strip().lower() == "true" and v.get("chain_name") and str(v["chain_name"]) not in ("nan", ""):
            chain_html = f'<span class="chain-badge">Part of {esc(v["chain_name"])}</span>'

        # info grid items
        addr = esc(v.get("street_address", ""))
        postal = esc(v.get("postal_code", ""))
        full_addr = f"{addr}, {city}, {abbr} {postal}".strip(", ")
        phone = v.get("phone", "")
        website = v.get("website", "")
        rating = v.get("rating_value", "")
        review_count = v.get("review_count", "")
        lat = v.get("latitude", "")
        lng = v.get("longitude", "")
        description = v.get("description", "")
        services = v.get("services", "")

        info_items = []
        if full_addr and full_addr not in (",", ""):
            info_items.append(f'<div class="info-item"><span class="info-label">Address</span><span class="info-value">{full_addr}</span></div>')
        if phone and str(phone) not in ("nan", ""):
            info_items.append(f'<div class="info-item"><span class="info-label">Phone</span><span class="info-value">{format_phone_link(phone)}</span></div>')
        if website and str(website) not in ("nan", ""):
            info_items.append(f'<div class="info-item"><span class="info-label">Website</span><span class="info-value">{format_website_link(website)}</span></div>')
        if rating and str(rating) not in ("nan", ""):
            rc_text = ""
            if review_count and str(review_count) not in ("nan", ""):
                rc_text = f" ({int(float(review_count))} reviews)"
            info_items.append(f'<div class="info-item"><span class="info-label">Rating</span><span class="info-value">{star_html(str(rating))}{rc_text}</span></div>')

        info_grid = '<div class="info-grid">' + "\n".join(info_items) + "</div>" if info_items else ""

        # description
        desc_html = ""
        if description and str(description) not in ("nan", ""):
            desc_html = f'<div class="listing-description"><p>{esc(description)}</p></div>'

        # services
        svcs_html = ""
        if services and str(services) not in ("nan", ""):
            svcs_html = f'<div class="listing-services"><h2>Services</h2>{services_tags(str(services))}</div>'

        # map link
        map_html = ""
        if lat and str(lat) not in ("nan", "") and lng and str(lng) not in ("nan", ""):
            map_html = f'<a href="https://www.google.com/maps?q={lat},{lng}" target="_blank" rel="noopener" class="btn map-link">View on Google Maps</a>'

        # similar nearby
        nearby_venues = [x for x in by_city.get(ckey, []) if x["slug"] != slug]
        if len(nearby_venues) < 3:
            state_others = [x for x in by_state.get(abbr, []) if x["slug"] != slug and x["slug"] not in [n["slug"] for n in nearby_venues]]
            nearby_venues.extend(state_others)
        nearby_venues = nearby_venues[:5]
        nearby_html = ""
        if nearby_venues:
            nearby_cards = "".join(venue_card(nv) for nv in nearby_venues)
            nearby_html = f'<section class="nearby-section"><h2>Similar Nearby</h2><div class="venue-grid">{nearby_cards}</div></section>'

        # JSON-LD
        jsonld = build_jsonld(v)

        # claim form
        claim_html = f"""
<div class="claim-section">
  <h2>Own This Business?</h2>
  <p>Claim your listing to update information and respond to reviews</p>
  <form class="claim-form" data-action="{CLAIM_URL}" method="POST">
    <input type="hidden" name="venue_slug" value="{esc(slug)}">
    <input type="hidden" name="venue_name" value="{name}">
    <input type="text" name="owner_name" placeholder="Your Name" required>
    <input type="email" name="email" placeholder="Email Address" required>
    <input type="tel" name="phone" placeholder="Phone Number">
    <textarea name="message" placeholder="Tell us about your business..." rows="3"></textarea>
    <button type="submit" class="btn">Claim This Listing</button>
  </form>
  <div style="margin-top:20px">
    <a href="mailto:hello@saunafinder.com?subject=Upgrade to Featured: {name}" class="btn btn-secondary">Upgrade to Featured - $29/mo</a>
  </div>
</div>
"""

        body = f"""
<nav class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/states/{ss}.html">{esc(sn)}</a> &rsaquo; {city_crumb} &rsaquo; {name}</nav>
<div class="listing-header">
  <h1>{name}{cat_html}</h1>
  {chain_html}
</div>
{info_grid}
{desc_html}
{svcs_html}
{map_html}
{nearby_html}
{claim_html}
<p class="back-link"><a href="/directory.html">&larr; Back to Directory</a></p>
"""
        write(os.path.join(OUT_DIR, "listings", f"{slug}.html"),
              page_shell(f"{v['name']} — Sauna & Cold Plunge | SaunaFinder", body,
                         description=f"{v['name']} in {v['city']}, {sn}. Find hours, services, ratings and more.",
                         canonical=f"{BASE_URL}/listings/{slug}.html",
                         extra_head=f'<script type="application/ld+json">{jsonld}</script>'))

        if listing_count % 500 == 0:
            print(f"       ... {listing_count} listings generated")

    print(f"       {listing_count} listing pages generated")

    # ── SITEMAP & ROBOTS ─────────────────────────────────────────────────
    print("[10/10] Generating sitemap.xml & robots.txt...")
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    sm_entries = []
    sm_entries.append(sm_url(BASE_URL + "/", today, "1.0", "weekly"))
    sm_entries.append(sm_url(BASE_URL + "/directory.html", today, "0.6", "weekly"))
    for abbr in all_states:
        ss = slugify(state_name_for(abbr))
        sm_entries.append(sm_url(f"{BASE_URL}/states/{ss}.html", today, "0.8", "weekly"))
    for ckey in city_hubs:
        cs = city_hub_slugs[ckey]
        sm_entries.append(sm_url(f"{BASE_URL}/cities/{cs}.html", today, "0.7", "weekly"))
    for v in venues:
        sm_entries.append(sm_url(f"{BASE_URL}/listings/{v['slug']}.html", today, "0.5", "monthly"))

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "\n".join(sm_entries)
    sitemap += "\n</urlset>\n"
    write(os.path.join(OUT_DIR, "sitemap.xml"), sitemap)

    robots = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
"""
    write(os.path.join(OUT_DIR, "robots.txt"), robots)

    # ── summary ──────────────────────────────────────────────────────────
    elapsed = time.time() - t0
    print(f"\n{'='*60}")
    print(f"  SaunaFinder v2 build complete in {elapsed:.1f}s")
    print(f"{'='*60}")
    file_counts = count_files(OUT_DIR)
    total_size = 0
    for ext, (cnt, sz) in sorted(file_counts.items()):
        total_size += sz
        print(f"  {ext:12s}: {cnt:>6,} files  ({sz/1024/1024:.1f} MB)")
    print(f"  {'TOTAL':12s}: {sum(c for c,s in file_counts.values()):>6,} files  ({total_size/1024/1024:.1f} MB)")
    print(f"{'='*60}")


def sm_url(loc: str, lastmod: str, priority: str, freq: str) -> str:
    return f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>"""


def build_jsonld(v: dict) -> str:
    import json as _json
    ld = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": v["name"],
    }
    addr_parts = {}
    if v.get("street_address") and str(v["street_address"]) not in ("nan", ""):
        addr_parts["streetAddress"] = v["street_address"]
    if v.get("city"):
        addr_parts["addressLocality"] = v["city"]
    if v.get("state_abbr"):
        addr_parts["addressRegion"] = v["state_abbr"]
    if v.get("postal_code") and str(v["postal_code"]) not in ("nan", ""):
        addr_parts["postalCode"] = str(v["postal_code"])
    addr_parts["addressCountry"] = "US"
    if addr_parts:
        ld["address"] = {"@type": "PostalAddress", **addr_parts}
    if v.get("phone") and str(v["phone"]) not in ("nan", ""):
        ld["telephone"] = v["phone"]
    if v.get("website") and str(v["website"]) not in ("nan", ""):
        ld["url"] = v["website"]
    if v.get("latitude") and str(v["latitude"]) not in ("nan", "") and v.get("longitude") and str(v["longitude"]) not in ("nan", ""):
        ld["geo"] = {
            "@type": "GeoCoordinates",
            "latitude": float(v["latitude"]),
            "longitude": float(v["longitude"]),
        }
    if v.get("rating_value") and str(v["rating_value"]) not in ("nan", ""):
        agg = {"@type": "AggregateRating", "ratingValue": float(v["rating_value"])}
        if v.get("review_count") and str(v["review_count"]) not in ("nan", ""):
            agg["reviewCount"] = int(float(v["review_count"]))
        ld["aggregateRating"] = agg
    if v.get("description") and str(v["description"]) not in ("nan", ""):
        ld["description"] = v["description"]
    return _json.dumps(ld, ensure_ascii=False)


def count_files(root: str) -> dict:
    """Return {ext: (count, total_bytes)} dict."""
    counts: dict[str, list] = defaultdict(lambda: [0, 0])
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            ext = os.path.splitext(fn)[1] or "(no ext)"
            fp = os.path.join(dirpath, fn)
            sz = os.path.getsize(fp)
            counts[ext][0] += 1
            counts[ext][1] += sz
    return counts


# ── STATIC ASSETS ────────────────────────────────────────────────────────────
CSS_CONTENT = r"""
/* SaunaFinder v2 — Dark Theme */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f0f0f;--card:#1a1a1a;--border:#333;
  --accent:#00d4ff;--gold:#ffd700;--text:#e0e0e0;--muted:#888;
  --font:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  --radius:8px;
}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font-family:var(--font);line-height:1.6;min-height:100vh}
a{color:var(--accent);text-decoration:none;transition:color .2s}
a:hover{color:#fff}
.container{max-width:1200px;margin:0 auto;padding:0 20px}

/* Header */
.site-header{background:#111;border-bottom:1px solid var(--border);padding:16px 0;position:sticky;top:0;z-index:100}
.header-inner{display:flex;align-items:center;justify-content:space-between}
.logo{font-size:1.5rem;font-weight:700;color:#fff}
.logo .accent{color:var(--accent)}
.main-nav a{margin-left:24px;color:var(--muted);font-size:.95rem}
.main-nav a:hover{color:#fff}
.mobile-toggle{display:none;background:none;border:none;color:#fff;font-size:1.5rem;cursor:pointer}

/* Hero */
.hero{text-align:center;padding:60px 0 40px}
.hero h1{font-size:2.4rem;color:#fff;margin-bottom:12px}
.hero-sub{color:var(--muted);font-size:1.1rem;margin-bottom:30px}

/* Stats */
.stats-bar{display:flex;justify-content:center;gap:40px;margin:24px 0}
.stat{text-align:center}
.stat-num{display:block;font-size:2rem;font-weight:700;color:var(--accent)}
.stat-label{font-size:.85rem;color:var(--muted);text-transform:uppercase;letter-spacing:1px}

/* Sections */
.section{padding:40px 0}
.section-title{font-size:1.6rem;color:#fff;margin-bottom:24px}

/* Grids */
.venue-grid,.state-grid,.city-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}
.state-grid{grid-template-columns:repeat(auto-fill,minmax(200px,1fr))}
.city-grid{grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}

/* Cards */
.venue-card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px;transition:transform .2s,border-color .2s,box-shadow .2s;display:flex;flex-direction:column;gap:8px}
.venue-card:hover{border-color:var(--accent);transform:translateY(-4px);box-shadow:0 8px 24px rgba(0,212,255,.1)}
.venue-card-detailed{gap:10px}
.card-title{font-size:1.1rem}
.card-title a{color:#fff}
.card-title a:hover{color:var(--accent)}
.card-location{color:var(--muted);font-size:.9rem}
.card-address{color:var(--muted);font-size:.9rem}
.card-rating{font-size:.9rem}
.card-services{display:flex;flex-wrap:wrap;gap:6px}
.card-meta{font-size:.9rem;color:var(--muted)}

/* State / city cards */
.state-card,.city-hub-card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px;text-align:center;transition:transform .2s,border-color .2s,box-shadow .2s}
.state-card:hover,.city-hub-card:hover{border-color:var(--accent);transform:translateY(-4px);box-shadow:0 8px 24px rgba(0,212,255,.1)}
.state-card h3,.city-hub-card h3{color:#fff;font-size:1rem;margin-bottom:6px}
.state-card .count,.city-hub-card .count{color:var(--muted);font-size:.85rem}

/* Buttons */
.btn{display:inline-block;background:var(--accent);color:#000;font-weight:600;padding:10px 20px;border-radius:var(--radius);border:none;cursor:pointer;font-size:.95rem;transition:background .2s,transform .1s;text-align:center}
.btn:hover{background:#00b8d9;color:#000;transform:translateY(-1px)}
.btn-sm{padding:8px 16px;font-size:.85rem}
.btn-secondary{background:transparent;border:1px solid var(--accent);color:var(--accent)}
.btn-secondary:hover{background:var(--accent);color:#000}

/* Stars */
.stars{color:var(--gold);font-size:1rem}
.star.empty{color:#555}
.star.half{opacity:.6}
.rating-num{color:var(--muted);font-size:.85rem;margin-left:4px}
.review-count{color:var(--muted);font-size:.85rem}

/* Badges */
.category-badge{background:rgba(0,212,255,.15);color:var(--accent);padding:3px 10px;border-radius:20px;font-size:.75rem;font-weight:600;text-transform:uppercase;letter-spacing:.5px}
.chain-badge{background:#ff6b35;color:#fff;padding:4px 12px;border-radius:20px;font-size:.8rem;font-weight:600;display:inline-block;margin-bottom:12px}
.featured-badge{background:var(--gold);color:#111;padding:4px 12px;border-radius:20px;font-size:.8rem;font-weight:600}

/* Service tags */
.service-tag{display:inline-block;background:rgba(0,212,255,.1);color:var(--accent);border:1px solid rgba(0,212,255,.2);padding:6px 14px;border-radius:20px;font-size:.85rem;margin:4px}
.service-tag-sm{display:inline-block;background:rgba(0,212,255,.08);color:var(--accent);padding:3px 8px;border-radius:12px;font-size:.75rem}

/* Breadcrumb */
.breadcrumb{padding:16px 0;font-size:.9rem;color:var(--muted)}
.breadcrumb a{color:var(--muted)}
.breadcrumb a:hover{color:var(--accent)}

/* Listing detail */
.listing-header{margin-bottom:24px}
.listing-header h1{font-size:1.8rem;color:#fff;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.info-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px;margin-bottom:24px}
.info-item{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:16px}
.info-label{display:block;color:var(--muted);font-size:.8rem;text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px}
.info-value{color:#fff;font-size:.95rem}
.listing-description{margin-bottom:24px;padding:20px;background:var(--card);border-radius:var(--radius);border:1px solid var(--border)}
.listing-services{margin-bottom:24px}
.listing-services h2{font-size:1.2rem;color:#fff;margin-bottom:12px}
.map-link{margin-bottom:24px}

/* Nearby */
.nearby-section{margin:32px 0}
.nearby-section h2{font-size:1.3rem;color:#fff;margin-bottom:16px}
.nearby-links{display:flex;flex-wrap:wrap;gap:12px}
.nearby-link{display:inline-block;background:var(--card);border:1px solid var(--border);padding:10px 18px;border-radius:var(--radius);color:var(--muted);font-size:.9rem}
.nearby-link:hover{border-color:var(--accent);color:#fff}

/* Claim section */
.claim-section{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:32px;margin:32px 0}
.claim-section h2{color:#fff;margin-bottom:8px}
.claim-section p{color:var(--muted);margin-bottom:20px}
.claim-form input,.claim-form textarea{background:var(--bg);border:1px solid var(--border);color:#fff;padding:12px;border-radius:6px;width:100%;margin-bottom:12px;font-family:var(--font);font-size:.95rem}
.claim-form input::placeholder,.claim-form textarea::placeholder{color:#666}
.claim-form input:focus,.claim-form textarea:focus{outline:none;border-color:var(--accent)}
.claim-form button{width:100%}

/* Search */
.search-box{margin-bottom:24px}
.search-box input{width:100%;background:var(--card);border:1px solid var(--border);color:#fff;padding:14px 20px;border-radius:var(--radius);font-size:1rem;font-family:var(--font)}
.search-box input:focus{outline:none;border-color:var(--accent)}

/* City subheading */
.city-subheading{font-size:1.2rem;color:#fff;margin:28px 0 12px;padding-bottom:8px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.city-hub-link{font-size:.85rem;color:var(--accent);font-weight:400}

/* Back link */
.back-link{margin:24px 0;font-size:.9rem}

/* Phone / website */
.phone-link,.website-link{color:var(--accent)}

/* Footer */
.site-footer{border-top:1px solid var(--border);padding:32px 0;text-align:center;color:var(--muted);font-size:.9rem;margin-top:40px}
.site-footer p{margin-bottom:8px}

/* Success / error messages */
.form-msg{padding:12px;border-radius:var(--radius);margin-top:12px;font-size:.9rem}
.form-msg.success{background:rgba(0,255,100,.1);color:#0f8}
.form-msg.error{background:rgba(255,50,50,.1);color:#f55}

/* Responsive */
@media(max-width:768px){
  .hero h1{font-size:1.6rem}
  .stats-bar{gap:20px}
  .stat-num{font-size:1.4rem}
  .main-nav{display:none;position:absolute;top:100%;left:0;right:0;background:#111;padding:20px;flex-direction:column;border-bottom:1px solid var(--border)}
  .main-nav.open{display:flex}
  .main-nav a{margin:8px 0;margin-left:0}
  .mobile-toggle{display:block}
  .venue-grid,.state-grid,.city-grid{grid-template-columns:1fr}
  .info-grid{grid-template-columns:1fr}
  .listing-header h1{font-size:1.4rem}
}
"""

JS_CONTENT = r"""
// SaunaFinder v2 — Client-side scripts

// Mobile nav toggle
document.addEventListener('DOMContentLoaded', function() {
  var toggle = document.querySelector('.mobile-toggle');
  var nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function() {
      nav.classList.toggle('open');
    });
  }

  // Directory search filter
  var searchInput = document.getElementById('directory-search');
  if (searchInput) {
    var grid = document.getElementById('directory-grid');
    var cards = grid ? Array.from(grid.querySelectorAll('.venue-card')) : [];
    searchInput.addEventListener('input', function() {
      var q = this.value.toLowerCase().trim();
      var count = 0;
      cards.forEach(function(card) {
        var text = card.textContent.toLowerCase();
        if (!q || text.indexOf(q) !== -1) {
          card.style.display = '';
          count++;
        } else {
          card.style.display = 'none';
        }
      });
    });
  }

  // Claim form handler
  var forms = document.querySelectorAll('.claim-form');
  forms.forEach(function(form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      var url = form.getAttribute('data-action');
      var data = new FormData(form);
      var obj = {};
      data.forEach(function(v, k) { obj[k] = v; });
      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true;
      btn.textContent = 'Submitting...';

      // Remove old messages
      var old = form.parentNode.querySelector('.form-msg');
      if (old) old.remove();

      fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(obj)
      }).then(function(res) {
        if (res.ok) return res.json();
        throw new Error('Request failed');
      }).then(function() {
        var msg = document.createElement('div');
        msg.className = 'form-msg success';
        msg.textContent = 'Claim submitted! We will review and get back to you within 24-48 hours.';
        form.parentNode.insertBefore(msg, form.nextSibling);
        form.reset();
        btn.disabled = false;
        btn.textContent = 'Claim This Listing';
      }).catch(function() {
        var msg = document.createElement('div');
        msg.className = 'form-msg error';
        msg.textContent = 'Something went wrong. Please email hello@saunafinder.com instead.';
        form.parentNode.insertBefore(msg, form.nextSibling);
        btn.disabled = false;
        btn.textContent = 'Claim This Listing';
      });
    });
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(function(a) {
    a.addEventListener('click', function(e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
});
"""

if __name__ == "__main__":
    main()
