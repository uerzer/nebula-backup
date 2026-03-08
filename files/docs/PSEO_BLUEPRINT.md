# Pieter Levels pSEO Blueprint
## The Complete Programmatic SEO Playbook

> Reverse-engineered from nomads.com, remoteok.com, photoai.com, interiorai.com, hoodmaps.com

---

## The Core Philosophy

Pieter Levels never writes content. He builds systems that generate content at scale.

The fundamental insight: **search demand exists in patterns**. Every city has the same questions. Every job title has the same tool needs. Every room has the same style options. If you can map the pattern, you can own the pattern -- at scale, automatically, before anyone else does.

One template + one dataset = thousands of pages.
One dataset + two dimensions = tens of thousands of pages.
Add UGC = millions of pages.

---

## The 3 Core Patterns

### Pattern 1: The Combinatorial Multiplier

**Formula:** Dimension A x Dimension B = Total Pages

**Examples from Levels:**
- remoteok.com: `[tag] x [tag]` = `/remote-python+backend-jobs` (39k+ pages)
- interiorai.com: `[room] x [style]` = `/interior-design/living-room-with-scandinavian` (550k+ pages)
- nomads.com: `[city] x [intent]` = `/berlin/cost` `/berlin/coworking` (130k+ pages)

**How to apply:**
1. Find your two strongest dimensions (tool x use-case, job x tool, location x problem)
2. Build a clean dataset for each dimension (even 50 x 50 = 2,500 pages)
3. Write ONE template that works for every combination
4. Generate all URLs programmatically
5. Ensure each page has enough unique data to avoid thin content penalties

**Minimum viable dimensions:** 20 x 20 = 400 pages (worth doing)
**Sweet spot:** 100 x 100 = 10,000 pages
**Scale ceiling:** 500 x 500 = 250,000 pages

---

### Pattern 2: The Taxonomy Cluster

**Formula:** Map every demand cluster in your niche → one page per cluster

**Examples from Levels:**
- photoai.com: profession x aesthetic x app x occasion (~160 curated hubs)
- Each hub cross-links to all related hubs in the footer

**How to apply:**
1. Do keyword research across your entire niche
2. Group keywords into demand clusters (all "copywriter AI tools" queries = one cluster)
3. Build one page per cluster with a locked template
4. Add cross-links between related clusters
5. ~100-200 pages covers most niches completely

**When to use this vs. Combinatorial:**
- Use Taxonomy when dimensions don't cleanly multiply
- Use Combinatorial when you have two independent, orthogonal dimensions
- Use both together for maximum coverage

---

### Pattern 3: UGC as the Scale Layer

**Formula:** User actions auto-publish as indexed pages

**Examples from Levels:**
- interiorai.com: every render → `/interior-design/[room]-with-[style]-[id]`
- photoai.com: every photo → `/photos/[prompt-slug]-[id]`
- hoodmaps.com: every city map → `/{city}-neighborhood-map`

**How to apply:**
1. Design your product so user outputs are naturally shareable
2. Auto-publish every user output as a unique URL
3. Generate a title/meta description from the user's inputs
4. Add canonical tags to prevent duplicate content issues
5. Let Google index them -- the long-tail volume is massive

**This is the ceiling-breaker.** Curated pages top out at ~10k. UGC pages scale to millions with zero marginal effort once the product has users.

---

## The URL Architecture

### Levels' URL Patterns (Decoded)

```
nomads.com/{city}                          → city hub (130k cities)
nomads.com/{city}/cost                     → intent sub-page
nomads.com/{city}/coworking               → intent sub-page
nomads.com/{city}/compare/{city2}         → comparison page
nomads.com/{city}/near                    → proximity page

remoteok.com/remote-jobs                  → root
remoteok.com/remote-{tag}-jobs            → single tag
remoteok.com/remote-{tag1}+{tag2}-jobs   → tag combo

photoai.com/{use-case-slug}               → taxonomy hub
photoai.com/photos/{prompt}-{id}          → UGC page

interiorai.com/interior-design/{room}-with-{style}      → combo hub
interiorai.com/interior-design/{room}-with-{style}-{id} → UGC render
```

### URL Design Rules
1. **Keywords in slug** -- always. `/remote-python-jobs` not `/jobs/123`
2. **Flat over nested** -- max 2 levels deep for indexability
3. **Hyphens not underscores**
4. **No pagination in URL** -- use infinite scroll or load more
5. **Canonical tags** on all UGC to point to the parent template

---

## The Template Architecture

### What Every Levels Page Has

1. **H1** = primary keyword (exact match or close variant)
2. **Data block** = the unique data for this combination (salary ranges, tool list, cost of living, design renders)
3. **Related pages block** = internal links to 6-12 related combinations
4. **CTA** = product action (generate, search, browse)
5. **Meta title** = `[Keyword] | [Site Name]`
6. **Meta description** = templated, data-injected

### Template Formula
```
H1: [Keyword Phrase]
Subhead: [One sentence with secondary keyword]

[Data Table or Visual -- the unique value]

[2-3 paragraphs of templated copy with data injected]

[Related: links to 8 similar pages]

[CTA: primary product action]
```

### The Thin Content Trap (How Levels Avoids It)
- Every page has REAL data (not just text)
- Data is specific to the combination (costs for Berlin ≠ costs for Lisbon)
- User-generated renders make every UGC page visually unique
- Internal linking distributes authority across all pages
- Pages answer a SPECIFIC query, not a generic one

---

## The Data Strategy

### Where Levels Gets His Data
- **nomads.com**: crowdsourced cost data + user reports
- **remoteok.com**: job board data (real listings = real data)
- **interiorai.com**: AI-generated renders (the product IS the data)
- **photoai.com**: user-generated photos
- **hoodmaps.com**: crowdsourced neighborhood ratings

### Data Source Options (Ranked by Quality)
1. **Your product output** (best -- unique, can't be copied)
2. **Public APIs** (government data, job boards, property APIs)
3. **Scraped/aggregated** (viable, legal grey area -- check ToS)
4. **AI-generated** (risky for pure text, fine for structured data)
5. **Crowdsourced** (slow to start, powerful at scale)

### Minimum Data Requirements
- At least 3-5 unique data points per page
- Data must differ meaningfully between pages
- Structured data markup (schema.org) for all data tables

---

## The Launch Sequence

### Phase 1: Foundation (Week 1-2)
- [ ] Define your two primary dimensions
- [ ] Build dataset for both dimensions (even a spreadsheet works)
- [ ] Write the master template (one page, manually)
- [ ] Test: does this page rank for the target keyword?
- [ ] If yes, proceed to generation

### Phase 2: Generation (Week 3-4)
- [ ] Build the page generator (Python/JS script or no-code tool)
- [ ] Generate top 100 combinations first (highest volume keywords)
- [ ] Submit sitemap to Google Search Console
- [ ] Set up internal linking between all generated pages
- [ ] Monitor for indexing in GSC

### Phase 3: Scale (Month 2-3)
- [ ] Generate remaining combinations
- [ ] Add second template variant (comparison pages, near pages)
- [ ] Begin UGC layer if product has users
- [ ] Build backlinks to top 10 hub pages (not to all pages -- hub authority flows down)

### Phase 4: Compound (Month 3+)
- [ ] Identify which combinations are ranking -- double down
- [ ] Add new dimensions (expand the matrix)
- [ ] Add new data sources (richer pages = better rankings)
- [ ] Launch adjacent pSEO cluster for related niche

---

## The Tools Stack

### For Building
- **Next.js / Astro** -- static site generation, perfect for pSEO at scale
- **Supabase / PlanetScale** -- database for your dimensions and data
- **Vercel** -- deployment, handles 100k+ pages fine

### For Data
- **Apify** -- scraping at scale
- **OpenAI API** -- structured data generation
- **Public datasets** -- data.gov, Kaggle, government APIs

### For Monitoring
- **Google Search Console** -- indexing and ranking data
- **Ahrefs / Semrush** -- keyword gap analysis
- **Screaming Frog** -- crawl your own site for issues

---

## Decision Tree: Which Pattern to Use

```
Do you have two independent dimensions that both have search demand?
├── YES → Use Combinatorial Multiplier
│   └── Are your dimensions geographic?
│       ├── YES → nomads pattern (city x intent)
│       └── NO → remoteok pattern (tag x tag) or interiorai pattern (noun x adjective)
└── NO → Use Taxonomy Cluster
    └── Does your product generate user outputs?
        ├── YES → Add UGC layer on top
        └── NO → Stay with curated taxonomy, plan for UGC later
```

---

## Red Flags (What Kills pSEO Sites)

1. **Thin content** -- pages with no real data get deindexed fast
2. **Duplicate content** -- templated text that's 95% identical across pages
3. **No internal linking** -- isolated pages don't accumulate authority
4. **Wrong dimensions** -- picking dimensions with no search demand
5. **Ignoring GSC** -- not monitoring which pages actually get indexed
6. **Launching all at once** -- Google needs time to crawl; drip-feed pages

---

## KPIs to Track

| Metric | Tool | Target (Month 3) |
|---|---|---|
| Pages indexed | GSC | >50% of generated pages |
| Organic impressions | GSC | 10k+/month |
| Click-through rate | GSC | >2% |
| Pages ranking top 10 | Ahrefs | 50+ |
| Organic traffic | Analytics | 1k+/month |

---

*Blueprint version 1.0 -- based on Pieter Levels site analysis, March 2026*
