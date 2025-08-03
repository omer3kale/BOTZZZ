import random
import json
import time
import numpy as np
from datetime import datetime, timedelta
import uuid
import hashlib
import requests
from typing import Dict, List, Optional

def scale_parameters(scale_factor=1):
    """Scale simulation parameters for large-scale influencer analysis."""
    global NUM_INFLUENCERS, NUM_REAL_USERS, NUM_BOTS, NUM_CONTENT, SIMULATION_STEPS
    NUM_INFLUENCERS = int(NUM_INFLUENCERS * scale_factor)
    NUM_REAL_USERS = int(NUM_REAL_USERS * scale_factor)
    NUM_BOTS = int(NUM_BOTS * scale_factor)
    NUM_CONTENT = int(NUM_CONTENT * scale_factor)
    SIMULATION_STEPS = int(SIMULATION_STEPS * scale_factor)
    print(f"TikTok Influencer Parameters scaled by factor {scale_factor}:")
    print(f"NUM_INFLUENCERS: {NUM_INFLUENCERS}")
    print(f"NUM_REAL_USERS: {NUM_REAL_USERS}")
    print(f"NUM_BOTS: {NUM_BOTS}")
    print(f"NUM_CONTENT: {NUM_CONTENT}")
    print(f"SIMULATION_STEPS: {SIMULATION_STEPS}")

# TikTok Influencer Simulation Parameters
NUM_INFLUENCERS = 15
NUM_REAL_USERS = 500
NUM_BOTS = 150
NUM_CONTENT = 25
SIMULATION_STEPS = 100

# Real-time TikTok Market Data (2024-2025)
TIKTOK_MARKET_DATA = {
    "global_statistics": {
        "monthly_active_users": 1500000000,  # 1.5 billion MAU
        "daily_active_users": 1000000000,    # 1 billion DAU
        "average_time_spent_daily": 95,      # minutes
        "videos_uploaded_daily": 34000000,   # 34 million videos/day
        "creator_fund_size": 2000000000,     # $2 billion
        "advertising_revenue_2024": 18500000000  # $18.5 billion
    },
    "influencer_economics": {
        "tier_1_mega": {
            "followers_range": (10000000, 100000000),
            "avg_views_per_video": (5000000, 50000000),
            "cpm_usd": (2.5, 8.0),
            "brand_deal_value": (50000, 1000000),
            "conversion_rate": 0.045,  # 4.5% average
            "engagement_rate": 0.08    # 8% average
        },
        "tier_2_macro": {
            "followers_range": (1000000, 10000000),
            "avg_views_per_video": (500000, 5000000),
            "cpm_usd": (1.8, 5.5),
            "brand_deal_value": (10000, 100000),
            "conversion_rate": 0.065,  # 6.5% higher engagement
            "engagement_rate": 0.12    # 12% average
        },
        "tier_3_micro": {
            "followers_range": (100000, 1000000),
            "avg_views_per_video": (50000, 500000),
            "cpm_usd": (1.2, 3.5),
            "brand_deal_value": (1000, 25000),
            "conversion_rate": 0.085,  # 8.5% micro-influencer advantage
            "engagement_rate": 0.18    # 18% average
        },
        "tier_4_nano": {
            "followers_range": (10000, 100000),
            "avg_views_per_video": (5000, 50000),
            "cpm_usd": (0.8, 2.0),
            "brand_deal_value": (500, 5000),
            "conversion_rate": 0.12,   # 12% highest conversion
            "engagement_rate": 0.25    # 25% average
        }
    },
    "product_categories": {
        "beauty_cosmetics": {
            "market_size_billion": 147.8,
            "social_commerce_share": 0.34,
            "avg_order_value": 45.20,
            "conversion_rate": 0.078,
            "return_rate": 0.12,
            "paypal_usage": 0.67
        },
        "fashion_apparel": {
            "market_size_billion": 368.2,
            "social_commerce_share": 0.28,
            "avg_order_value": 89.50,
            "conversion_rate": 0.052,
            "return_rate": 0.18,
            "paypal_usage": 0.58
        },
        "health_fitness": {
            "market_size_billion": 96.7,
            "social_commerce_share": 0.31,
            "avg_order_value": 67.80,
            "conversion_rate": 0.069,
            "return_rate": 0.09,
            "paypal_usage": 0.72
        },
        "tech_gadgets": {
            "market_size_billion": 124.5,
            "social_commerce_share": 0.22,
            "avg_order_value": 156.30,
            "conversion_rate": 0.034,
            "return_rate": 0.14,
            "paypal_usage": 0.81
        },
        "food_beverage": {
            "market_size_billion": 78.9,
            "social_commerce_share": 0.19,
            "avg_order_value": 32.40,
            "conversion_rate": 0.089,
            "return_rate": 0.06,
            "paypal_usage": 0.63
        }
    },
    "geographic_markets": {
        "north_america": {
            "user_base": 150000000,
            "avg_cpm": 3.2,
            "purchasing_power": "high",
            "paypal_penetration": 0.78,
            "conversion_premium": 1.2
        },
        "europe": {
            "user_base": 100000000,
            "avg_cpm": 2.8,
            "purchasing_power": "high",
            "paypal_penetration": 0.65,
            "conversion_premium": 1.1
        },
        "asia_pacific": {
            "user_base": 800000000,
            "avg_cpm": 1.4,
            "purchasing_power": "medium",
            "paypal_penetration": 0.42,
            "conversion_premium": 0.9
        },
        "latin_america": {
            "user_base": 120000000,
            "avg_cpm": 1.1,
            "purchasing_power": "medium",
            "paypal_penetration": 0.38,
            "conversion_premium": 0.8
        }
    }
}

# Enhanced TikTok Bot Types with Influencer Focus
TIKTOK_BOT_TYPES = {
    "follower_boost_bot": {
        "description": "Rapid follower inflation for influencer credibility",
        "behavior": {
            "follow_rate": 0.95,
            "engagement_rate": 0.02,
            "like_rate": 0.08,
            "comment_rate": 0.01,
            "share_rate": 0.005,
            "view_completion": 0.15,  # Low completion rate
            "operation_speed": "high",
            "detection_difficulty": "low"
        },
        "economics": {
            "cost_per_follow": 0.008,
            "bulk_pricing": True,
            "minimum_order": 1000,
            "delivery_time_hours": 24
        },
        "detection_signatures": {
            "rapid_following_sprees": True,
            "low_profile_completion": True,
            "inactive_after_follow": True,
            "geographic_clustering": True,
            "account_age_patterns": True
        }
    },
    "engagement_amplifier": {
        "description": "Boost post engagement metrics for algorithm favor",
        "behavior": {
            "follow_rate": 0.15,
            "engagement_rate": 0.85,
            "like_rate": 0.90,
            "comment_rate": 0.25,
            "share_rate": 0.15,
            "view_completion": 0.75,  # High completion for algorithm
            "operation_speed": "medium",
            "detection_difficulty": "medium"
        },
        "economics": {
            "cost_per_engagement": 0.015,
            "package_deals": True,
            "targeting_premium": 1.5,
            "delivery_time_hours": 6
        },
        "detection_signatures": {
            "synchronized_engagement": True,
            "engagement_velocity_spikes": True,
            "similar_interaction_patterns": True,
            "coordinated_timing": True
        }
    },
    "viral_manipulation_bot": {
        "description": "Artificially trigger viral algorithm patterns",
        "behavior": {
            "follow_rate": 0.25,
            "engagement_rate": 0.95,
            "like_rate": 0.95,
            "comment_rate": 0.45,
            "share_rate": 0.35,
            "view_completion": 0.85,
            "operation_speed": "coordinated",
            "detection_difficulty": "high"
        },
        "economics": {
            "cost_per_viral_push": 150.0,
            "success_rate": 0.65,
            "roi_multiplier": 8.2,
            "delivery_time_hours": 3
        },
        "detection_signatures": {
            "unnatural_viral_velocity": True,
            "cross_platform_coordination": True,
            "engagement_pattern_anomalies": True,
            "geographic_impossibilities": True
        }
    },
    "conversion_funnel_bot": {
        "description": "Drive traffic to external payment sites",
        "behavior": {
            "follow_rate": 0.35,
            "engagement_rate": 0.70,
            "like_rate": 0.75,
            "comment_rate": 0.40,
            "share_rate": 0.25,
            "link_click_rate": 0.85,  # High external link engagement
            "view_completion": 0.65,
            "operation_speed": "targeted",
            "detection_difficulty": "high"
        },
        "economics": {
            "cost_per_click": 0.25,
            "conversion_tracking": True,
            "paypal_integration_bonus": 1.3,
            "delivery_time_hours": 2
        },
        "detection_signatures": {
            "high_external_link_ratio": True,
            "payment_site_focus": True,
            "conversion_funnel_patterns": True,
            "click_through_rate_anomalies": True
        }
    },
    "sophisticated_ai_influencer_bot": {
        "description": "Advanced AI mimicking real influencer audience behavior",
        "behavior": {
            "follow_rate": 0.18,
            "engagement_rate": 0.35,
            "like_rate": 0.45,
            "comment_rate": 0.12,
            "share_rate": 0.08,
            "view_completion": 0.72,
            "comment_sophistication": "high",
            "operation_speed": "human_like",
            "detection_difficulty": "very_high"
        },
        "economics": {
            "cost_per_interaction": 0.08,
            "ai_premium": 2.5,
            "human_like_guarantee": True,
            "delivery_time_hours": 12
        },
        "detection_signatures": {
            "ai_text_patterns": True,
            "consistent_behavioral_metrics": True,
            "scheduled_activity_windows": True,
            "limited_platform_diversity": True
        }
    }
}

# PayPal Integration Patterns for Influencer Commerce
PAYPAL_COMMERCE_PATTERNS = {
    "influencer_payment_flows": {
        "direct_product_sales": {
            "conversion_rate": 0.068,
            "average_cart_value": 67.50,
            "paypal_fee_percentage": 0.0349,
            "chargeback_rate": 0.012,
            "customer_satisfaction": 0.87
        },
        "affiliate_commissions": {
            "commission_rate": (0.05, 0.25),
            "payment_frequency": "monthly",
            "minimum_payout": 50.0,
            "paypal_fee_percentage": 0.0199,
            "delayed_payment_risk": 0.08
        },
        "brand_sponsorship_payments": {
            "payment_size_range": (500, 50000),
            "payment_timing": "milestone_based",
            "international_fees": 0.045,
            "tax_withholding": 0.24,
            "dispute_rate": 0.03
        },
        "fan_donations_tips": {
            "average_donation": 12.30,
            "recurring_donor_rate": 0.34,
            "paypal_fee_percentage": 0.0349,
            "fraud_detection_accuracy": 0.94
        }
    },
    "payment_security_metrics": {
        "fraud_detection_rate": 0.996,
        "false_positive_rate": 0.004,
        "dispute_resolution_time_days": 14,
        "merchant_protection_coverage": 0.89,
        "buyer_protection_claims": 0.015
    },
    "conversion_optimization": {
        "one_click_checkout": {
            "conversion_lift": 0.23,
            "cart_abandonment_reduction": 0.31,
            "mobile_optimization": 0.89
        },
        "express_checkout": {
            "checkout_time_reduction": 0.67,
            "conversion_rate_improvement": 0.18,
            "user_satisfaction_score": 0.91
        }
    }
}

# Enhanced Network Forensics for TikTok
TIKTOK_NETWORK_PATTERNS = {
    "real_users": {
        "mobile_primary": 0.89,  # TikTok is mobile-first
        "connection_types": [
            {"type": "mobile_5g", "speed_mbps": (50, 500), "latency_ms": (15, 40), "weight": 0.35},
            {"type": "mobile_4g", "speed_mbps": (5, 50), "latency_ms": (30, 80), "weight": 0.45},
            {"type": "wifi", "speed_mbps": (25, 300), "latency_ms": (10, 30), "weight": 0.20}
        ],
        "video_quality_preferences": ["720p", "1080p", "auto"],
        "data_usage_awareness": True
    },
    "bots": {
        "mobile_emulation": 0.95,  # Bots must appear mobile
        "connection_types": [
            {"type": "datacenter_mobile_proxy", "speed_mbps": (100, 1000), "latency_ms": (5, 15), "weight": 0.6},
            {"type": "residential_mobile_proxy", "speed_mbps": (20, 100), "latency_ms": (20, 60), "weight": 0.3},
            {"type": "vpn_mobile", "speed_mbps": (10, 50), "latency_ms": (50, 150), "weight": 0.1}
        ],
        "suspicious_indicators": [
            "consistent_mobile_model_patterns",
            "identical_app_versions",
            "synchronized_location_updates",
            "unrealistic_data_usage_patterns"
        ]
    }
}

# TikTok Behavioral Patterns
TIKTOK_BEHAVIORAL_PATTERNS = {
    "real_users": {
        "scroll_velocity_pixels_per_second": (100, 800),
        "video_completion_rate": (0.45, 0.85),
        "interaction_delay_ms": (500, 3000),
        "multi_tasking_probability": 0.7,
        "sound_on_probability": 0.75,
        "full_screen_preference": 0.95
    },
    "bots": {
        "scroll_velocity_pixels_per_second": (200, 400),  # Too consistent
        "video_completion_rate": (0.15, 0.95),  # Depends on bot type
        "interaction_delay_ms": (100, 500),  # Too fast
        "robotic_scroll_patterns": True,
        "no_sound_interaction": True,
        "perfect_video_centering": True
    }
}

def generate_tiktok_influencer_profile(tier: str) -> Dict:
    """Generate realistic TikTok influencer with payment integration."""
    tier_data = TIKTOK_MARKET_DATA["influencer_economics"][tier]
    
    # Select product category based on influencer type
    categories = list(TIKTOK_MARKET_DATA["product_categories"].keys())
    weights = [0.35, 0.25, 0.15, 0.15, 0.10]  # Beauty/Fashion dominant
    category = random.choices(categories, weights=weights)[0]
    category_data = TIKTOK_MARKET_DATA["product_categories"][category]
    
    # Geographic focus
    geographic_markets = list(TIKTOK_MARKET_DATA["geographic_markets"].keys())
    geo_weights = [0.4, 0.25, 0.25, 0.1]
    primary_market = random.choices(geographic_markets, weights=geo_weights)[0]
    market_data = TIKTOK_MARKET_DATA["geographic_markets"][primary_market]
    
    followers = random.randint(*tier_data["followers_range"])
    
    influencer = {
        "influencer_id": f"tiktok_inf_{uuid.uuid4().hex[:8]}",
        "username": f"@{category.split('_')[0]}influencer{random.randint(100, 9999)}",
        "tier": tier,
        "category": category,
        "primary_market": primary_market,
        
        # Audience metrics
        "follower_count": followers,
        "following_count": random.randint(500, 5000),
        "total_videos": random.randint(50, 2000),
        "total_likes": random.randint(followers, followers * 10),
        "average_views_per_video": random.randint(*tier_data["avg_views_per_video"]),
        "engagement_rate": tier_data["engagement_rate"] + random.uniform(-0.02, 0.02),
        
        # Economic metrics
        "estimated_cpm": random.uniform(*tier_data["cpm_usd"]),
        "brand_deal_value_range": tier_data["brand_deal_value"],
        "conversion_rate": tier_data["conversion_rate"] + random.uniform(-0.01, 0.01),
        
        # PayPal commerce integration
        "paypal_business_account": True,
        "products_sold": random.randint(10, 500) if tier in ["tier_3_micro", "tier_4_nano"] else 0,
        "monthly_product_revenue": random.uniform(1000, 50000) if tier in ["tier_3_micro", "tier_4_nano"] else 0,
        "paypal_transaction_volume": random.uniform(5000, 200000),
        "payment_conversion_rate": category_data["conversion_rate"] * market_data["conversion_premium"],
        "average_order_value": category_data["avg_order_value"],
        "paypal_fee_monthly": 0,  # Will be calculated
        
        # Content strategy
        "content_frequency_per_week": random.randint(3, 21),
        "product_promotion_rate": random.uniform(0.15, 0.4),
        "affiliate_partnerships": random.randint(2, 15),
        "sponsored_content_rate": random.uniform(0.05, 0.25),
        
        # Audience demographics
        "audience_age_distribution": {
            "13-17": random.uniform(0.15, 0.35),
            "18-24": random.uniform(0.25, 0.45),
            "25-34": random.uniform(0.15, 0.30),
            "35+": random.uniform(0.05, 0.15)
        },
        "audience_gender_split": {
            "female": random.uniform(0.45, 0.75) if category in ["beauty_cosmetics", "fashion_apparel"] else random.uniform(0.35, 0.65),
            "male": None  # Will be calculated as 1 - female
        },
        "audience_geographic_distribution": {
            primary_market: random.uniform(0.4, 0.7),
            "other_markets": None  # Will be calculated
        },
        
        # Account quality metrics
        "account_age_months": random.randint(6, 48),
        "verification_status": "verified" if tier in ["tier_1_mega", "tier_2_macro"] else "unverified",
        "content_quality_score": random.uniform(0.6, 0.95),
        "brand_safety_score": random.uniform(0.7, 0.98),
        
        # Bot contamination estimates
        "estimated_bot_followers": int(followers * random.uniform(0.05, 0.25)),
        "bot_engagement_percentage": random.uniform(0.08, 0.30),
        "authentic_engagement_rate": None  # Will be calculated
    }
    
    # Calculate derived metrics
    influencer["audience_gender_split"]["male"] = 1 - influencer["audience_gender_split"]["female"]
    influencer["authentic_engagement_rate"] = influencer["engagement_rate"] * (1 - influencer["bot_engagement_percentage"])
    
    # Calculate PayPal fees
    monthly_volume = influencer["paypal_transaction_volume"]
    paypal_fee_rate = PAYPAL_COMMERCE_PATTERNS["influencer_payment_flows"]["direct_product_sales"]["paypal_fee_percentage"]
    influencer["paypal_fee_monthly"] = monthly_volume * paypal_fee_rate
    
    return influencer

def generate_tiktok_content_with_commerce(influencer: Dict) -> Dict:
    """Generate TikTok content with commerce integration."""
    category = influencer["category"]
    category_data = TIKTOK_MARKET_DATA["product_categories"][category]
    
    # Content type based on category
    content_types = {
        "beauty_cosmetics": ["tutorial", "review", "transformation", "product_demo", "routine"],
        "fashion_apparel": ["outfit", "haul", "styling_tips", "lookbook", "trend_alert"],
        "health_fitness": ["workout", "nutrition", "transformation", "tips", "motivation"],
        "tech_gadgets": ["unboxing", "review", "comparison", "tips", "tutorial"],
        "food_beverage": ["recipe", "review", "cooking", "taste_test", "food_prep"]
    }
    
    content_type = random.choice(content_types[category])
    is_promotional = random.random() < influencer["product_promotion_rate"]
    
    video = {
        "video_id": f"tiktok_{uuid.uuid4().hex[:11]}",
        "influencer_id": influencer["influencer_id"],
        "username": influencer["username"],
        "content_type": content_type,
        "category": category,
        "is_promotional": is_promotional,
        "has_product_links": is_promotional and random.random() < 0.8,
        "paypal_checkout_integration": is_promotional and random.random() < 0.6,
        
        # Video metrics
        "duration_seconds": random.randint(15, 180),  # TikTok range
        "views": random.randint(
            int(influencer["average_views_per_video"] * 0.3),
            int(influencer["average_views_per_video"] * 2.5)
        ),
        "likes": 0,  # Will be calculated
        "comments": 0,  # Will be calculated
        "shares": 0,  # Will be calculated
        "saves": 0,  # Will be calculated
        
        # Commerce metrics
        "product_mentions": random.randint(1, 5) if is_promotional else 0,
        "external_link_clicks": 0,  # Will be calculated during simulation
        "paypal_conversions": 0,  # Will be calculated during simulation
        "estimated_revenue": 0.0,  # Will be calculated
        
        # Content metadata
        "upload_time": (datetime.now() - timedelta(hours=random.randint(1, 72))).isoformat(),
        "trending_hashtags": [f"#{category.replace('_', '')}", "#fyp", "#viral", "#trending"],
        "custom_hashtags": [f"#{influencer['username'][1:]}"] + [f"#tag{i}" for i in range(random.randint(2, 8))],
        "music_track": f"trending_audio_{random.randint(1, 1000)}",
        "effects_used": random.randint(0, 5),
        
        # Engagement quality
        "completion_rate": random.uniform(0.45, 0.85),
        "replay_rate": random.uniform(0.15, 0.45),
        "engagement_velocity": random.uniform(0.02, 0.15),  # Engagement per hour
        
        # Algorithm performance
        "for_you_page_performance": random.uniform(0.1, 0.8),
        "hashtag_challenge_participation": random.random() < 0.3,
        "duet_responses": random.randint(0, 50),
        "stitch_uses": random.randint(0, 25)
    }
    
    # Calculate engagement metrics based on views and influencer metrics
    base_engagement_rate = influencer["engagement_rate"]
    video["likes"] = int(video["views"] * base_engagement_rate * random.uniform(0.8, 1.2))
    video["comments"] = int(video["likes"] * random.uniform(0.05, 0.15))
    video["shares"] = int(video["likes"] * random.uniform(0.02, 0.08))
    video["saves"] = int(video["likes"] * random.uniform(0.03, 0.12))
    
    # Calculate commerce metrics for promotional content
    if is_promotional and video["has_product_links"]:
        click_through_rate = random.uniform(0.02, 0.08)
        video["external_link_clicks"] = int(video["views"] * click_through_rate)
        
        if video["paypal_checkout_integration"]:
            conversion_rate = influencer["payment_conversion_rate"]
            video["paypal_conversions"] = int(video["external_link_clicks"] * conversion_rate)
            video["estimated_revenue"] = video["paypal_conversions"] * influencer["average_order_value"]
    
    return video

def generate_tiktok_bot_with_commerce_focus(bot_type: str, target_influencers: List[Dict]) -> Dict:
    """Generate TikTok bot with commerce and PayPal targeting."""
    bot_config = TIKTOK_BOT_TYPES[bot_type]
    
    # Select target influencer based on bot objectives
    target_influencer = random.choice(target_influencers)
    
    # Mobile device simulation (TikTok requirement)
    mobile_devices = [
        {"brand": "iPhone", "model": "iPhone 14", "os": "iOS 16.1", "app_version": "27.5.0"},
        {"brand": "Samsung", "model": "Galaxy S23", "os": "Android 13", "app_version": "27.5.0"},
        {"brand": "Google", "model": "Pixel 7", "os": "Android 13", "app_version": "27.5.0"},
        {"brand": "Xiaomi", "model": "Mi 13", "os": "Android 13", "app_version": "27.5.0"}
    ]
    
    device = random.choice(mobile_devices)
    
    # Location targeting for commerce bots
    commerce_locations = [
        {"country": "US", "city": "Los Angeles", "timezone": "UTC-8", "purchasing_power": "high"},
        {"country": "US", "city": "New York", "timezone": "UTC-5", "purchasing_power": "high"},
        {"country": "UK", "city": "London", "timezone": "UTC+0", "purchasing_power": "high"},
        {"country": "CA", "city": "Toronto", "timezone": "UTC-5", "purchasing_power": "high"},
        {"country": "AU", "city": "Sydney", "timezone": "UTC+11", "purchasing_power": "high"}
    ]
    
    location = random.choice(commerce_locations)
    
    bot = {
        "bot_id": f"tiktok_bot_{bot_type}_{uuid.uuid4().hex[:8]}",
        "bot_type": bot_type,
        "description": bot_config["description"],
        "target_influencer": target_influencer["influencer_id"],
        "target_category": target_influencer["category"],
        
        # Device and network
        "device_profile": device,
        "location": location,
        "network_profile": {
            "connection_type": random.choice(["mobile_5g", "mobile_4g", "wifi"]),
            "ip_type": "residential_proxy" if bot_type in ["conversion_funnel_bot", "sophisticated_ai_influencer_bot"] else "datacenter",
            "proxy_rotation": True,
            "mobile_emulation": True
        },
        
        # Behavioral configuration
        "behavior_config": bot_config["behavior"],
        "operation_economics": bot_config["economics"],
        "detection_signatures": bot_config["detection_signatures"],
        
        # Commerce targeting
        "commerce_focus": bot_type in ["conversion_funnel_bot", "viral_manipulation_bot"],
        "paypal_interaction_patterns": {
            "checkout_abandonment_rate": random.uniform(0.7, 0.9),  # High abandonment for bots
            "payment_completion_rate": random.uniform(0.1, 0.3),    # Low completion
            "fraud_risk_score": random.uniform(0.6, 0.95),
            "chargeback_probability": random.uniform(0.15, 0.4)
        },
        
        # Activity patterns
        "daily_action_quota": random.randint(100, 1000),
        "active_hours": list(range(24)) if bot_type == "follower_boost_bot" else random.sample(range(24), random.randint(8, 16)),
        "coordination_group": f"group_{hashlib.md5(str(random.randint(1, 50)).encode()).hexdigest()[:6]}",
        
        # Economic impact
        "operation_cost_per_day": random.uniform(5.0, 50.0),
        "revenue_impact_multiplier": random.uniform(1.5, 8.0) if bot_type == "viral_manipulation_bot" else random.uniform(0.1, 1.2),
        
        # Detection evasion
        "human_like_score": random.uniform(0.2, 0.9),
        "detection_evasion_techniques": random.sample([
            "mobile_behavior_mimicking",
            "natural_scroll_patterns",
            "realistic_video_consumption",
            "delayed_interactions",
            "geo_appropriate_activity",
            "app_background_simulation"
        ], random.randint(3, 6))
    }
    
    return bot

def simulate_paypal_transaction(video: Dict, user_profile: Dict, influencer: Dict) -> Dict:
    """Simulate PayPal transaction with detailed metrics."""
    if not video.get("paypal_checkout_integration") or not video.get("has_product_links"):
        return {"transaction_occurred": False}
    
    # Transaction probability based on user type and targeting
    if user_profile["user_type"] == "real":
        base_conversion = influencer["payment_conversion_rate"]
        # Adjust for user demographics and content quality
        age_group = user_profile.get("age_group", "18-24")
        age_multiplier = {
            "13-17": 0.6,  # Lower purchasing power
            "18-24": 1.0,  # Baseline
            "25-34": 1.3,  # Higher purchasing power
            "35+": 1.1     # Selective but valuable
        }.get(age_group, 1.0)
        
        conversion_prob = base_conversion * age_multiplier * random.uniform(0.8, 1.2)
    else:  # bot
        # Bots have very low genuine conversion
        bot_commerce_config = user_profile.get("paypal_interaction_patterns", {})
        conversion_prob = bot_commerce_config.get("payment_completion_rate", 0.15)
    
    if random.random() > conversion_prob:
        return {"transaction_occurred": False, "abandoned_at": random.choice(["product_page", "cart", "checkout", "payment"])}
    
    # Transaction details
    category_data = TIKTOK_MARKET_DATA["product_categories"][influencer["category"]]
    base_order_value = category_data["avg_order_value"]
    
    # Calculate transaction amount with variance
    order_value = base_order_value * random.uniform(0.6, 2.5)
    
    # PayPal fees and processing
    paypal_fee_rate = PAYPAL_COMMERCE_PATTERNS["influencer_payment_flows"]["direct_product_sales"]["paypal_fee_percentage"]
    paypal_fee = order_value * paypal_fee_rate
    net_revenue = order_value - paypal_fee
    
    # Risk assessment for fraud detection
    if user_profile["user_type"] == "bot":
        risk_score = user_profile.get("paypal_interaction_patterns", {}).get("fraud_risk_score", 0.8)
        fraud_detected = risk_score > 0.7
    else:
        fraud_detected = random.random() < 0.004  # Low false positive rate
        risk_score = random.uniform(0.01, 0.15)
    
    transaction = {
        "transaction_occurred": True,
        "transaction_id": f"pp_{uuid.uuid4().hex[:16]}",
        "timestamp": datetime.now().isoformat(),
        "user_id": user_profile["user_id"],
        "user_type": user_profile["user_type"],
        "influencer_id": influencer["influencer_id"],
        "video_id": video["video_id"],
        
        # Financial details
        "order_value": round(order_value, 2),
        "paypal_fee": round(paypal_fee, 2),
        "net_revenue": round(net_revenue, 2),
        "currency": "USD",
        
        # Payment method
        "payment_method": random.choice(["paypal_balance", "credit_card", "bank_account", "buy_now_pay_later"]),
        "checkout_type": "express_checkout" if random.random() < 0.6 else "standard_checkout",
        
        # Risk and fraud
        "fraud_risk_score": risk_score,
        "fraud_detected": fraud_detected,
        "chargeback_risk": random.uniform(0.01, 0.8) if user_profile["user_type"] == "bot" else random.uniform(0.005, 0.02),
        
        # Customer details
        "customer_location": user_profile.get("country", "US"),
        "new_customer": random.random() < 0.4,
        "repeat_purchase": random.random() < 0.25,
        
        # Conversion funnel
        "time_from_click_to_purchase_minutes": random.uniform(2, 45) if user_profile["user_type"] == "real" else random.uniform(0.5, 5),
        "cart_abandonment_recovered": random.random() < 0.15,
        
        # Business impact
        "attributed_to_influencer": True,
        "commission_owed": net_revenue * random.uniform(0.05, 0.25),
        "lifetime_value_estimate": order_value * random.uniform(2.5, 8.0) if user_profile["user_type"] == "real" else 0
    }
    
    return transaction

# Generate TikTok influencers
print("Generating TikTok influencers with commerce integration...")
influencers = []

# Distribution across tiers
tier_distribution = [
    ("tier_1_mega", 2),
    ("tier_2_macro", 4),
    ("tier_3_micro", 6),
    ("tier_4_nano", 3)
]

for tier, count in tier_distribution:
    for _ in range(count):
        influencer = generate_tiktok_influencer_profile(tier)
        influencers.append(influencer)

# Generate TikTok content
print("Generating TikTok content with PayPal integration...")
tiktok_videos = []

for _ in range(NUM_CONTENT):
    influencer = random.choice(influencers)
    video = generate_tiktok_content_with_commerce(influencer)
    tiktok_videos.append(video)

# Generate real users
print("Generating real TikTok users...")
real_users = []

for i in range(NUM_REAL_USERS):
    age_groups = ["13-17", "18-24", "25-34", "35+"]
    age_weights = [0.25, 0.45, 0.22, 0.08]  # TikTok demographics
    age_group = random.choices(age_groups, weights=age_weights)[0]
    
    # Interest alignment with product categories
    interests = random.sample(list(TIKTOK_MARKET_DATA["product_categories"].keys()), random.randint(2, 4))
    
    # Geographic distribution
    countries = list(TIKTOK_MARKET_DATA["geographic_markets"].keys())
    country_weights = [0.4, 0.25, 0.25, 0.1]
    country = random.choices(countries, weights=country_weights)[0]
    
    user = {
        "user_id": f"tiktok_user_{uuid.uuid4().hex[:8]}",
        "user_type": "real",
        "age_group": age_group,
        "country": country,
        "interests": interests,
        "gender": random.choice(["female", "male", "other"]),
        
        # App usage patterns
        "daily_usage_minutes": random.randint(30, 180),
        "videos_watched_per_session": random.randint(10, 100),
        "preferred_content_length": random.choice(["short", "medium", "long"]),
        "sound_on_preference": random.random() < 0.75,
        
        # Commerce behavior
        "purchase_probability": random.uniform(0.02, 0.15),
        "average_order_value": random.uniform(20, 200),
        "paypal_user": random.random() < TIKTOK_MARKET_DATA["geographic_markets"][country]["paypal_penetration"],
        "previous_social_commerce": random.random() < 0.35,
        
        # Device and network
        "device_type": "mobile",  # TikTok is mobile-first
        "device_os": random.choice(["iOS", "Android"]),
        "app_version": "27.5.0",
        "connection_quality": random.choice(["excellent", "good", "fair"]),
        
        # Engagement patterns
        "engagement_rate": random.uniform(0.05, 0.25),
        "comment_probability": random.uniform(0.02, 0.12),
        "share_probability": random.uniform(0.01, 0.08),
        "follow_probability": random.uniform(0.005, 0.03)
    }
    
    real_users.append(user)

# Generate TikTok bots
print("Generating TikTok bots with commerce targeting...")
tiktok_bots = []

for i in range(NUM_BOTS):
    bot_type = random.choice(list(TIKTOK_BOT_TYPES.keys()))
    bot = generate_tiktok_bot_with_commerce_focus(bot_type, influencers)
    tiktok_bots.append(bot)

# Run enhanced simulation
print("Running TikTok influencer commerce simulation...")
engagement_log = []
paypal_transactions = []
detection_events = []

for step in range(SIMULATION_STEPS):
    current_time = datetime.now() + timedelta(minutes=step * 15)  # 15-minute intervals
    
    # Real user behavior
    for user in real_users:
        if random.random() < 0.3:  # 30% active per interval
            # Select video based on interests
            relevant_videos = [v for v in tiktok_videos 
                             if v["category"] in user["interests"]]
            if not relevant_videos:
                relevant_videos = random.sample(tiktok_videos, min(3, len(tiktok_videos)))
            
            video = random.choice(relevant_videos)
            influencer = next(inf for inf in influencers if inf["influencer_id"] == video["influencer_id"])
            
            # Watch behavior
            watch_time = random.uniform(5, video["duration_seconds"])
            completion_rate = watch_time / video["duration_seconds"]
            
            engagement_event = {
                "timestamp": current_time.isoformat(),
                "step": step,
                "user_id": user["user_id"],
                "user_type": "real",
                "action": "view",
                "video_id": video["video_id"],
                "influencer_id": influencer["influencer_id"],
                "category": video["category"],
                "watch_time_seconds": watch_time,
                "completion_rate": completion_rate,
                "country": user["country"],
                "age_group": user["age_group"],
                "device_os": user["device_os"],
                "is_promotional_content": video["is_promotional"]
            }
            
            engagement_log.append(engagement_event)
            
            # Engagement actions
            if completion_rate > 0.7 and random.random() < user["engagement_rate"]:
                if random.random() < 0.8:  # Like
                    engagement_log.append({
                        "timestamp": current_time.isoformat(),
                        "step": step,
                        "user_id": user["user_id"],
                        "user_type": "real",
                        "action": "like",
                        "video_id": video["video_id"],
                        "influencer_id": influencer["influencer_id"]
                    })
                
                if random.random() < user["comment_probability"]:
                    engagement_log.append({
                        "timestamp": current_time.isoformat(),
                        "step": step,
                        "user_id": user["user_id"],
                        "user_type": "real",
                        "action": "comment",
                        "video_id": video["video_id"],
                        "influencer_id": influencer["influencer_id"],
                        "comment_authenticity": random.uniform(0.8, 1.0)
                    })
            
            # PayPal transaction simulation
            if video["has_product_links"] and random.random() < 0.05:  # 5% click external links
                # Add user_type to user profile for transaction simulation
                user_profile = dict(user)
                user_profile["user_type"] = "real"
                user_profile["user_id"] = user["user_id"]
                
                transaction = simulate_paypal_transaction(video, user_profile, influencer)
                if transaction["transaction_occurred"]:
                    paypal_transactions.append(transaction)
    
    # Bot behavior
    for bot in tiktok_bots:
        if random.random() < 0.6:  # 60% active per interval
            target_videos = [v for v in tiktok_videos 
                           if v["influencer_id"] == bot["target_influencer"]]
            if not target_videos:
                target_videos = random.sample(tiktok_videos, min(2, len(tiktok_videos)))
            
            video = random.choice(target_videos)
            influencer = next(inf for inf in influencers if inf["influencer_id"] == video["influencer_id"])
            
            bot_config = bot["behavior_config"]
            
            # Bot view behavior
            if random.random() < 0.9:
                watch_time = random.uniform(5, video["duration_seconds"] * bot_config["view_completion"])
                
                engagement_event = {
                    "timestamp": current_time.isoformat(),
                    "step": step,
                    "user_id": bot["bot_id"],
                    "user_type": "bot",
                    "bot_type": bot["bot_type"],
                    "action": "view",
                    "video_id": video["video_id"],
                    "influencer_id": influencer["influencer_id"],
                    "watch_time_seconds": watch_time,
                    "completion_rate": watch_time / video["duration_seconds"],
                    "bot_location": bot["location"]["country"],
                    "detection_risk": random.uniform(0.3, 0.9),
                    "commerce_targeted": bot["commerce_focus"]
                }
                
                engagement_log.append(engagement_event)
                
                # Bot engagement actions
                if random.random() < bot_config["like_rate"]:
                    engagement_log.append({
                        "timestamp": current_time.isoformat(),
                        "step": step,
                        "user_id": bot["bot_id"],
                        "user_type": "bot",
                        "bot_type": bot["bot_type"],
                        "action": "like",
                        "video_id": video["video_id"],
                        "influencer_id": influencer["influencer_id"],
                        "suspicious_timing": True
                    })
                
                # Bot PayPal interaction (usually fraudulent)
                if video["has_product_links"] and bot["commerce_focus"] and random.random() < 0.15:
                    # Add user_type to bot profile for transaction simulation
                    bot_profile = dict(bot)
                    bot_profile["user_type"] = "bot"
                    bot_profile["user_id"] = bot["bot_id"]
                    
                    transaction = simulate_paypal_transaction(video, bot_profile, influencer)
                    if transaction["transaction_occurred"]:
                        paypal_transactions.append(transaction)
                        
                        # High probability of fraud detection for bot transactions
                        if transaction["fraud_detected"]:
                            detection_events.append({
                                "timestamp": current_time.isoformat(),
                                "event_type": "fraudulent_paypal_transaction",
                                "bot_id": bot["bot_id"],
                                "transaction_id": transaction["transaction_id"],
                                "risk_score": transaction["fraud_risk_score"],
                                "amount": transaction["order_value"]
                            })

# Calculate comprehensive metrics
print("Calculating TikTok commerce analytics...")

total_transactions = len(paypal_transactions)
genuine_transactions = len([t for t in paypal_transactions if not t.get("fraud_detected", False)])
fraudulent_transactions = total_transactions - genuine_transactions

total_revenue = sum(t["order_value"] for t in paypal_transactions)
genuine_revenue = sum(t["order_value"] for t in paypal_transactions if not t.get("fraud_detected", False))
fraud_loss = total_revenue - genuine_revenue

analytics = {
    "tiktok_market_overview": TIKTOK_MARKET_DATA,
    "simulation_summary": {
        "influencers": len(influencers),
        "videos": len(tiktok_videos),
        "real_users": len(real_users),
        "bots": len(tiktok_bots),
        "engagement_events": len(engagement_log),
        "paypal_transactions": total_transactions,
        "fraud_detection_events": len(detection_events)
    },
    "commerce_performance": {
        "total_revenue": round(total_revenue, 2),
        "genuine_revenue": round(genuine_revenue, 2),
        "fraud_loss": round(fraud_loss, 2),
        "fraud_rate": round(fraudulent_transactions / total_transactions if total_transactions > 0 else 0, 3),
        "average_order_value": round(total_revenue / total_transactions if total_transactions > 0 else 0, 2),
        "conversion_rate": round(total_transactions / len(engagement_log) if len(engagement_log) > 0 else 0, 4)
    },
    "paypal_integration_metrics": {
        "total_fees_collected": round(sum(t["paypal_fee"] for t in paypal_transactions), 2),
        "fraud_detection_accuracy": round(len(detection_events) / fraudulent_transactions if fraudulent_transactions > 0 else 1.0, 3),
        "chargeback_risk": round(sum(t["chargeback_risk"] for t in paypal_transactions) / total_transactions if total_transactions > 0 else 0, 3)
    },
    "influencer_tier_performance": {},
    "bot_impact_analysis": {
        "bot_engagement_percentage": round(len([e for e in engagement_log if e["user_type"] == "bot"]) / len(engagement_log), 3),
        "bot_transaction_percentage": round(len([t for t in paypal_transactions if "bot" in t["user_id"]]) / total_transactions if total_transactions > 0 else 0, 3),
        "estimated_revenue_inflation": round((fraud_loss / genuine_revenue) if genuine_revenue > 0 else 0, 3)
    }
}

# Tier performance analysis
for tier in ["tier_1_mega", "tier_2_macro", "tier_3_micro", "tier_4_nano"]:
    tier_influencers = [inf for inf in influencers if inf["tier"] == tier]
    tier_videos = [v for v in tiktok_videos if any(v["influencer_id"] == inf["influencer_id"] for inf in tier_influencers)]
    tier_transactions = [t for t in paypal_transactions if any(t["influencer_id"] == inf["influencer_id"] for inf in tier_influencers)]
    
    analytics["influencer_tier_performance"][tier] = {
        "influencer_count": len(tier_influencers),
        "total_revenue": round(sum(t["order_value"] for t in tier_transactions), 2),
        "average_conversion_rate": round(sum(inf["payment_conversion_rate"] for inf in tier_influencers) / len(tier_influencers) if tier_influencers else 0, 4),
        "transactions": len(tier_transactions)
    }

# Save comprehensive data
import os
os.makedirs("../data", exist_ok=True)

simulation_data = {
    "metadata": {
        "platform": "tiktok",
        "simulation_type": "influencer_commerce_with_paypal",
        "timestamp": datetime.now().isoformat(),
        "enhanced_features": [
            "real_time_market_data",
            "paypal_integration",
            "commerce_conversion_tracking",
            "fraud_detection",
            "influencer_tier_analysis"
        ]
    },
    "influencers": influencers,
    "videos": tiktok_videos,
    "real_users": real_users,
    "bots": tiktok_bots,
    "engagement_log": engagement_log,
    "paypal_transactions": paypal_transactions,
    "detection_events": detection_events,
    "analytics": analytics
}

with open("../data/tiktok_influencer_commerce_simulation.json", "w") as f:
    json.dump(simulation_data, f, indent=2, default=str)

print(f"\n🎯 TikTok Influencer Commerce Simulation Complete!")
print(f"📊 Total Influencers: {len(influencers)}")
print(f"🎬 Total Videos: {len(tiktok_videos)}")
print(f"👥 Real Users: {len(real_users)} | 🤖 Bots: {len(tiktok_bots)}")
print(f"💰 PayPal Transactions: {total_transactions}")
print(f"💵 Total Revenue: ${total_revenue:,.2f}")
print(f"🚨 Fraud Loss: ${fraud_loss:,.2f} ({analytics['commerce_performance']['fraud_rate']:.1%})")
print(f"🛡️ Fraud Detection Events: {len(detection_events)}")

if __name__ == "__main__":
    scale_parameters(scale_factor=1)
