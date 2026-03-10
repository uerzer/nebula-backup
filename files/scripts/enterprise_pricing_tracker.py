import httpx
import json
import os
from datetime import datetime, timezone

DATE_STR = "20260310"
SCAN_TS = datetime.now(timezone.utc).isoformat()
headers = {"User-Agent": "OpportunityScanner/1.0"}
client = httpx.Client(timeout=30, headers=headers)

data = {"scan_timestamp": SCAN_TS, "date": DATE_STR, "pricing_intel": [], "gaps": []}

# 1. Scan HN for pricing discussions
print(">>> Scanning for enterprise pricing discussions...")
try:
    r = client.get("https://hn.algolia.com/api/v1/search", params={"query": "enterprise pricing SaaS expensive alternative", "tags": "story", "hitsPerPage": 15})
    if r.status_code == 200:
        hits = r.json().get("hits", [])
        for h in hits[:12]:
            data["pricing_intel"].append({"source": "HN", "title": h.get("title",""), "points": h.get("points",0), "url": "https://news.ycombinator.com/item?id={}".format(h.get("objectID","")), "category": "pricing_discussion"})
        print("   Found {} pricing discussions".format(len(hits)))
except Exception as e:
    print("   HN pricing error: {}".format(e))

# 2. Scan for open-source alternatives (pricing gaps)
print(">>> Scanning for open-source alternatives...")
try:
    r = client.get("https://api.github.com/search/repositories", params={"q": "open-source alternative enterprise SaaS created:>2025-12-01", "sort": "stars", "order": "desc", "per_page": 15})
    if r.status_code == 200:
        repos = r.json().get("items", [])
        for repo in repos[:10]:
            data["gaps"].append({"source": "GitHub", "name": repo["full_name"], "description": repo.get("description","")[:200] if repo.get("description") else "", "stars": repo["stargazers_count"], "url": repo["html_url"], "gap_type": "open_source_alternative", "opportunity_score": min(100, repo["stargazers_count"] // 5)})
        print("   Found {} OSS alternatives".format(len(repos)))
except Exception as e:
    print("   GitHub error: {}".format(e))

# 3. Scan for "too expensive" complaints
print(">>> Scanning pricing complaints...")
try:
    r = client.get("https://hn.algolia.com/api/v1/search", params={"query": "too expensive overpriced cheaper alternative", "tags": "story", "hitsPerPage": 10})
    if r.status_code == 200:
        hits = r.json().get("hits", [])
        for h in hits[:8]:
            data["gaps"].append({"source": "HN", "name": h.get("title","")[:80], "description": "Pricing complaint - {} points".format(h.get("points",0)), "stars": h.get("points",0), "url": "https://news.ycombinator.com/item?id={}".format(h.get("objectID","")), "gap_type": "pricing_complaint", "opportunity_score": min(100, (h.get("points",0) or 0) // 3)})
        print("   Found {} pricing complaints".format(len(hits)))
except Exception as e:
    print("   Complaints error: {}".format(e))

data["gaps"].sort(key=lambda x: x.get("opportunity_score",0), reverse=True)
data["summary"] = {
    "total_intel": len(data["pricing_intel"]),
    "total_gaps": len(data["gaps"]),
    "top_gap": data["gaps"][0]["name"] if data["gaps"] else "N/A",
    "avg_score": round(sum(g.get("opportunity_score",0) for g in data["gaps"]) / max(1,len(data["gaps"])), 1)
}

os.makedirs("/home/user/files/data/data", exist_ok=True)
with open("/home/user/files/data/data/enterprise_pricing_intelligence_{}.json".format(DATE_STR), "w") as f:
    json.dump(data, f, indent=2)

md = "# Enterprise Pricing Intelligence - {}\n\n**Scan Time:** {}\n\n".format(DATE_STR, SCAN_TS)
md += "## Summary\n- Pricing discussions tracked: {}\n- Pricing gaps identified: {}\n- Top opportunity: {}\n- Avg opportunity score: {}\n\n".format(data["summary"]["total_intel"], data["summary"]["total_gaps"], data["summary"]["top_gap"], data["summary"]["avg_score"])
md += "## Top Pricing Gaps\n\n| Source | Name | Score | Type |\n|--------|------|-------|------|\n"
for g in data["gaps"][:15]:
    md += "| {} | {} | {} | {} |\n".format(g["source"], g["name"][:50], g["opportunity_score"], g["gap_type"])

with open("/home/user/files/data/data/enterprise_pricing_intelligence_{}.md".format(DATE_STR), "w") as f:
    f.write(md)

print("\nDone! Files saved to data/data/enterprise_pricing_intelligence_{}.[json|md]".format(DATE_STR))
print("Summary: {}".format(json.dumps(data["summary"], indent=2)))