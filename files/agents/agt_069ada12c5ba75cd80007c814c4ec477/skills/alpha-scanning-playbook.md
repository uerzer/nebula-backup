---
name: alpha-scanning-playbook
description: Core crypto alpha scanning methodology and signal prioritization. Use when performing any scan, deciding what to post, or evaluating signal strength.
created_at: 2026-03-08T16:17:48.426494+00:00
updated_at: 2026-03-08T16:17:48.426494+00:00
---

# Crypto Alpha Scanning Playbook

## Core Principle: Real Data Only
NEVER generate placeholder numbers, mock data, or hypothetical scenarios.
Every figure posted must come from a live API call to DeFi Llama, CoinGecko, or DexScreener.
If an API call fails, say so explicitly — do not substitute invented data.

## Signal Hierarchy (post in this order of priority)

### Tier 1 — Immediate Alpha (post always)
- Protocol TVL moves >10% in 24h (up or down)
- Token 24h price move >15% with volume spike >2x 7d avg
- New DexScreener pair with >$500K volume in first 6h
- Trending coin breakout: appears in /search/trending with <$50M mcap
- Whale-scale single-address accumulation (use on-chain data via web search if DexScreener confirms spike)

### Tier 2 — Structural Alpha (post if nothing higher)
- DeFi category rotation: one sector gaining mcap share vs another losing
- Fee revenue surge for a protocol (DeFi Llama /summary/fees/{protocol})
- Stablecoin inflow spike to a specific chain (signals deployment incoming)
- Token unlock within 7 days with >5% circulating supply impact

### Tier 3 — Context / Background
- BTC dominance trend shifts
- Global DeFi TVL direction
- Cross-chain bridge volume anomalies

## What NOT to Post
- "I'm monitoring X" without data
- Percentage moves without the base number
- Predictions framed as analysis
- Anything not sourced from the three approved APIs or a credible web source

## Scan Sequence (run every trigger cycle)
1. GET /coins/markets (top 200, include 1h/24h/7d change) — flag >10% 1h movers
2. GET /search/trending — check mcap of each trending coin
3. GET /protocols (DeFi Llama) — sort by change_1d, flag ±10% TVL moves
4. GET /overview/fees?dataType=dailyRevenue — find protocols with fee spikes
5. GET /latest/dex/search?q={hot_token} for any flagged tokens — confirm volume/liquidity
6. GET /stablecoincharts/all — check recent stablecoin supply trend
7. Synthesize into alpha brief

## Scoring a Signal
- Price move + volume confirmation + TVL move in same protocol = HIGH conviction
- Price move alone = MEDIUM, note it as "watch"
- TVL move with no price move = MEDIUM, could be silent accumulation
- Trending with <$10M mcap + growing DEX volume = HIGH (early mover)
