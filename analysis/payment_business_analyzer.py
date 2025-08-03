import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

class PaymentBusinessAnalyzer:
    """Advanced analyzer for social media payment business ecosystems."""
    
    def __init__(self):
        self.business_models = {
            "affiliate_marketing": {
                "commission_rates": {"low": 0.02, "medium": 0.05, "high": 0.12},
                "conversion_attribution_window": 30,  # days
                "average_cookie_duration": 7,  # days
                "cross_platform_tracking": True
            },
            "direct_sales": {
                "platform_fees": {"instagram": 0.05, "twitter": 0.03, "youtube": 0.45, "tiktok": 0.02},
                "payment_processing": 0.029,  # Stripe average
                "chargeback_rate": 0.015,
                "return_rate": 0.08
            },
            "subscription_conversion": {
                "free_trial_conversion": 0.15,
                "monthly_to_annual_upgrade": 0.25,
                "churn_rates": {"monthly": 0.05, "annual": 0.02},
                "customer_acquisition_cost": {"organic": 25, "paid": 75, "influencer": 45}
            },
            "in_app_purchases": {
                "mobile_conversion_rates": {"ios": 0.04, "android": 0.02},
                "average_session_value": {"gaming": 12.50, "shopping": 45.20, "productivity": 8.90},
                "retention_impact": {"first_purchase": 0.3, "repeat_purchaser": 0.7}
            }
        }
        
        self.market_segments = {
            "micro_influencers": {
                "follower_range": (1000, 10000),
                "engagement_rate": (0.05, 0.15),
                "cost_per_post": (50, 500),
                "conversion_rate": 0.035,
                "authenticity_score": 0.85
            },
            "macro_influencers": {
                "follower_range": (100000, 1000000),
                "engagement_rate": (0.02, 0.08),
                "cost_per_post": (1000, 10000),
                "conversion_rate": 0.025,
                "authenticity_score": 0.70
            },
            "mega_influencers": {
                "follower_range": (1000000, 50000000),
                "engagement_rate": (0.01, 0.05),
                "cost_per_post": (10000, 500000),
                "conversion_rate": 0.015,
                "authenticity_score": 0.60
            }
        }
        
        # Bot impact on payment businesses
        self.bot_impact_models = {
            "fake_engagement_inflation": {
                "like_farms": {"cost_per_1000": 5, "detection_rate": 0.75, "business_damage": 0.15},
                "comment_farms": {"cost_per_1000": 15, "detection_rate": 0.65, "business_damage": 0.25},
                "follower_farms": {"cost_per_1000": 8, "detection_rate": 0.85, "business_damage": 0.30}
            },
            "conversion_fraud": {
                "fake_clicks": {"cost_per_click": 0.1, "conversion_rate": 0.001, "attribution_pollution": 0.2},
                "bot_purchases": {"detection_rate": 0.9, "chargeback_rate": 0.8, "account_ban_rate": 0.95},
                "review_manipulation": {"cost_per_review": 2, "trust_degradation": 0.4, "long_term_damage": 0.6}
            },
            "algorithm_manipulation": {
                "trending_hijacking": {"cost": 500, "reach_amplification": 10, "sustainability": 0.1},
                "hashtag_flooding": {"cost": 200, "visibility_boost": 3, "platform_penalty_risk": 0.7},
                "coordinated_sharing": {"cost": 1000, "viral_simulation": 15, "detection_sophistication": 0.8}
            }
        }
    
    def analyze_social_commerce_ecosystem(self, platform_data):
        """Comprehensive analysis of social commerce ecosystem."""
        
        analysis = {
            "ecosystem_health": self._calculate_ecosystem_health(platform_data),
            "revenue_streams": self._analyze_revenue_streams(platform_data),
            "bot_contamination": self._assess_bot_contamination(platform_data),
            "market_efficiency": self._evaluate_market_efficiency(platform_data),
            "business_sustainability": self._project_business_sustainability(platform_data)
        }
        
        return analysis
    
    def _calculate_ecosystem_health(self, platform_data):
        """Calculate overall health of the social commerce ecosystem."""
        
        # Extract key metrics
        total_users = len(platform_data.get("real_users", [])) + len(platform_data.get("bots", []))
        real_users = len(platform_data.get("real_users", []))
        bot_ratio = 1 - (real_users / total_users) if total_users > 0 else 0
        
        engagement_events = platform_data.get("engagement_log", [])
        real_engagement = len([e for e in engagement_events if e.get("user_type") == "real"])
        total_engagement = len(engagement_events)
        organic_engagement_ratio = real_engagement / total_engagement if total_engagement > 0 else 0
        
        # Calculate conversion quality
        payment_events = platform_data.get("payment_business_events", [])
        legitimate_conversions = len([e for e in payment_events if e.get("user_type") != "bot"])
        
        # Health score calculation
        authenticity_score = organic_engagement_ratio * 0.4 + (1 - bot_ratio) * 0.3 + min(legitimate_conversions / 100, 1) * 0.3
        
        return {
            "overall_health_score": authenticity_score,
            "bot_contamination_level": bot_ratio,
            "organic_engagement_ratio": organic_engagement_ratio,
            "legitimate_conversion_rate": legitimate_conversions / len(payment_events) if payment_events else 0,
            "ecosystem_sustainability": "high" if authenticity_score > 0.8 else "medium" if authenticity_score > 0.6 else "low",
            "trust_degradation_risk": bot_ratio * 0.7 + (1 - organic_engagement_ratio) * 0.3
        }
    
    def _analyze_revenue_streams(self, platform_data):
        """Analyze different revenue streams and their performance."""
        
        revenue_analysis = {}
        
        # Affiliate marketing analysis
        affiliate_conversions = [e for e in platform_data.get("payment_business_events", []) 
                               if e.get("attribution_source") in ["affiliate_link", "promo_code"]]
        
        affiliate_revenue = sum([
            e.get("transaction_value", 0) * self.business_models["affiliate_marketing"]["commission_rates"]["medium"]
            for e in affiliate_conversions
        ])
        
        # Direct sales analysis
        direct_sales = [e for e in platform_data.get("payment_business_events", []) 
                       if e.get("attribution_source") == "direct_purchase"]
        
        direct_revenue = sum([e.get("transaction_value", 0) for e in direct_sales])
        platform_fees = direct_revenue * self.business_models["direct_sales"]["platform_fees"]["instagram"]
        
        # Subscription analysis
        subscription_events = [e for e in platform_data.get("payment_business_events", []) 
                             if "subscription" in e.get("event_type", "")]
        
        subscription_revenue = sum([e.get("transaction_value", 0) for e in subscription_events])
        
        revenue_analysis = {
            "affiliate_marketing": {
                "total_revenue": affiliate_revenue,
                "conversion_count": len(affiliate_conversions),
                "average_commission": affiliate_revenue / len(affiliate_conversions) if affiliate_conversions else 0,
                "performance_trend": "increasing" if len(affiliate_conversions) > 10 else "stable"
            },
            "direct_sales": {
                "gross_revenue": direct_revenue,
                "platform_fees": platform_fees,
                "net_revenue": direct_revenue - platform_fees,
                "conversion_count": len(direct_sales),
                "average_order_value": direct_revenue / len(direct_sales) if direct_sales else 0
            },
            "subscriptions": {
                "total_revenue": subscription_revenue,
                "subscriber_count": len(subscription_events),
                "average_subscription_value": subscription_revenue / len(subscription_events) if subscription_events else 0,
                "projected_annual_revenue": subscription_revenue * 12
            },
            "total_ecosystem_revenue": affiliate_revenue + direct_revenue + subscription_revenue
        }
        
        return revenue_analysis
    
    def _assess_bot_contamination(self, platform_data):
        """Assess the level and impact of bot contamination."""
        
        engagement_events = platform_data.get("engagement_log", [])
        bot_events = [e for e in engagement_events if e.get("user_type") == "bot"]
        
        # Bot type analysis
        bot_type_distribution = {}
        for event in bot_events:
            bot_type = event.get("bot_type", "unknown")
            bot_type_distribution[bot_type] = bot_type_distribution.get(bot_type, 0) + 1
        
        # Calculate financial impact
        fake_engagement_cost = sum([
            self.bot_impact_models["fake_engagement_inflation"]["like_farms"]["business_damage"] * 
            event.get("business_impact", {}).get("operation_cost", 0)
            for event in bot_events if event.get("action") == "like"
        ])
        
        algorithm_manipulation_impact = len([
            e for e in bot_events if e.get("coordinated_activity", False)
        ]) * self.bot_impact_models["algorithm_manipulation"]["coordinated_sharing"]["cost"]
        
        trust_degradation_cost = len(bot_events) * 0.5  # $0.50 per fake engagement in trust cost
        
        return {
            "bot_contamination_percentage": len(bot_events) / len(engagement_events) * 100 if engagement_events else 0,
            "bot_type_distribution": bot_type_distribution,
            "financial_impact": {
                "fake_engagement_cost": fake_engagement_cost,
                "algorithm_manipulation_cost": algorithm_manipulation_impact,
                "trust_degradation_cost": trust_degradation_cost,
                "total_bot_damage": fake_engagement_cost + algorithm_manipulation_impact + trust_degradation_cost
            },
            "detection_efficacy": {
                "detected_bots": len([e for e in bot_events if e.get("detection_risk_score", 0) > 0.7]),
                "undetected_bots": len([e for e in bot_events if e.get("detection_risk_score", 0) <= 0.7]),
                "detection_rate": len([e for e in bot_events if e.get("detection_risk_score", 0) > 0.7]) / len(bot_events) if bot_events else 0
            },
            "impact_on_metrics": {
                "engagement_inflation": len(bot_events) / len(engagement_events) if engagement_events else 0,
                "conversion_pollution": len([e for e in bot_events if e.get("business_impact", {}).get("conversion_occurred")]),
                "social_proof_contamination": sum([e.get("business_impact", {}).get("social_proof_value", 0) for e in bot_events])
            }
        }
    
    def _evaluate_market_efficiency(self, platform_data):
        """Evaluate the efficiency of the social media marketing ecosystem."""
        
        # Calculate return on ad spend (ROAS)
        total_marketing_spend = sum([
            influencer.get("revenue_per_post", 0) 
            for influencer in platform_data.get("influencers", [])
        ])
        
        total_revenue = sum([
            event.get("transaction_value", 0) 
            for event in platform_data.get("payment_business_events", [])
        ])
        
        roas = total_revenue / total_marketing_spend if total_marketing_spend > 0 else 0
        
        # Calculate customer acquisition cost (CAC)
        total_conversions = len(platform_data.get("payment_business_events", []))
        cac = total_marketing_spend / total_conversions if total_conversions > 0 else 0
        
        # Calculate lifetime value (LTV)
        average_transaction_value = total_revenue / total_conversions if total_conversions > 0 else 0
        estimated_ltv = average_transaction_value * 3.5  # Industry average multiplier
        
        # Market efficiency metrics
        efficiency_score = min(roas / 3, 1) * 0.4 + min(estimated_ltv / cac / 3, 1) * 0.6 if cac > 0 else 0
        
        return {
            "return_on_ad_spend": roas,
            "customer_acquisition_cost": cac,
            "estimated_customer_lifetime_value": estimated_ltv,
            "ltv_to_cac_ratio": estimated_ltv / cac if cac > 0 else 0,
            "market_efficiency_score": efficiency_score,
            "cost_per_engagement": total_marketing_spend / len(platform_data.get("engagement_log", [])) if platform_data.get("engagement_log") else 0,
            "conversion_rate": total_conversions / len(platform_data.get("engagement_log", [])) if platform_data.get("engagement_log") else 0,
            "revenue_per_engagement": total_revenue / len(platform_data.get("engagement_log", [])) if platform_data.get("engagement_log") else 0
        }
    
    def _project_business_sustainability(self, platform_data):
        """Project the long-term sustainability of current business models."""
        
        # Trend analysis
        engagement_events = platform_data.get("engagement_log", [])
        payment_events = platform_data.get("payment_business_events", [])
        
        # Group events by time periods for trend analysis
        daily_engagement = {}
        daily_revenue = {}
        
        for event in engagement_events:
            date = event.get("timestamp", "")[:10]  # Extract date
            daily_engagement[date] = daily_engagement.get(date, 0) + 1
        
        for event in payment_events:
            date = event.get("timestamp", "")[:10]
            daily_revenue[date] = daily_revenue.get(date, 0) + event.get("transaction_value", 0)
        
        # Calculate growth rates
        sorted_dates = sorted(daily_engagement.keys())
        if len(sorted_dates) >= 2:
            early_engagement = sum([daily_engagement[date] for date in sorted_dates[:len(sorted_dates)//2]])
            late_engagement = sum([daily_engagement[date] for date in sorted_dates[len(sorted_dates)//2:]])
            engagement_growth_rate = (late_engagement - early_engagement) / early_engagement if early_engagement > 0 else 0
            
            early_revenue = sum([daily_revenue.get(date, 0) for date in sorted_dates[:len(sorted_dates)//2]])
            late_revenue = sum([daily_revenue.get(date, 0) for date in sorted_dates[len(sorted_dates)//2:]])
            revenue_growth_rate = (late_revenue - early_revenue) / early_revenue if early_revenue > 0 else 0
        else:
            engagement_growth_rate = 0
            revenue_growth_rate = 0
        
        # Bot contamination trend
        bot_events = [e for e in engagement_events if e.get("user_type") == "bot"]
        bot_contamination_rate = len(bot_events) / len(engagement_events) if engagement_events else 0
        
        # Sustainability factors
        sustainability_score = (
            min(max(engagement_growth_rate, -0.5), 0.5) * 0.3 +  # Engagement growth (capped)
            min(max(revenue_growth_rate, -0.5), 0.5) * 0.4 +      # Revenue growth (capped)
            (1 - bot_contamination_rate) * 0.3                     # Bot contamination (inverted)
        )
        
        return {
            "engagement_growth_rate": engagement_growth_rate,
            "revenue_growth_rate": revenue_growth_rate,
            "bot_contamination_trend": bot_contamination_rate,
            "sustainability_score": sustainability_score,
            "sustainability_rating": (
                "high" if sustainability_score > 0.7 else
                "medium" if sustainability_score > 0.4 else
                "low"
            ),
            "projected_12_month_revenue": sum(daily_revenue.values()) * 12 if daily_revenue else 0,
            "risk_factors": [
                "bot_contamination" if bot_contamination_rate > 0.3 else None,
                "declining_engagement" if engagement_growth_rate < -0.1 else None,
                "revenue_stagnation" if revenue_growth_rate < 0.05 else None
            ],
            "recommendations": self._generate_sustainability_recommendations(
                engagement_growth_rate, revenue_growth_rate, bot_contamination_rate
            )
        }
    
    def _generate_sustainability_recommendations(self, engagement_growth, revenue_growth, bot_contamination):
        """Generate actionable recommendations for business sustainability."""
        
        recommendations = []
        
        if bot_contamination > 0.3:
            recommendations.append({
                "priority": "high",
                "category": "bot_mitigation",
                "action": "Implement advanced bot detection systems",
                "expected_impact": "Reduce bot contamination by 60-80%",
                "cost_estimate": "$50,000 - $200,000 initial investment"
            })
        
        if engagement_growth < 0:
            recommendations.append({
                "priority": "high",
                "category": "engagement_optimization",
                "action": "Diversify content strategy and improve targeting",
                "expected_impact": "Increase organic engagement by 25-40%",
                "cost_estimate": "$20,000 - $50,000 monthly"
            })
        
        if revenue_growth < 0.05:
            recommendations.append({
                "priority": "medium",
                "category": "monetization_optimization",
                "action": "A/B test pricing strategies and payment flows",
                "expected_impact": "Improve conversion rates by 15-30%",
                "cost_estimate": "$10,000 - $30,000 for testing infrastructure"
            })
        
        # Always include general recommendations
        recommendations.extend([
            {
                "priority": "medium",
                "category": "data_analytics",
                "action": "Implement comprehensive attribution tracking",
                "expected_impact": "Improve marketing ROI visibility by 50%",
                "cost_estimate": "$15,000 - $40,000 setup cost"
            },
            {
                "priority": "low",
                "category": "compliance",
                "action": "Ensure GDPR/CCPA compliance for payment data",
                "expected_impact": "Reduce legal risk and improve user trust",
                "cost_estimate": "$5,000 - $15,000 for compliance audit"
            }
        ])
        
        return recommendations
    
    def generate_comprehensive_report(self, platform_data):
        """Generate a comprehensive analysis report."""
        
        analysis = self.analyze_social_commerce_ecosystem(platform_data)
        
        report = {
            "executive_summary": {
                "overall_health": analysis["ecosystem_health"]["overall_health_score"],
                "total_revenue": analysis["revenue_streams"]["total_ecosystem_revenue"],
                "bot_impact": analysis["bot_contamination"]["financial_impact"]["total_bot_damage"],
                "market_efficiency": analysis["market_efficiency"]["market_efficiency_score"],
                "sustainability_outlook": analysis["business_sustainability"]["sustainability_rating"]
            },
            "detailed_analysis": analysis,
            "actionable_insights": {
                "immediate_actions": [r for r in analysis["business_sustainability"]["recommendations"] if r["priority"] == "high"],
                "medium_term_goals": [r for r in analysis["business_sustainability"]["recommendations"] if r["priority"] == "medium"],
                "long_term_strategy": [r for r in analysis["business_sustainability"]["recommendations"] if r["priority"] == "low"]
            },
            "financial_projections": {
                "current_monthly_revenue": analysis["revenue_streams"]["total_ecosystem_revenue"],
                "projected_annual_revenue": analysis["business_sustainability"]["projected_12_month_revenue"],
                "potential_savings_from_bot_mitigation": analysis["bot_contamination"]["financial_impact"]["total_bot_damage"] * 0.7,
                "roi_improvement_potential": analysis["market_efficiency"]["return_on_ad_spend"] * 1.3
            },
            "risk_assessment": {
                "high_risk_factors": [f for f in analysis["business_sustainability"]["risk_factors"] if f],
                "mitigation_strategies": analysis["business_sustainability"]["recommendations"],
                "compliance_considerations": ["GDPR compliance", "Payment data security", "Advertising transparency"],
                "platform_dependency_risk": "high" if len(set([e.get("platform") for e in platform_data.get("engagement_log", [])])) < 3 else "medium"
            }
        }
        
        return report

# Usage example and test data generation
def generate_sample_payment_business_data():
    """Generate sample data for testing the payment business analyzer."""
    
    sample_data = {
        "influencers": [
            {
                "influencer_id": "inf_001",
                "username": "@fashionista_pro",
                "follower_count": 50000,
                "engagement_rate": 0.08,
                "business_type": "e_commerce",
                "revenue_per_post": 2500,
                "conversion_rate": 0.025
            },
            {
                "influencer_id": "inf_002", 
                "username": "@tech_reviewer",
                "follower_count": 200000,
                "engagement_rate": 0.05,
                "business_type": "affiliate_marketing",
                "revenue_per_post": 5000,
                "conversion_rate": 0.02
            }
        ],
        "real_users": [{"user_id": f"user_{i}", "age_group": "25-34", "purchase_behavior": {"average_purchase_value": random.uniform(50, 300)}} for i in range(100)],
        "bots": [{"bot_id": f"bot_{i}", "bot_type": "engagement_amplifier"} for i in range(25)],
        "engagement_log": [
            {
                "timestamp": datetime.now().isoformat(),
                "user_type": "real" if random.random() > 0.2 else "bot",
                "action": random.choice(["like", "share", "comment"]),
                "business_impact": {"conversion_occurred": random.random() < 0.03}
            }
            for _ in range(500)
        ],
        "payment_business_events": [
            {
                "timestamp": datetime.now().isoformat(),
                "event_type": "conversion",
                "transaction_value": random.uniform(25, 500),
                "attribution_source": random.choice(["affiliate_link", "direct_purchase", "promo_code"])
            }
            for _ in range(25)
        ]
    }
    
    return sample_data

if __name__ == "__main__":
    # Test the payment business analyzer
    analyzer = PaymentBusinessAnalyzer()
    sample_data = generate_sample_payment_business_data()
    
    print("=== Payment Business Analysis Report ===")
    report = analyzer.generate_comprehensive_report(sample_data)
    
    print(f"Overall Health Score: {report['executive_summary']['overall_health']:.2f}")
    print(f"Total Revenue: ${report['executive_summary']['total_revenue']:.2f}")
    print(f"Bot Impact Cost: ${report['executive_summary']['bot_impact']:.2f}")
    print(f"Market Efficiency: {report['executive_summary']['market_efficiency']:.2f}")
    print(f"Sustainability Outlook: {report['executive_summary']['sustainability_outlook']}")
    
    # Save comprehensive analysis
    import os
    os.makedirs("../data", exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"../data/payment_business_analysis_{timestamp}.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\nComprehensive analysis saved to: ../data/payment_business_analysis_{timestamp}.json")
