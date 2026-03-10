---
name: crypto-channel-format
description: Discord post format and writing style for the crypto channel. Use when composing any message to post to the channel.
created_at: 2026-03-08T16:17:49.058691+00:00
updated_at: 2026-03-08T16:17:49.058691+00:00
---

# Crypto Channel Post Format

## Channel: #crypto
Target: traders who want actionable alpha, not educational content.
Tone: Direct, data-first, no fluff. Never say "I think" — say "data shows".

## Post Structure

### Alpha Brief (triggered scan output)
```
**[SIGNAL TYPE] — [ASSET/PROTOCOL]**

[ONE LINE: what happened with exact numbers]

Data:
- [metric 1]: [value from API] (source: DeFi Llama / CoinGecko / DexScreener)
- [metric 2]: [value]
- [metric 3]: [value]

Context: [1-2 sentences: why this matters, what it could mean]

Watch: [specific level, event, or confirmation to watch for]
```

### Example — Correct Format
```
**TVL SURGE — Hyperliquid**

Hyperliquid TVL hit $4.18B, up 8.3% in 24h while total DeFi TVL up only 1.1%.

Data:
- TVL: $4,180,000,000 (DeFi Llama, live)
- TVL 24h change: +8.3%
- Daily fees: $4.89M (DeFi Llama /summary/fees/hyperliquid)
- HYPE price: check CoinGecko /coins/hyperliquid

Context: Hyperliquid is taking DEX perp market share. Fee growth outpacing TVL growth = efficient capital.

Watch: TVL hold above $4B on any BTC dip = accumulation signal.
```

### Example — Whale Move
```
**WHALE ACCUMULATION — ADA**

348M ADA acquired at avg $0.26 per on-chain data. Cost basis ~$90M.

Data:
- Token price: [live from CoinGecko] 
- 24h volume: [live]
- Market cap: [live]
- Cost basis vs current price: [calculate]

Context: Large single-entity accumulation at this scale typically precedes exchange listing or protocol catalyst.

Watch: $0.32 resistance. Volume confirmation needed.
```

## Rules
- Always include source label (DeFi Llama / CoinGecko / DexScreener)
- Always include timestamp if data is time-sensitive ("as of [UTC time]")
- Use USD figures with full numbers for context (not just percentages)
- Max 1 post per scan cycle UNLESS multiple Tier 1 signals fire simultaneously
- If no Tier 1 or Tier 2 signals: post "No significant alpha detected this cycle. [top 3 metrics snapshot]"

## Pump.fun Token Criteria (when scanning new launches)
Only flag if ALL of:
- Volume >$500K in first 6h (DexScreener)
- Liquidity >$100K (DexScreener pair data)
- NOT a named meme copy (do basic web search to check)
- Price not already up >300% from launch (too late)
