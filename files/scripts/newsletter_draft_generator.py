#!/usr/bin/env python3
"""
Edge Finder Newsletter Draft Generator
Compiles all scanner outputs and news aggregation into newsletter formats
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class NewsletterGenerator:
    def __init__(self, date_str: str):
        self.date_str = date_str
        self.base_path = Path("/home/user/files")
        self.data = {}
        
    def load_json(self, filepath: str) -> Dict:
        """Load JSON file and return data"""
        try:
            with open(self.base_path / filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load {filepath}: {e}")
            return {}
    
    def load_all_data(self):
        """Load all scanner outputs and news aggregation"""
        print("Loading all data sources...")
        
        # News aggregation
        self.data['news'] = self.load_json(f"outputs/newsletter-content/news_aggregation_{self.date_str}.json")
        
        # Scanner outputs
        self.data['ai_agency'] = self.load_json(f"data/ai_agency_leads_{self.date_str}.json")
        self.data['crypto_arbitrage'] = self.load_json(f"data/crypto_arbitrage_intelligence_{self.date_str}.json")
        self.data['enterprise_pricing'] = self.load_json(f"data/enterprise_pricing_gaps_{self.date_str}.json")
        self.data['viral_trends'] = self.load_json(f"data/viral_trend_intelligence_{self.date_str}.json")
        
        print(f"✓ Loaded {len([k for k, v in self.data.items() if v])} data sources")
        
    def generate_markdown(self) -> str:
        """Generate Markdown newsletter draft"""
        print("Generating Markdown newsletter...")
        
        date_obj = datetime.strptime(self.date_str, "%Y%m%d")
        formatted_date = date_obj.strftime("%B %d, %Y")
        
        md = f"""# Edge Finder Newsletter
## {formatted_date}

*Your daily intelligence briefing on emerging opportunities, viral trends, and market gaps*

---

"""
        
        # News Section
        if self.data.get('news', {}).get('stories'):
            md += "## 📰 Trending News & Stories\n\n"
            stories = self.data['news']['stories'][:10]  # Top 10
            
            for i, story in enumerate(stories, 1):
                md += f"### {i}. {story.get('title', 'Untitled')}\n"
                if story.get('url'):
                    md += f"🔗 [{story['url']}]({story['url']})\n\n"
                md += f"**Source:** {story.get('source', 'Unknown')} | "
                md += f"**Category:** {story.get('category', 'General')} | "
                md += f"**Score:** {story.get('final_score', 0):.1f}\n\n"
                if story.get('summary'):
                    md += f"{story['summary']}\n\n"
                md += "---\n\n"
        
        # AI Agency Opportunities
        if self.data.get('ai_agency', {}).get('leads'):
            leads = self.data['ai_agency']['leads']
            md += f"## 🤖 AI Agency Opportunities\n\n"
            md += f"**{len(leads)} high-potential leads identified**\n\n"
            
            for lead in leads[:5]:  # Top 5
                md += f"### {lead.get('company_name', 'Unknown Company')}\n"
                md += f"- **Industry:** {lead.get('industry', 'N/A')}\n"
                md += f"- **Signal:** {lead.get('signal_type', 'N/A')}\n"
                md += f"- **Urgency:** {lead.get('urgency_score', 0)}/10\n"
                md += f"- **Opportunity:** {lead.get('opportunity_description', 'N/A')}\n"
                if lead.get('url'):
                    md += f"- **Link:** [{lead['url']}]({lead['url']})\n"
                md += "\n"
        
        # Viral Trends
        if self.data.get('viral_trends', {}).get('trends'):
            trends = self.data['viral_trends']['trends']
            md += f"## 🔥 Viral Trends\n\n"
            md += f"**{len(trends)} emerging trends tracked**\n\n"
            
            for trend in trends[:5]:  # Top 5
                md += f"### {trend.get('topic', 'Unknown Trend')}\n"
                md += f"- **Platform:** {trend.get('platform', 'N/A')}\n"
                md += f"- **Velocity:** {trend.get('velocity_score', 0)}/10\n"
                md += f"- **Volume:** {trend.get('volume', 'N/A')}\n"
                if trend.get('insight'):
                    md += f"- **Insight:** {trend['insight']}\n"
                md += "\n"
        
        # Enterprise Pricing Gaps
        if self.data.get('enterprise_pricing', {}).get('gaps'):
            gaps = self.data['enterprise_pricing']['gaps']
            md += f"## 💰 Enterprise Pricing Gaps\n\n"
            md += f"**{len(gaps)} market gaps identified**\n\n"
            
            for gap in gaps[:5]:  # Top 5
                md += f"### {gap.get('category', 'Unknown Category')}\n"
                md += f"- **Gap Type:** {gap.get('gap_type', 'N/A')}\n"
                md += f"- **Opportunity Score:** {gap.get('opportunity_score', 0)}/10\n"
                md += f"- **Description:** {gap.get('description', 'N/A')}\n"
                if gap.get('market_size'):
                    md += f"- **Market Size:** {gap['market_size']}\n"
                md += "\n"
        
        # Crypto Arbitrage
        if self.data.get('crypto_arbitrage', {}).get('opportunities'):
            opps = self.data['crypto_arbitrage']['opportunities']
            md += f"## ⚡ Crypto Arbitrage Opportunities\n\n"
            md += f"**{len(opps)} arbitrage opportunities detected**\n\n"
            
            for opp in opps[:5]:  # Top 5
                md += f"### {opp.get('pair', 'Unknown Pair')}\n"
                md += f"- **Spread:** {opp.get('spread_percentage', 0):.2f}%\n"
                md += f"- **Profit Potential:** {opp.get('profit_potential', 'N/A')}\n"
                md += f"- **Exchanges:** {opp.get('exchanges', 'N/A')}\n"
                md += f"- **Risk Level:** {opp.get('risk_level', 'N/A')}\n"
                md += "\n"
        
        # Footer
        md += """---

## 📊 Intelligence Summary

"""
        
        summary_stats = []
        if self.data.get('news'):
            summary_stats.append(f"- **News Stories:** {len(self.data['news'].get('stories', []))}")
        if self.data.get('ai_agency'):
            summary_stats.append(f"- **AI Agency Leads:** {len(self.data['ai_agency'].get('leads', []))}")
        if self.data.get('viral_trends'):
            summary_stats.append(f"- **Viral Trends:** {len(self.data['viral_trends'].get('trends', []))}")
        if self.data.get('enterprise_pricing'):
            summary_stats.append(f"- **Pricing Gaps:** {len(self.data['enterprise_pricing'].get('gaps', []))}")
        if self.data.get('crypto_arbitrage'):
            summary_stats.append(f"- **Crypto Opportunities:** {len(self.data['crypto_arbitrage'].get('opportunities', []))}")
        
        md += "\n".join(summary_stats)
        md += "\n\n*Generated automatically by Edge Finder Intelligence System*\n"
        
        return md
    
    def generate_html(self) -> str:
        """Generate HTML email-ready newsletter"""
        print("Generating HTML newsletter...")
        
        date_obj = datetime.strptime(self.date_str, "%Y%m%d")
        formatted_date = date_obj.strftime("%B %d, %Y")
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edge Finder Newsletter - {formatted_date}</title>
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
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }}
        h3 {{
            color: #555;
            margin-top: 20px;
        }}
        .story {{
            background-color: #f8f9fa;
            padding: 15px;
            margin: 15px 0;
            border-left: 3px solid #3498db;
            border-radius: 4px;
        }}
        .meta {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        .opportunity {{
            background-color: #e8f5e9;
            padding: 15px;
            margin: 15px 0;
            border-left: 3px solid #4caf50;
            border-radius: 4px;
        }}
        .trend {{
            background-color: #fff3e0;
            padding: 15px;
            margin: 15px 0;
            border-left: 3px solid #ff9800;
            border-radius: 4px;
        }}
        .stat {{
            display: inline-block;
            background-color: #3498db;
            color: white;
            padding: 5px 10px;
            border-radius: 3px;
            margin-right: 10px;
            font-size: 0.9em;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #ecf0f1;
            color: #7f8c8d;
            font-size: 0.9em;
            text-align: center;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📈 Edge Finder Newsletter</h1>
        <p class="meta">{formatted_date}</p>
        <p><em>Your daily intelligence briefing on emerging opportunities, viral trends, and market gaps</em></p>
        
"""
        
        # News Section
        if self.data.get('news', {}).get('stories'):
            html += '<h2>📰 Trending News & Stories</h2>\n'
            stories = self.data['news']['stories'][:10]
            
            for i, story in enumerate(stories, 1):
                html += f'<div class="story">\n'
                html += f'<h3>{i}. {story.get("title", "Untitled")}</h3>\n'
                html += f'<p class="meta">'
                html += f'<strong>Source:</strong> {story.get("source", "Unknown")} | '
                html += f'<strong>Category:</strong> {story.get("category", "General")} | '
                html += f'<strong>Score:</strong> {story.get("final_score", 0):.1f}'
                html += f'</p>\n'
                if story.get('summary'):
                    html += f'<p>{story["summary"]}</p>\n'
                if story.get('url'):
                    html += f'<p><a href="{story["url"]}" target="_blank">Read more →</a></p>\n'
                html += '</div>\n'
        
        # AI Agency Opportunities
        if self.data.get('ai_agency', {}).get('leads'):
            leads = self.data['ai_agency']['leads']
            html += f'<h2>🤖 AI Agency Opportunities</h2>\n'
            html += f'<p><span class="stat">{len(leads)} leads identified</span></p>\n'
            
            for lead in leads[:5]:
                html += '<div class="opportunity">\n'
                html += f'<h3>{lead.get("company_name", "Unknown Company")}</h3>\n'
                html += '<ul>\n'
                html += f'<li><strong>Industry:</strong> {lead.get("industry", "N/A")}</li>\n'
                html += f'<li><strong>Signal:</strong> {lead.get("signal_type", "N/A")}</li>\n'
                html += f'<li><strong>Urgency:</strong> {lead.get("urgency_score", 0)}/10</li>\n'
                html += f'<li><strong>Opportunity:</strong> {lead.get("opportunity_description", "N/A")}</li>\n'
                if lead.get('url'):
                    html += f'<li><a href="{lead["url"]}" target="_blank">View lead →</a></li>\n'
                html += '</ul>\n'
                html += '</div>\n'
        
        # Viral Trends
        if self.data.get('viral_trends', {}).get('trends'):
            trends = self.data['viral_trends']['trends']
            html += f'<h2>🔥 Viral Trends</h2>\n'
            html += f'<p><span class="stat">{len(trends)} trends tracked</span></p>\n'
            
            for trend in trends[:5]:
                html += '<div class="trend">\n'
                html += f'<h3>{trend.get("topic", "Unknown Trend")}</h3>\n'
                html += '<ul>\n'
                html += f'<li><strong>Platform:</strong> {trend.get("platform", "N/A")}</li>\n'
                html += f'<li><strong>Velocity:</strong> {trend.get("velocity_score", 0)}/10</li>\n'
                html += f'<li><strong>Volume:</strong> {trend.get("volume", "N/A")}</li>\n'
                if trend.get('insight'):
                    html += f'<li><strong>Insight:</strong> {trend["insight"]}</li>\n'
                html += '</ul>\n'
                html += '</div>\n'
        
        # Enterprise Pricing Gaps
        if self.data.get('enterprise_pricing', {}).get('gaps'):
            gaps = self.data['enterprise_pricing']['gaps']
            html += f'<h2>💰 Enterprise Pricing Gaps</h2>\n'
            html += f'<p><span class="stat">{len(gaps)} gaps identified</span></p>\n'
            
            for gap in gaps[:5]:
                html += '<div class="opportunity">\n'
                html += f'<h3>{gap.get("category", "Unknown Category")}</h3>\n'
                html += '<ul>\n'
                html += f'<li><strong>Gap Type:</strong> {gap.get("gap_type", "N/A")}</li>\n'
                html += f'<li><strong>Opportunity Score:</strong> {gap.get("opportunity_score", 0)}/10</li>\n'
                html += f'<li><strong>Description:</strong> {gap.get("description", "N/A")}</li>\n'
                if gap.get('market_size'):
                    html += f'<li><strong>Market Size:</strong> {gap["market_size"]}</li>\n'
                html += '</ul>\n'
                html += '</div>\n'
        
        # Crypto Arbitrage
        if self.data.get('crypto_arbitrage', {}).get('opportunities'):
            opps = self.data['crypto_arbitrage']['opportunities']
            html += f'<h2>⚡ Crypto Arbitrage Opportunities</h2>\n'
            html += f'<p><span class="stat">{len(opps)} opportunities detected</span></p>\n'
            
            for opp in opps[:5]:
                html += '<div class="trend">\n'
                html += f'<h3>{opp.get("pair", "Unknown Pair")}</h3>\n'
                html += '<ul>\n'
                html += f'<li><strong>Spread:</strong> {opp.get("spread_percentage", 0):.2f}%</li>\n'
                html += f'<li><strong>Profit Potential:</strong> {opp.get("profit_potential", "N/A")}</li>\n'
                html += f'<li><strong>Exchanges:</strong> {opp.get("exchanges", "N/A")}</li>\n'
                html += f'<li><strong>Risk Level:</strong> {opp.get("risk_level", "N/A")}</li>\n'
                html += '</ul>\n'
                html += '</div>\n'
        
        # Footer
        html += """
        <div class="footer">
            <p><strong>Intelligence Summary</strong></p>
"""
        
        if self.data.get('news'):
            html += f'<p>📰 {len(self.data["news"].get("stories", []))} News Stories</p>\n'
        if self.data.get('ai_agency'):
            html += f'<p>🤖 {len(self.data["ai_agency"].get("leads", []))} AI Agency Leads</p>\n'
        if self.data.get('viral_trends'):
            html += f'<p>🔥 {len(self.data["viral_trends"].get("trends", []))} Viral Trends</p>\n'
        if self.data.get('enterprise_pricing'):
            html += f'<p>💰 {len(self.data["enterprise_pricing"].get("gaps", []))} Pricing Gaps</p>\n'
        if self.data.get('crypto_arbitrage'):
            html += f'<p>⚡ {len(self.data["crypto_arbitrage"].get("opportunities", []))} Crypto Opportunities</p>\n'
        
        html += """
            <p><em>Generated automatically by Edge Finder Intelligence System</em></p>
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def generate_metadata(self) -> Dict:
        """Generate JSON metadata"""
        print("Generating metadata...")
        
        date_obj = datetime.strptime(self.date_str, "%Y%m%d")
        
        metadata = {
            "newsletter_date": self.date_str,
            "formatted_date": date_obj.strftime("%B %d, %Y"),
            "generated_at": datetime.now().isoformat(),
            "version": "1.0",
            "stats": {
                "news_stories": len(self.data.get('news', {}).get('stories', [])),
                "ai_agency_leads": len(self.data.get('ai_agency', {}).get('leads', [])),
                "viral_trends": len(self.data.get('viral_trends', {}).get('trends', [])),
                "enterprise_gaps": len(self.data.get('enterprise_pricing', {}).get('gaps', [])),
                "crypto_opportunities": len(self.data.get('crypto_arbitrage', {}).get('opportunities', []))
            },
            "data_sources": list(self.data.keys()),
            "output_files": {
                "markdown": f"outputs/newsletter-drafts/edge_finder_{self.date_str}.md",
                "html": f"outputs/newsletter-drafts/edge_finder_{self.date_str}.html",
                "metadata": f"outputs/newsletter-drafts/edge_finder_{self.date_str}_metadata.json"
            }
        }
        
        return metadata
    
    def save_outputs(self, markdown: str, html: str, metadata: Dict):
        """Save all output files"""
        output_dir = self.base_path / "outputs" / "newsletter-drafts"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save Markdown
        md_path = output_dir / f"edge_finder_{self.date_str}.md"
        with open(md_path, 'w') as f:
            f.write(markdown)
        print(f"✓ Saved Markdown: {md_path}")
        
        # Save HTML
        html_path = output_dir / f"edge_finder_{self.date_str}.html"
        with open(html_path, 'w') as f:
            f.write(html)
        print(f"✓ Saved HTML: {html_path}")
        
        # Save metadata
        meta_path = output_dir / f"edge_finder_{self.date_str}_metadata.json"
        with open(meta_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✓ Saved Metadata: {meta_path}")
        
        return {
            "markdown": str(md_path),
            "html": str(html_path),
            "metadata": str(meta_path)
        }

def main():
    date_str = "20260225"
    
    print(f"\n{'='*60}")
    print(f"Edge Finder Newsletter Draft Generator")
    print(f"Date: {date_str}")
    print(f"{'='*60}\n")
    
    generator = NewsletterGenerator(date_str)
    
    # Load all data
    generator.load_all_data()
    
    # Generate outputs
    markdown = generator.generate_markdown()
    html = generator.generate_html()
    metadata = generator.generate_metadata()
    
    # Save files
    files = generator.save_outputs(markdown, html, metadata)
    
    print(f"\n{'='*60}")
    print("Newsletter generation complete!")
    print(f"{'='*60}\n")
    print(f"Files created:")
    for format_type, filepath in files.items():
        print(f"  - {format_type}: {filepath}")
    
    print(f"\nStats:")
    for key, value in metadata['stats'].items():
        print(f"  - {key.replace('_', ' ').title()}: {value}")

if __name__ == "__main__":
    main()
