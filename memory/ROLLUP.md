# ROLLUP.md -- Continuity State
> Auto-generated: 2026-03-10T09:16:00Z
> Source: Evening Review heartbeat + daily log processing
> Next auto-update: Evening Review heartbeat (9 PM WET daily)

## Active Context
- [DONE] OpenClaw Parity -- all 6 phases shipped (boot, daily logs, memory persistence, heartbeats, skill injection, session continuity)
- [Decision] 5 workspace bootstrap files at docs/workspace/ (SOUL, IDENTITY, USER, AGENTS, TOOLS)
- [Decision] Ephemeral agent architecture: persistent files + memory = brain surviving agent termination
- [Decision] Boot protocol uses user_preference memories (not file pointers) -- actual context injected every session
- [Decision] Sub-agent behavior injected via prompt_sections (workflow + best_practices), not skills files
- [Decision] Session-end protocol saves: mappings, patterns, daily log entry, scratchpad note
- [Blocker] Telegram bot lacks group access to Just Bull -- needs manual re-add
- [Blocker] 6 GitHub repos need manual Pages enable
- [Blocker] Discord Channel Monitor needs DISCORD_BOT_TOKEN configured

## System Architecture (Live)
- 14 active triggers (4 heartbeats + memory compaction + 9 operational)
- Boot protocol: 6 pref:soul:* memories auto-loaded every session
- Persist protocol: session-end saves mappings, patterns, daily log, transcript
- Daily logs: data/memory/daily/YYYY-MM-DD.md (append-only)
- Session transcripts: data/sessions/YYYY-MM-DD-{channel}.md
- Heartbeats: 7AM morning brief, 1PM midday pulse (w/ memory health), 9PM evening review (w/ compaction + rollup)
- Weekly: Monday 8AM self-evolution scan
- 5 key sub-agents have OpenClaw behavior injected via prompt_sections
- Memory layer: SQLite + FTS5 + sqlite-vec, hybrid BM25+cosine retrieval (384-dim BAAI/bge-small-en-v1.5)

## Recent Insights (2026-03-10 maintenance)
- Daily log processing: 2 logs processed (2026-03-09, 2026-02-12), 7 facts extracted, 1 log archived to monthly
- Memory compaction: 0 memories compacted (all fresh), 0 sessions compacted, DB healthy
- Monthly archive created: data/memory/monthly/2026-02.md (Feb 2026 summary from daily-logs/2026-02-12.md)
- Full OpenClaw loop confirmed: boot (memories) -> execute (with routing) -> persist (mappings + logs + transcripts) -> compact (nightly)
- Batch with Code Agent: one script replaces 20 individual delegations
- 3x daily heartbeat is pragmatic -- 30-min would waste agent runs for marginal gain

## Session Status
- 36 total channels, 45+ agents, 14 active triggers
- Memory DB: 7 active memories (3 insights, 3 decisions, 1 conversation), 1.6MB
- First evening review maintenance run completed successfully
- Weekly self-evolution loop trigger active (Monday 8AM) but not yet tested

## Key Facts
- [Preference] User wants concise, results-first communication
- [Preference] User prefers Nebula to act autonomously, not ask permission
- [Lesson] Ephemeral agents need persistent state files -- the files ARE the brain
- [Lesson] Check AGENTS.md routing table before delegating
- [Lesson] Memories ARE the bootstrap, not instructions to read files
- [Lesson] Static workspace files are theater unless wired into runtime behavior
- [Fact] Memory compaction engine at code/nebula_memory.py (MemoryEngine + SessionManager + MemoryCompactor)
- [Fact] 5 workspace bootstrap files at docs/workspace/
- [Fact] Feb 2026: Decided to adapt OpenClaw patterns to Nebula, not use directly
- [Fact] Nebula orchestrator cannot have skills installed directly (not a regular agent slug)

## Open Todos
- [ ] Fix Telegram bot access to Just Bull group
- [ ] Configure DISCORD_BOT_TOKEN for Discord Channel Monitor
- [ ] Enable GitHub Pages on 6 repos
- [ ] Test weekly self-evolution loop next Monday
- [ ] Monitor heartbeat system stability over next week
