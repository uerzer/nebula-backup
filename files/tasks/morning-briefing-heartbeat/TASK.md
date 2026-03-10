---
slug: morning-briefing-heartbeat
title: Morning Briefing Heartbeat
steps:
- description: 'CONTEXT LOAD: Read docs/docs/workspace/ROLLUP.md for active priorities
    and blockers. Check scratchpad notes (manage_memories action=list) for yesterday''s
    evening review findings. This grounds today''s briefing in what actually happened
    yesterday and what''s still open.'
  agent_slug: nebula
  format_guide: 'Extract: open work items, yesterday''s shipped items, any carry-forward
    blockers. Keep as structured bullet notes for use by later steps.'
- description: 'Check GitHub for overnight activity across uerzer repos: new issues,
    PRs opened/merged, CI failures in the last 12 hours. Summarize the top 5 items.'
  agent_id: agt_06989c177bdb790b80009f281ba948d2
  agent_slug: github-agent
  format_guide: 'Concise bullet list: new issues, PRs, CI status. Max 5 items. No
    preamble.'
- description: Check Nebula inbox (pho@nebula.me) for any overnight emails. Flag anything
    urgent.
  agent_id: agt_069a741c38ed7d9280004cc859c2cb1c
  agent_slug: inbox-agent
  format_guide: List sender, subject, urgency. Max 5 items. Say 'Inbox clear' if nothing.
- description: Search web for current BTC, ETH, SOL prices and 24h changes.
  agent_slug: nebula
  action_key: web-search
  action_props:
    query: bitcoin ethereum solana price today
- description: 'DAILY LOG: Write a scratchpad note summarizing this morning''s findings.
    Use manage_memories(action=''add_note'') with format: ''[MORNING {date}] GitHub:
    {count} items. Email: {count} items. Priorities: {top 3 from ROLLUP}. Alerts:
    {any issues or none}.'' This creates the daily append-only log entry.'
  agent_slug: nebula
  format_guide: Write exactly ONE scratchpad note via manage_memories add_note. Keep
    under 300 chars. Start with [MORNING YYYY-MM-DD].
- description: 'Compile all gathered intelligence into a MORNING BRIEFING and post
    to Discord general channel (ID: 1466917155475034339). Keep under 2000 chars.'
  agent_id: agt_069931853f6170268000f6f8ba95ae28
  agent_slug: discord-agent
  format_guide: 'MORNING BRIEFING -- {date}


    OVERNIGHT:

    - {github + email items}


    TODAY''S PRIORITIES:

    1. {from ROLLUP}


    MARKETS: BTC ${price}, ETH ${price}, SOL ${price}


    ALERTS: {issues or ''All systems nominal''}'
---