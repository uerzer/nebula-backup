# Nebula Channel Backups

This repository contains complete conversation backups of all Nebula channels for **hax man** (phobik2000+ai@gmail.com). Each channel is preserved in chronological order with full message content, metadata, and structured manifests for easy search and reference.

## What This Repo Contains

- **`channels/{channel-name}/conversation.md`** — Full message history in chronological order, formatted as `**[timestamp] username:** message content`
- **`channels/{channel-name}/manifest.json`** — Channel metadata including message count, date range, participant list, and backup timestamp

Backups are version-controlled so every run produces a timestamped Git commit history, enabling point-in-time recovery and diff-based change tracking.

## Backed-Up Channels

| # | Channel | Folder | Messages | Last Backup |
|---|---------|--------|----------|-------------|
| 1 | general | [channels/general](./channels/general) | — | 2026-03-01 |
| 2 | astrology | [channels/astrology](./channels/astrology) | — | 2026-03-01 |
| 3 | grok | [channels/grok](./channels/grok) | — | 2026-03-01 |
| 4 | nanobot | [channels/nanobot](./channels/nanobot) | — | 2026-03-01 |
| 5 | levelsio | [channels/levelsio](./channels/levelsio) | — | 2026-03-01 |
| 6 | marketing | [channels/marketing](./channels/marketing) | — | 2026-03-01 |
| 7 | business-intelligence-automation | [channels/business-intelligence-automation](./channels/business-intelligence-automation) | — | 2026-03-01 |
| 8 | discord-agent-setup | [channels/discord-agent-setup](./channels/discord-agent-setup) | — | 2026-03-01 |
| 9 | reverse | [channels/reverse](./channels/reverse) | — | 2026-03-01 |
| 10 | vst | [channels/vst](./channels/vst) | — | 2026-03-01 |
| 11 | hf | [channels/hf](./channels/hf) | — | 2026-03-01 |
| 12 | crypto | [channels/crypto](./channels/crypto) | — | 2026-03-01 |
| 13 | internal-self-improvement | [channels/internal-self-improvement](./channels/internal-self-improvement) | — | 2026-03-01 |
| 14 | memory | [channels/memory](./channels/memory) | — | 2026-03-01 |
| 15 | gsd | [channels/gsd](./channels/gsd) | — | 2026-03-01 |
| 16 | market-research | [channels/market-research](./channels/market-research) | — | 2026-03-01 |
| 17 | funnel | [channels/funnel](./channels/funnel) | — | 2026-03-01 |
| 18 | new-ssh | [channels/new-ssh](./channels/new-ssh) | — | 2026-03-01 |
| 19 | self-improvement | [channels/self-improvement](./channels/self-improvement) | — | 2026-03-01 |
| 20 | execution-tracker | [channels/execution-tracker](./channels/execution-tracker) | — | 2026-03-01 |
| 21 | opportunity-assessment | [channels/opportunity-assessment](./channels/opportunity-assessment) | — | 2026-03-01 |
| 22 | trend-analysis | [channels/trend-analysis](./channels/trend-analysis) | — | 2026-03-01 |
| 23 | daily-scanner-intelligence-run | [channels/daily-scanner-intelligence-run](./channels/daily-scanner-intelligence-run) | — | 2026-03-01 |
| 24 | daily-framework-content-scanner | [channels/daily-framework-content-scanner](./channels/daily-framework-content-scanner) | — | 2026-03-01 |
| 25 | daily-newsletter-draft-edge-finder | [channels/daily-newsletter-draft-edge-finder](./channels/daily-newsletter-draft-edge-finder) | — | 2026-03-01 |
| 26 | ocwasbot-coordination-trigger | [channels/ocwasbot-coordination-trigger](./channels/ocwasbot-coordination-trigger) | 8 | 2026-03-01 |
| 27 | auto-load-context | [channels/auto-load-context](./channels/auto-load-context) | 50+ | 2026-03-01 |
| 28 | test | [channels/test](./channels/test) | 30 | 2026-03-01 |

**Total channels backed up: 28**

## Last Backup

**Date:** 2026-03-01
**Automated by:** Nebula Channel Backup Agent (Weekly trigger)
**Repo:** [uerzer/nebula-backup](https://github.com/uerzer/nebula-backup)

## Backup Schedule

Backups run automatically every week via the **Weekly Nebula Channel Backup** trigger. Each run fetches the latest messages from all active channels and commits them to this repo with a descriptive commit message.

## Structure

```
nebula-backup/
  README.md
  channels/
    general/
      conversation.md
      manifest.json
    astrology/
      conversation.md
      manifest.json
    ... (28 channels total)
```

## Notes

- The `auto-load-context` channel is a high-volume automated trigger channel (355+ executions); only the most recent 50 messages are captured per backup run.
- The `test` channel is archived but preserved for historical reference.
- Channels with `—` message counts were backed up in earlier runs; check their individual `manifest.json` for exact counts.
