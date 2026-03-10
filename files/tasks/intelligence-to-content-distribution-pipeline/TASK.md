---
slug: intelligence-to-content-distribution-pipeline
title: Intelligence-to-Content Distribution Pipeline
steps:
- description: 'Read today''s scanner intelligence outputs. Browse workspace files
    for the latest unified_opportunity_intelligence, daily_framework_scan_report,
    and edge_finder newsletter draft files (today''s date). Compile a structured briefing
    document that includes: (1) Top 5 ranked opportunities with scores, TAM, and one-line
    summaries, (2) Any new frameworks added to the master playbook today, (3) Top
    3 news stories from the newsletter draft. Save this compiled briefing to outputs/content-pipeline/daily_briefing_<date>.md'
  agent_slug: nebula
  format_guide: 'Markdown briefing document with sections: ## Top Opportunities, ##
    New Frameworks, ## Trending News. Each item should have a one-liner hook suitable
    for social media adaptation.'
- description: 'Generate a Twitter/X thread from the daily briefing. Create a 5-7
    tweet thread using hook-driven copywriting: Tweet 1 = pattern-interrupt hook about
    the #1 opportunity, Tweets 2-5 = one opportunity or framework each with a specific
    insight/number, Tweet 6 = the ''so what'' actionable takeaway, Tweet 7 = CTA to
    follow for daily alpha. Each tweet must be under 280 characters. Save to outputs/content-pipeline/twitter_thread_<date>.md'
  agent_slug: nebula
  format_guide: 'Numbered tweet thread in markdown. Each tweet on its own line prefixed
    with [1/7], [2/7] etc. No hashtag spam - max 2 relevant hashtags on the last tweet
    only. Tone: sharp, data-driven, slightly contrarian. Like a smarter version of
    tech Twitter.'
- description: 'Generate 2 Reddit posts from the daily briefing. Post 1: For r/Entrepreneur
    - a value-first deep dive on the highest-scoring micro SaaS opportunity (problem,
    market size, validation signal, suggested MVP approach). Post 2: For r/SideProject
    - a shorter ''I analyzed X opportunities today, here''s what stood out'' format
    highlighting 2-3 ideas with scores. Both should feel like genuine community contributions,
    not promotion. Save to outputs/content-pipeline/reddit_posts_<date>.md'
  agent_slug: nebula
  format_guide: 'Two posts separated by ---. Each has: Title (compelling but not clickbait),
    Body (markdown formatted, uses bullet points for scanability). r/Entrepreneur
    post should be 300-500 words. r/SideProject post should be 150-250 words. No self-promotion
    links. End with ''What do you think?'' style engagement question.'
- description: 'Generate a Telegram broadcast message from the daily briefing. Create
    a concise executive summary for the Just Bull group: emoji-accented header, 3-5
    bullet points of today''s top signals (opportunities + frameworks + news), and
    a one-line ''bottom line'' verdict. Keep under 500 characters for mobile readability.
    Save to outputs/content-pipeline/telegram_broadcast_<date>.md'
  agent_slug: nebula
  format_guide: 'Telegram-native formatting with HTML tags (<b>, <i>, <code>). Use
    line breaks for readability. Structure: Bold header line, blank line, bullet points
    with relevant emoji, blank line, bold bottom-line takeaway.'
- description: 'Generate a Discord digest message from the daily briefing. Create
    a formatted intelligence drop for jd''s server: use Discord markdown (bold, code
    blocks, embeds-style formatting). Include a ''Daily Alpha'' header, the top 3
    opportunities as numbered items with scores, any new frameworks as a separate
    section, and a ''What to Watch'' forward-looking item. Save to outputs/content-pipeline/discord_digest_<date>.md'
  agent_slug: nebula
  format_guide: 'Discord markdown formatting. Use **bold** for headers, `code` for
    scores/numbers, > blockquotes for key insights. Keep total length under 2000 characters
    (Discord message limit). Structure: header, opportunities, frameworks, what-to-watch.'
- description: 'Generate a blog-ready long-form article from the daily briefing. Write
    a 600-1000 word article titled ''Daily Edge: [Top Theme] - [Date]'' that weaves
    together the opportunity intelligence, framework insights, and news into a cohesive
    narrative. Include an intro hook, 3 main sections, and a conclusion with actionable
    next steps. This is the SEO-friendly evergreen piece. Save to outputs/content-pipeline/blog_post_<date>.md'
  agent_slug: nebula
  format_guide: 'Clean markdown with H1 title, H2 section headers, bold key phrases,
    and inline links where relevant. Include a YAML frontmatter block with title,
    date, tags, and description for static site generators. Tone: authoritative but
    accessible, like a premium research newsletter.'
- description: 'DISTRIBUTE - Twitter: Read outputs/content-pipeline/twitter_thread_<date>.md.
    Post each tweet in sequence using twitter-post-tweet for the first tweet, then
    twitter-reply-to-tweet for subsequent tweets to create a proper thread. Save the
    thread URL.'
  agent_id: agt_069ad9ffb43e77f68000868be694918d
  agent_slug: social-distribution-engine
  action_key: twitter-post-tweet
  action_props:
    text: '{{tweet_content}}'
- description: 'DISTRIBUTE - Reddit r/Entrepreneur: Read the first post from outputs/content-pipeline/reddit_posts_<date>.md.
    Submit to r/Entrepreneur using reddit-submit-a-post with kind=self (text post).'
  agent_id: agt_069ad9ffb43e77f68000868be694918d
  agent_slug: social-distribution-engine
  action_key: reddit-submit-a-post
  action_props:
    subreddit: Entrepreneur
    kind: self
- description: 'DISTRIBUTE - Reddit r/SideProject: Read the second post from outputs/content-pipeline/reddit_posts_<date>.md.
    Submit to r/SideProject using reddit-submit-a-post with kind=self (text post).'
  agent_id: agt_069ad9ffb43e77f68000868be694918d
  agent_slug: social-distribution-engine
  action_key: reddit-submit-a-post
  action_props:
    subreddit: SideProject
    kind: self
- description: 'DISTRIBUTE - Telegram: Read outputs/content-pipeline/telegram_broadcast_<date>.md.
    Send the message to the Just Bull Telegram group using telegram-send-message with
    parse_mode=HTML.'
  agent_id: agt_069930866b7a76bb8000b8d921b233bf
  agent_slug: telegram-agent
  action_key: telegram-send-message
  action_props:
    parse_mode: HTML
- description: 'DISTRIBUTE - Discord: Read outputs/content-pipeline/discord_digest_<date>.md.
    Send the formatted digest to the appropriate channel in jd''s server using discord-send-message.'
  agent_id: agt_069931853f6170268000f6f8ba95ae28
  agent_slug: discord-agent
  action_key: discord-send-message
- description: 'DISTRIBUTE - Blog to GitHub: Read outputs/content-pipeline/blog_post_<date>.md.
    Commit it to the uerzer/opportunity-intelligence repository under /blog/ directory
    with a descriptive commit message including today''s date.'
  agent_id: agt_06989c177bdb790b80009f281ba948d2
  agent_slug: github-agent
  action_key: github-create-or-update-file-contents
- description: 'DISTRIBUTE - Newsletter Email: Read the latest Edge Finder newsletter
    HTML from outputs/newsletter-drafts/edge_finder_<date>.html. Send it as an email
    with subject ''Edge Finder Daily - [date]'' to the subscriber list (start with
    sending to pho@nebula.me for review). This closes the newsletter dead-end.'
  agent_slug: nebula
  action_key: send-nebula-email
  action_props:
    subject: Edge Finder Daily
---