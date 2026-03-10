---
name: defi-llama-api-guide
description: DeFi Llama API endpoint usage guide with correct slugs and gotchas. Use when querying DeFi Llama for TVL, fees, or volume data.
created_at: 2026-03-08T16:17:49.647223+00:00
updated_at: 2026-03-08T16:17:49.647223+00:00
---

# DeFi Llama API Usage Guide

## Base URL
https://api.llama.fi  (free, public, no auth required)

## Key Endpoints and Usage

### Protocol TVL
GET /protocols
Returns all protocols. Key fields: name, tvl, change_1h, change_1d, change_7d, slug, mcap
Use to find top movers: sort by |change_1d| descending.

GET /tvl/{protocol}
Returns single float. Use for quick TVL check.
Example: GET /tvl/hyperliquid -> 4180000000.0

GET /protocol/{protocol}
Full historical data. Use when you need TVL trend, not just current.

### Chain TVL
GET /v2/chains
All chains with current TVL. Sort to find which chains are growing fastest.

### Fees and Revenue (important for alpha)
GET /overview/fees?dataType=dailyRevenue
List all protocols sorted by daily revenue. Spikes here = real usage.

GET /summary/fees/{protocol}
Protocol-specific fee breakdown. Hyperliquid slug: "hyperliquid"
Returns total24h, total7d, change_1d

### DEX Volumes
GET /overview/dexs?dataType=dailyVolume
All DEX protocols by daily volume. Use to spot volume rotation.

### Stablecoins
GET /stablecoins
GET /stablecoincharts/all
GET /stablecoincharts/{chain}  (use "Solana", "Arbitrum", "Ethereum" etc.)

## Important Protocol Slugs
- hyperliquid
- aave
- aave-v3
- uniswap
- gmx
- lido
- makerdao
- curve
- pancakeswap
- jupiter (Solana)

## Common Gotchas
- The free base URL is https://api.llama.fi NOT https://pro-api.llama.fi
- Pro endpoints (marked with lock) require API key inserted in URL path — skip these, free endpoints are sufficient
- Protocol slugs are lowercase-hyphenated, not camelCase
- TVL numbers are in USD as raw floats (divide by 1e9 for billions)
- change_1d field is a percentage float (8.3 means +8.3%)
