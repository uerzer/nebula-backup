---
slug: evening-review-heartbeat
title: Evening Review Heartbeat
steps:
- description: 'CONTEXT LOAD: Read scratchpad notes for today''s full activity log
    (look for [MORNING] and [MIDDAY] entries). Read docs/docs/workspace/ROLLUP.md
    for priorities that were set. This reconstructs the full day''s context before
    the review.'
  agent_slug: nebula
  format_guide: 'Reconstruct the day: what was planned (ROLLUP), what was found (morning/midday
    notes), what''s still open.'
- description: 'DAILY LOG PROMOTION: Use browse_files to find today''s daily log in
    the data/memory/daily/ folder (filename is today''s date YYYY-MM-DD.md). Read
    it with text_editor. Extract durable items: (1) Decisions that affect future work,
    (2) New blockers or resolved blockers, (3) Patterns/lessons learned, (4) Project
    status changes. Summarize these for the persist step later.'
  agent_slug: nebula
  format_guide: 'Search for today''s daily log file. Read it. List durable items in
    categories: DECISIONS, BLOCKERS (new/resolved), LESSONS, STATUS CHANGES. If no
    daily log exists for today, note that and skip.'
- description: 'Check GitHub for today''s full activity: commits pushed, PRs merged,
    issues closed across all uerzer repos. Summarize accomplishments.'
  agent_id: agt_06989c177bdb790b80009f281ba948d2
  agent_slug: github-agent
  format_guide: 'Bullet list of today''s shipped items: commits, merges, issues closed.
    Max 10 items. No preamble.'
- description: 'Run memory compaction: delegate to nebula-memory-layer to consolidate
    today''s memories and report stats.'
  agent_id: agt_069aec4d2ca57f3e8000fb7f8bba84f7
  agent_slug: nebula-memory-layer
- description: 'PERSIST STATE: Do THREE things:

    1. Write scratchpad note via manage_memories(action=''add_note'') with format:
    ''[EVENING {date}] Shipped: {items}. Carry forward: {unfinished}. Lessons: {patterns}.
    Memory stats: {compaction}.''

    2. Update the pref:rollup:current-state memory via manage_memories(action=''save'',
    key=''pref:rollup:current-state'', category=''user_preference'') with current
    active projects, blockers, infrastructure state, and durable items promoted from
    today''s daily log. This memory is loaded on every future session boot.

    3. Update docs/docs/workspace/ROLLUP.md file to match the memory content.'
  agent_slug: nebula
  format_guide: 'Do THREE things: (1) Scratchpad note via add_note, [EVENING YYYY-MM-DD]
    format, max 500 chars. (2) Save pref:rollup:current-state memory with full state:
    ACTIVE WORK, BLOCKERS, INFRASTRUCTURE sections. Include today''s promoted items.
    (3) Overwrite ROLLUP.md to match.'
- description: 'Compile into EVENING REVIEW and post to Discord general channel (ID:
    1466917155475034339). Keep under 2000 chars.'
  agent_id: agt_069931853f6170268000f6f8ba95ae28
  agent_slug: discord-agent
  format_guide: 'EVENING REVIEW -- {date}


    SHIPPED:

    - {accomplishments}


    CARRY FORWARD:

    - {unfinished items}


    LESSONS:

    - {patterns or ''None today''}


    MEMORY: {compaction stats}'
---