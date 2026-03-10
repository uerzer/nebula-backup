---
slug: midday-pulse-heartbeat
title: Midday Pulse Heartbeat
steps:
- description: 'CONTEXT LOAD: Check scratchpad notes for today''s morning briefing
    findings (look for [MORNING] entry). Read docs/docs/workspace/ROLLUP.md for current
    priorities. This tells you what was flagged this morning so you only report NEW
    developments.'
  agent_slug: nebula
  format_guide: Extract morning findings and current priorities. Identify what to
    check for changes since morning.
- description: 'MEMORY HEALTH CHECK: List all memories via manage_memories(action=''list'').
    Count total memories. Check if any pref:rollup:* or pref:soul:* memories are missing
    (these are critical boot memories). Also browse_files for data/memory/daily/ to
    verify today''s daily log exists. Report: total_memories, missing_critical, daily_log_exists.'
  agent_slug: nebula
  format_guide: 'Count memories, check for critical boot memories (pref:rollup:current-state,
    pref:soul:session-boot-protocol, pref:soul:agent-routing). Verify today''s daily
    log file exists. Report as: Memories: X total, Critical: all present/missing Y,
    Daily log: exists/missing.'
- description: 'STALE TASK DETECTION: Search past messages for any tasks or todos
    that were started but not completed in the last 48 hours. Check manage_tasks(action=''search'')
    for any failed or stale recipe executions. Flag anything that needs attention.'
  agent_slug: nebula
  format_guide: List stale/failed tasks if any. Say 'No stale tasks' if clean. Max
    5 items.
- description: Check GitHub for any new PRs requiring review, new issues, or CI failures
    since the morning briefing (last 6 hours).
  agent_id: agt_06989c177bdb790b80009f281ba948d2
  agent_slug: github-agent
  format_guide: Only report items needing action. Say 'Nothing new since morning'
    if quiet. No preamble.
- description: 'DAILY LOG: Write a scratchpad note summarizing midday findings. Use
    manage_memories(action=''add_note'') with format: ''[MIDDAY {date}] New since
    morning: {items or ''nothing''}. Action needed: {yes/no}.'' Only write this note
    -- do not post to Discord if nothing actionable.'
  agent_slug: nebula
  format_guide: Write exactly ONE scratchpad note via manage_memories add_note. Keep
    under 200 chars. Start with [MIDDAY YYYY-MM-DD].
- description: 'Only if there is something actionable from the checks above, post
    a brief MIDDAY PULSE to Discord general channel (ID: 1466917155475034339). Skip
    entirely if nothing notable.'
  agent_id: agt_069931853f6170268000f6f8ba95ae28
  agent_slug: discord-agent
  format_guide: 'MIDDAY PULSE -- {date}

    PROGRESS: {items}

    BLOCKERS: {items}

    NEEDS ATTENTION: {items}'
  filtering_prompt: Only post if there are actionable items found in prior steps.
    If the midday check found nothing new since morning, skip this step entirely --
    do not spam Discord.
---