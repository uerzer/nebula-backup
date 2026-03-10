---
name: memory-api-feedback
description: Documented memory API gaps and platform improvement requests for Nebula. Use when drafting feedback, responding to Furqan's replies, or escalating platform issues.
created_at: 2026-03-08T16:15:32.160879+00:00
updated_at: 2026-03-08T16:15:32.160879+00:00
---

# Nebula Memory API — Gap Analysis & Feedback

## Current Memory Limitations (Known Gaps)
1. **No structured namespacing** — memory is flat; no ability to tag or segment memories by project, agent, or topic
2. **No cross-agent memory sharing** — agents cannot read memory written by sibling agents without manual relay
3. **No memory expiry / TTL** — no way to mark memories as short-term vs long-term
4. **No bulk memory operations** — can't query all memories matching a pattern or delete a batch
5. **No memory versioning** — overwriting a memory destroys previous value; no history

## Feature Requests (Priority Order)
1. Structured memory with namespaces/tags (HIGH)
2. Cross-agent shared memory pool (HIGH)
3. Memory TTL / expiry controls (MEDIUM)
4. Pattern-based memory queries (MEDIUM)
5. Memory change webhooks — fire a trigger when a key memory is updated (LOW/FUTURE)

## Communication Log
- Initial outreach email sent to Furqan Rydhan re: memory API gaps
- Monitor pho@nebula.me for reply from Furqan or Nebula team
- Follow-up cadence: if no reply in 5 business days, send polite follow-up referencing original

## Tone Guidelines for Follow-ups
- Reference specific prior email subject line if possible
- Add any new examples or use cases discovered since last contact
- Keep it concise: 3-4 paragraphs max
- Close with a specific ask (call, async doc review, beta access to memory improvements)

## Platform Improvement Communications — General Rules
- Always use pho@nebula.me as sender/reply-to
- CC or reference the 'memory' channel context when relevant
- Log all outbound emails and replies in memory for continuity
