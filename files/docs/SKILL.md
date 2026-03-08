# Skill: Programmatic SEO (Pieter Levels Method)

## What This Skill Does
Equips any agent to plan, build, and scale a programmatic SEO site using the patterns reverse-engineered from Pieter Levels' portfolio (nomads.com, remoteok.com, photoai.com, interiorai.com, hoodmaps.com).

An agent with this skill can:
- Analyze any niche for pSEO opportunity
- Define the optimal dimension pair for combinatorial scaling
- Design the full URL architecture
- Generate page templates
- Build the data schema
- Write the page generator script
- Monitor and iterate based on GSC data

---

## Core Methodology

### The One Formula
```
One template + one dataset = thousands of pages
One dataset + two dimensions = tens of thousands of pages
Add UGC = millions of pages
```

### The 3 Patterns

**Pattern 1: Combinatorial Multiplier**
- Pick Dimension A (e.g. tools) and Dimension B (e.g. use cases)
- Cross them: A x B = total pages
- URL: `/{dim-a-slug}/{dim-b-slug}` or `/{dim-a}/for/{dim-b}`
- Use when: two independent dimensions both have search demand
- Example: 500 tools x 100 use cases = 50,000 pages

**Pattern 2: Taxonomy Cluster**
- Map every demand cluster in niche
- One hub page per cluster
- URL: `/{category}/{cluster-slug}`
- Use when: dimensions don't cleanly multiply, or for top-of-funnel hubs
- Example: `/for/freelance-writers`, `/for/solopreneurs`

**Pattern 3: UGC Scale Layer**
- User actions auto-publish as indexed pages
- URL: `/{category}/{user-input-slug}-{id}`
- Use when: product generates user outputs (renders, reports, results)
- Example: every AI photo render → a new indexed page

---

## Agent Workflow

### Task: Analyze a niche for pSEO opportunity
1. Search for top 20 keywords in the niche
2. Identify repeating patterns in keyword structure (what changes between keywords?)
3. The changing part = your dimensions
4. Estimate volume: count unique values in each dimension, multiply
5. Check competition: are there existing pSEO sites? How many pages do they have?
6. Verdict: viable if >10,000 potential pages and no dominant player above 100k pages

### Task: Design URL architecture for a site
1. Define Dimension A (the noun -- tool, city, job, room)
2. Define Dimension B (the modifier -- use case, intent, style, tag)
3. Design URL structure:
   - Tier 1 hubs: `/{dim-a-slug}` (one per Dimension A value)
   - Tier 2 hubs: `/for/{dim-b-slug}` (one per Dimension B value)
   - Tier 3 combos: `/{dim-a-slug}/for/{dim-b-slug}` (A x B combinations)
   - Tier 4 comparisons: `/compare/{slug1}-vs-{slug2}` (optional)
4. Ensure all URLs are keyword-rich, flat (max 2 levels), hyphenated

### Task: Write a page template
1. H1: `[Dimension A] for [Dimension B]: [Benefit]`
2. Intro paragraph: what this combination means, who it's for (2-3 sentences, data-injected)
3. Data block: the unique value -- table, list, or visual with data specific to this combo
4. Body: 3-5 paragraphs with templated structure, variables injected from dataset
5. Related section: 6-8 internal links to similar combinations
6. CTA: primary product action (subscribe, generate, search, browse)
7. Meta title: `[Keyword] | [Site Name]` (max 60 chars)
8. Meta description: `[Benefit] for [Dimension B]. [Data point]. [CTA].` (max 155 chars)

### Task: Build the data schema
```json
{
  "dimension_a": {
    "slug": "string (url-safe)",
    "name": "string (display)",
    "category": "string",
    "description": "string",
    "data_fields": ["field1", "field2"],
    "related": ["slug1", "slug2"]
  },
  "dimension_b": {
    "slug": "string (url-safe)",
    "name": "string (display)",
    "description": "string",
    "top_dimension_a": ["slug1", "slug2"],
    "related": ["slug1", "slug2"]
  }
}
```

### Task: Generate pages (Astro + Supabase)
```javascript
// getStaticPaths for combination pages
export async function getStaticPaths() {
  const { data: tools } = await supabase.from('tools').select('*')
  const { data: usecases } = await supabase.from('usecases').select('*')

  return tools.flatMap(tool =>
    usecases.map(usecase => ({
      params: { tool: tool.slug, usecase: usecase.slug },
      props: { tool, usecase }
    }))
  )
}
```

### Task: Submit and monitor
1. Generate sitemap.xml with all URLs
2. Submit to Google Search Console
3. After 2 weeks: check Coverage report -- how many pages indexed?
4. Check Performance report -- which pages have impressions?
5. Double down on pages with impressions, investigate pages with zero

---

## Decision Rules

### Which pattern to use
- Two independent dimensions with search demand → **Combinatorial**
- One dimension with many sub-types → **Taxonomy**
- Product generates user outputs → **UGC layer** (add on top of either)
- All three available → **Stack them** (taxonomy hubs + combinatorial matrix + UGC)

### When to launch
- Minimum: 50 Dimension A values + 20 Dimension B values = 1,000 combo pages
- Better: 100 x 50 = 5,000 pages
- Don't wait for perfect data -- launch with 80% complete, fill gaps after

### When to scale
- Any page hitting top 20 in GSC → expand that cluster
- CTR below 1% → fix meta titles/descriptions
- Pages not indexed after 4 weeks → check thin content, add more data
- Traffic plateau → add new dimension or new data source

---

## Quality Checklist (Run Before Publishing)

- [ ] Every page has at least 5 unique data points specific to its combination
- [ ] H1 contains the primary keyword
- [ ] Meta title is under 60 characters and contains keyword
- [ ] Meta description is under 155 characters and has a CTA
- [ ] Every page links to at least 6 related pages
- [ ] No two pages have identical body text (templates must inject unique data)
- [ ] Canonical tags set correctly on all UGC pages
- [ ] Sitemap includes all generated pages
- [ ] robots.txt is not blocking any pSEO pages
- [ ] Schema markup (ItemList or FAQPage) added to hub pages

---

## Red Flags (Stop and Fix)

- Pages getting deindexed → thin content, add more data immediately
- Manual action in GSC → remove affected pages, fix template, resubmit
- Crawl budget warnings → reduce crawl depth, consolidate thin pages
- Duplicate content warnings → check canonical tags, ensure data variability
- Traffic spike then crash → Google algo update, check for thin content at scale

---

## Reference Files
- Full methodology: `docs/PSEO_BLUEPRINT.md`
- Site-specific strategy: `docs/PSEO_NEWSLETTER_STRATEGY.md`
- Data schemas and templates: see strategy doc

---

## Quick Start Prompt (for any agent)

> "You have the pSEO skill loaded. The site is [SITE URL or DESCRIPTION]. The niche is [NICHE]. 
> Your task: analyze the niche, propose the two primary dimensions, design the URL architecture, 
> write one sample page template, and output the data schema as JSON. 
> Reference PSEO_BLUEPRINT.md for methodology and PSEO_NEWSLETTER_STRATEGY.md for a worked example."

---

*Skill version 1.0 -- March 2026*
*Based on: nomads.com, remoteok.com, photoai.com, interiorai.com, hoodmaps.com*
