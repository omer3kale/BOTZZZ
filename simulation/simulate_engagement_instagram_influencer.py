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
    """Scale simulation parameters for large-scale Instagram influencer analysis."""
    global NUM_INFLUENCERS, NUM_REAL_USERS, NUM_BOTS, NUM_CONTENT, SIMULATION_STEPS
    NUM_INFLUENCERS = int(NUM_INFLUENCERS * scale_factor)
    NUM_REAL_USERS = int(NUM_REAL_USERS * scale_factor)
    NUM_BOTS = int(NUM_BOTS * scale_factor)
    NUM_CONTENT = int(NUM_CONTENT * scale_factor)
    SIMULATION_STEPS = int(SIMULATION_STEPS * scale_factor)
    print(f"Instagram Influencer Parameters scaled by factor {scale_factor}:")
    print(f"NUM_INFLUENCERS: {NUM_INFLUENCERS}")
    print(f"NUM_REAL_USERS: {NUM_REAL_USERS}")
    print(f"NUM_BOTS: {NUM_BOTS}")
    print(f"NUM_CONTENT: {NUM_CONTENT}")
    print(f"SIMULATION_STEPS: {SIMULATION_STEPS}")

# Instagram Influencer Simulation Parameters
NUM_INFLUENCERS = 20
NUM_REAL_USERS = 800
NUM_BOTS = 200
NUM_CONTENT = 40
SIMULATION_STEPS = 120

# Real-time Instagram Market Data (2024-2025)
INSTAGRAM_MARKET_DATA = {
    "global_statistics": {
        "monthly_active_users": 2350000000,  # 2.35 billion MAU
        "daily_active_users": 1440000000,    # 1.44 billion DAU
        "stories_posted_daily": 500000000,   # 500 million stories/day
        "posts_shared_daily": 95000000,      # 95 million posts/day
        "shopping_tags_monthly": 130000000,  # 130 million shopping tags
        "advertising_revenue_2024": 47500000000  # $47.5 billion
    },
    "influencer_economics": {
        "mega_influencer": {
            "followers_range": (1000000, 50000000),
            "avg_engagement_rate": 0.042,  # 4.2%
            "cost_per_post": (10000, 1000000),
            "story_cost": (5000, 100000),
            "conversion_rate": 0.035,
            "brand_partnerships_monthly": (5, 25),
            "product_sales_monthly": (0, 500000)  # Some don't sell products
        },
        "macro_influencer": {
            "followers_range": (100000, 1000000),
            "avg_engagement_rate": 0.067,  # 6.7%
            "cost_per_post": (1000, 15000),
            "story_cost": (500, 5000),
            "conversion_rate": 0.058,
            "brand_partnerships_monthly": (3, 15),
            "product_sales_monthly": (1000, 50000)
        },
        "micro_influencer": {
            "followers_range": (10000, 100000),
            "avg_engagement_rate": 0.098,  # 9.8%
            "cost_per_post": (100, 2000),
            "story_cost": (50, 500),
            "conversion_rate": 0.082,
            "brand_partnerships_monthly": (2, 8),
            "product_sales_monthly": (500, 15000)
        },
        "nano_influencer": {
            "followers_range": (1000, 10000),
            "avg_engagement_rate": 0.125,  # 12.5%
            "cost_per_post": (50, 500),
            "story_cost": (25, 150),
            "conversion_rate": 0.115,
            "brand_partnerships_monthly": (1, 4),
            "product_sales_monthly": (200, 3000)
        }
    },
    "content_performance_by_type": {
        "feed_posts": {
            "average_reach": 0.23,  # 23% of followers
            "engagement_rate": 0.067,
            "lifespan_hours": 48,
            "shopping_conversion": 0.045
        },
        "stories": {
            "average_reach": 0.45,  # 45% of followers
            "completion_rate": 0.73,
            "lifespan_hours": 24,
            "swipe_up_rate": 0.067,
            "shopping_sticker_conversion": 0.089,
            "engagement_rate": 0.085,
            "shopping_conversion": 0.089
        },
        "reels": {
            "average_reach": 0.67,  # 67% of followers (algorithm boost)
            "engagement_rate": 0.125,
            "lifespan_hours": 168,  # 1 week
            "shopping_conversion": 0.078
        },
        "igtv": {
            "average_reach": 0.15,  # 15% of followers
            "engagement_rate": 0.045,
            "completion_rate": 0.34,
            "lifespan_hours": 720,  # 30 days
            "shopping_conversion": 0.023
        }
    },
    "shopping_categories": {
        "fashion_lifestyle": {
            "market_size_billion": 284.7,
            "instagram_share": 0.42,
            "avg_order_value": 127.50,
            "return_rate": 0.22,
            "repeat_purchase_rate": 0.34,
            "paypal_usage": 0.61,
            "seasonal_multiplier": {
                "q1": 0.85, "q2": 1.0, "q3": 0.95, "q4": 1.45
            }
        },
        "beauty_skincare": {
            "market_size_billion": 189.3,
            "instagram_share": 0.56,
            "avg_order_value": 78.20,
            "return_rate": 0.15,
            "repeat_purchase_rate": 0.58,
            "paypal_usage": 0.69,
            "seasonal_multiplier": {
                "q1": 1.1, "q2": 1.0, "q3": 0.9, "q4": 1.3
            }
        },
        "fitness_wellness": {
            "market_size_billion": 112.8,
            "instagram_share": 0.38,
            "avg_order_value": 89.90,
            "return_rate": 0.08,
            "repeat_purchase_rate": 0.41,
            "paypal_usage": 0.74,
            "seasonal_multiplier": {
                "q1": 1.3, "q2": 1.1, "q3": 0.95, "q4": 0.8
            }
        },
        "home_decor": {
            "market_size_billion": 167.4,
            "instagram_share": 0.29,
            "avg_order_value": 156.30,
            "return_rate": 0.18,
            "repeat_purchase_rate": 0.27,
            "paypal_usage": 0.58,
            "seasonal_multiplier": {
                "q1": 0.9, "q2": 1.1, "q3": 1.0, "q4": 1.2
            }
        },
        "food_beverage": {
            "market_size_billion": 98.6,
            "instagram_share": 0.24,
            "avg_order_value": 45.80,
            "return_rate": 0.05,
            "repeat_purchase_rate": 0.67,
            "paypal_usage": 0.65,
            "seasonal_multiplier": {
                "q1": 1.0, "q2": 1.05, "q3": 1.1, "q4": 1.15
            }
        }
    },
    "geographic_performance": {
        "north_america": {
            "user_base": 230000000,
            "avg_cpm": 4.8,
            "conversion_rate_multiplier": 1.25,
            "avg_order_value_multiplier": 1.4,
            "paypal_penetration": 0.79,
            "premium_audience": True
        },
        "europe": {
            "user_base": 190000000,
            "avg_cpm": 3.9,
            "conversion_rate_multiplier": 1.15,
            "avg_order_value_multiplier": 1.2,
            "paypal_penetration": 0.67,
            "premium_audience": True
        },
        "asia_pacific": {
            "user_base": 950000000,
            "avg_cpm": 2.1,
            "conversion_rate_multiplier": 0.95,
            "avg_order_value_multiplier": 0.85,
            "paypal_penetration": 0.45,
            "premium_audience": False
        },
        "latin_america": {
            "user_base": 180000000,
            "avg_cpm": 1.7,
            "conversion_rate_multiplier": 0.88,
            "avg_order_value_multiplier": 0.75,
            "paypal_penetration": 0.41,
            "premium_audience": False
        },
        "middle_east_africa": {
            "user_base": 140000000,
            "avg_cpm": 2.3,
            "conversion_rate_multiplier": 0.82,
            "avg_order_value_multiplier": 0.8,
            "paypal_penetration": 0.38,
            "premium_audience": False
        }
    }
}

# Instagram-specific Bot Types with Commerce Focus
INSTAGRAM_BOT_TYPES = {
    "follower_growth_bot": {
        "description": "Mass follower acquisition for influencer credibility",
        "behavior": {
            "follow_rate": 0.98,
            "unfollow_rate": 0.85,  # Follow/unfollow strategy
            "like_rate": 0.12,
            "comment_rate": 0.03,
            "story_view_rate": 0.08,
            "profile_visit_rate": 0.25,
            "operation_speed": "high",
            "detection_difficulty": "medium"
        },
        "economics": {
            "cost_per_follow": 0.006,
            "bulk_discount": 0.3,
            "retention_rate": 0.75,  # How many followers stick
            "delivery_speed_hours": 72
        },
        "detection_signatures": {
            "rapid_follow_unfollow": True,
            "low_engagement_correlation": True,
            "mass_simultaneous_actions": True,
            "profile_incompleteness": True
        }
    },
    "engagement_pod_bot": {
        "description": "Coordinated engagement to boost algorithm visibility",
        "behavior": {
            "follow_rate": 0.20,
            "like_rate": 0.95,
            "comment_rate": 0.65,
            "story_view_rate": 0.75,
            "save_rate": 0.25,
            "share_rate": 0.15,
            "operation_speed": "coordinated",
            "detection_difficulty": "high"
        },
        "economics": {
            "cost_per_engagement_set": 0.08,
            "coordination_premium": 1.8,
            "algorithm_boost_guarantee": True,
            "delivery_speed_hours": 6
        },
        "detection_signatures": {
            "synchronized_engagement_timing": True,
            "reciprocal_engagement_patterns": True,
            "unusual_engagement_velocity": True,
            "cross_account_coordination": True
        }
    },
    "shopping_conversion_bot": {
        "description": "Artificial shopping engagement and traffic driving",
        "behavior": {
            "follow_rate": 0.30,
            "like_rate": 0.80,
            "comment_rate": 0.35,
            "shopping_tag_interaction": 0.90,
            "story_shopping_sticker_rate": 0.85,
            "external_link_click_rate": 0.75,
            "cart_abandonment_rate": 0.88,  # High abandonment
            "purchase_completion_rate": 0.08,  # Low actual purchase
            "operation_speed": "targeted",
            "detection_difficulty": "very_high"
        },
        "economics": {
            "cost_per_shopping_interaction": 0.15,
            "ecommerce_targeting_premium": 2.2,
            "paypal_integration_bonus": 1.4,
            "fake_purchase_cost": 5.0  # Cost to simulate purchase
        },
        "detection_signatures": {
            "high_shopping_interaction_low_purchase": True,
            "cart_abandonment_patterns": True,
            "payment_page_bouncing": True,
            "unrealistic_browsing_patterns": True
        }
    },
    "story_engagement_bot": {
        "description": "Instagram Stories engagement manipulation",
        "behavior": {
            "follow_rate": 0.15,
            "story_view_rate": 0.95,
            "story_reaction_rate": 0.45,
            "story_reply_rate": 0.12,
            "poll_vote_rate": 0.80,
            "quiz_participation_rate": 0.70,
            "question_response_rate": 0.25,
            "operation_speed": "medium",
            "detection_difficulty": "medium"
        },
        "economics": {
            "cost_per_story_view": 0.004,
            "interactive_element_premium": 1.5,
            "24_hour_guarantee": True,
            "delivery_speed_hours": 2
        },
        "detection_signatures": {
            "unrealistic_story_completion_rates": True,
            "identical_interaction_timing": True,
            "poll_response_patterns": True,
            "story_screenshot_detection": False  # Bots don't screenshot
        }
    },
    "reels_viral_bot": {
        "description": "Instagram Reels algorithm manipulation for viral content",
        "behavior": {
            "follow_rate": 0.25,
            "like_rate": 0.90,
            "comment_rate": 0.55,
            "share_rate": 0.40,
            "save_rate": 0.35,
            "reels_completion_rate": 0.85,
            "reels_replay_rate": 0.60,
            "operation_speed": "burst",
            "detection_difficulty": "high"
        },
        "economics": {
            "cost_per_viral_push": 200.0,
            "success_probability": 0.72,
            "reach_amplification": 15.3,  # 15.3x reach increase
            "engagement_multiplier": 8.7
        },
        "detection_signatures": {
            "unnatural_viral_velocity": True,
            "engagement_spike_patterns": True,
            "coordinated_sharing": True,
            "algorithm_gaming_indicators": True
        }
    }
}

# PayPal Shopping Integration for Instagram
INSTAGRAM_PAYPAL_PATTERNS = {
    "checkout_experiences": {
        "instagram_shopping": {
            "native_checkout": {
                "conversion_rate": 0.089,
                "cart_abandonment": 0.68,
                "average_transaction_value": 67.40,
                "paypal_usage_rate": 0.34,
                "mobile_optimization": 0.95
            },
            "external_website": {
                "conversion_rate": 0.054,
                "cart_abandonment": 0.78,
                "average_transaction_value": 89.20,
                "paypal_usage_rate": 0.67,
                "mobile_optimization": 0.72
            }
        },
        "story_shopping": {
            "shopping_stickers": {
                "click_through_rate": 0.067,
                "conversion_rate": 0.112,
                "impulse_purchase_rate": 0.78,
                "paypal_express_usage": 0.81
            },
            "swipe_up_links": {
                "click_through_rate": 0.045,
                "conversion_rate": 0.078,
                "bounce_rate": 0.64,
                "paypal_usage_rate": 0.59
            }
        }
    },
    "influencer_monetization": {
        "creator_fund_payments": {
            "min_payout_threshold": 100.0,
            "payment_frequency": "monthly",
            "paypal_fee_rate": 0.025,
            "international_fee": 0.045
        },
        "brand_collaboration_payments": {
            "escrow_usage": 0.67,
            "payment_protection": True,
            "dispute_rate": 0.04,
            "average_payment_delay_days": 7
        },
        "affiliate_commissions": {
            "commission_range": (0.03, 0.30),
            "cookie_duration_days": 30,
            "cross_device_tracking": True,
            "paypal_payout_rate": 0.78
        }
    },
    "fraud_prevention": {
        "bot_transaction_patterns": {
            "rapid_checkout_abandonment": 0.92,
            "payment_method_cycling": True,
            "address_inconsistencies": 0.85,
            "device_fingerprint_mismatches": 0.78,
            "behavioral_anomalies": 0.94
        },
        "detection_accuracy": {
            "genuine_user_false_positive": 0.006,
            "bot_detection_rate": 0.94,
            "sophisticated_bot_detection": 0.67,
            "coordinated_attack_detection": 0.89
        }
    }
}

def generate_instagram_influencer(tier: str) -> Dict:
    """Generate realistic Instagram influencer with shopping integration."""
    tier_data = INSTAGRAM_MARKET_DATA["influencer_economics"][tier]
    
    # Select primary category
    categories = list(INSTAGRAM_MARKET_DATA["shopping_categories"].keys())
    category_weights = [0.35, 0.30, 0.15, 0.12, 0.08]  # Fashion/Beauty dominant
    category = random.choices(categories, weights=category_weights)[0]
    category_data = INSTAGRAM_MARKET_DATA["shopping_categories"][category]
    
    # Geographic focus
    geo_markets = list(INSTAGRAM_MARKET_DATA["geographic_performance"].keys())
    geo_weights = [0.35, 0.25, 0.25, 0.10, 0.05]
    primary_geo = random.choices(geo_markets, weights=geo_weights)[0]
    geo_data = INSTAGRAM_MARKET_DATA["geographic_performance"][primary_geo]
    
    followers = random.randint(*tier_data["followers_range"])
    base_engagement = tier_data["avg_engagement_rate"]
    
    # Calculate seasonal adjustment
    current_quarter = f"q{((datetime.now().month - 1) // 3) + 1}"
    seasonal_multiplier = category_data["seasonal_multiplier"][current_quarter]
    
    influencer = {
        "influencer_id": f"ig_inf_{uuid.uuid4().hex[:8]}",
        "username": f"@{category.replace('_', '')}.{random.choice(['guru', 'expert', 'style', 'official', 'co'])}{random.randint(100, 999)}",
        "tier": tier,
        "category": category,
        "primary_geography": primary_geo,
        
        # Basic metrics
        "follower_count": followers,
        "following_count": random.randint(200, 3000),
        "post_count": random.randint(100, 5000),
        "story_highlights": random.randint(5, 50),
        "engagement_rate": base_engagement + random.uniform(-0.01, 0.01),
        "reach_rate": random.uniform(0.15, 0.45),
        
        # Content strategy
        "posts_per_week": random.randint(3, 14),
        "stories_per_day": random.randint(2, 15),
        "reels_per_week": random.randint(1, 7),
        "igtv_per_month": random.randint(0, 4),
        
        # Commerce integration
        "has_business_account": True,
        "instagram_shopping_enabled": True,
        "paypal_business_setup": True,
        "monthly_product_revenue": random.uniform(
            *tier_data["product_sales_monthly"]
        ) * seasonal_multiplier,
        "average_order_value": category_data["avg_order_value"] * geo_data["avg_order_value_multiplier"],
        "conversion_rate": tier_data["conversion_rate"] * geo_data["conversion_rate_multiplier"],
        
        # PayPal metrics
        "paypal_transaction_volume_monthly": 0,  # Will be calculated
        "paypal_fees_monthly": 0,  # Will be calculated
        "paypal_chargeback_rate": random.uniform(0.008, 0.025),
        "paypal_dispute_rate": random.uniform(0.015, 0.040),
        
        # Brand partnerships
        "brand_partnerships_monthly": random.randint(*tier_data["brand_partnerships_monthly"]),
        "avg_brand_deal_value": random.uniform(*tier_data["cost_per_post"]),
        "sponsored_post_rate": random.uniform(0.08, 0.25),
        
        # Audience demographics
        "audience_age_groups": {
            "13-17": random.uniform(0.05, 0.20),
            "18-24": random.uniform(0.25, 0.45),
            "25-34": random.uniform(0.25, 0.40),
            "35-44": random.uniform(0.10, 0.25),
            "45+": random.uniform(0.05, 0.15)
        },
        "audience_gender_split": {
            "female": random.uniform(0.60, 0.85) if category in ["fashion_lifestyle", "beauty_skincare"] else random.uniform(0.45, 0.65),
            "male": None,  # Calculated
            "other": random.uniform(0.01, 0.03)
        },
        "audience_geography": {
            primary_geo: random.uniform(0.45, 0.75),
            "secondary_markets": None  # Calculated
        },
        
        # Quality metrics
        "account_age_months": random.randint(12, 84),
        "verification_status": "verified" if tier in ["mega_influencer", "macro_influencer"] and random.random() < 0.7 else "unverified",
        "content_quality_score": random.uniform(0.65, 0.95),
        "brand_safety_rating": random.uniform(0.75, 0.98),
        
        # Bot contamination
        "estimated_bot_followers": int(followers * random.uniform(0.08, 0.35)),
        "bot_engagement_rate": random.uniform(0.12, 0.40),
        "authentic_engagement_rate": 0,  # Calculated
        
        # Shopping performance
        "shopping_post_performance": {
            "click_through_rate": random.uniform(0.02, 0.08),
            "save_rate": random.uniform(0.03, 0.12),
            "share_rate": random.uniform(0.01, 0.05),
            "story_shopping_ctr": random.uniform(0.04, 0.11)
        }
    }
    
    # Calculate derived metrics
    influencer["audience_gender_split"]["male"] = 1 - influencer["audience_gender_split"]["female"] - influencer["audience_gender_split"]["other"]
    influencer["authentic_engagement_rate"] = influencer["engagement_rate"] * (1 - influencer["bot_engagement_rate"])
    
    # PayPal transaction volume calculation
    monthly_transactions = int(influencer["monthly_product_revenue"] / influencer["average_order_value"])
    influencer["paypal_transaction_volume_monthly"] = influencer["monthly_product_revenue"] * category_data["paypal_usage"]
    
    # PayPal fees calculation
    paypal_fee_rate = 0.0349  # Standard PayPal rate
    influencer["paypal_fees_monthly"] = influencer["paypal_transaction_volume_monthly"] * paypal_fee_rate
    
    return influencer

def generate_instagram_content(influencer: Dict) -> Dict:
    """Generate Instagram content with shopping integration."""
    content_types = ["feed_posts", "stories", "reels", "igtv"]
    content_weights = [0.40, 0.35, 0.20, 0.05]
    content_type = random.choices(content_types, weights=content_weights)[0]
    
    performance_data = INSTAGRAM_MARKET_DATA["content_performance_by_type"][content_type]
    category_data = INSTAGRAM_MARKET_DATA["shopping_categories"][influencer["category"]]
    
    # Determine if content is promotional
    is_shopping_content = random.random() < 0.3  # 30% of content has shopping
    is_sponsored = random.random() < influencer["sponsored_post_rate"]
    
    content = {
        "content_id": f"ig_{content_type}_{uuid.uuid4().hex[:11]}",
        "influencer_id": influencer["influencer_id"],
        "content_type": content_type,
        "category": influencer["category"],
        "is_shopping_content": is_shopping_content,
        "is_sponsored": is_sponsored,
        "has_shopping_tags": is_shopping_content and random.random() < 0.8,
        "has_paypal_checkout": is_shopping_content and random.random() < 0.6,
        
        # Content metadata
        "created_at": (datetime.now() - timedelta(hours=random.randint(1, 168))).isoformat(),
        "caption_length": random.randint(50, 2200) if content_type == "feed_post" else random.randint(10, 500),
        "hashtags_count": random.randint(5, 30),
        "mentions_count": random.randint(0, 8),
        "location_tagged": random.random() < 0.4,
        
        # Engagement metrics (will be populated during simulation)
        "views": 0,
        "likes": 0,
        "comments": 0,
        "saves": 0,
        "shares": 0,
        "reach": 0,
        "impressions": 0,
        
        # Shopping metrics
        "shopping_tag_clicks": 0,
        "external_link_clicks": 0,
        "paypal_checkouts_initiated": 0,
        "paypal_transactions_completed": 0,
        "shopping_revenue": 0.0,
        
        # Content performance expectations
        "expected_reach_rate": performance_data["average_reach"],
        "expected_engagement_rate": performance_data["engagement_rate"],
        "content_lifespan_hours": performance_data["lifespan_hours"],
        "shopping_conversion_rate": performance_data.get("shopping_conversion", 0.0),
        
        # Algorithm factors
        "posting_time_optimal": random.random() < 0.7,
        "trending_audio_used": content_type == "reels" and random.random() < 0.6,
        "trending_hashtags_used": random.randint(2, 8),
        "user_generated_content": random.random() < 0.2
    }
    
    # Calculate expected metrics based on influencer and content type
    follower_reach = int(influencer["follower_count"] * content["expected_reach_rate"])
    content["reach"] = follower_reach
    content["impressions"] = int(follower_reach * random.uniform(1.2, 3.5))
    content["views"] = content["impressions"] if content_type in ["story", "reels"] else content["reach"]
    
    return content

def generate_instagram_bot(bot_type: str, target_influencers: List[Dict]) -> Dict:
    """Generate Instagram bot with shopping and PayPal interaction patterns."""
    bot_config = INSTAGRAM_BOT_TYPES[bot_type]
    target_influencer = random.choice(target_influencers)
    
    # Instagram-specific device profiles
    instagram_devices = [
        {"device": "iPhone 14 Pro", "os": "iOS 16.2", "app_version": "267.0", "screen": "1179x2556"},
        {"device": "Samsung Galaxy S23", "os": "Android 13", "app_version": "267.0", "screen": "1080x2340"},
        {"device": "Google Pixel 7", "os": "Android 13", "app_version": "267.0", "screen": "1080x2400"},
        {"device": "iPhone 13", "os": "iOS 15.7", "app_version": "266.1", "screen": "1170x2532"}
    ]
    
    device = random.choice(instagram_devices)
    
    # Bot farm locations (common Instagram bot sources)
    bot_locations = [
        {"country": "BD", "city": "Dhaka", "timezone": "UTC+6", "proxy_type": "residential"},
        {"country": "PK", "city": "Lahore", "timezone": "UTC+5", "proxy_type": "datacenter"},
        {"country": "ID", "city": "Jakarta", "timezone": "UTC+7", "proxy_type": "mobile"},
        {"country": "VN", "city": "Ho Chi Minh City", "timezone": "UTC+7", "proxy_type": "residential"},
        {"country": "NG", "city": "Lagos", "timezone": "UTC+1", "proxy_type": "datacenter"},
        {"country": "RU", "city": "Moscow", "timezone": "UTC+3", "proxy_type": "vpn"}
    ]
    
    location = random.choice(bot_locations)
    
    bot = {
        "bot_id": f"ig_bot_{bot_type}_{uuid.uuid4().hex[:8]}",
        "bot_type": bot_type,
        "description": bot_config["description"],
        "target_influencer_id": target_influencer["influencer_id"],
        "target_category": target_influencer["category"],
        
        # Technical specs
        "device_profile": device,
        "location": location,
        "creation_date": (datetime.now() - timedelta(days=random.randint(1, 1095))).isoformat(),
        
        # Bot configuration
        "behavior_config": bot_config["behavior"],
        "economics": bot_config["economics"],
        "detection_signatures": bot_config["detection_signatures"],
        
        # Instagram-specific features
        "profile_completeness": random.uniform(0.2, 0.8),
        "profile_picture": random.random() < 0.7,
        "bio_filled": random.random() < 0.6,
        "story_highlights": random.randint(0, 3),
        "posts_count": random.randint(0, 50),
        
        # Shopping interaction patterns
        "shopping_behavior": {
            "cart_abandonment_rate": random.uniform(0.85, 0.98),
            "checkout_completion_rate": random.uniform(0.02, 0.15),
            "payment_method_cycling": True,
            "suspicious_browsing_pattern": True,
            "rapid_checkout_attempts": True
        },
        
        # PayPal fraud patterns
        "paypal_fraud_indicators": {
            "multiple_payment_methods": random.randint(3, 12),
            "address_mismatches": random.uniform(0.7, 0.95),
            "device_fingerprint_inconsistency": random.uniform(0.8, 0.98),
            "behavioral_velocity_anomalies": True,
            "chargeback_history": random.random() < 0.3
        },
        
        # Operation parameters
        "daily_action_limit": random.randint(100, 2000),
        "operation_hours": random.sample(range(24), random.randint(8, 24)),
        "proxy_rotation_frequency": random.randint(2, 24),  # hours
        "account_warming_period": random.randint(3, 21),  # days
        
        # Coordination
        "bot_farm_id": f"farm_{hashlib.md5(str(random.randint(1, 100)).encode()).hexdigest()[:8]}",
        "coordination_group": f"group_{random.randint(1, 20)}",
        "operation_batch": datetime.now().strftime("%Y%m%d"),
        
        # Economics
        "operation_cost_daily": random.uniform(2.0, 25.0),
        "success_rate": random.uniform(0.65, 0.92),
        "roi_multiplier": random.uniform(3.2, 12.8) if bot_type == "reels_viral_bot" else random.uniform(0.8, 2.5)
    }
    
    return bot

def simulate_instagram_shopping_transaction(content: Dict, user_profile: Dict, influencer: Dict) -> Dict:
    """Simulate Instagram shopping transaction with PayPal integration."""
    if not content.get("has_shopping_tags") and not content.get("has_paypal_checkout"):
        return {"transaction_occurred": False, "reason": "no_shopping_integration"}
    
    # Base conversion probability
    if user_profile["user_type"] == "real":
        base_conversion = influencer["conversion_rate"]
        
        # Adjust for content type
        content_multipliers = {
            "feed_post": 1.0,
            "story": 1.3,  # Higher urgency
            "reels": 1.1,
            "igtv": 0.7
        }
        content_multiplier = content_multipliers.get(content["content_type"], 1.0)
        
        # User demographics impact
        age_group = user_profile.get("age_group", "25-34")
        age_multipliers = {
            "13-17": 0.4,  # Limited purchasing power
            "18-24": 1.2,  # High engagement, moderate power
            "25-34": 1.4,  # Peak purchasing power
            "35-44": 1.1,  # Selective but valuable
            "45+": 0.8    # Lower social commerce adoption
        }
        age_multiplier = age_multipliers.get(age_group, 1.0)
        
        # Geography impact
        geo_data = INSTAGRAM_MARKET_DATA["geographic_performance"][user_profile.get("country", "north_america")]
        geo_multiplier = geo_data["conversion_rate_multiplier"]
        
        final_conversion_rate = base_conversion * content_multiplier * age_multiplier * geo_multiplier
        
    else:  # Bot user
        # Bots have very low genuine conversion but high interaction
        shopping_behavior = user_profile.get("shopping_behavior", {})
        final_conversion_rate = shopping_behavior.get("checkout_completion_rate", 0.08)
    
    # Check if transaction occurs
    if random.random() > final_conversion_rate:
        abandon_stages = ["product_view", "add_to_cart", "checkout_initiation", "payment_details"]
        return {
            "transaction_occurred": False, 
            "abandoned_at": random.choice(abandon_stages),
            "time_spent_seconds": random.randint(10, 300)
        }
    
    # Calculate transaction details
    category_data = INSTAGRAM_MARKET_DATA["shopping_categories"][influencer["category"]]
    base_aov = influencer["average_order_value"]
    
    # Order value with variance
    order_value = base_aov * random.uniform(0.4, 3.2)
    
    # PayPal processing
    paypal_usage_rate = category_data["paypal_usage"]
    uses_paypal = random.random() < paypal_usage_rate
    
    if uses_paypal:
        payment_method = "paypal"
        if content["content_type"] == "story":
            # Stories often use express checkout
            checkout_type = "express" if random.random() < 0.8 else "standard"
        else:
            checkout_type = "express" if random.random() < 0.4 else "standard"
        
        # PayPal fees
        paypal_fee_rate = 0.0349 + 0.0030  # Rate + fixed fee approximation
        paypal_fee = order_value * paypal_fee_rate
    else:
        payment_method = random.choice(["credit_card", "debit_card", "apple_pay", "google_pay"])
        checkout_type = "standard"
        paypal_fee = 0.0
    
    # Fraud detection
    if user_profile["user_type"] == "bot":
        fraud_indicators = user_profile.get("paypal_fraud_indicators", {})
        fraud_risk_score = random.uniform(0.6, 0.95)
        fraud_detected = fraud_risk_score > 0.7
    else:
        fraud_risk_score = random.uniform(0.01, 0.12)
        fraud_detected = fraud_risk_score > 0.08  # Lower threshold for fraud
    
    transaction = {
        "transaction_occurred": True,
        "transaction_id": f"ig_shop_{uuid.uuid4().hex[:12]}",
        "timestamp": datetime.now().isoformat(),
        "user_id": user_profile["user_id"],
        "user_type": user_profile["user_type"],
        "content_id": content["content_id"],
        "influencer_id": influencer["influencer_id"],
        
        # Financial details
        "order_value": round(order_value, 2),
        "payment_method": payment_method,
        "checkout_type": checkout_type,
        "paypal_fee": round(paypal_fee, 2) if uses_paypal else 0.0,
        "net_revenue": round(order_value - paypal_fee, 2),
        "currency": "USD",
        
        # Shopping journey
        "content_type": content["content_type"],
        "shopping_entry_point": "shopping_tag" if content["has_shopping_tags"] else "bio_link",
        "time_from_click_to_purchase": random.randint(120, 2400) if user_profile["user_type"] == "real" else random.randint(30, 180),
        "items_in_cart": random.randint(1, 5),
        
        # Risk assessment
        "fraud_risk_score": fraud_risk_score,
        "fraud_detected": fraud_detected,
        "chargeback_probability": random.uniform(0.01, 0.02) if user_profile["user_type"] == "real" else random.uniform(0.15, 0.45),
        
        # Business metrics
        "customer_acquisition_cost": random.uniform(5.0, 25.0),
        "lifetime_value_estimate": order_value * random.uniform(2.8, 8.5) if user_profile["user_type"] == "real" else 0,
        "influencer_commission": order_value * random.uniform(0.05, 0.20),
        
        # Attribution
        "attribution_window_hours": 24 if content["content_type"] == "story" else 168,
        "multi_touch_attribution": random.random() < 0.35,
        "first_purchase": random.random() < 0.45,
        "repeat_customer": random.random() < 0.32
    }
    
    return transaction

# Generate Instagram influencers
print("Generating Instagram influencers with shopping integration...")
influencers = []

tier_distribution = [
    ("mega_influencer", 3),
    ("macro_influencer", 6),
    ("micro_influencer", 8),
    ("nano_influencer", 3)
]

for tier, count in tier_distribution:
    for _ in range(count):
        influencer = generate_instagram_influencer(tier)
        influencers.append(influencer)

# Generate Instagram content
print("Generating Instagram content with shopping features...")
instagram_content = []

for _ in range(NUM_CONTENT):
    influencer = random.choice(influencers)
    content = generate_instagram_content(influencer)
    instagram_content.append(content)

# Generate real users
print("Generating real Instagram users...")
real_users = []

for i in range(NUM_REAL_USERS):
    # Instagram demographics
    age_groups = ["13-17", "18-24", "25-34", "35-44", "45+"]
    age_weights = [0.15, 0.35, 0.28, 0.15, 0.07]
    age_group = random.choices(age_groups, weights=age_weights)[0]
    
    # Geographic distribution
    geo_markets = list(INSTAGRAM_MARKET_DATA["geographic_performance"].keys())
    geo_weights = [0.35, 0.25, 0.25, 0.10, 0.05]
    country = random.choices(geo_markets, weights=geo_weights)[0]
    
    # Shopping interests
    shopping_categories = list(INSTAGRAM_MARKET_DATA["shopping_categories"].keys())
    interests = random.sample(shopping_categories, random.randint(1, 3))
    
    user = {
        "user_id": f"ig_user_{uuid.uuid4().hex[:8]}",
        "user_type": "real",
        "age_group": age_group,
        "country": country,
        "interests": interests,
        "gender": random.choice(["female", "male", "other"]),
        
        # Instagram usage
        "daily_usage_minutes": random.randint(25, 150),
        "stories_viewed_daily": random.randint(20, 200),
        "posts_liked_daily": random.randint(10, 100),
        "accounts_following": random.randint(100, 2000),
        
        # Shopping behavior
        "shops_on_instagram": random.random() < 0.44,  # 44% shop on Instagram
        "average_monthly_spending": random.uniform(50, 500),
        "preferred_payment_method": random.choices(
            ["paypal", "credit_card", "apple_pay", "google_pay"],
            weights=[0.35, 0.40, 0.15, 0.10]
        )[0],
        "impulse_buyer": random.random() < 0.32,
        
        # Device and behavior
        "primary_device": random.choice(["iPhone", "Android"]),
        "connection_quality": random.choice(["excellent", "good", "fair"]),
        "notification_enabled": random.random() < 0.78,
        
        # Engagement patterns
        "engagement_likelihood": random.uniform(0.02, 0.15),
        "comment_probability": random.uniform(0.01, 0.08),
        "story_interaction_rate": random.uniform(0.05, 0.25),
        "share_probability": random.uniform(0.005, 0.03)
    }
    
    real_users.append(user)

# Generate Instagram bots
print("Generating Instagram bots...")
instagram_bots = []

for i in range(NUM_BOTS):
    bot_type = random.choice(list(INSTAGRAM_BOT_TYPES.keys()))
    bot = generate_instagram_bot(bot_type, influencers)
    instagram_bots.append(bot)

# Run simulation
print("Running Instagram influencer shopping simulation...")
engagement_log = []
shopping_transactions = []
detection_events = []

for step in range(SIMULATION_STEPS):
    current_time = datetime.now() + timedelta(minutes=step * 12)  # 12-minute intervals
    
    # Real user interactions
    for user in real_users:
        if random.random() < 0.25:  # 25% active per interval
            # Select content based on interests
            relevant_content = [c for c in instagram_content 
                             if c["category"] in user["interests"]]
            if not relevant_content:
                relevant_content = random.sample(instagram_content, min(3, len(instagram_content)))
            
            content = random.choice(relevant_content)
            influencer = next(inf for inf in influencers if inf["influencer_id"] == content["influencer_id"])
            
            # Interaction type based on content
            if content["content_type"] == "story":
                interaction_duration = random.randint(3, 15)  # Seconds
                action = "story_view"
            elif content["content_type"] == "reels":
                interaction_duration = random.randint(5, 60)
                action = "reels_view"
            else:
                interaction_duration = random.randint(2, 30)
                action = "post_view"
            
            engagement_event = {
                "timestamp": current_time.isoformat(),
                "step": step,
                "user_id": user["user_id"],
                "user_type": "real",
                "action": action,
                "content_id": content["content_id"],
                "content_type": content["content_type"],
                "influencer_id": influencer["influencer_id"],
                "category": content["category"],
                "interaction_duration": interaction_duration,
                "country": user["country"],
                "age_group": user["age_group"],
                "device": user["primary_device"]
            }
            
            engagement_log.append(engagement_event)
            
            # Shopping interaction
            if content["has_shopping_tags"] and user["shops_on_instagram"]:
                if random.random() < 0.08:  # 8% click shopping tags
                    # Add user_type to user profile for transaction simulation
                    user_profile = dict(user)
                    user_profile["user_type"] = "real"
                    user_profile["user_id"] = user["user_id"]
                    
                    shopping_transaction = simulate_instagram_shopping_transaction(
                        content, user_profile, influencer
                    )
                    
                    if shopping_transaction["transaction_occurred"]:
                        shopping_transactions.append(shopping_transaction)
            
            # Regular engagement
            if random.random() < user["engagement_likelihood"]:
                engagement_type = random.choices(
                    ["like", "comment", "save", "share"],
                    weights=[0.7, 0.15, 0.1, 0.05]
                )[0]
                
                engagement_log.append({
                    "timestamp": current_time.isoformat(),
                    "step": step,
                    "user_id": user["user_id"],
                    "user_type": "real",
                    "action": engagement_type,
                    "content_id": content["content_id"],
                    "influencer_id": influencer["influencer_id"],
                    "authenticity_score": random.uniform(0.85, 1.0)
                })
    
    # Bot interactions
    for bot in instagram_bots:
        if random.random() < 0.4:  # 40% active per interval
            # Target specific influencer
            target_content = [c for c in instagram_content 
                            if c["influencer_id"] == bot["target_influencer_id"]]
            if not target_content:
                target_content = random.sample(instagram_content, min(2, len(instagram_content)))
            
            content = random.choice(target_content)
            influencer = next(inf for inf in influencers if inf["influencer_id"] == content["influencer_id"])
            
            bot_behavior = bot["behavior_config"]
            
            # Bot interaction
            engagement_event = {
                "timestamp": current_time.isoformat(),
                "step": step,
                "user_id": bot["bot_id"],
                "user_type": "bot",
                "bot_type": bot["bot_type"],
                "action": f"bot_{content['content_type']}_interaction",
                "content_id": content["content_id"],
                "influencer_id": influencer["influencer_id"],
                "bot_farm_id": bot["bot_farm_id"],
                "detection_risk": random.uniform(0.4, 0.95),
                "suspicious_timing": True
            }
            
            engagement_log.append(engagement_event)
            
            # Bot shopping behavior (usually fraudulent)
            if content["has_shopping_tags"] and bot["bot_type"] == "shopping_conversion_bot":
                if random.random() < 0.25:  # High shopping interaction rate
                    # Add user_type to bot profile for transaction simulation
                    bot_profile = dict(bot)
                    bot_profile["user_type"] = "bot"
                    bot_profile["user_id"] = bot["bot_id"]
                    
                    shopping_transaction = simulate_instagram_shopping_transaction(
                        content, bot_profile, influencer
                    )
                    
                    if shopping_transaction["transaction_occurred"]:
                        shopping_transactions.append(shopping_transaction)
                        
                        # Fraud detection event
                        if shopping_transaction["fraud_detected"]:
                            detection_events.append({
                                "timestamp": current_time.isoformat(),
                                "event_type": "instagram_shopping_fraud",
                                "bot_id": bot["bot_id"],
                                "transaction_id": shopping_transaction["transaction_id"],
                                "fraud_score": shopping_transaction["fraud_risk_score"],
                                "amount": shopping_transaction["order_value"]
                            })
            
            # Bot engagement actions
            bot_behavior = bot["behavior_config"]
            if random.random() < bot_behavior["like_rate"]:
                engagement_log.append({
                    "timestamp": current_time.isoformat(),
                    "step": step,
                    "user_id": bot["bot_id"],
                    "user_type": "bot",
                    "bot_type": bot["bot_type"],
                    "action": "like",
                    "content_id": content["content_id"],
                    "influencer_id": influencer["influencer_id"],
                    "automation_detected": True
                })

# Calculate comprehensive analytics
print("Calculating Instagram shopping analytics...")

total_transactions = len(shopping_transactions)
genuine_transactions = len([t for t in shopping_transactions if not t.get("fraud_detected", False)])
bot_transactions = len([t for t in shopping_transactions if "bot" in t.get("user_id", "")])

total_revenue = sum(t["order_value"] for t in shopping_transactions)
genuine_revenue = sum(t["order_value"] for t in shopping_transactions if not t.get("fraud_detected", False))
paypal_fees = sum(t["paypal_fee"] for t in shopping_transactions)

analytics = {
    "instagram_market_data": INSTAGRAM_MARKET_DATA,
    "simulation_summary": {
        "influencers": len(influencers),
        "content_pieces": len(instagram_content),
        "real_users": len(real_users),
        "bots": len(instagram_bots),
        "total_engagements": len(engagement_log),
        "shopping_transactions": total_transactions,
        "fraud_detection_events": len(detection_events)
    },
    "shopping_performance": {
        "total_revenue": round(total_revenue, 2),
        "genuine_revenue": round(genuine_revenue, 2),
        "fraud_loss": round(total_revenue - genuine_revenue, 2),
        "fraud_rate": round((total_transactions - genuine_transactions) / total_transactions if total_transactions > 0 else 0, 3),
        "paypal_fees_total": round(paypal_fees, 2),
        "net_revenue": round(genuine_revenue - paypal_fees, 2),
        "average_order_value": round(total_revenue / total_transactions if total_transactions > 0 else 0, 2)
    },
    "platform_metrics": {
        "engagement_rate": round(len(engagement_log) / (len(real_users) + len(instagram_bots)) / SIMULATION_STEPS, 3),
        "bot_engagement_percentage": round(len([e for e in engagement_log if e["user_type"] == "bot"]) / len(engagement_log), 3),
        "shopping_conversion_rate": round(total_transactions / len([e for e in engagement_log if "view" in e["action"]]) if len(engagement_log) > 0 else 0, 4),
        "paypal_usage_rate": round(len([t for t in shopping_transactions if t["payment_method"] == "paypal"]) / total_transactions if total_transactions > 0 else 0, 3)
    },
    "tier_performance": {},
    "category_performance": {},
    "fraud_analysis": {
        "bot_transaction_rate": round(bot_transactions / total_transactions if total_transactions > 0 else 0, 3),
        "fraud_detection_accuracy": round(len(detection_events) / bot_transactions if bot_transactions > 0 else 1.0, 3),
        "chargeback_risk": round(sum(t["chargeback_probability"] for t in shopping_transactions) / total_transactions if total_transactions > 0 else 0, 3)
    }
}

# Tier performance analysis
for tier in ["mega_influencer", "macro_influencer", "micro_influencer", "nano_influencer"]:
    tier_influencers = [inf for inf in influencers if inf["tier"] == tier]
    tier_transactions = [t for t in shopping_transactions 
                        if any(t["influencer_id"] == inf["influencer_id"] for inf in tier_influencers)]
    
    analytics["tier_performance"][tier] = {
        "influencer_count": len(tier_influencers),
        "total_revenue": round(sum(t["order_value"] for t in tier_transactions), 2),
        "transaction_count": len(tier_transactions),
        "avg_conversion_rate": round(sum(inf["conversion_rate"] for inf in tier_influencers) / len(tier_influencers) if tier_influencers else 0, 4)
    }

# Category performance analysis
for category in INSTAGRAM_MARKET_DATA["shopping_categories"].keys():
    category_transactions = [t for t in shopping_transactions 
                           if any(inf["category"] == category and inf["influencer_id"] == t["influencer_id"] for inf in influencers)]
    
    analytics["category_performance"][category] = {
        "transaction_count": len(category_transactions),
        "total_revenue": round(sum(t["order_value"] for t in category_transactions), 2),
        "avg_order_value": round(sum(t["order_value"] for t in category_transactions) / len(category_transactions) if category_transactions else 0, 2)
    }

# Save comprehensive data
import os
os.makedirs("../data", exist_ok=True)

simulation_data = {
    "metadata": {
        "platform": "instagram",
        "simulation_type": "influencer_shopping_with_paypal",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "shopping_integration",
            "paypal_transactions",
            "fraud_detection",
            "tier_analysis",
            "real_time_market_data"
        ]
    },
    "influencers": influencers,
    "content": instagram_content,
    "real_users": real_users,
    "bots": instagram_bots,
    "engagement_log": engagement_log,
    "shopping_transactions": shopping_transactions,
    "detection_events": detection_events,
    "analytics": analytics
}

with open("../data/instagram_influencer_shopping_simulation.json", "w") as f:
    json.dump(simulation_data, f, indent=2, default=str)

print(f"\n📸 Instagram Influencer Shopping Simulation Complete!")
print(f"👥 Influencers: {len(influencers)} | Content: {len(instagram_content)}")
print(f"🧑‍🤝‍🧑 Real Users: {len(real_users)} | 🤖 Bots: {len(instagram_bots)}")
print(f"🛒 Shopping Transactions: {total_transactions}")
print(f"💰 Total Revenue: ${total_revenue:,.2f}")
print(f"💳 PayPal Fees: ${paypal_fees:,.2f}")
print(f"🚨 Fraud Loss: ${total_revenue - genuine_revenue:,.2f}")
print(f"🛡️ Fraud Detection Events: {len(detection_events)}")

if __name__ == "__main__":
    scale_parameters(scale_factor=1)
