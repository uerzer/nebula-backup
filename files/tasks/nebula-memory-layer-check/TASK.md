---
slug: daily-memory-maintenance-rollup
title: Daily Memory Maintenance + Rollup
steps:
- description: 'DAILY LOG PROCESSING: Use browse_files to find all daily log files
    in data/memory/daily/ folder. Read the last 7 days of logs. Extract durable facts
    (decisions, patterns, mappings, blockers) that should be promoted to long-term
    memory. For logs older than 30 days, create a monthly summary at data/memory/monthly/YYYY-MM.md
    and delete the individual daily files. Report: logs_processed, facts_extracted,
    logs_archived.'
  agent_slug: nebula
  format_guide: 'List daily logs found. For each, extract durable facts. Summarize:
    X logs processed, Y facts to promote, Z logs archived to monthly summary.'
- description: 'Run memory compaction: load nebula_memory.py from code/nebula_memory.py,
    instantiate MemoryEngine + SessionManager + MemoryCompactor with memory.db, call
    auto_compact() to compress memories older than 7 days and sessions over 20K tokens.
    Report stats: memories_processed, insights_created, facts_extracted.'
  agent_id: agt_069aec4d2ca57f3e8000fb7f8bba84f7
  agent_slug: nebula-memory-layer
- description: 'Generate ROLLUP: Using compaction results AND daily log facts, build
    the continuity state. Do TWO things: (1) Update the pref:rollup:current-state
    memory via manage_memories(action=''save'', key=''pref:rollup:current-state'',
    category=''user_preference'') with active projects, blockers, infrastructure state,
    and promoted daily log items. This memory auto-loads on every future session.
    (2) Update docs/docs/workspace/ROLLUP.md file to match.'
  agent_slug: nebula
  format_guide: 'Update BOTH the pref:rollup:current-state memory AND the ROLLUP.md
    file with: ACTIVE WORK, BLOCKERS, INFRASTRUCTURE, RECENT INSIGHTS sections.'
- description: 'Backup memory.db to GitHub: commit the memory.db file and the updated
    ROLLUP.md to the uerzer/nebula-backup repository under the memory/ directory.
    Include compaction stats in the commit message.'
  agent_id: agt_06989c177bdb790b80009f281ba948d2
  agent_slug: github-agent
  action_key: github-create-or-update-file-contents
  action_props:
    owner: uerzer
    repo: nebula-backup
---