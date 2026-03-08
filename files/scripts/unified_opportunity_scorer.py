#!/usr/bin/env python3
"""
Unified Opportunity Scorer
Aggregates and ranks opportunities from all intelligence scanners
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


def load_scanner_data(date_str: str = "20260303") -> Dict[str, Any]:
    """Load all intelligence data from scanners"""
    
    data = {
        'crypto': None,
        'viral': None,
        'ai_agency_raw': None,
        'enterprise_raw': None,
        'micro_saas_raw': None,
        'ai_agency_intel': None,
        'enterprise_intel': None,
        'micro_saas_intel': None
    }
    
    # Load intelligence reports
    try:
        with open(f'data/crypto_arbitrage_intelligence_{date_str}.json', 'r') as f:
            data['crypto'] = json.load(f)
    except Exception as e:
        print(f"Failed to load crypto: {e}")
    
    try:
        with open(f'data/viral_trends_intelligence_{date_str}.json', 'r') as f:
            data['viral'] = json.load(f)
    except Exception as e:
        print(f"Failed to load viral: {e}")
    
    try:
        with open(f'data/ai_agency_leads_{date_str}.json', 'r') as f:
            data['ai_agency_raw'] = json.load(f)
    except Exception as e:
        print(f"Failed to load ai_agency_raw: {e}")
    
    try:
        with open(f'data/ai_agency_leads_intelligence_{date_str}.json', 'r') as f:
            data['ai_agency_intel'] = json.load(f)
    except Exception as e:
        print(f"Failed to load ai_agency_intel: {e}")
    
    try:
        with open(f'data/enterprise_pricing_gaps_{date_str}.json', 'r') as f:
            data['enterprise_raw'] = json.load(f)
    except Exception as e:
        print(f"Failed to load enterprise_raw: {e}")
    
    try:
        with open(f'data/enterprise_pricing_intelligence_{date_str}.json', 'r') as f:
            data['enterprise_intel'] = json.load(f)
    except Exception as e:
        print(f"Failed to load enterprise_intel: {e}")
    
    try:
        with open(f'data/micro_saas_validation_{date_str}.json', 'r') as f:
            data['micro_saas_raw'] = json.load(f)
    except Exception as e:
        print(f"Failed to load micro_saas_raw: {e}")
    
    try:
        with open(f'data/micro_saas_validation_intelligence_{date_str}.json', 'r') as f:
            data['micro_saas_intel'] = json.load(f)
    except Exception as e:
        print(f"Failed to load micro_saas_intel: {e}")
    
    return data


def extract_opportunities(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract and normalize opportunities from all scanners"""
    
    opportunities = []
    
    # Extract from micro_saas_raw (has the validation scores)
    if data['micro_saas_raw'] and 'rankings' in data['micro_saas_raw']:
        for rank in data['micro_saas_raw']['rankings']:
            opp = {
                'source': 'micro_saas_validation',
                'name': rank.get('idea_name', 'Unknown'),
                'score': rank.get('weighted_score', 0),
                'decision': rank.get('go_decision', {}).get('decision', 'UNKNOWN'),
                'confidence': rank.get('go_decision', {}).get('confidence', 0),
                'risk_profile': rank.get('risk_profile', {}).get('overall', 'UNKNOWN'),
                'market_size': rank.get('market_data', {}).get('market_opportunity', 0),
                'target_customers': rank.get('market_data', {}).get('target_market_size', 0),
                'price_range': rank.get('market_data', {}).get('ideal_price_range', 'N/A'),
                'revenue_potential': rank.get('market_data', {}).get('year1_revenue_potential', 'N/A'),
                'high_risk_count': rank.get('risk_profile', {}).get('high_risk_count', 0),
                'dimension_scores': rank.get('dimension_scores', {}),
                'raw_data': rank
            }
            opportunities.append(opp)
    
    # Extract from enterprise_raw (pricing gaps)
    if data['enterprise_raw'] and 'categories' in data['enterprise_raw']:
        for category in data['enterprise_raw']['categories']:
            for gap in category.get('pricing_gaps', []):
                opp = {
                    'source': 'enterprise_pricing',
                    'name': f"{gap.get('gap_type', 'Unknown')} ({category.get('category', 'Unknown')})",
                    'score': gap.get('severity', 0),
                    'decision': 'GO' if gap.get('severity', 0) >= 85 else 'CAUTIOUS GO',
                    'confidence': 80 if gap.get('severity', 0) >= 85 else 60,
                    'risk_profile': 'LOW' if gap.get('severity', 0) >= 90 else 'MEDIUM',
                    'market_size': gap.get('opportunity_size_numeric', 0),
                    'target_customers': gap.get('potential_customers', 'N/A'),
                    'price_range': gap.get('ideal_price_point', 'N/A'),
                    'revenue_potential': gap.get('monthly_revenue_potential', 'N/A'),
                    'high_risk_count': 0,
                    'dimension_scores': {
                        'severity': {'score': gap.get('severity', 0), 'reasoning': gap.get('description', '')}
                    },
                    'raw_data': gap
                }
                opportunities.append(opp)
    
    # Extract from ai_agency_raw (lead segments)
    if data['ai_agency_raw'] and 'lead_segments' in data['ai_agency_raw']:
        for segment_type, segments in data['ai_agency_raw']['lead_segments'].items():
            for segment in segments:
                # Convert budget to annual value for comparison
                budget = segment.get('avg_budget', '$0/month')
                opp = {
                    'source': 'ai_agency_leads',
                    'name': segment.get('segment', 'Unknown'),
                    'score': segment.get('urgency_score', 0),
                    'decision': 'GO' if segment.get('urgency_score', 0) >= 85 else 'CAUTIOUS GO',
                    'confidence': 75,
                    'risk_profile': 'LOW' if segment.get('competition_level', '').lower() in ['low', 'medium'] else 'MEDIUM',
                    'market_size': segment.get('market_size', 'N/A'),
                    'target_customers': segment.get('market_size', 'N/A'),
                    'price_range': budget,
                    'revenue_potential': 'N/A',
                    'high_risk_count': 1 if segment.get('competition_level', '').lower() == 'high' else 0,
                    'dimension_scores': {
                        'urgency': {'score': segment.get('urgency_score', 0), 'reasoning': 'AI agency opportunity'},
                        'competition': {'score': 100 - (25 if 'high' in segment.get('competition_level', '').lower() else 0), 'reasoning': segment.get('competition_level', 'N/A')}
                    },
                    'raw_data': segment
                }
                opportunities.append(opp)
    
    # Viral trends - note: currently empty but keeping structure
    if data['viral'] and 'opportunities' in data['viral']:
        for priority_level in ['high_priority', 'medium_priority']:
            for trend in data['viral']['opportunities'].get(priority_level, []):
                opp = {
                    'source': 'viral_trends',
                    'name': trend.get('name', 'Unknown Trend'),
                    'score': 85 if priority_level == 'high_priority' else 70,
                    'decision': 'GO',
                    'confidence': 70,
                    'risk_profile': 'MEDIUM',
                    'market_size': 'N/A',
                    'target_customers': 'N/A',
                    'price_range': 'N/A',
                    'revenue_potential': 'N/A',
                    'high_risk_count': 1,
                    'dimension_scores': {},
                    'raw_data': trend
                }
                opportunities.append(opp)
    
    # Crypto opportunities
    if data['crypto'] and 'arbitrage_opportunities' in data['crypto']:
        arb_opps = data['crypto']['arbitrage_opportunities']
        if arb_opps:
            opp = {
                'source': 'crypto_arbitrage',
                'name': 'Crypto Arbitrage Opportunities',
                'score': 50,  # Low score due to low market activity
                'decision': 'NO GO',
                'confidence': 80,
                'risk_profile': 'HIGH',
                'market_size': 'Variable',
                'target_customers': 'N/A',
                'price_range': 'N/A',
                'revenue_potential': 'Low',
                'high_risk_count': 2,
                'dimension_scores': {},
                'raw_data': arb_opps
            }
            opportunities.append(opp)
    
    return opportunities


def rank_opportunities(opportunities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Rank opportunities by weighted score"""
    
    # Sort by score descending
    ranked = sorted(opportunities, key=lambda x: x.get('score', 0), reverse=True)
    
    # Add rank number
    for i, opp in enumerate(ranked, 1):
        opp['rank'] = i
    
    return ranked


def generate_unified_report(ranked_opportunities: List[Dict[str, Any]], date_str: str) -> Dict[str, Any]:
    """Generate unified intelligence report"""
    
    # Categorize by decision
    strong_go = [o for o in ranked_opportunities if 'STRONG GO' in o.get('decision', '')]
    go = [o for o in ranked_opportunities if o.get('decision', '') == 'GO']
    cautious_go = [o for o in ranked_opportunities if 'CAUTIOUS' in o.get('decision', '')]
    no_go = [o for o in ranked_opportunities if 'NO GO' in o.get('decision', '')]
    
    # Categorize by source
    by_source = {}
    for opp in ranked_opportunities:
        source = opp.get('source', 'unknown')
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(opp)
    
    # Top opportunities
    top_10 = ranked_opportunities[:10]
    
    report = {
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'scan_date': date_str,
        'total_opportunities': len(ranked_opportunities),
        'summary': {
            'by_decision': {
                'strong_go': len(strong_go),
                'go': len(go),
                'cautious_go': len(cautious_go),
                'no_go': len(no_go)
            },
            'by_source': {source: len(opps) for source, opps in by_source.items()},
            'avg_score': sum(o.get('score', 0) for o in ranked_opportunities) / len(ranked_opportunities) if ranked_opportunities else 0
        },
        'top_10_opportunities': top_10,
        'all_opportunities': ranked_opportunities,
        'categories': {
            'strong_go': strong_go,
            'go': go,
            'cautious_go': cautious_go,
            'no_go': no_go
        },
        'by_source': by_source
    }
    
    return report


def generate_markdown_report(report: Dict[str, Any]) -> str:
    """Generate human-readable markdown report"""
    
    md = f"""# Unified Opportunity Intelligence Report
Generated: {report['generated_at']}
Scan Date: {report['scan_date']}

## Executive Summary

**Total Opportunities Analyzed:** {report['total_opportunities']}

### By Decision Category
- **STRONG GO:** {report['summary']['by_decision']['strong_go']} opportunities
- **GO:** {report['summary']['by_decision']['go']} opportunities
- **CAUTIOUS GO:** {report['summary']['by_decision']['cautious_go']} opportunities
- **NO GO:** {report['summary']['by_decision']['no_go']} opportunities

### By Source
"""
    
    for source, count in report['summary']['by_source'].items():
        md += f"- **{source}:** {count} opportunities\n"
    
    md += f"\n**Average Opportunity Score:** {report['summary']['avg_score']:.1f}/100\n\n"
    
    md += "## Top 10 Opportunities\n\n"
    
    for opp in report['top_10_opportunities']:
        md += f"### {opp['rank']}. {opp['name']}\n"
        md += f"**Score:** {opp['score']:.1f}/100 | **Decision:** {opp['decision']} | **Confidence:** {opp['confidence']}%\n\n"
        md += f"- **Source:** {opp['source']}\n"
        md += f"- **Risk Profile:** {opp['risk_profile']}\n"
        
        if isinstance(opp.get('market_size'), (int, float)):
            md += f"- **Market Size:** ${opp['market_size']:,.0f}\n"
        else:
            md += f"- **Market Size:** {opp.get('market_size', 'N/A')}\n"
        
        md += f"- **Target Customers:** {opp.get('target_customers', 'N/A')}\n"
        md += f"- **Price Range:** {opp.get('price_range', 'N/A')}\n"
        md += f"- **Revenue Potential:** {opp.get('revenue_potential', 'N/A')}\n"
        
        if opp.get('dimension_scores'):
            md += "\n**Key Metrics:**\n"
            for dim, data in list(opp['dimension_scores'].items())[:5]:
                if isinstance(data, dict) and 'score' in data:
                    md += f"- {dim}: {data['score']}/100 - {data.get('reasoning', 'N/A')}\n"
        
        md += "\n---\n\n"
    
    # Add category breakdowns
    md += "## Opportunities by Decision Category\n\n"
    
    for category in ['strong_go', 'go', 'cautious_go', 'no_go']:
        category_name = category.replace('_', ' ').upper()
        opps = report['categories'][category]
        
        if opps:
            md += f"### {category_name} ({len(opps)} opportunities)\n\n"
            for opp in opps[:5]:  # Top 5 per category
                md += f"- **#{opp['rank']} {opp['name']}** (Score: {opp['score']:.1f}, Confidence: {opp['confidence']}%)\n"
            
            if len(opps) > 5:
                md += f"- ... and {len(opps) - 5} more\n"
            md += "\n"
    
    return md


def main():
    """Main execution"""
    
    print("=== Unified Opportunity Scorer ===\n")
    
    # Load data
    print("Loading scanner data...")
    data = load_scanner_data()
    
    # Extract opportunities
    print("Extracting opportunities...")
    opportunities = extract_opportunities(data)
    print(f"Found {len(opportunities)} total opportunities\n")
    
    # Rank opportunities
    print("Ranking opportunities...")
    ranked = rank_opportunities(opportunities)
    
    # Generate reports
    print("Generating unified report...")
    report = generate_unified_report(ranked, "20260303")
    
    print("Generating markdown report...")
    markdown = generate_markdown_report(report)
    
    # Save outputs
    json_path = 'data/unified_opportunity_intelligence_20260303.json'
    md_path = 'data/unified_opportunity_intelligence_20260303.md'
    
    with open(json_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✓ Saved JSON report: {json_path}")
    
    with open(md_path, 'w') as f:
        f.write(markdown)
    print(f"✓ Saved Markdown report: {md_path}")
    
    # Print summary
    print("\n=== Summary ===")
    print(f"Total Opportunities: {report['total_opportunities']}")
    print(f"Average Score: {report['summary']['avg_score']:.1f}/100")
    print(f"\nTop 3:")
    for opp in ranked[:3]:
        print(f"  {opp['rank']}. {opp['name']} - Score: {opp['score']:.1f}")
    
    return report


if __name__ == "__main__":
    main()
