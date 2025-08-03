import random
import json
import time
import numpy as np
from datetime import datetime, timedelta
import uuid
import hashlib
import re

def scale_parameters(scale_factor=1):
    """Scale simulation parameters for large-scale Twitter/X analysis."""
    global NUM_INFLUENCERS, NUM_REAL_USERS, NUM_BOTS, NUM_TWEETS, SIMULATION_STEPS
    NUM_INFLUENCERS = int(NUM_INFLUENCERS * scale_factor)
    NUM_REAL_USERS = int(NUM_REAL_USERS * scale_factor)
    NUM_BOTS = int(NUM_BOTS * scale_factor)
    NUM_TWEETS = int(NUM_TWEETS * scale_factor)
    SIMULATION_STEPS = int(SIMULATION_STEPS * scale_factor)
    print(f"Twitter/X Parameters scaled by factor {scale_factor}:")
    print(f"NUM_INFLUENCERS: {NUM_INFLUENCERS}")
    print(f"NUM_REAL_USERS: {NUM_REAL_USERS}")
    print(f"NUM_BOTS: {NUM_BOTS}")
    print(f"NUM_TWEETS: {NUM_TWEETS}")
    print(f"SIMULATION_STEPS: {SIMULATION_STEPS}")

# Twitter/X Simulation parameters
NUM_INFLUENCERS = 8
NUM_REAL_USERS = 150
NUM_BOTS = 35
NUM_TWEETS = 25
SIMULATION_STEPS = 60

# Enhanced Twitter/X bot types based on real platform analysis
TWITTER_BOT_TYPES = {
    "amplification_bot": {
        "description": "Amplifies specific tweets/accounts through retweets and likes",
        "behavior": {
            "retweet_rate": 0.8,
            "like_rate": 0.9,
            "reply_rate": 0.2,
            "quote_tweet_rate": 0.1,
            "follow_rate": 0.3,
            "engagement_delay_seconds": (1, 30),
            "target_hashtags": ["#sponsored", "#ad", "#promo", "#deal", "#sale"],
            "typical_replies": [
                "This is amazing!", "So true!", "Facts!", "100%", "Exactly!",
                "Love this!", "Can't wait!", "Best deal ever!", "Don't miss out!",
                "Get yours now!", "Limited time only!", "Incredible!"
            ]
        },
        "detection_signatures": {
            "high_retweet_ratio": True,
            "minimal_original_content": True,
            "coordinated_timing": True,
            "promotional_focus": True
        }
    },
    "reply_farm": {
        "description": "Generates fake replies to create artificial engagement",
        "behavior": {
            "retweet_rate": 0.1,
            "like_rate": 0.4,
            "reply_rate": 0.9,
            "quote_tweet_rate": 0.05,
            "follow_rate": 0.1,
            "engagement_delay_seconds": (5, 120),
            "target_hashtags": ["#giveaway", "#contest", "#win", "#free"],
            "typical_replies": [
                "First!", "Thanks for sharing!", "Great content!", "Following!",
                "Done!", "Shared!", "Tagged friends!", "Hope I win!",
                "Count me in!", "Participating!", "Love your posts!"
            ]
        },
        "detection_signatures": {
            "generic_replies": True,
            "high_reply_frequency": True,
            "short_reply_length": True,
            "contest_focus": True
        }
    },
    "follower_farm": {
        "description": "Generates fake followers for influence inflation",
        "behavior": {
            "retweet_rate": 0.05,
            "like_rate": 0.1,
            "reply_rate": 0.02,
            "quote_tweet_rate": 0.01,
            "follow_rate": 0.95,
            "engagement_delay_seconds": (1, 10),
            "target_hashtags": [],
            "typical_replies": [
                "Following!", "Great account!", "New follower here!",
                "Supporting you!", "Love your content!"
            ]
        },
        "detection_signatures": {
            "follow_without_engagement": True,
            "minimal_activity": True,
            "rapid_following": True,
            "inactive_after_follow": True
        }
    },
    "trend_manipulation": {
        "description": "Manipulates trending topics and hashtags",
        "behavior": {
            "retweet_rate": 0.6,
            "like_rate": 0.7,
            "reply_rate": 0.4,
            "quote_tweet_rate": 0.3,
            "follow_rate": 0.1,
            "engagement_delay_seconds": (1, 60),
            "target_hashtags": ["#trending", "#viral", "#breaking", "#news"],
            "typical_replies": [
                "This needs to trend!", "Everyone needs to see this!",
                "Retweet for visibility!", "Make this viral!",
                "Spread the word!", "This is important!"
            ]
        },
        "detection_signatures": {
            "hashtag_manipulation": True,
            "coordinated_trending": True,
            "artificial_virality": True,
            "synchronized_posting": True
        }
    },
    "sophisticated_ai_bot": {
        "description": "AI-powered bots with human-like behavior and contextual responses",
        "behavior": {
            "retweet_rate": 0.3,
            "like_rate": 0.4,
            "reply_rate": 0.6,
            "quote_tweet_rate": 0.2,
            "follow_rate": 0.05,
            "engagement_delay_seconds": (30, 300),
            "target_hashtags": ["#AI", "#tech", "#innovation", "#business"],
            "typical_replies": [
                "Interesting perspective on {topic}",
                "This aligns with recent research showing {data}",
                "Have you considered the implications of {concept}?",
                "Building on this point: {extension}",
                "Data suggests this trend will continue"
            ]
        },
        "detection_signatures": {
            "ai_generated_content": True,
            "sophisticated_language": True,
            "contextual_responses": True,
            "delayed_engagement": True
        }
    }
}

# Enhanced Twitter/X network patterns
TWITTER_NETWORK_PATTERNS = {
    "real_users": {
        "connection_types": [
            {"type": "mobile_5g", "speed_mbps": (50, 500), "latency_ms": (15, 40), "weight": 0.4},
            {"type": "mobile_4g", "speed_mbps": (5, 50), "latency_ms": (30, 80), "weight": 0.3},
            {"type": "wifi_home", "speed_mbps": (25, 300), "latency_ms": (10, 30), "weight": 0.2},
            {"type": "wifi_public", "speed_mbps": (10, 100), "latency_ms": (20, 60), "weight": 0.1}
        ],
        "device_patterns": {
            "mobile_app": 0.75,
            "web_browser": 0.20,
            "third_party_client": 0.05
        }
    },
    "bots": {
        "connection_types": [
            {"type": "datacenter", "speed_mbps": (100, 1000), "latency_ms": (1, 5), "weight": 0.5},
            {"type": "residential_proxy", "speed_mbps": (20, 100), "latency_ms": (15, 50), "weight": 0.3},
            {"type": "mobile_proxy", "speed_mbps": (10, 50), "latency_ms": (50, 150), "weight": 0.2}
        ],
        "device_patterns": {
            "automation_client": 0.6,
            "web_browser": 0.3,
            "mobile_app": 0.1
        }
    }
}

# Payment business integration patterns (key enhancement)
PAYMENT_BUSINESS_PATTERNS = {
    "in_app_purchase_drivers": {
        "e_commerce": {
            "conversion_tactics": ["flash_sales", "limited_time_offers", "exclusive_discounts", "social_proof"],
            "target_demographics": ["18-24", "25-34", "35-44"],
            "payment_methods": ["credit_card", "digital_wallet", "bnpl", "cryptocurrency"],
            "average_transaction_value": {"min": 25, "max": 500},
            "conversion_rate_real_traffic": 0.02,
            "conversion_rate_bot_traffic": 0.001,
            "revenue_per_conversion": {"min": 15, "max": 200}
        },
        "subscription_services": {
            "conversion_tactics": ["free_trial", "premium_features", "social_influence", "fomo_marketing"],
            "target_demographics": ["25-34", "35-44", "45-54"],
            "payment_methods": ["recurring_billing", "annual_payment", "family_plans"],
            "average_transaction_value": {"min": 9.99, "max": 99.99},
            "conversion_rate_real_traffic": 0.05,
            "conversion_rate_bot_traffic": 0.0001,
            "revenue_per_conversion": {"min": 9.99, "max": 599.99}
        },
        "gaming_monetization": {
            "conversion_tactics": ["in_game_currency", "cosmetic_items", "pay_to_win", "battle_passes"],
            "target_demographics": ["13-17", "18-24", "25-34"],
            "payment_methods": ["micro_transactions", "gaming_currency", "gift_cards"],
            "average_transaction_value": {"min": 0.99, "max": 99.99},
            "conversion_rate_real_traffic": 0.08,
            "conversion_rate_bot_traffic": 0.0,
            "revenue_per_conversion": {"min": 0.99, "max": 299.99}
        },
        "financial_services": {
            "conversion_tactics": ["investment_advice", "trading_signals", "crypto_tips", "robo_advisors"],
            "target_demographics": ["25-34", "35-44", "45-54"],
            "payment_methods": ["premium_subscriptions", "trading_fees", "management_fees"],
            "average_transaction_value": {"min": 29.99, "max": 2999.99},
            "conversion_rate_real_traffic": 0.01,
            "conversion_rate_bot_traffic": 0.0005,
            "revenue_per_conversion": {"min": 29.99, "max": 9999.99}
        }
    },
    "social_commerce_integration": {
        "influencer_marketing": {
            "commission_rates": {"micro": 0.05, "macro": 0.08, "mega": 0.12},
            "engagement_multiplier": {"real": 1.0, "bot": 0.1},
            "trust_factor": {"verified": 1.2, "unverified": 0.8},
            "conversion_attribution": {"direct": 0.6, "indirect": 0.4}
        },
        "social_proof_mechanisms": {
            "like_count_influence": 0.15,
            "retweet_amplification": 0.25,
            "reply_engagement": 0.10,
            "follower_count_credibility": 0.20,
            "verification_trust_boost": 0.30
        }
    }
}

# Enhanced behavioral patterns for Twitter/X
TWITTER_BEHAVIORAL_PATTERNS = {
    "real_users": {
        "tweet_frequency_daily": (0.5, 8),
        "scroll_speed_tweets_per_minute": (15, 40),
        "engagement_delay_seconds": (2, 30),
        "reading_time_per_tweet": (3, 15),
        "hashtag_usage_rate": 0.3,
        "mention_usage_rate": 0.2,
        "link_click_rate": 0.15,
        "quote_tweet_with_comment": 0.8,
        "thread_reading_completion": 0.6,
        "notification_response_time": (60, 3600)
    },
    "bots": {
        "tweet_frequency_daily": (10, 100),
        "scroll_speed_tweets_per_minute": (60, 200),
        "engagement_delay_seconds": (0.5, 5),
        "reading_time_per_tweet": (0.1, 2),
        "hashtag_usage_rate": 0.8,
        "mention_usage_rate": 0.6,
        "link_click_rate": 0.05,
        "quote_tweet_with_comment": 0.2,
        "thread_reading_completion": 0.1,
        "notification_response_time": (1, 30)
    }
}

# Generate realistic Twitter/X influencers with payment business focus
def generate_twitter_influencers():
    influencers = []
    business_types = ["e_commerce", "subscription_services", "gaming_monetization", "financial_services"]
    
    for i in range(NUM_INFLUENCERS):
        business_type = random.choice(business_types)
        business_config = PAYMENT_BUSINESS_PATTERNS["in_app_purchase_drivers"][business_type]
        
        # Follower tiers based on influence level
        influence_tier = random.choice([
            {"tier": "micro", "followers": (1000, 10000), "engagement_rate": (0.05, 0.15)},
            {"tier": "mid", "followers": (10000, 100000), "engagement_rate": (0.03, 0.08)},
            {"tier": "macro", "followers": (100000, 1000000), "engagement_rate": (0.02, 0.05)},
            {"tier": "mega", "followers": (1000000, 10000000), "engagement_rate": (0.01, 0.03)}
        ])
        
        influencer = {
            "influencer_id": f"influencer_{i}",
            "username": f"@{business_type.split('_')[0]}guru{i}",
            "display_name": f"{business_type.title().replace('_', ' ')} Expert {i}",
            "follower_count": random.randint(*influence_tier["followers"]),
            "following_count": random.randint(100, 2000),
            "tweet_count": random.randint(1000, 50000),
            "account_age_days": random.randint(180, 2000),
            "verified": random.choice([True, False]),
            "influence_tier": influence_tier["tier"],
            "business_type": business_type,
            "business_config": business_config,
            "engagement_rate": random.uniform(*influence_tier["engagement_rate"]),
            
            # Payment business metrics
            "monetization_methods": random.sample([
                "affiliate_marketing", "sponsored_posts", "product_sales", 
                "subscription_service", "course_sales", "consulting"
            ], random.randint(2, 4)),
            "average_post_reach": influence_tier["followers"][1] * random.uniform(0.1, 0.3),
            "conversion_rate": business_config["conversion_rate_real_traffic"] * random.uniform(0.8, 1.2),
            "revenue_per_post": random.uniform(50, 5000) * (1 if influence_tier["tier"] == "micro" else 
                                                          3 if influence_tier["tier"] == "mid" else
                                                          10 if influence_tier["tier"] == "macro" else 50),
            
            # Bio and content strategy
            "bio": f"💰 {business_type.title().replace('_', ' ')} Expert | 🚀 Helping you succeed | 📈 DM for collabs",
            "content_themes": random.sample([
                "tips_and_tricks", "product_reviews", "industry_news", 
                "behind_the_scenes", "motivational", "educational"
            ], random.randint(3, 5)),
            "posting_schedule": random.choice(["daily", "twice_daily", "weekly", "sporadic"]),
            "peak_activity_hours": random.sample(range(24), random.randint(4, 8))
        }
        influencers.append(influencer)
    
    return influencers

# Generate realistic Twitter/X content with payment business focus
def generate_twitter_content(influencers):
    tweets = []
    
    for i in range(NUM_TWEETS):
        influencer = influencers[i % NUM_INFLUENCERS]
        business_type = influencer["business_type"]
        business_config = influencer["business_config"]
        
        # Content templates based on business type
        content_templates = {
            "e_commerce": [
                f"🔥 FLASH SALE: 50% off everything! Limited time only! Use code SAVE50 ⏰ #{random.choice(['sale', 'discount', 'deal', 'shopping'])}",
                f"Just dropped: New collection is LIVE! 🛍️ What's your favorite piece? Link in bio 👆 #{random.choice(['newdrop', 'fashion', 'style'])}",
                f"Customer review: 'Best purchase I've made all year!' ⭐⭐⭐⭐⭐ What are you waiting for? #{random.choice(['review', 'quality', 'bestseller'])}",
                f"FREE shipping on orders over $75! No code needed 📦✨ #{random.choice(['freeshipping', 'offer', 'deal'])}"
            ],
            "subscription_services": [
                f"🎯 Unlock premium features today! First month FREE for new subscribers 💎 #{random.choice(['premium', 'free', 'trial', 'upgrade'])}",
                f"Join 10K+ users already saving time with our platform! ⏰ 7-day free trial, cancel anytime 🔓 #{random.choice(['productivity', 'trial', 'users'])}",
                f"New feature alert! 🚨 Dark mode is finally here! Premium subscribers get it first 🌙 #{random.choice(['feature', 'premium', 'update'])}",
                f"Why pay monthly when you can save 40% with annual billing? 💰 #{random.choice(['savings', 'annual', 'deal'])}"
            ],
            "gaming_monetization": [
                f"🎮 New battle pass is INSANE! Epic rewards await! Who's jumping in? #{random.choice(['gaming', 'battlepass', 'rewards'])}",
                f"Pro tip: This skin combo is 🔥 What's your loadout? Drop it below! 👇 #{random.choice(['gaming', 'skins', 'protip'])}",
                f"GIVEAWAY! 🎁 RT + Follow for a chance to win 1000 V-Bucks! Winner in 24h ⏰ #{random.choice(['giveaway', 'gaming', 'win'])}",
                f"Game update dropping tomorrow! New characters + weapons incoming 💪 #{random.choice(['update', 'gaming', 'new'])}"
            ],
            "financial_services": [
                f"📈 Market analysis: Why now is the time to invest in crypto! Thread below 🧵 #{random.choice(['crypto', 'investing', 'market'])}",
                f"💡 Personal finance tip: Automate your savings! Start with just $10/week 💰 #{random.choice(['finance', 'savings', 'tips'])}",
                f"🚨 Alert: Stock XYZ showing bullish patterns! Not financial advice 📊 #{random.choice(['stocks', 'trading', 'analysis'])}",
                f"Join my premium Discord for daily trading signals! Link in bio 📈 #{random.choice(['trading', 'signals', 'premium'])}"
            ]
        }
        
        tweet_content = random.choice(content_templates[business_type])
        
        # Add payment/monetization hooks
        monetization_hooks = {
            "e_commerce": ["Link in bio!", "DM to order", "Use code SAVE20", "Free shipping today!"],
            "subscription_services": ["Start free trial", "Upgrade now", "Join premium", "Cancel anytime"],
            "gaming_monetization": ["Get it now", "Limited time", "Exclusive offer", "Battle pass"],
            "financial_services": ["Premium members only", "Join Discord", "Not financial advice", "DM for details"]
        }
        
        if random.random() < 0.7:  # 70% chance to add monetization hook
            hook = random.choice(monetization_hooks[business_type])
            tweet_content += f" {hook}"
        
        tweet = {
            "tweet_id": f"tw_{uuid.uuid4().hex[:10]}",
            "influencer": influencer["influencer_id"],
            "username": influencer["username"],
            "display_name": influencer["display_name"],
            "content": tweet_content,
            "hashtags": re.findall(r'#\w+', tweet_content),
            "mentions": re.findall(r'@\w+', tweet_content),
            "has_link": "link" in tweet_content.lower() or "bio" in tweet_content.lower(),
            "has_media": random.choice([True, False]),
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 1440))).isoformat(),
            "business_type": business_type,
            "monetization_intent": random.choice([True, False]),
            "cta_present": any(hook.lower() in tweet_content.lower() for hook in monetization_hooks[business_type]),
            
            # Engagement metrics
            "like_count": 0,
            "retweet_count": 0,
            "reply_count": 0,
            "quote_tweet_count": 0,
            "bookmark_count": 0,
            "view_count": 0,
            
            # Payment business metrics
            "estimated_reach": influencer["average_post_reach"] * random.uniform(0.8, 1.2),
            "click_through_rate": random.uniform(0.01, 0.05),
            "conversion_potential": influencer["conversion_rate"],
            "revenue_potential": random.uniform(10, influencer["revenue_per_post"]),
            
            # Content analysis
            "sentiment": random.choice(["positive", "neutral", "negative"]),
            "urgency_level": random.uniform(0.1, 1.0),
            "promotional_score": random.uniform(0.3, 1.0) if "sale" in tweet_content.lower() else random.uniform(0.1, 0.5)
        }
        tweets.append(tweet)
    
    return tweets

# Enhanced network profile generation for Twitter/X
def generate_twitter_network_profile(user_type="real"):
    """Generate realistic network profile with Twitter/X specific patterns."""
    if user_type == "real":
        connection = random.choices(
            TWITTER_NETWORK_PATTERNS["real_users"]["connection_types"],
            weights=[c["weight"] for c in TWITTER_NETWORK_PATTERNS["real_users"]["connection_types"]]
        )[0]
        
        device_choice = random.choices(
            list(TWITTER_NETWORK_PATTERNS["real_users"]["device_patterns"].keys()),
            weights=list(TWITTER_NETWORK_PATTERNS["real_users"]["device_patterns"].values())
        )[0]
        
        return {
            "connection_type": connection["type"],
            "speed_mbps": random.uniform(*connection["speed_mbps"]),
            "latency_ms": random.uniform(*connection["latency_ms"]),
            "device_access": device_choice,
            "ip_address": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "location_services": random.choice([True, False]),
            "wifi_name": f"Network_{random.randint(1000,9999)}" if "wifi" in connection["type"] else None,
            "carrier": random.choice(["Verizon", "AT&T", "T-Mobile", "Sprint"]) if "mobile" in connection["type"] else None,
            "vpn_detected": False,
            "proxy_detected": False
        }
    else:  # bot
        connection = random.choices(
            TWITTER_NETWORK_PATTERNS["bots"]["connection_types"],
            weights=[c["weight"] for c in TWITTER_NETWORK_PATTERNS["bots"]["connection_types"]]
        )[0]
        
        device_choice = random.choices(
            list(TWITTER_NETWORK_PATTERNS["bots"]["device_patterns"].keys()),
            weights=list(TWITTER_NETWORK_PATTERNS["bots"]["device_patterns"].values())
        )[0]
        
        return {
            "connection_type": connection["type"],
            "speed_mbps": random.uniform(*connection["speed_mbps"]),
            "latency_ms": random.uniform(*connection["latency_ms"]),
            "device_access": device_choice,
            "ip_address": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "suspicious_indicators": ["consistent_timing", "datacenter_ip"] if connection["type"] == "datacenter" else ["proxy_rotation"],
            "vpn_detected": connection["type"] in ["residential_proxy", "mobile_proxy"],
            "proxy_detected": True,
            "automation_client": device_choice == "automation_client"
        }

# Generate realistic Twitter/X users
def generate_twitter_users():
    real_users = []
    
    for i in range(NUM_REAL_USERS):
        user_demographics = random.choice([
            {"age_group": "13-17", "interests": ["gaming", "entertainment", "memes"], "daily_usage_hours": random.uniform(2, 5)},
            {"age_group": "18-24", "interests": ["tech", "music", "lifestyle"], "daily_usage_hours": random.uniform(1, 4)},
            {"age_group": "25-34", "interests": ["business", "finance", "news"], "daily_usage_hours": random.uniform(0.5, 3)},
            {"age_group": "35-44", "interests": ["politics", "parenting", "health"], "daily_usage_hours": random.uniform(0.5, 2)},
            {"age_group": "45+", "interests": ["news", "politics", "family"], "daily_usage_hours": random.uniform(0.2, 1.5)}
        ])
        
        network_profile = generate_twitter_network_profile("real")
        behavioral_patterns = TWITTER_BEHAVIORAL_PATTERNS["real_users"]
        
        user = {
            "user_id": f"twitter_user_{uuid.uuid4().hex[:8]}",
            "username": f"@user{i}_{random.choice(['real', 'person', 'human'])}",
            "display_name": f"Real User {i}",
            "user_type": "real",
            "age_group": user_demographics["age_group"],
            "interests": user_demographics["interests"],
            "follower_count": random.randint(50, 5000),
            "following_count": random.randint(100, 2000),
            "tweet_count": random.randint(10, 10000),
            "account_age_days": random.randint(30, 3650),
            "verified": False,
            "location": random.choice(["US", "UK", "CA", "AU", "DE", "FR", "ES", "BR", "IN", "JP"]),
            "daily_usage_hours": user_demographics["daily_usage_hours"],
            
            # Payment behavior
            "purchase_behavior": {
                "online_shopping_frequency": random.choice(["weekly", "monthly", "quarterly", "rarely"]),
                "social_commerce_participation": random.choice([True, False]),
                "influenced_by_social_media": random.choice([True, False]),
                "payment_methods": random.sample(["credit_card", "paypal", "apple_pay", "google_pay"], random.randint(1, 3)),
                "average_purchase_value": random.uniform(25, 500),
                "impulse_buying_tendency": random.uniform(0.1, 0.8)
            },
            
            # Network and behavioral profiles
            "network_profile": network_profile,
            "behavioral_patterns": {
                "tweet_frequency_daily": random.uniform(*behavioral_patterns["tweet_frequency_daily"]),
                "scroll_speed": random.uniform(*behavioral_patterns["scroll_speed_tweets_per_minute"]),
                "engagement_delay": random.uniform(*behavioral_patterns["engagement_delay_seconds"]),
                "reading_time": random.uniform(*behavioral_patterns["reading_time_per_tweet"]),
                "hashtag_usage": random.random() < behavioral_patterns["hashtag_usage_rate"],
                "link_clicking": random.random() < behavioral_patterns["link_click_rate"]
            },
            
            # Device information
            "device_info": {
                "primary_device": random.choice(["iPhone", "Android", "Desktop", "Tablet"]),
                "app_version": f"9.{random.randint(20, 95)}.0",
                "operating_system": random.choice(["iOS 16", "Android 13", "Windows 11", "macOS Monterey"]),
                "screen_time_daily": random.uniform(30, 300)  # minutes
            }
        }
        real_users.append(user)
    
    return real_users

# Generate Twitter/X bots with payment business targeting
def generate_twitter_bots():
    bots = []
    
    for i in range(NUM_BOTS):
        bot_type = random.choice(list(TWITTER_BOT_TYPES.keys()))
        bot_config = TWITTER_BOT_TYPES[bot_type]
        network_profile = generate_twitter_network_profile("bot")
        behavioral_patterns = TWITTER_BEHAVIORAL_PATTERNS["bots"]
        
        # Bot farm location patterns (realistic bot origins)
        bot_locations = [
            {"country": "RU", "city": "Moscow", "timezone": "UTC+3"},
            {"country": "CN", "city": "Beijing", "timezone": "UTC+8"},
            {"country": "BD", "city": "Dhaka", "timezone": "UTC+6"},
            {"country": "PK", "city": "Karachi", "timezone": "UTC+5"},
            {"country": "NG", "city": "Lagos", "timezone": "UTC+1"},
            {"country": "ID", "city": "Jakarta", "timezone": "UTC+7"}
        ]
        
        location = random.choice(bot_locations)
        
        bot = {
            "bot_id": f"twitter_bot_{bot_type}_{uuid.uuid4().hex[:8]}",
            "username": f"@{random.choice(['real', 'user', 'person', 'human'])}{i}_{random.randint(1000,9999)}",
            "display_name": f"{random.choice(['John', 'Jane', 'Alex', 'Sam'])} {random.choice(['Smith', 'Johnson', 'Brown'])}",
            "user_type": "bot",
            "bot_type": bot_type,
            "bot_description": bot_config["description"],
            "follower_count": random.randint(10, 10000),
            "following_count": random.randint(500, 5000),
            "tweet_count": random.randint(100, 50000),
            "account_age_days": random.randint(1, 365),
            "verified": False,
            "location": location,
            "behavior_config": bot_config["behavior"],
            "detection_signatures": bot_config["detection_signatures"],
            
            # Payment business targeting
            "target_business_types": random.sample([
                "e_commerce", "subscription_services", "gaming_monetization", "financial_services"
            ], random.randint(1, 3)),
            "target_keywords": random.sample([
                "sale", "discount", "deal", "free", "premium", "buy", "order", "shop", "invest", "trade"
            ], random.randint(3, 6)),
            "engagement_strategy": random.choice([
                "amplify_promotional_content", "fake_social_proof", "manipulate_trends", "generate_fake_reviews"
            ]),
            
            # Operation parameters
            "daily_action_quota": random.randint(50, 1000),
            "operation_hours": random.choice([
                list(range(24)),  # 24/7 operation
                [9, 10, 11, 12, 13, 14, 15, 16, 17],  # Business hours
                [18, 19, 20, 21, 22, 23]  # Evening peak
            ]),
            "coordination_group": f"farm_{hashlib.md5(str(i % 5).encode()).hexdigest()[:6]}",
            
            # Network and behavioral profiles
            "network_profile": network_profile,
            "behavioral_patterns": {
                "tweet_frequency_daily": random.uniform(*behavioral_patterns["tweet_frequency_daily"]),
                "scroll_speed": random.uniform(*behavioral_patterns["scroll_speed_tweets_per_minute"]),
                "engagement_delay": random.uniform(*behavioral_patterns["engagement_delay_seconds"]),
                "reading_time": random.uniform(*behavioral_patterns["reading_time_per_tweet"]),
                "automated_responses": True,
                "consistent_timing": True
            },
            
            # Economic impact
            "operation_costs": {
                "cost_per_action": random.uniform(0.001, 0.01),
                "monthly_operation_cost": random.uniform(50, 500),
                "proxy_costs": random.uniform(10, 100) if network_profile["proxy_detected"] else 0
            },
            "revenue_impact": {
                "conversion_pollution": random.uniform(0.001, 0.01),
                "trust_degradation": random.uniform(0.05, 0.2),
                "platform_value_erosion": random.uniform(0.01, 0.05)
            }
        }
        bots.append(bot)
    
    return bots

# Calculate payment business impact
def calculate_payment_business_impact(engagement_event, user_profile, tweet_data):
    """Calculate the economic impact on payment businesses from social media engagement."""
    
    if user_profile["user_type"] == "real":
        # Real user impact on payment businesses
        base_conversion_prob = tweet_data.get("conversion_potential", 0.02)
        
        # Adjust for user demographics and behavior
        age_multiplier = {
            "13-17": 0.8,  # Lower purchasing power
            "18-24": 1.2,  # High engagement, impulse buying
            "25-34": 1.5,  # Peak purchasing power
            "35-44": 1.3,  # Stable income
            "45+": 0.9     # More conservative spending
        }.get(user_profile.get("age_group", "25-34"), 1.0)
        
        final_conversion_prob = base_conversion_prob * age_multiplier
        
        if random.random() < final_conversion_prob:
            # Conversion occurred
            business_type = tweet_data.get("business_type", "e_commerce")
            business_config = PAYMENT_BUSINESS_PATTERNS["in_app_purchase_drivers"][business_type]
            
            transaction_value = random.uniform(
                business_config["average_transaction_value"]["min"],
                business_config["average_transaction_value"]["max"]
            )
            
            commission_rate = 0.05  # 5% average commission
            platform_fee = transaction_value * 0.03  # 3% platform fee
            
            return {
                "conversion_occurred": True,
                "transaction_value_usd": transaction_value,
                "business_revenue": transaction_value * (1 - commission_rate),
                "platform_revenue": platform_fee,
                "influencer_commission": transaction_value * commission_rate,
                "payment_processor_fee": transaction_value * 0.029,  # Stripe average
                "net_economic_value": transaction_value - platform_fee,
                "attribution_confidence": random.uniform(0.7, 0.95),
                "customer_lifetime_value": transaction_value * random.uniform(3, 8),
                "repeat_purchase_probability": random.uniform(0.3, 0.7)
            }
        else:
            # No conversion but potential value
            return {
                "conversion_occurred": False,
                "engagement_value": random.uniform(0.01, 0.05),
                "brand_awareness_impact": random.uniform(0.001, 0.01),
                "future_conversion_probability": random.uniform(0.05, 0.2),
                "social_proof_value": random.uniform(0.005, 0.02)
            }
    
    else:  # bot
        # Bot impact (mostly negative)
        return {
            "conversion_occurred": False,
            "fake_engagement_cost": random.uniform(0.01, 0.05),
            "trust_erosion_impact": random.uniform(0.1, 0.5),
            "algorithm_manipulation_damage": random.uniform(0.05, 0.2),
            "advertiser_fraud_loss": random.uniform(0.02, 0.1),
            "platform_reputation_damage": random.uniform(0.01, 0.05),
            "detection_and_cleanup_cost": random.uniform(0.005, 0.02)
        }

# Enhanced Twitter/X simulation with payment business focus
def run_twitter_simulation():
    print("Starting Enhanced Twitter/X Bot Simulation with Payment Business Analysis...")
    
    # Generate data
    influencers = generate_twitter_influencers()
    tweets = generate_twitter_content(influencers)
    real_users = generate_twitter_users()
    bots = generate_twitter_bots()
    
    engagement_log = []
    payment_business_events = []
    detection_events = []
    
    print(f"Generated {len(influencers)} influencers, {len(tweets)} tweets, {len(real_users)} real users, {len(bots)} bots")
    
    for step in range(SIMULATION_STEPS):
        current_time = datetime.now() + timedelta(minutes=step * 15)  # 15-minute intervals
        hour = current_time.hour
        
        # Real user behavior
        for user in real_users:
            if random.random() < 0.4:  # 40% chance of activity per step
                target_tweets = random.sample(tweets, min(3, len(tweets)))
                
                for tweet in target_tweets:
                    # Interest-based engagement probability
                    engagement_prob = 0.1
                    if any(interest in tweet["content"].lower() for interest in user["interests"]):
                        engagement_prob = 0.3
                    
                    if random.random() < engagement_prob:
                        action = random.choices(
                            ["like", "retweet", "reply", "quote_tweet", "bookmark"],
                            weights=[0.4, 0.2, 0.15, 0.1, 0.15]
                        )[0]
                        
                        # Calculate payment business impact
                        business_impact = calculate_payment_business_impact(
                            {"action": action}, user, tweet
                        )
                        
                        engagement_event = {
                            "timestamp": current_time.isoformat(),
                            "step": step,
                            "user": user["user_id"],
                            "user_type": "real",
                            "action": action,
                            "tweet_id": tweet["tweet_id"],
                            "influencer": tweet["influencer"],
                            "business_type": tweet["business_type"],
                            "user_age_group": user["age_group"],
                            "user_location": user["location"],
                            "device_type": user["device_info"]["primary_device"],
                            
                            # Network data
                            "connection_type": user["network_profile"]["connection_type"],
                            "latency_ms": user["network_profile"]["latency_ms"],
                            "device_access": user["network_profile"]["device_access"],
                            
                            # Behavioral data
                            "engagement_delay_seconds": user["behavioral_patterns"]["engagement_delay"],
                            "reading_time_seconds": user["behavioral_patterns"]["reading_time"],
                            "organic_engagement": True,
                            
                            # Payment business impact
                            "business_impact": business_impact,
                            "monetization_potential": tweet.get("monetization_intent", False),
                            "cta_interaction": tweet.get("cta_present", False) and action in ["like", "retweet"],
                            
                            # Detection scores
                            "authenticity_score": random.uniform(0.8, 1.0),
                            "bot_probability": random.uniform(0.01, 0.05)
                        }
                        
                        engagement_log.append(engagement_event)
                        
                        # Track payment business events
                        if business_impact.get("conversion_occurred"):
                            payment_business_events.append({
                                "timestamp": current_time.isoformat(),
                                "event_type": "conversion",
                                "user_id": user["user_id"],
                                "tweet_id": tweet["tweet_id"],
                                "business_type": tweet["business_type"],
                                "transaction_value": business_impact["transaction_value_usd"],
                                "attribution_source": "twitter_engagement",
                                "conversion_path": [action],
                                "customer_segment": user["age_group"]
                            })
                        
                        # Update tweet metrics
                        if action == "like":
                            tweet["like_count"] += 1
                        elif action == "retweet":
                            tweet["retweet_count"] += 1
                        elif action == "reply":
                            tweet["reply_count"] += 1
                        elif action == "quote_tweet":
                            tweet["quote_tweet_count"] += 1
                        elif action == "bookmark":
                            tweet["bookmark_count"] += 1
        
        # Bot behavior with payment business targeting
        for bot in bots:
            if hour in bot["operation_hours"] and random.random() < 0.7:
                # Target tweets based on business interests
                target_tweets = [t for t in tweets 
                               if t["business_type"] in bot["target_business_types"]
                               or any(keyword in t["content"].lower() for keyword in bot["target_keywords"])]
                
                if not target_tweets:
                    target_tweets = random.sample(tweets, min(2, len(tweets)))
                
                for tweet in random.sample(target_tweets, min(2, len(target_tweets))):
                    bot_config = bot["behavior_config"]
                    
                    # Determine bot action based on type
                    action_probs = {
                        "like": bot_config["like_rate"],
                        "retweet": bot_config["retweet_rate"],
                        "reply": bot_config["reply_rate"],
                        "quote_tweet": bot_config["quote_tweet_rate"]
                    }
                    
                    for action, prob in action_probs.items():
                        if random.random() < prob:
                            # Calculate detection risk
                            detection_risk = random.uniform(0.3, 0.9) if bot["bot_type"] != "sophisticated_ai_bot" else random.uniform(0.1, 0.4)
                            
                            # Calculate negative business impact
                            business_impact = calculate_payment_business_impact(
                                {"action": action}, bot, tweet
                            )
                            
                            engagement_event = {
                                "timestamp": current_time.isoformat(),
                                "step": step,
                                "user": bot["bot_id"],
                                "user_type": "bot",
                                "bot_type": bot["bot_type"],
                                "action": action,
                                "tweet_id": tweet["tweet_id"],
                                "influencer": tweet["influencer"],
                                "business_type": tweet["business_type"],
                                "bot_location": bot["location"]["country"],
                                "coordination_group": bot["coordination_group"],
                                
                                # Network data
                                "connection_type": bot["network_profile"]["connection_type"],
                                "proxy_detected": bot["network_profile"]["proxy_detected"],
                                "automation_client": bot["network_profile"]["automation_client"],
                                
                                # Behavioral data
                                "engagement_delay_seconds": bot["behavioral_patterns"]["engagement_delay"],
                                "automated_response": True,
                                "consistent_timing": bot["behavioral_patterns"]["consistent_timing"],
                                
                                # Detection data
                                "detection_risk_score": detection_risk,
                                "detection_signatures": list(bot["detection_signatures"].keys()),
                                "target_keywords_matched": [kw for kw in bot["target_keywords"] if kw in tweet["content"].lower()],
                                
                                # Economic impact
                                "business_impact": business_impact,
                                "operation_cost": bot["operation_costs"]["cost_per_action"],
                                "revenue_pollution": True,
                                
                                # Bot metrics
                                "authenticity_score": random.uniform(0.1, 0.4),
                                "bot_probability": random.uniform(0.6, 0.95)
                            }
                            
                            engagement_log.append(engagement_event)
                            
                            # Generate detection events for high-risk bots
                            if detection_risk > 0.7:
                                detection_events.append({
                                    "timestamp": current_time.isoformat(),
                                    "detection_type": "bot_behavior_analysis",
                                    "bot_id": bot["bot_id"],
                                    "tweet_id": tweet["tweet_id"],
                                    "risk_score": detection_risk,
                                    "detection_method": random.choice([
                                        "timing_analysis", "behavioral_clustering", 
                                        "network_analysis", "content_analysis"
                                    ]),
                                    "confidence": random.uniform(0.7, 0.95),
                                    "recommended_action": "suspend" if detection_risk > 0.85 else "flag_for_review"
                                })
                            
                            # Update tweet metrics (bot inflation)
                            if action == "like":
                                tweet["like_count"] += 1
                            elif action == "retweet":
                                tweet["retweet_count"] += 1
                            elif action == "reply":
                                tweet["reply_count"] += 1
                            elif action == "quote_tweet":
                                tweet["quote_tweet_count"] += 1
    
    return {
        "influencers": influencers,
        "tweets": tweets,
        "real_users": real_users,
        "bots": bots,
        "engagement_log": engagement_log,
        "payment_business_events": payment_business_events,
        "detection_events": detection_events
    }

# Run simulation and generate comprehensive analysis
if __name__ == "__main__":
    print("=== Enhanced Twitter/X Bot Simulation with Payment Business Analysis ===")
    
    simulation_data = run_twitter_simulation()
    
    # Calculate comprehensive metrics
    total_engagements = len(simulation_data["engagement_log"])
    real_user_engagements = len([e for e in simulation_data["engagement_log"] if e["user_type"] == "real"])
    bot_engagements = len([e for e in simulation_data["engagement_log"] if e["user_type"] == "bot"])
    
    # Payment business analysis
    total_conversions = len([e for e in simulation_data["payment_business_events"] if e["event_type"] == "conversion"])
    total_conversion_value = sum([e["transaction_value"] for e in simulation_data["payment_business_events"]])
    
    # Bot impact analysis
    bot_inflation_rate = bot_engagements / total_engagements if total_engagements > 0 else 0
    high_risk_detections = len([e for e in simulation_data["detection_events"] if e["risk_score"] > 0.8])
    
    # Economic impact
    real_user_business_value = sum([
        e.get("business_impact", {}).get("net_economic_value", 0) 
        for e in simulation_data["engagement_log"] 
        if e["user_type"] == "real" and e.get("business_impact", {}).get("conversion_occurred", False)
    ])
    
    bot_damage_cost = sum([
        e.get("business_impact", {}).get("trust_erosion_impact", 0) +
        e.get("business_impact", {}).get("detection_and_cleanup_cost", 0)
        for e in simulation_data["engagement_log"] 
        if e["user_type"] == "bot"
    ])
    
    # Compile comprehensive dataset
    comprehensive_data = {
        "metadata": {
            "simulation_type": "twitter_x_payment_business_analysis",
            "timestamp": datetime.now().isoformat(),
            "features": [
                "payment_business_integration",
                "social_commerce_analysis", 
                "bot_detection_systems",
                "economic_impact_modeling",
                "conversion_tracking",
                "influencer_monetization_analysis"
            ],
            "parameters": simulation_data
        },
        "simulation_results": simulation_data,
        "analytics": {
            "engagement_metrics": {
                "total_engagements": total_engagements,
                "real_user_engagements": real_user_engagements,
                "bot_engagements": bot_engagements,
                "bot_inflation_rate": bot_inflation_rate
            },
            "payment_business_metrics": {
                "total_conversions": total_conversions,
                "total_conversion_value_usd": total_conversion_value,
                "average_transaction_value": total_conversion_value / total_conversions if total_conversions > 0 else 0,
                "real_user_business_value": real_user_business_value,
                "bot_damage_cost": bot_damage_cost,
                "net_business_impact": real_user_business_value - bot_damage_cost
            },
            "detection_metrics": {
                "total_detection_events": len(simulation_data["detection_events"]),
                "high_risk_detections": high_risk_detections,
                "detection_accuracy": random.uniform(0.75, 0.90),
                "false_positive_rate": random.uniform(0.02, 0.08)
            },
            "business_type_analysis": {
                business_type: {
                    "influencer_count": len([i for i in simulation_data["influencers"] if i["business_type"] == business_type]),
                    "tweet_count": len([t for t in simulation_data["tweets"] if t["business_type"] == business_type]),
                    "engagement_count": len([e for e in simulation_data["engagement_log"] if e.get("business_type") == business_type]),
                    "conversion_count": len([e for e in simulation_data["payment_business_events"] if e.get("business_type") == business_type])
                }
                for business_type in ["e_commerce", "subscription_services", "gaming_monetization", "financial_services"]
            }
        },
        "payment_business_patterns": PAYMENT_BUSINESS_PATTERNS,
        "bot_type_analysis": {
            bot_type: len([b for b in simulation_data["bots"] if b["bot_type"] == bot_type])
            for bot_type in TWITTER_BOT_TYPES.keys()
        }
    }
    
    # Save data
    import os
    os.makedirs("../data", exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"../data/twitter_x_payment_business_simulation_{timestamp}.json"
    
    with open(output_filename, 'w') as f:
        json.dump(comprehensive_data, f, indent=2, default=str)
    
    print(f"\n=== Simulation Results ===")
    print(f"Total Engagements: {total_engagements}")
    print(f"Real User Engagements: {real_user_engagements}")
    print(f"Bot Engagements: {bot_engagements}")
    print(f"Bot Inflation Rate: {bot_inflation_rate:.2%}")
    print(f"Total Conversions: {total_conversions}")
    print(f"Total Conversion Value: ${total_conversion_value:.2f}")
    print(f"Real User Business Value: ${real_user_business_value:.2f}")
    print(f"Bot Damage Cost: ${bot_damage_cost:.2f}")
    print(f"Net Business Impact: ${real_user_business_value - bot_damage_cost:.2f}")
    print(f"High-Risk Bot Detections: {high_risk_detections}")
    print(f"\nData saved to: {output_filename}")
    
    # Scale parameters example
    print(f"\n=== Scaling Example ===")
    scale_parameters(scale_factor=5)
