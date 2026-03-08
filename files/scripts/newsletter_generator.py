#!/usr/bin/env python3
"""
Edge Finder Newsletter Generator
Compiles news aggregation and scanner outputs into newsletter drafts (Markdown, HTML, JSON)
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

def load_json_file(filepath: str) -> Dict[str, Any]:
    """Load and parse JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def format_date(date_str: str) -> str:
    """Format ISO date to readable format"""
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%B %d, %Y')
    except:
        return date_str

def generate_markdown(data: Dict[str, Any], date: str) -> str:
    """Generate Markdown newsletter"""
    md = f"""# Edge Finder Newsletter
## {format_date(date)}

> Your daily intelligence briefing on emerging opportunities, viral trends, and market inefficiencies

---

## Top Stories & Trends

"""
    
    # Add news stories
    if 'news' in data and data['news']:
        news_items = data['news'][:10]  # Top 10 stories
        for i, story in enumerate(news_items, 1):
            md += f"### {i}. {story['title']}\n\n"
            md += f"**Category:** {story.get('category', 'General')} | "
            md += f"**Score:** {story.get('relevance_score', 0):.1f} | "
            md += f"**Engagement:** {story.get('points', 0)} points, {story.get('num_comments', 0)} comments\n\n"
            md += f"[Read More]({story['url']})\n\n"
            md += "---\n\n"
    
    # Add viral trends section
    if 'viral_trends' in data and data['viral_trends']:
        md += "## Viral Trend Intelligence\n\n"
        vt = data['viral_trends']
        
        # Add key insights
        if 'key_insights' in vt:
            md += "### Key Insights\n\n"
            for insight in vt['key_insights'][:5]:
                md += f"- {insight}\n"
            md += "\n---\n\n"
        
        # Add Product Hunt intelligence
        if 'product_hunt_intelligence' in vt:
            ph = vt['product_hunt_intelligence']
            md += "### Product Hunt 2026 Playbook\n\n"
            if 'success_metrics_2026' in ph:
                md += "**Success Metrics:**\n"
                metrics = ph['success_metrics_2026']
                for key, value in list(metrics.items())[:3]:
                    md += f"- {key.replace('_', ' ').title()}: {value}\n"
            md += "\n---\n\n"
        
        # Add immediate action steps
        if 'immediate_action_steps' in vt:
            md += "### Immediate Actions\n\n"
            for step in vt['immediate_action_steps'][:5]:
                md += f"{step}\n\n"
            md += "---\n\n"
    
    # Add crypto arbitrage section
    if 'crypto_arbitrage' in data and data['crypto_arbitrage']:
        md += "## Crypto Arbitrage Opportunities\n\n"
        arb = data['crypto_arbitrage']
        if 'opportunities' in arb and arb['opportunities']:
            for opp in arb['opportunities'][:3]:
                md += f"### {opp.get('pair', 'N/A')}\n\n"
                md += f"**Spread:** {opp.get('spread_percentage', 0):.2f}% | "
                md += f"**Exchanges:** {opp.get('buy_exchange', 'N/A')} -> {opp.get('sell_exchange', 'N/A')}\n\n"
                md += "---\n\n"
        else:
            md += "*No significant arbitrage opportunities detected today.*\n\n"
    
    # Footer
    md += """---

## About Edge Finder

Edge Finder is your automated intelligence system for discovering emerging opportunities before they hit mainstream. 
Powered by AI-driven scanners monitoring viral trends, pricing gaps, and market inefficiencies 24/7.

*This is an automated digest. Review and validate all opportunities before taking action.*
"""
    
    return md

def generate_html(data: Dict[str, Any], date: str) -> str:
    """Generate HTML email-ready newsletter"""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edge Finder Newsletter - {format_date(date)}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #1a1a1a;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #2c3e50;
            margin-top: 30px;
            border-left: 4px solid #4CAF50;
            padding-left: 15px;
        }}
        h3 {{
            color: #34495e;
            margin-top: 20px;
        }}
        .meta {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin: 10px 0;
        }}
        .story {{
            border-bottom: 1px solid #ecf0f1;
            padding: 20px 0;
        }}
        .story:last-child {{
            border-bottom: none;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.85em;
            font-weight: 600;
            margin-right: 5px;
        }}
        .badge-tech {{
            background-color: #e3f2fd;
            color: #1976d2;
        }}
        .badge-ai {{
            background-color: #f3e5f5;
            color: #7b1fa2;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #ecf0f1;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        .highlight {{
            background-color: #fff9c4;
            padding: 2px 4px;
            border-radius: 2px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Edge Finder Newsletter</h1>
        <p class="meta"><strong>{format_date(date)}</strong></p>
        <p style="font-style: italic; color: #7f8c8d;">Your daily intelligence briefing on emerging opportunities, viral trends, and market inefficiencies</p>
        
        <h2>Top Stories &amp; Trends</h2>
"""
    
    # Add news stories
    if 'news' in data and data['news']:
        news_items = data['news'][:10]
        for i, story in enumerate(news_items, 1):
            category = story.get('category', 'General')
            badge_class = 'badge-ai' if 'AI' in category else 'badge-tech'
            
            html += f"""        <div class="story">
            <h3>{i}. {story['title']}</h3>
            <p class="meta">
                <span class="badge {badge_class}">{category}</span>
                Score: {story.get('relevance_score', 0):.1f} | 
                {story.get('points', 0)} points, {story.get('num_comments', 0)} comments
            </p>
            <p><a href="{story['url']}" target="_blank">Read More &rarr;</a></p>
        </div>
"""
    
    # Add viral trends section
    if 'viral_trends' in data and data['viral_trends']:
        html += """        
        <h2>Viral Trend Intelligence</h2>
"""
        vt = data['viral_trends']
        
        # Add key insights
        if 'key_insights' in vt:
            html += """        <div class="story">
            <h3>Key Insights</h3>
            <ul>
"""
            for insight in vt['key_insights'][:5]:
                html += f"                <li>{insight}</li>\n"
            html += """            </ul>
        </div>
"""
        
        # Add Product Hunt intelligence
        if 'product_hunt_intelligence' in vt:
            ph = vt['product_hunt_intelligence']
            html += """        <div class="story">
            <h3>Product Hunt 2026 Playbook</h3>
"""
            if 'success_metrics_2026' in ph:
                html += "            <p><strong>Success Metrics:</strong></p>\n            <ul>\n"
                metrics = ph['success_metrics_2026']
                for key, value in list(metrics.items())[:3]:
                    html += f"                <li>{key.replace('_', ' ').title()}: {value}</li>\n"
                html += "            </ul>\n"
            html += "        </div>\n"
        
        # Add immediate actions
        if 'immediate_action_steps' in vt:
            html += """        <div class="story">
            <h3>Immediate Actions</h3>
            <ol>
"""
            for step in vt['immediate_action_steps'][:5]:
                html += f"                <li>{step}</li>\n"
            html += """            </ol>
        </div>
"""
    
    # Add crypto arbitrage section
    if 'crypto_arbitrage' in data and data['crypto_arbitrage']:
        html += """        
        <h2>Crypto Arbitrage Opportunities</h2>
"""
        arb = data['crypto_arbitrage']
        if 'opportunities' in arb and arb['opportunities']:
            for opp in arb['opportunities'][:3]:
                html += f"""        <div class="story">
            <h3>{opp.get('pair', 'N/A')}</h3>
            <p class="meta">
                Spread: <span class="highlight">{opp.get('spread_percentage', 0):.2f}%</span> | 
                {opp.get('buy_exchange', 'N/A')} &rarr; {opp.get('sell_exchange', 'N/A')}
            </p>
        </div>
"""
        else:
            html += "        <p><em>No significant arbitrage opportunities detected today.</em></p>\n"
    
    # Footer
    html += """        
        <div class="footer">
            <h3>About Edge Finder</h3>
            <p>Edge Finder is your automated intelligence system for discovering emerging opportunities before they hit mainstream. 
            Powered by AI-driven scanners monitoring viral trends, pricing gaps, and market inefficiencies 24/7.</p>
            <p><em>This is an automated digest. Review and validate all opportunities before taking action.</em></p>
        </div>
    </div>
</body>
</html>
"""
    
    return html

def main():
    """Main newsletter generation workflow"""
    # Get today's date
    today = datetime.utcnow().strftime('%Y%m%d')
    
    # Create output directory
    output_dir = Path('/home/user/files/outputs/newsletter-drafts')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load data sources
    print("Loading data sources...")
    
    data = {
        'news': [],
        'viral_trends': [],
        'crypto_arbitrage': {},
        'metadata': {
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'date': today,
            'version': '1.0'
        }
    }
    
    # Load news aggregation
    news_file = Path(f'/home/user/files/outputs/newsletter-content/news_aggregation_{today}.json')
    if news_file.exists():
        news_data = load_json_file(str(news_file))
        data['news'] = news_data.get('stories', [])
        print(f"Loaded {len(data['news'])} news stories")
    else:
        print(f"Warning: News aggregation file not found: {news_file}")
    
    # Load viral trends
    viral_file = Path(f'data/viral_trends_scan_{today}.json')
    if viral_file.exists():
        viral_data = load_json_file(str(viral_file))
        # Extract the actual trend insights from the nested structure
        data['viral_trends'] = viral_data
        print(f"Loaded viral trends analysis")
    else:
        print(f"Warning: Viral trends file not found: {viral_file}")
    
    # Load crypto arbitrage
    crypto_file = Path(f'data/crypto_arbitrage_scan_{today}.json')
    if crypto_file.exists():
        data['crypto_arbitrage'] = load_json_file(str(crypto_file))
        opp_count = len(data['crypto_arbitrage'].get('opportunities', []))
        print(f"Loaded {opp_count} crypto arbitrage opportunities")
    else:
        print(f"Warning: Crypto arbitrage file not found: {crypto_file}")
    
    # Generate outputs
    print("\nGenerating newsletter drafts...")
    
    # Markdown
    markdown_content = generate_markdown(data, today)
    markdown_file = output_dir / f'newsletter_draft_{today}.md'
    with open(markdown_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    print(f"Created: {markdown_file}")
    
    # HTML
    html_content = generate_html(data, today)
    html_file = output_dir / f'newsletter_draft_{today}.html'
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Created: {html_file}")
    
    # JSON metadata
    json_file = output_dir / f'newsletter_draft_{today}.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Created: {json_file}")
    
    # Summary
    print("\n" + "="*60)
    print("NEWSLETTER GENERATION COMPLETE")
    print("="*60)
    print(f"\nDate: {format_date(today)}")
    print(f"News Stories: {len(data['news'])}")
    print(f"Viral Trends: {len(data['viral_trends'])}")
    print(f"Crypto Opportunities: {len(data['crypto_arbitrage'].get('opportunities', []))}")
    print(f"\nOutput Files:")
    print(f"  - Markdown: {markdown_file}")
    print(f"  - HTML: {html_file}")
    print(f"  - JSON: {json_file}")
    
    return {
        'status': 'success',
        'files_created': [str(markdown_file), str(html_file), str(json_file)],
        'stats': {
            'news_count': len(data['news']),
            'trends_count': len(data['viral_trends']),
            'crypto_count': len(data['crypto_arbitrage'].get('opportunities', []))
        }
    }

if __name__ == '__main__':
    result = main()
    print(f"\nResult: {json.dumps(result, indent=2)}")
