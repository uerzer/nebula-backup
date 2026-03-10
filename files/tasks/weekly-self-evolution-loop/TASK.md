---
slug: weekly-self-evolution-loop
title: Weekly Self-Evolution Loop
steps:
- description: 'CONTEXT LOAD: Read the full scratchpad (manage_memories action=list)
    to review all [MORNING], [MIDDAY], [EVENING] log entries from the past week. Also
    read docs/docs/workspace/ROLLUP.md for current state. This is the raw material
    for pattern extraction.'
  agent_slug: nebula
  format_guide: 'Compile a week-in-review: how many heartbeats ran, what was shipped,
    what kept carrying forward, any repeated blockers or failures. Look for patterns
    across days.'
- description: 'Search past 7 days of conversation history for patterns: failed delegations,
    tool errors, tasks that could not be completed, repeated manual workarounds. Cross-reference
    with scratchpad entries to identify capability gaps.'
  agent_slug: nebula
  format_guide: 'List of gaps with frequency and impact. Example: ''Code Agent timeout
    on large files (3 occurrences, high impact)'''
- description: 'Browse the community skills registry for skills matching identified
    gaps and active projects. Install any highly relevant skills on appropriate agents.
    Check for: memory management, content distribution, SEO, crypto, data analysis
    skills.'
  agent_slug: nebula
- description: 'PERSIST LEARNINGS: For each new pattern or lesson discovered this
    week, save it as a permanent memory using manage_memories(action=''save''). Categories:
    learned_constraint for failures/limits, api_pattern for tool quirks, user_preference
    for workflow preferences. Also update the SOUL anti-patterns list if new anti-patterns
    were discovered.'
  agent_slug: nebula
  format_guide: Save 1-5 new memories from this week's patterns. Use descriptive keys
    like 'learned:github-api-rate-limit-handling' or 'pattern:batch-threshold-3-items'.
    Then update docs/docs/workspace/SOUL.md evolution log section with a dated entry
    summarizing this week.
- description: 'If capability gaps warrant it: create new agents, update existing
    agent prompts (best_practices sections), or build new recipe templates. Update
    docs/docs/workspace/AGENTS.md routing table if any agents were added or changed.'
  agent_slug: nebula
  format_guide: Only make changes if gaps justify them. Don't create agents or recipes
    speculatively. Update AGENTS.md only if actual changes were made.
  file_paths:
  - docs/docs/workspace/AGENTS.md
- description: 'WEEKLY LOG: Write a scratchpad note with format ''[EVOLUTION {date}]
    Gaps: {count}. Memories saved: {count}. Skills installed: {count}. Agents updated:
    {count}. Top insight: {one-liner}.'' Then reset old daily log entries from scratchpad
    that are >7 days old to keep it clean.'
  agent_slug: nebula
  format_guide: Write ONE scratchpad note via manage_memories add_note starting with
    [EVOLUTION YYYY-MM-DD]. Max 300 chars. Then use manage_memories reset_notes ONLY
    if scratchpad has >20 entries (to prevent bloat).
- description: 'Post evolution report summary to Discord general channel (ID: 1466917155475034339).
    Keep concise.'
  agent_id: agt_069931853f6170268000f6f8ba95ae28
  agent_slug: discord-agent
  format_guide: 'WEEKLY EVOLUTION -- {date}


    GAPS FOUND: {top 3}

    LEARNINGS SAVED: {count} new memories

    SKILLS: {installed or ''none this week''}

    AGENT CHANGES: {updates or ''none''}

    TOP INSIGHT: {one-liner}

    NEXT WEEK: {focus areas}'
---