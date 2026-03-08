#!/usr/bin/env python3
"""
Micro SaaS Validation Framework
Scores ideas based on: Market Size, Competition, Technical Feasibility, Monetization, Time-to-Market
"""

import json
from datetime import datetime
from pathlib import Path

# Validation Framework Scoring Criteria
SCORING_CRITERIA = {
    "market_size": {
        "weight": 0.25,
        "thresholds": {
            100: "$1B+ TAM",
            80: "$100M-$1B TAM", 
            60: "$10M-$100M TAM",
            40: "$1M-$10M TAM",
            20: "<$1M TAM"
        }
    },
    "competition": {
        "weight": 0.20,
        "thresholds": {
            100: "No direct competitors, underserved niche",
            80: "1-2 weak competitors, clear differentiation",
            60: "3-5 competitors, fragmented market",
            40: "5-10 competitors, crowded",
            20: "10+ established competitors"
        }
    },
    "technical_feasibility": {
        "weight": 0.20,
        "thresholds": {
            100: "No-code/low-code, 1-2 months",
            80: "Standard tech stack, 3-4 months",
            60: "Moderate complexity, 4-6 months",
            40: "Complex tech, 6-12 months",
            20: "Requires R&D, 12+ months"
        }
    },
    "monetization": {
        "weight": 0.20,
        "thresholds": {
            100: "Clear willingness to pay, proven pricing models, high LTV:CAC",
            80: "Established category with pricing benchmarks",
            60: "New category, requires education",
            40: "Monetization unproven",
            20: "No clear path to revenue"
        }
    },
    "time_to_market": {
        "weight": 0.15,
        "thresholds": {
            100: "Launch in 1-2 months",
            80: "Launch in 3-4 months",
            60: "Launch in 4-6 months",
            40: "Launch in 6-12 months",
            20: "12+ months to launch"
        }
    }
}

# Extract micro SaaS ideas from intelligence reports
MICRO_SAAS_IDEAS = [
    {
        "id": "ms001",
        "name": "Vertical SaaS for Construction Compliance",
        "description": "Construction project management focused on permitting, safety compliance, and subcontractor coordination. Addresses mid-market SaaS squeeze by going deep in vertical.",
        "source": "Enterprise Pricing Intelligence - Mid-Market SaaS Squeeze",
        "category": "Vertical SaaS",
        "target_market": "Small to mid-size construction companies (10-500 employees)",
        "estimated_tam": "$5B-$8B (subset of $120B vertical SaaS opportunity)",
        "pricing_model": "$200-$400/user/month (2-3x premium vs horizontal tools)",
        "key_insight": "Domain expertise + compliance + switching costs = 3x pricing power. Vertical SaaS achieves 120%+ NRR.",
        "market_drivers": [
            "Generic mid-tier SaaS being commoditized by AI",
            "Construction industry underserved by tech",
            "Compliance requirements create lock-in"
        ]
    },
    {
        "id": "ms002", 
        "name": "Vertical SaaS for Veterinary Practice Management",
        "description": "Veterinary-specific practice management combining scheduling, EMR, inventory, and billing. Targets underpriced vertical SaaS opportunity.",
        "source": "Enterprise Pricing Intelligence - Vertical SaaS Premium Gap",
        "category": "Vertical SaaS",
        "target_market": "Veterinary clinics and animal hospitals",
        "estimated_tam": "$2B-$4B (32K vet practices in US, $50K-$120K ACV)",
        "pricing_model": "$300-$500/user/month or $3K-$8K/month flat per clinic",
        "key_insight": "Vertical tools should charge 30-50% premium over horizontal. Vet market has weak incumbents and high willingness to pay.",
        "market_drivers": [
            "Pet care spending grew 38% since 2020",
            "Existing tools underpriced vs value delivered",
            "High switching costs once data is in system"
        ]
    },
    {
        "id": "ms003",
        "name": "SMB AI Automation Platform (Manual Process Killer)",
        "description": "AI automation for SMBs targeting manual processes: invoice processing, commission calculations, data entry. Priced at $99-$499/month vs enterprise RPA at $228K/year.",
        "source": "Enterprise Pricing Intelligence - Enterprise vs SMB Automation Arbitrage",
        "category": "AI Automation",
        "target_market": "SMBs with 10-200 employees doing repetitive manual tasks",
        "estimated_tam": "$8B-$15B (2026-2028 SMB automation market)",
        "pricing_model": "Hybrid: $99-$499/month base + usage (per automation run, per document processed)",
        "key_insight": "Enterprise automation overpriced at $228K/yr with 30-50% failure rate. SMB tools deploy 3-5x faster with AI self-healing. 66% cost savings opportunity.",
        "market_drivers": [
            "AI platforms deploy 3-5x faster than traditional RPA",
            "SMB segment growing 8% faster than enterprise",
            "Labor costs forcing automation adoption"
        ]
    },
    {
        "id": "ms004",
        "name": "Logistics TMS with Per-Shipment Pricing",
        "description": "Transportation Management System for small-mid logistics companies using per-shipment pricing instead of per-seat. Modern usage-based model.",
        "source": "Enterprise Pricing Intelligence - Logistics TMS Pricing Revolution",
        "category": "Vertical SaaS",
        "target_market": "Small-mid logistics companies (10-100 trucks)",
        "estimated_tam": "$3B-$6B (54% of logistics SaaS shifting to per-shipment)",
        "pricing_model": "$2-$5 per shipment vs $150-$300/user/month (better unit economics for customers)",
        "key_insight": "54% of logistics SaaS shifting from per-seat to per-shipment. Aligns pricing with customer value and captures upside from growth.",
        "market_drivers": [
            "Per-seat pricing penalizes growth",
            "Customers prefer paying per transaction",
            "Usage-based preferred by 70% of businesses by 2026"
        ]
    },
    {
        "id": "ms005",
        "name": "SaaS Pricing Advisory Tool (Self-Service)",
        "description": "Self-service pricing intelligence platform for $10K-$100K MRR SaaS companies. Automated pricing analysis, benchmarking, and optimization recommendations.",
        "source": "Enterprise Pricing Intelligence - Founder-Led Underpricing Gap",
        "category": "SaaS Tools",
        "target_market": "Early-stage SaaS founders ($10K-$100K MRR)",
        "estimated_tam": "$500M-$1B (subset of $8B-$15B founder underpricing opportunity)",
        "pricing_model": "$99-$499/month SaaS + optional done-for-you at $2K-$5K",
        "key_insight": "40% of SaaS companies don't revisit pricing annually, leaving 30-40% revenue on table. Founders lack pricing expertise.",
        "market_drivers": [
            "40% of founders don't revisit pricing annually",
            "30-40% revenue left on table",
            "Current consulting at $15K-$50K too expensive for early stage"
        ]
    },
    {
        "id": "ms006",
        "name": "Healthcare Operations Management Platform",
        "description": "Vertical SaaS for outpatient clinics covering patient flow, compliance, staff scheduling, and billing. Targets mid-market SaaS squeeze survivors category.",
        "source": "Enterprise Pricing Intelligence - Mid-Market SaaS Squeeze Survivors",
        "category": "Vertical SaaS",
        "target_market": "Outpatient clinics, urgent care, specialty practices",
        "estimated_tam": "$8B-$12B (150K+ physician practices in US)",
        "pricing_model": "$250-$400/user/month or $5K-$15K/month per practice",
        "key_insight": "Healthcare vertical has domain depth + compliance requirements + switching costs. Can charge 3x premium vs horizontal tools.",
        "market_drivers": [
            "Healthcare IT spending growing 12% annually",
            "Compliance requirements create moat",
            "Labor shortage driving automation"
        ]
    },
    {
        "id": "ms007",
        "name": "AI-Powered Outcome-Based Task Tool",
        "description": "Rebuild commoditized workflows with AI and outcome-based pricing: $2/task completed, $10/analysis, $0.50/document vs traditional per-seat.",
        "source": "Enterprise Pricing Intelligence - AI Feature Premium",
        "category": "AI SaaS",
        "target_market": "Knowledge workers doing repetitive analysis/documentation",
        "estimated_tam": "$5B-$12B (AI outcome-based pricing opportunity)",
        "pricing_model": "Pure usage: $2/task, $10/analysis, $0.50/document (no seats)",
        "key_insight": "90% of 'AI features' are commoditized completions. True outcome-based AI commands premium. Aligns cost with value delivered.",
        "market_drivers": [
            "Per-seat pricing collapsing with AI",
            "Customers want to pay for outcomes not access",
            "LLM APIs enable scalable delivery"
        ]
    },
    {
        "id": "ms008",
        "name": "Usage-Based Billing Infrastructure for SaaS",
        "description": "Billing and metering infrastructure to help SaaS migrate from per-seat to usage-based pricing. Developer-focused tool.",
        "source": "Enterprise Pricing Intelligence - Usage-Based Pricing Migration",
        "category": "SaaS Infrastructure",
        "target_market": "B2B SaaS companies ($100K-$10M ARR) wanting to adopt usage-based pricing",
        "estimated_tam": "$1B-$2B (subset of $25B-$40B migration opportunity)",
        "pricing_model": "$500-$2K/month + 0.5-1% of processed revenue",
        "key_insight": "70% of businesses prefer usage-based by 2026 but most SaaS lacks infrastructure. Billing complexity is main blocker.",
        "market_drivers": [
            "70% prefer usage-based pricing by 2026",
            "Most SaaS built for per-seat, hard to migrate",
            "Stripe/Chargebee not purpose-built for complex metering"
        ]
    }
]

def calculate_score(idea_scores):
    """Calculate weighted validation score"""
    total_score = 0
    for criterion, value in idea_scores.items():
        if criterion in SCORING_CRITERIA:
            weight = SCORING_CRITERIA[criterion]["weight"]
            total_score += value * weight
    return round(total_score, 1)

def score_idea(idea):
    """Apply validation framework scoring to an idea"""
    
    scores = {}
    
    # Market Size scoring
    tam = idea["estimated_tam"]
    if "$1B" in tam or "$2B" in tam or any(f"${x}B" in tam for x in range(3, 20)):
        if any(f"${x}B" in tam for x in range(5, 20)):
            scores["market_size"] = 90
        else:
            scores["market_size"] = 80
    elif "M" in tam:
        scores["market_size"] = 60
    else:
        scores["market_size"] = 70
        
    # Competition scoring based on category and maturity
    if idea["category"] == "Vertical SaaS":
        if "Construction" in idea["name"] or "Veterinary" in idea["name"]:
            scores["competition"] = 80
        elif "Healthcare" in idea["name"]:
            scores["competition"] = 60
        else:
            scores["competition"] = 70
    elif idea["category"] == "AI Automation":
        scores["competition"] = 75
    elif idea["category"] == "SaaS Infrastructure":
        scores["competition"] = 65
    else:
        scores["competition"] = 70
        
    # Technical Feasibility
    if "AI" in idea["name"] or "AI" in idea["description"]:
        scores["technical_feasibility"] = 70
    elif idea["category"] == "Vertical SaaS":
        scores["technical_feasibility"] = 75
    elif "Infrastructure" in idea["category"]:
        scores["technical_feasibility"] = 60
    else:
        scores["technical_feasibility"] = 75
        
    # Monetization clarity
    if "pricing_model" in idea and "$" in idea["pricing_model"]:
        if "proven" in idea["key_insight"].lower() or "willingness to pay" in idea["key_insight"].lower():
            scores["monetization"] = 90
        elif "30-50% premium" in idea["key_insight"] or "3x pricing power" in idea["key_insight"]:
            scores["monetization"] = 85
        else:
            scores["monetization"] = 75
    else:
        scores["monetization"] = 60
        
    # Time to Market
    if idea["category"] == "Vertical SaaS":
        scores["time_to_market"] = 70
    elif "AI" in idea["category"]:
        scores["time_to_market"] = 75
    elif "Infrastructure" in idea["category"]:
        scores["time_to_market"] = 60
    else:
        scores["time_to_market"] = 70
        
    total_score = calculate_score(scores)
    
    return {
        **idea,
        "validation_scores": scores,
        "total_score": total_score,
        "grade": get_grade(total_score)
    }

def get_grade(score):
    """Convert score to letter grade"""
    if score >= 85:
        return "A"
    elif score >= 80:
        return "A-"
    elif score >= 75:
        return "B+"
    elif score >= 70:
        return "B"
    elif score >= 65:
        return "B-"
    else:
        return "C"

def main():
    print("=" * 80)
    print("MICRO SAAS VALIDATION FRAMEWORK")
    print("=" * 80)
    print()
    
    scored_ideas = [score_idea(idea) for idea in MICRO_SAAS_IDEAS]
    scored_ideas.sort(key=lambda x: x["total_score"], reverse=True)
    
    print(f"Validated {len(scored_ideas)} micro SaaS ideas")
    print()
    print("SCORING CRITERIA:")
    for criterion, config in SCORING_CRITERIA.items():
        print(f"  • {criterion.replace('_', ' ').title()}: {int(config['weight']*100)}% weight")
    print()
    
    output_date = datetime.now().strftime("%Y%m%d")
    output_file = f"data/micro_saas_validation_{output_date}.json"
    
    output_data = {
        "scan_date": datetime.now().isoformat(),
        "scan_type": "Micro SaaS Validation",
        "total_ideas": len(scored_ideas),
        "scoring_criteria": SCORING_CRITERIA,
        "validated_ideas": scored_ideas
    }
    
    Path("data").mkdir(exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"✓ Saved validation data to {output_file}")
    print()
    
    print("TOP 5 MICRO SAAS IDEAS (by validation score):")
    print()
    for i, idea in enumerate(scored_ideas[:5], 1):
        print(f"{i}. {idea['name']} - Score: {idea['total_score']}/100 (Grade: {idea['grade']})")
        print(f"   Category: {idea['category']}")
        print(f"   TAM: {idea['estimated_tam']}")
        print(f"   Scores: Market={idea['validation_scores']['market_size']}, "
              f"Competition={idea['validation_scores']['competition']}, "
              f"Tech={idea['validation_scores']['technical_feasibility']}, "
              f"Monetization={idea['validation_scores']['monetization']}, "
              f"TTM={idea['validation_scores']['time_to_market']}")
        print()
    
    return output_file

if __name__ == "__main__":
    output_file = main()
    print(f"Validation complete. Results saved to {output_file}")
