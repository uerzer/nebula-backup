# NexusAI — 14-Day Launch Execution Plan
## Dental Practice AI Agency | Cold Outreach Campaign

**Start Date:** ________ (fill in when you begin)
**Domain Warm Deadline:** Start date + 14 days
**First Send Date:** Start date + 14 days
**Target:** 1-3 paying clients at $1,500-$3,000/mo within 45 days

---

## PHASE 1: INFRASTRUCTURE (Days 1-3)

### Day 1 — Domain & Email Setup
- [ ] Buy cold email domain (e.g., `trynexusai.com` or `nexusai-solutions.com`)
  - Namecheap, Cloudflare, or Google Domains — ~$12/year
  - DO NOT use your primary domain for cold email
- [ ] Set up email on the domain (Google Workspace $6/mo or Zoho free)
  - Create: alex@trynexusai.com (or your chosen sender name)
- [ ] Configure DNS records:
  - [ ] SPF record: `v=spf1 include:_spf.google.com ~all`
  - [ ] DKIM: Follow provider's guide to generate and add TXT record
  - [ ] DMARC: `v=DMARC1; p=none; rua=mailto:dmarc@trynexusai.com`
- [ ] Sign up for email warmup service:
  - Instantly.ai (free tier: 1 account, 200 warmup emails/day) OR
  - Smartlead ($39/mo but better deliverability tracking)
- [ ] Start warmup — this runs for 14 days automatically
- [ ] Verify warmup is active (check dashboard shows emails sending/receiving)

### Day 2 — Booking & Landing Page
- [ ] Create Calendly or Cal.com booking page
  - Title: "NexusAI — 15-Min Discovery Call"
  - Duration: 15 minutes
  - Availability: Tue-Thu, 9am-4pm (your timezone)
  - Confirmation email: enabled
  - Reminder: 1 hour before
- [ ] Update calendar link in email personalizer: `--calendar YOUR_LINK`
- [ ] Deploy landing page to GitHub Pages (DONE — see URL below)
  - Or buy a domain and point it at the GitHub Pages site
- [ ] Update landing page with:
  - [ ] Real booking link (replace #book hrefs)
  - [ ] Real email address (replace hello@nexusai.example.com)
  - [ ] Real phone number or remove it
  - [ ] Your city/state in schema markup

### Day 3 — Lead Generation
- [ ] Get Google Places API key:
  - Go to console.cloud.google.com
  - Create project → Enable "Places API"
  - Create API key (restrict to Places API only)
  - $200 free credit covers ~6,600 place searches
- [ ] Run lead scraper with API key:
  ```bash
  export GOOGLE_PLACES_API_KEY="your-key"
  python lead_scraper.py --niche "dentist" --city "Austin, TX" --limit 50
  python lead_scraper.py --niche "dentist" --city "Denver, CO" --limit 50
  python lead_scraper.py --niche "dentist" --city "Phoenix, AZ" --limit 50
  ```
- [ ] Review leads CSV — sort by lead_score, flag top 50
- [ ] Run email personalizer on top 50 leads:
  ```bash
  python personalize_emails.py --input dental_leads_master.csv --output ready_to_send.csv --sender "Alex" --company "NexusAI Solutions" --calendar "YOUR_CALENDLY_LINK"
  ```

---

## PHASE 2: DEMO BUILD (Days 4-7)

### Day 4-5 — Build AI Chatbot Demo
- [ ] Sign up for n8n Cloud (free tier) or self-host on Railway
- [ ] Create chatbot workflow:
  - Trigger: Webhook (chat widget sends message)
  - OpenAI node: GPT-4o-mini with dental practice system prompt
  - System prompt should cover: services, hours, insurance, pricing FAQs
  - Response node: Return AI answer
- [ ] Create a simple chat widget (HTML/JS) that calls the n8n webhook
- [ ] Test with 20 common dental questions:
  - "Do you accept Delta Dental insurance?"
  - "What are your hours?"
  - "How much does a cleaning cost?"
  - "Can I book an appointment?"
  - "Do you do emergency appointments?"

### Day 5-6 — Build Booking Demo
- [ ] Set up Cal.com account (free, open source)
- [ ] Create demo booking page for fictional "Bright Smile Dental"
  - Services: Cleaning ($150), Whitening ($300), Consultation (Free)
  - Available slots: Mon-Fri 8am-5pm
- [ ] Connect chatbot to booking: When user asks to book, return Cal.com link
- [ ] Test end-to-end: Chat → "I want to book" → Booking link → Confirmation

### Day 6-7 — Build Review Request Demo
- [ ] Create automated review request flow in n8n:
  - Trigger: Webhook (simulating "appointment completed")
  - Wait 2 hours node
  - Send SMS via Twilio ($1/mo + $0.0079/message) or email
  - Message: "Hi {patient_name}, thanks for visiting Bright Smile Dental! If you had a great experience, we'd love a quick Google review: {google_review_link}"
- [ ] Record 3-minute Loom walkthrough of the full demo:
  1. Show the chatbot answering questions on a website
  2. Show booking widget with available slots
  3. Show review request being sent automatically
  4. Show "results dashboard" (can be a simple spreadsheet)
- [ ] Save Loom link — this is your proof of concept for sales calls

---

## PHASE 3: PERSONALIZATION (Days 8-13)

### Day 8-9 — First 20 Loom Videos
- [ ] Open each lead's website in browser
- [ ] Record 90-second Loom video per lead:
  - "Hey [owner], I pulled up [business name]'s website..."
  - Point out: no online booking visible
  - Point out: no chat widget
  - Show their Google reviews count vs a competitor
  - Show 10-second clip of your demo: "Here's what this could look like"
- [ ] 10 videos per day = 2 days for 20 leads
- [ ] Paste each Loom URL into the CRM spreadsheet

### Day 10-11 — Next 20 Loom Videos
- [ ] Record 10 more videos (Day 10)
- [ ] Record 10 more videos (Day 11)
- [ ] Update CRM with all Loom URLs
- [ ] Update personalized email CSVs with Loom URLs (Email 3)

### Day 12-13 — Load & Final Prep
- [ ] Load first 50 personalized emails into sending tool (Instantly.ai or Smartlead)
- [ ] Set up sending schedule:
  - Email 1: Day 14 (tomorrow)
  - Email 2: Day 17
  - Email 3: Day 21 (Loom video)
  - Email 4: Day 28
  - Email 5: Day 35
- [ ] Set sending window: Tuesday-Thursday, 7:30-9:00 AM recipient's local time
- [ ] Set daily limit: 25-30 emails/day for new domain
- [ ] Test with your own email first — send yourself Email 1 and check:
  - [ ] Lands in inbox (not spam)
  - [ ] All merge fields populated correctly
  - [ ] Calendar link works
  - [ ] Formatting looks good on mobile
- [ ] Prepare call script for when prospects book:
  - Discovery questions (5 min): Current patient volume? Biggest bottleneck? Using any software?
  - Demo walkthrough (5 min): Show chatbot, booking, review system
  - Pricing & close (5 min): Starter $497/mo or Growth $997/mo, 30-day guarantee

---

## PHASE 4: LAUNCH (Day 14+)

### Day 14 — First Send
- [ ] Verify domain warmup score (should be 90%+ inbox placement)
- [ ] Activate email campaign — first batch of 25-30 emails goes out
- [ ] Monitor replies throughout the day (check every 2 hours)
- [ ] Respond to ALL replies within 2 hours
- [ ] Log every reply in CRM with sentiment (positive/neutral/negative)

### Days 15-30 — Scale & Convert
- [ ] Send 20-25 new emails per day (continuing follow-up cadence)
- [ ] Record Loom videos for new leads as you go (10/day)
- [ ] Track metrics daily:
  - Open rate (target: 45%+)
  - Reply rate (target: 3-5% on Email 1, 8-12% on Email 3)
  - Calls booked
  - Deals closed
- [ ] By Day 30 target: ~350 emails sent, 7-17 replies, 3-8 calls, 1-3 clients

---

## KEY METRICS TRACKER

| Week | Emails Sent | Opens | Replies | Calls Booked | Deals Closed | MRR |
|------|------------|-------|---------|--------------|-------------|-----|
| 1    |            |       |         |              |             |     |
| 2    |            |       |         |              |             |     |
| 3    |            |       |         |              |             |     |
| 4    |            |       |         |              |             |     |

---

## COST BREAKDOWN

| Item | Cost | Notes |
|------|------|-------|
| Cold email domain | $12/year | Namecheap/Cloudflare |
| Email hosting | $0-6/mo | Zoho free or Google Workspace |
| Instantly.ai | $0-30/mo | Free tier for warmup, paid for sending |
| Google Places API | $0 | $200 free credit |
| Cal.com | $0 | Free tier |
| n8n Cloud | $0-20/mo | Free tier for demo |
| Twilio | ~$1/mo | For review SMS demo |
| Loom | $0 | Free tier (25 videos) |
| **Total startup cost** | **$12-70** | **Everything else is sweat equity** |

---

## FILES & TOOLS REFERENCE

| Asset | Location | Status |
|-------|----------|--------|
| Lead Scraper | `code/ai-agency-outreach/lead_scraper.py` | Ready |
| Email Personalizer | `code/ai-agency-outreach/personalize_emails.py` | Ready |
| Email Sequence (5 emails) | `code/ai-agency-outreach/email_sequence.md` | Ready |
| Landing Page | `code/ai-agency-landing/index.html` + `styles.css` | Ready |
| CRM Tracker | `data/nexusai_crm.csv` | Ready |
| Sample Leads (60) | `data/dental_leads_master.csv` | Ready — replace with real leads |
| Outreach Strategy | `docs/ai_agency_outreach_strategy.md` | Reference |

---

## THE ONLY THING THAT MATTERS

Day 14: Send the first email.
Day 30: Close the first client.

Everything else is preparation for those two moments. Don't over-polish. Don't add features. Don't switch niches. Ship ugly, iterate later.
