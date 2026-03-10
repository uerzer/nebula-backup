---
name: saunafinder-project
description: SaunaFinder project context, scraping targets, and Supabase schema conventions. Use when working on SaunaFinder development, scraping plungesaunafinder.com, building venue databases, or designing Supabase schemas.
created_at: 2026-03-08T14:34:05.078935+00:00
updated_at: 2026-03-08T14:34:05.078935+00:00
---

# SaunaFinder Project

## Overview
SaunaFinder is a venue discovery project targeting plungesaunafinder.com as the primary scraping source.
The goal is to extract sauna/plunge venue data and build a structured, queryable database.

## Scraping Target
- Primary source: https://www.plungesaunafinder.com
- Extract: venue names, addresses, coordinates, amenities, pricing, hours, contact info, photos
- Handle pagination, dynamic content (JS-rendered), and rate limits gracefully
- Use rotating user agents and respectful crawl delays (1-2s between requests)

## Data Pipeline
1. Scrape raw HTML/JSON from source
2. Parse and normalize venue fields
3. Deduplicate by name + address or coordinates
4. Upsert into Supabase

## Supabase Schema Conventions
- Table: `venues`
  - id: uuid (primary key, gen_random_uuid())
  - name: text NOT NULL
  - address: text
  - city: text
  - state: text
  - zip: text
  - country: text DEFAULT 'US'
  - lat: float8
  - lng: float8
  - phone: text
  - website: text
  - hours: jsonb
  - amenities: text[]
  - price_range: text (e.g. '$', '$$', '$$$')
  - image_urls: text[]
  - source_url: text
  - created_at: timestamptz DEFAULT now()
  - updated_at: timestamptz DEFAULT now()

- Table: `scrape_runs`
  - id: uuid
  - started_at: timestamptz
  - completed_at: timestamptz
  - venues_found: int
  - venues_added: int
  - venues_updated: int
  - errors: jsonb
  - status: text ('running', 'completed', 'failed')

## GitHub Workflow
- Repo: push scraper scripts, schema migrations, and pipeline code to GitHub
- Use descriptive commit messages: "feat: add venue scraper for plungesaunafinder"
- Store scripts under /scrapers, schemas under /supabase/migrations

## Supabase Access
- Use the Supabase REST API (PostgREST) for upserts and queries
- Prefer upsert with on_conflict=name,city to avoid duplicates
- Use RLS policies: service_role key for pipeline writes, anon key for reads
