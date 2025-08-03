import random
import json
import time
import numpy as np
from datetime import datetime, timedelta
import uuid
import hashlib

def scale_parameters(scale_factor=1):
    """Scale simulation parameters for large-scale view generation."""
    global NUM_CREATORS, NUM_REAL_USERS, NUM_BOTS, NUM_CONTENT, SIMULATION_STEPS
    NUM_CREATORS = int(NUM_CREATORS * scale_factor)
    NUM_REAL_USERS = int(NUM_REAL_USERS * scale_factor)
    NUM_BOTS = int(NUM_BOTS * scale_factor)
    NUM_CONTENT = int(NUM_CONTENT * scale_factor)
    SIMULATION_STEPS = int(SIMULATION_STEPS * scale_factor)
    print(f"Parameters scaled by factor {scale_factor}:")
    print(f"NUM_CREATORS: {NUM_CREATORS}")
    print(f"NUM_REAL_USERS: {NUM_REAL_USERS}")
    print(f"NUM_BOTS: {NUM_BOTS}")
    print(f"NUM_CONTENT: {NUM_CONTENT}")
    print(f"SIMULATION_STEPS: {SIMULATION_STEPS}")

# Simulation parameters
NUM_CREATORS = 5
NUM_REAL_USERS = 100
NUM_BOTS = 20
NUM_CONTENT = 10
SIMULATION_STEPS = 50

# Enhanced real-time parameters for network forensics
NETWORK_PATTERNS = {
    "real_users": {
        "connection_types": [
            {"type": "fiber", "speed_mbps": (100, 1000), "latency_ms": (5, 15), "weight": 0.3},
            {"type": "cable", "speed_mbps": (25, 300), "latency_ms": (10, 30), "weight": 0.4},
            {"type": "mobile_5g", "speed_mbps": (50, 500), "latency_ms": (15, 40), "weight": 0.2},
            {"type": "mobile_4g", "speed_mbps": (5, 50), "latency_ms": (30, 80), "weight": 0.1}
        ],
        "isp_providers": ["Comcast", "Verizon", "AT&T", "Charter", "Spectrum", "Local ISP"]
    },
    "bots": {
        "connection_types": [
            {"type": "datacenter", "speed_mbps": (100, 1000), "latency_ms": (1, 5), "weight": 0.6},
            {"type": "residential_proxy", "speed_mbps": (20, 100), "latency_ms": (15, 50), "weight": 0.3},
            {"type": "mobile_proxy", "speed_mbps": (10, 50), "latency_ms": (50, 150), "weight": 0.1}
        ],
        "suspicious_indicators": ["identical_connection_speed", "consistent_low_latency", "simultaneous_connections"]
    }
}

# Temporal behavior patterns for realistic activity
TEMPORAL_PATTERNS = {
    "hourly_activity": {
        0: 0.1, 1: 0.05, 2: 0.03, 3: 0.02, 4: 0.02, 5: 0.03,
        6: 0.1, 7: 0.2, 8: 0.3, 9: 0.4, 10: 0.5, 11: 0.6,
        12: 0.7, 13: 0.6, 14: 0.5, 15: 0.6, 16: 0.7, 17: 0.8,
        18: 0.9, 19: 1.0, 20: 0.9, 21: 0.8, 22: 0.6, 23: 0.3
    },
    "bot_patterns": {
        "24x7_activity": 0.95,  # Consistent activity
        "coordinated_burst": 0.8,  # Synchronized spikes
        "no_human_sleep": True
    }
}

# Behavioral micro-patterns for human vs bot detection
BEHAVIORAL_PATTERNS = {
    "real_users": {
        "pause_frequency": (0.1, 0.4),  # Pauses per video
        "seek_behavior": (0.05, 0.2),   # Scrubbing frequency
        "volume_adjustments": (0.02, 0.1),
        "click_hesitation_ms": (200, 2000),
        "mouse_movement_natural": True,
        "quality_changes": (0, 2)  # Video quality adjustments
    },
    "bots": {
        "pause_frequency": (0, 0.02),  # Almost no pauses
        "seek_behavior": (0, 0.01),    # Linear playback
        "volume_adjustments": (0, 0),  # No volume changes
        "click_hesitation_ms": (50, 100),  # Robotic timing
        "mouse_movement_linear": True,
        "perfect_center_clicks": True
    }
}

# Enhanced detection system parameters
DETECTION_SYSTEM = {
    "accuracy_rates": {
        "view_farm_detection": 0.85,
        "engagement_pod_detection": 0.75,
        "subscriber_farm_detection": 0.90,
        "sophisticated_bot_detection": 0.45
    },
    "risk_thresholds": {
        "low_risk": 0.3,
        "medium_risk": 0.6,
        "high_risk": 0.8
    },
    "detection_features": [
        "network_pattern_analysis",
        "behavioral_clustering",
        "temporal_anomaly_detection",
        "device_fingerprint_analysis"
    ]
}

# Real bot data patterns based on research
BOT_TYPES = {
    "view_farm": {
        "description": "Basic view farming bots",
        "behavior": {
            "watch_time_range": (10, 45),  # seconds
            "engagement_rate": 0.02,  # Very low engagement
            "comment_rate": 0.01,
            "like_rate": 0.05,
            "subscriber_rate": 0.001,
            "typical_comments": [
                "First!", "Nice video!", "Good work!", "Amazing!", "Thanks for sharing",
                "Great content", "Love this", "Awesome video", "Perfect", "Nice one"
            ]
        },
        "detection_signatures": {
            "rapid_successive_views": True,
            "low_session_duration": True,
            "generic_comments": True,
            "unusual_geographic_patterns": True
        }
    },
    "engagement_pod": {
        "description": "Coordinated engagement manipulation",
        "behavior": {
            "watch_time_range": (60, 300),  # Longer watch times
            "engagement_rate": 0.8,  # Very high engagement
            "comment_rate": 0.6,
            "like_rate": 0.9,
            "subscriber_rate": 0.1,
            "typical_comments": [
                "This deserves more views!", "Underrated channel!", "Why doesn't this have more likes?",
                "Algorithm needs to push this!", "Quality content right here", "This should be trending",
                "More people need to see this", "Incredible work as always", "Keep up the great content",
                "Your best video yet!"
            ]
        },
        "detection_signatures": {
            "coordinated_timing": True,
            "similar_comment_patterns": True,
            "high_engagement_correlation": True,
            "account_age_patterns": True
        }
    },
    "subscriber_farm": {
        "description": "Fake subscriber generation",
        "behavior": {
            "watch_time_range": (5, 30),  # Very short watch times
            "engagement_rate": 0.01,  # Almost no engagement
            "comment_rate": 0.005,
            "like_rate": 0.02,
            "subscriber_rate": 0.95,  # Primary purpose
            "typical_comments": [
                "Subbed!", "New subscriber here", "Great channel", "Subscribed", "Supporting you"
            ]
        },
        "detection_signatures": {
            "subscription_without_engagement": True,
            "minimal_watch_time": True,
            "account_creation_bursts": True,
            "inactive_after_subscription": True
        }
    },
    "sophisticated_bot": {
        "description": "Advanced AI-powered bots with human-like behavior",
        "behavior": {
            "watch_time_range": (120, 600),  # Human-like watch times
            "engagement_rate": 0.15,  # Moderate engagement
            "comment_rate": 0.08,
            "like_rate": 0.25,
            "subscriber_rate": 0.03,
            "typical_comments": [
                "Really enjoyed the part about {topic}", "Your explanation of {concept} was clear",
                "Have you considered {suggestion}?", "This reminds me of {reference}",
                "Looking forward to the next video on this topic", "Great editing on this one",
                "The background music choice was perfect", "Your presentation style keeps improving"
            ]
        },
        "detection_signatures": {
            "ai_generated_text_patterns": True,
            "consistent_behavioral_metrics": True,
            "limited_cross_platform_activity": True,
            "scheduled_activity_patterns": True
        }
    }
}

# Real device fingerprints from bot research
REAL_BOT_DEVICES = [
    # Android bot farms
    {
        "device": "Android Bot Farm",
        "user_agent": "Mozilla/5.0 (Linux; Android 7.0; SM-G930F) AppleWebKit/537.36 YouTube/16.20.35",
        "screen_resolution": "1080x1920",
        "timezone": "UTC+8",
        "language": "en-US",
        "fingerprint_anomalies": ["consistent_battery_level", "identical_device_specs", "synchronized_activity"]
    },
    {
        "device": "Emulated Android",
        "user_agent": "Mozilla/5.0 (Linux; Android 9; AOSP on IA Emulator) AppleWebKit/537.36 YouTube/16.20.35",
        "screen_resolution": "720x1280",
        "timezone": "UTC+0",
        "language": "en-US",
        "fingerprint_anomalies": ["emulator_signatures", "missing_sensors", "virtual_device_patterns"]
    },
    # Headless Chrome farms
    {
        "device": "Headless Chrome Farm",
        "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 HeadlessChrome/91.0.4472.124",
        "screen_resolution": "1366x768",
        "timezone": "UTC+5:30",
        "language": "en-US",
        "fingerprint_anomalies": ["headless_indicators", "missing_plugins", "automation_markers"]
    },
    # Residential proxy bots
    {
        "device": "Residential Proxy Bot",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 YouTube/16.20.35",
        "screen_resolution": "1920x1080",
        "timezone": "UTC-5",
        "language": "en-US",
        "fingerprint_anomalies": ["proxy_leak_indicators", "ip_geolocation_mismatch", "unusual_connection_patterns"]
    }
]

# Enhanced network profile generation
def generate_network_profile(user_type="real"):
    """Generate realistic network profile with forensic capabilities."""
    if user_type == "real":
        connection = random.choices(
            NETWORK_PATTERNS["real_users"]["connection_types"],
            weights=[c["weight"] for c in NETWORK_PATTERNS["real_users"]["connection_types"]]
        )[0]
        
        return {
            "connection_type": connection["type"],
            "speed_mbps": random.uniform(*connection["speed_mbps"]),
            "latency_ms": random.uniform(*connection["latency_ms"]),
            "isp_provider": random.choice(NETWORK_PATTERNS["real_users"]["isp_providers"]),
            "ip_address": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "dns_servers": ["8.8.8.8", "1.1.1.1", "isp_default"],
            "network_stability": random.uniform(0.8, 1.0),
            "bandwidth_variation": random.uniform(0.1, 0.3)
        }
    else:  # bot
        connection = random.choices(
            NETWORK_PATTERNS["bots"]["connection_types"],
            weights=[c["weight"] for c in NETWORK_PATTERNS["bots"]["connection_types"]]
        )[0]
        
        return {
            "connection_type": connection["type"],
            "speed_mbps": random.uniform(*connection["speed_mbps"]),
            "latency_ms": random.uniform(*connection["latency_ms"]),
            "isp_provider": "Datacenter" if connection["type"] == "datacenter" else "Proxy Service",
            "ip_address": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "suspicious_indicators": NETWORK_PATTERNS["bots"]["suspicious_indicators"],
            "proxy_detected": connection["type"] in ["residential_proxy", "mobile_proxy"],
            "datacenter_ip": connection["type"] == "datacenter",
            "network_stability": random.uniform(0.95, 1.0),  # Too stable
            "bandwidth_variation": random.uniform(0.01, 0.05)  # Too consistent
        }

# Enhanced behavioral pattern generation
def generate_behavioral_profile(user_type="real"):
    """Generate realistic behavioral patterns for detection."""
    if user_type == "real":
        patterns = BEHAVIORAL_PATTERNS["real_users"]
        return {
            "pause_frequency": random.uniform(*patterns["pause_frequency"]),
            "seek_behavior": random.uniform(*patterns["seek_behavior"]),
            "volume_adjustments": random.uniform(*patterns["volume_adjustments"]),
            "click_hesitation_ms": random.uniform(*patterns["click_hesitation_ms"]),
            "quality_changes": random.randint(*patterns["quality_changes"]),
            "interaction_naturalness": random.uniform(0.7, 1.0),
            "attention_span_minutes": random.uniform(5, 45),
            "multitasking_probability": random.uniform(0.2, 0.8),
            "return_probability": random.uniform(0.4, 0.8)
        }
    else:  # bot
        patterns = BEHAVIORAL_PATTERNS["bots"]
        return {
            "pause_frequency": random.uniform(*patterns["pause_frequency"]),
            "seek_behavior": random.uniform(*patterns["seek_behavior"]),
            "volume_adjustments": random.uniform(*patterns["volume_adjustments"]),
            "click_hesitation_ms": random.uniform(*patterns["click_hesitation_ms"]),
            "quality_changes": 0,  # No quality adjustments
            "interaction_naturalness": random.uniform(0.1, 0.4),
            "robotic_timing": True,
            "perfect_playback": True,
            "no_human_errors": True,
            "consistent_patterns": True
        }

# Enhanced detection risk calculation
def calculate_detection_risk(user_profile, behavior_data, network_data):
    """Calculate comprehensive detection risk score."""
    if user_profile.get("user_type") == "real":
        return random.uniform(0.01, 0.05)  # Low false positive rate
    
    # Bot detection scoring
    risk_score = 0.0
    
    # Network-based risk factors
    if network_data.get("datacenter_ip"):
        risk_score += 0.3
    if network_data.get("proxy_detected"):
        risk_score += 0.2
    if network_data.get("bandwidth_variation", 1.0) < 0.1:
        risk_score += 0.2  # Too consistent bandwidth
    
    # Behavioral risk factors
    if behavior_data.get("pause_frequency", 1.0) < 0.05:
        risk_score += 0.2  # No pauses
    if behavior_data.get("click_hesitation_ms", 1000) < 150:
        risk_score += 0.2  # Too fast clicks
    if behavior_data.get("robotic_timing"):
        risk_score += 0.3
    
    # Bot type specific adjustments
    bot_type = user_profile.get("bot_type", "")
    base_detection_rate = DETECTION_SYSTEM["accuracy_rates"].get(f"{bot_type}_detection", 0.5)
    
    final_score = min(1.0, risk_score * base_detection_rate + random.uniform(-0.1, 0.1))
    return max(0.0, final_score)

# Economic impact calculation with enhanced parameters
def calculate_economic_impact(event_data, user_profile):
    """Calculate detailed economic impact per event."""
    if user_profile.get("user_type") == "real":
        # Real user economic value
        base_value = random.uniform(0.001, 0.008)  # Base CPM value
        watch_percentage = 0.5  # Default value
        
        # Adjust for engagement quality
        if event_data.get("action") == "view":
            watch_percentage = event_data.get("watch_percentage", random.uniform(0.1, 1.0))
            if watch_percentage > 0.7:
                base_value *= 1.5  # High engagement premium
            elif watch_percentage < 0.3:
                base_value *= 0.5  # Low engagement penalty
        
        # Premium subscriber bonus
        if user_profile.get("subscription_status") == "premium":
            base_value *= 1.3
        
        return {
            "economic_value_usd": base_value,
            "ad_revenue_potential": True,
            "engagement_quality": "high" if watch_percentage > 0.5 else "medium",
            "subscriber_value": random.uniform(5.0, 50.0) if event_data.get("action") == "subscribe" else 0
        }
    else:  # bot
        # Bot economic impact (mostly negative)
        bot_type = user_profile.get("bot_type", "")
        operation_costs = {
            "view_farm": 0.0005,
            "engagement_pod": 0.002,
            "subscriber_farm": 0.0015,
            "sophisticated_bot": 0.005
        }
        
        return {
            "operation_cost_usd": operation_costs.get(bot_type, 0.001),
            "revenue_pollution": True,
            "ad_fraud_impact": random.uniform(0.0001, 0.0005),
            "detection_cost": 0.0001,  # Cost to detect and remove
            "platform_reputation_damage": random.uniform(0.001, 0.01)
        }

# Enhanced content interaction scoring
def analyze_content_interaction(comment_text, user_profile, video_content):
    """Analyze content interaction sophistication."""
    if user_profile.get("user_type") == "real":
        # Real user content analysis
        relevance_indicators = [
            video_content.get("category", "").lower() in comment_text.lower(),
            len(comment_text.split()) > 3,  # Not too short
            "!" not in comment_text or comment_text.count("!") < 3,  # Not too excited
            any(word in comment_text.lower() for word in ["thanks", "helpful", "learned", "great"])
        ]
        
        return {
            "content_relevance_score": sum(relevance_indicators) / len(relevance_indicators),
            "sentiment_authenticity": random.uniform(0.7, 1.0),
            "context_awareness": True,
            "personal_touch": random.random() < 0.6,
            "language_complexity": random.uniform(0.6, 1.0)
        }
    else:  # bot
        # Bot content analysis
        generic_patterns = ["first!", "nice", "great", "amazing", "perfect"]
        is_generic = any(pattern in comment_text.lower() for pattern in generic_patterns)
        
        return {
            "content_relevance_score": random.uniform(0.1, 0.4),
            "sentiment_authenticity": random.uniform(0.1, 0.4),
            "template_detected": is_generic,
            "generic_response": True,
            "no_context_awareness": True,
            "language_complexity": random.uniform(0.1, 0.3)
        }

# Generate realistic creators and content
creators = []
for i in range(NUM_CREATORS):
    creator_types = ["gaming", "music", "education", "vlog", "tech", "beauty", "cooking", "comedy"]
    creator_type = random.choice(creator_types)
    
    creator = {
        "creator_id": f"creator_{i}",
        "channel_name": f"{creator_type.title()}Master{i}",
        "subscriber_count": random.randint(1000, 1000000),
        "total_views": random.randint(10000, 50000000),
        "channel_age_days": random.randint(30, 2000),
        "content_type": creator_type,
        "upload_frequency": random.choice(["daily", "weekly", "bi-weekly", "monthly"]),
        "monetized": random.choice([True, False]),
        "verification_status": "verified" if random.random() > 0.7 else "unverified"
    }
    creators.append(creator)

# Generate realistic YouTube content
mockup_videos = []
for i in range(NUM_CONTENT):
    creator = creators[i % NUM_CREATORS]
    content_type = creator["content_type"]
    
    # Content-specific characteristics
    content_templates = {
        "gaming": {
            "titles": [f"EPIC {random.choice(['FORTNITE', 'MINECRAFT', 'VALORANT'])} GAMEPLAY #{i}",
                      f"NEW {random.choice(['UPDATE', 'PATCH', 'SEASON'])} REVIEW",
                      f"INSANE {random.choice(['CLUTCH', 'KILL', 'WIN'])} COMPILATION"],
            "duration_range": (300, 3600),
            "tags": ["gaming", "gameplay", "epic", "funny", "moments"]
        },
        "music": {
            "titles": [f"New Song Release - Track {i}", f"Behind the Scenes - Studio Session {i}",
                      f"Live Performance - Song {i}"],
            "duration_range": (180, 300),
            "tags": ["music", "song", "artist", "new", "release"]
        },
        "education": {
            "titles": [f"How to Master {random.choice(['Python', 'Math', 'Science'])} - Lesson {i}",
                      f"Complete Guide to {random.choice(['Programming', 'Physics', 'Chemistry'])}",
                      f"Tutorial: Advanced {random.choice(['Calculus', 'Biology', 'History'])}"],
            "duration_range": (600, 2400),
            "tags": ["education", "tutorial", "learning", "guide", "tips"]
        },
        "vlog": {
            "titles": [f"My Daily Routine - Day {i}", f"CRAZY Day in My Life - Vlog #{i}",
                      f"What I Ate Today - Food Vlog {i}"],
            "duration_range": (480, 1200),
            "tags": ["vlog", "daily", "life", "routine", "personal"]
        }
    }
    
    template = content_templates.get(content_type, content_templates["vlog"])
    
    video = {
        "video_id": f"yt_{uuid.uuid4().hex[:11]}",  # More realistic video IDs
        "creator": creator["creator_id"],
        "channel_name": creator["channel_name"],
        "title": random.choice(template["titles"]),
        "description": f"In this video, I'll show you {random.choice(['amazing', 'incredible', 'useful', 'entertaining'])} content about {content_type}. Don't forget to like and subscribe!",
        "tags": template["tags"] + [f"tag{i}", creator["channel_name"].lower()],
        "duration_sec": random.randint(*template["duration_range"]),
        "category": content_type.title(),
        "upload_date": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
        "thumbnails": {
            "default": f"https://i.ytimg.com/vi/{uuid.uuid4().hex[:11]}/default.jpg",
            "medium": f"https://i.ytimg.com/vi/{uuid.uuid4().hex[:11]}/mqdefault.jpg",
            "high": f"https://i.ytimg.com/vi/{uuid.uuid4().hex[:11]}/hqdefault.jpg"
        },
        "view_count": random.randint(100, 500000),
        "like_count": random.randint(10, 25000),
        "dislike_count": random.randint(0, 1000),
        "comment_count": random.randint(5, 5000),
        "engagement_rate": random.uniform(0.02, 0.15),
        "cpm_usd": random.uniform(0.5, 8.0),  # Cost per mille
        "rpm_usd": random.uniform(0.3, 4.0),  # Revenue per mille
        "monetization_enabled": creator["monetized"] and random.random() > 0.2
    }
    mockup_videos.append(video)

# Generate realistic real users
real_users = []
for i in range(NUM_REAL_USERS):
    user_demographics = random.choice([
        {"age_group": "13-17", "interests": ["gaming", "music", "comedy"], "watch_time_daily": random.uniform(2, 6)},
        {"age_group": "18-24", "interests": ["vlog", "music", "tech"], "watch_time_daily": random.uniform(1, 4)},
        {"age_group": "25-34", "interests": ["education", "tech", "cooking"], "watch_time_daily": random.uniform(0.5, 3)},
        {"age_group": "35-44", "interests": ["education", "cooking", "vlog"], "watch_time_daily": random.uniform(0.5, 2)},
        {"age_group": "45+", "interests": ["education", "cooking", "music"], "watch_time_daily": random.uniform(0.2, 1.5)}
    ])
    
    # Generate enhanced network and behavioral profiles
    network_profile = generate_network_profile("real")
    behavioral_profile = generate_behavioral_profile("real")
    
    user = {
        "user_id": f"user_{uuid.uuid4().hex[:8]}",
        "user_type": "real",
        "age_group": user_demographics["age_group"],
        "interests": user_demographics["interests"],
        "subscription_status": "premium" if random.random() < 0.3 else "free",
        "country": random.choice(["US", "UK", "CA", "AU", "DE", "FR", "ES", "IT", "BR", "IN", "JP", "KR"]),
        "language": random.choice(["en", "es", "pt", "de", "fr", "ja", "ko", "hi"]),
        "device_type": random.choice(["mobile", "desktop", "tablet", "tv"]),
        "watch_time_daily_hours": user_demographics["watch_time_daily"],
        "subscriber_to_channels": random.randint(5, 200),
        "account_age_days": random.randint(30, 3650),
        "activity_pattern": random.choice(["morning", "afternoon", "evening", "night", "random"]),
        
        # Enhanced parameters
        "network_profile": network_profile,
        "behavioral_profile": behavioral_profile,
        "device_fingerprint": {
            "screen_resolution": random.choice(["1920x1080", "1366x768", "375x812", "414x896"]),
            "user_agent": f"Mozilla/5.0 ({random.choice(['Windows NT 10.0', 'Macintosh', 'iPhone', 'Android'])}) AppleWebKit/537.36",
            "timezone": random.choice(["UTC-8", "UTC-5", "UTC+0", "UTC+1", "UTC+8"]),
            "hardware_acceleration": True,
            "cookies_enabled": True,
            "javascript_enabled": True
        },
        "session_patterns": {
            "average_session_duration": random.uniform(15, 180),  # minutes
            "videos_per_session": random.randint(1, 8),
            "return_probability": random.uniform(0.4, 0.8),
            "cross_video_correlation": True
        }
    }
    real_users.append(user)

# Generate sophisticated bots with realistic patterns
bots = []
for i in range(NUM_BOTS):
    bot_type = random.choice(list(BOT_TYPES.keys()))
    bot_config = BOT_TYPES[bot_type]
    device_profile = random.choice(REAL_BOT_DEVICES)
    
    # Generate enhanced network and behavioral profiles for bots
    network_profile = generate_network_profile("bot")
    behavioral_profile = generate_behavioral_profile("bot")
    
    # Bot farm location patterns (real bot farm locations)
    bot_farm_locations = [
        {"country": "BD", "city": "Dhaka", "timezone": "UTC+6"},  # Bangladesh
        {"country": "PK", "city": "Karachi", "timezone": "UTC+5"},  # Pakistan
        {"country": "ID", "city": "Jakarta", "timezone": "UTC+7"},  # Indonesia
        {"country": "PH", "city": "Manila", "timezone": "UTC+8"},  # Philippines
        {"country": "NG", "city": "Lagos", "timezone": "UTC+1"},  # Nigeria
        {"country": "VN", "city": "Ho Chi Minh City", "timezone": "UTC+7"},  # Vietnam
        {"country": "RU", "city": "Moscow", "timezone": "UTC+3"},  # Russia (proxy)
        {"country": "CN", "city": "Shenzhen", "timezone": "UTC+8"}  # China (VPN)
    ]
    
    location = random.choice(bot_farm_locations)
    
    bot = {
        "bot_id": f"bot_{bot_type}_{uuid.uuid4().hex[:8]}",
        "user_type": "bot",
        "bot_type": bot_type,
        "bot_description": bot_config["description"],
        "creation_date": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
        "location": location,
        "device_profile": device_profile,
        "behavior_config": bot_config["behavior"],
        "detection_signatures": bot_config["detection_signatures"],
        "target_creators": random.sample([c["creator_id"] for c in creators], random.randint(1, 3)),
        "daily_quota": random.randint(50, 500),  # Actions per day
        "activity_hours": random.choice([
            [0, 1, 2, 3, 4, 5],  # Night shift bots
            [9, 10, 11, 12, 13, 14],  # Day shift bots
            list(range(24))  # 24/7 bots
        ]),
        "proxy_rotation": random.choice([True, False]),
        "account_warming": random.choice([True, False]),  # Gradual activity increase
        "evasion_techniques": random.sample([
            "random_delays", "human_like_mouse_movement", "realistic_scroll_patterns",
            "browser_fingerprint_spoofing", "residential_proxies", "user_agent_rotation"
        ], random.randint(2, 4)),
        
        # Enhanced parameters
        "network_profile": network_profile,
        "behavioral_profile": behavioral_profile,
        "operation_metrics": {
            "cost_per_action": random.uniform(0.0005, 0.005),
            "success_rate": random.uniform(0.7, 0.95),
            "detection_evasion_score": random.uniform(0.3, 0.9)
        },
        "coordination_group": f"group_{hashlib.md5(str(i).encode()).hexdigest()[:6]}",  # Bot farm grouping
        "farm_batch_id": f"batch_{(datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y%m%d')}",
        "automation_signatures": {
            "consistent_timing": True,
            "perfect_mouse_movement": bot_type != "sophisticated_bot",
            "no_typos": True,
            "identical_interaction_patterns": True
        }
    }
    bots.append(bot)

# Engagement simulation with realistic patterns
engagement_log = []
detection_events = []
coordination_tracker = {}  # Track coordinated bot activity

print("Starting enhanced realistic YouTube bot simulation...")
print(f"Bot types: {[bot['bot_type'] for bot in bots]}")
print(f"Enhanced features: Network forensics, Behavioral analysis, Detection systems")

for step in range(SIMULATION_STEPS):
    current_time = datetime.now() + timedelta(minutes=step * 10)  # 10-minute intervals
    hour = current_time.hour
    
    # Apply temporal activity patterns
    temporal_activity_multiplier = TEMPORAL_PATTERNS["hourly_activity"].get(hour, 0.5)
    
    # Real user behavior with enhanced parameters
    for user in real_users:
        # Apply temporal patterns to activity
        user_activity_prob = temporal_activity_multiplier
        
        # Activity pattern based on user preferences
        if user["activity_pattern"] == "morning" and 6 <= hour <= 12:
            user_activity_prob *= 1.2
        elif user["activity_pattern"] == "afternoon" and 12 <= hour <= 18:
            user_activity_prob *= 1.3
        elif user["activity_pattern"] == "evening" and 18 <= hour <= 23:
            user_activity_prob *= 1.5
        elif user["activity_pattern"] == "night" and (0 <= hour <= 6 or 23 <= hour <= 24):
            user_activity_prob *= 0.8
        
        is_active = random.random() < min(user_activity_prob, 1.0)
        
        if not is_active:
            continue
        
        # Select content based on user interests
        relevant_videos = [v for v in mockup_videos 
                          if v["category"].lower() in [interest.lower() for interest in user["interests"]]]
        if not relevant_videos:
            relevant_videos = random.sample(mockup_videos, min(3, len(mockup_videos)))
        
        for video in random.sample(relevant_videos, min(2, len(relevant_videos))):
            # Realistic viewing behavior
            watch_probability = 0.3 if video["category"].lower() in [i.lower() for i in user["interests"]] else 0.1
            
            if random.random() < watch_probability:
                # Enhanced watch time calculation
                max_watch_time = min(video["duration_sec"], user["watch_time_daily_hours"] * 3600 / 10)
                attention_span = user["behavioral_profile"]["attention_span_minutes"] * 60
                
                # Natural dropoff curve with attention span
                effective_max_time = min(max_watch_time, attention_span)
                watch_time = random.uniform(30, effective_max_time)
                watch_percentage = watch_time / video["duration_sec"]
                
                # Calculate behavioral micro-patterns
                pause_events = int(watch_time / 60 * user["behavioral_profile"]["pause_frequency"])
                seek_events = int(watch_time / 60 * user["behavioral_profile"]["seek_behavior"])
                volume_changes = int(watch_time / 120 * user["behavioral_profile"]["volume_adjustments"])
                quality_changes = random.randint(0, user["behavioral_profile"]["quality_changes"])
                
                # Economic impact calculation
                economic_data = calculate_economic_impact(
                    {"action": "view", "watch_percentage": watch_percentage}, 
                    user
                )
                
                engagement_log.append({
                    "timestamp": current_time.isoformat(),
                    "step": step,
                    "user": user["user_id"],
                    "user_type": "real",
                    "action": "view",
                    "video_id": video["video_id"],
                    "creator": video["creator"],
                    "channel_name": video["channel_name"],
                    "title": video["title"],
                    "category": video["category"],
                    "watch_time_sec": watch_time,
                    "watch_percentage": watch_percentage,
                    "user_age_group": user["age_group"],
                    "user_country": user["country"],
                    "device_type": user["device_type"],
                    "subscription_status": user["subscription_status"],
                    "is_subscriber": random.random() < 0.1,
                    
                    # Enhanced network parameters
                    "network_latency_ms": user["network_profile"]["latency_ms"],
                    "connection_speed_mbps": user["network_profile"]["speed_mbps"],
                    "connection_type": user["network_profile"]["connection_type"],
                    "isp_provider": user["network_profile"]["isp_provider"],
                    "ip_address": user["network_profile"]["ip_address"],
                    
                    # Enhanced behavioral parameters
                    "pause_events": pause_events,
                    "seek_events": seek_events,
                    "volume_changes": volume_changes,
                    "quality_changes": quality_changes,
                    "click_hesitation_ms": user["behavioral_profile"]["click_hesitation_ms"],
                    "interaction_naturalness": user["behavioral_profile"]["interaction_naturalness"],
                    
                    # Enhanced device parameters
                    "screen_resolution": user["device_fingerprint"]["screen_resolution"],
                    "user_agent": user["device_fingerprint"]["user_agent"],
                    "timezone": user["device_fingerprint"]["timezone"],
                    "hardware_acceleration": user["device_fingerprint"]["hardware_acceleration"],
                    
                    # Enhanced economic parameters
                    "economic_value_usd": economic_data["economic_value_usd"],
                    "ad_revenue_potential": economic_data["ad_revenue_potential"],
                    "engagement_quality": economic_data["engagement_quality"],
                    
                    # Enhanced session parameters
                    "session_duration_minutes": user["session_patterns"]["average_session_duration"],
                    "videos_in_session": user["session_patterns"]["videos_per_session"],
                    "content_discovery_method": random.choice(["recommendations", "search", "trending", "direct"]),
                    "geographic_region": random.choice(["north_america", "europe", "asia_pacific", "other"]),
                    
                    # Detection and quality scores
                    "behavioral_naturalness_score": random.uniform(0.8, 1.0),
                    "content_relevance_score": random.uniform(0.7, 1.0),
                    "detection_risk_score": random.uniform(0.01, 0.05)  # Low for real users
                })
                
                # Engagement actions based on watch time with enhanced parameters
                if watch_percentage > 0.7:  # Watched most of the video
                    if random.random() < 0.15:  # 15% like rate for good videos
                        like_economic = calculate_economic_impact({"action": "like"}, user)
                        
                        engagement_log.append({
                            "timestamp": current_time.isoformat(),
                            "step": step,
                            "user": user["user_id"],
                            "user_type": "real",
                            "action": "like",
                            "video_id": video["video_id"],
                            "creator": video["creator"],
                            "user_country": user["country"],
                            "device_type": user["device_type"],
                            "network_latency_ms": user["network_profile"]["latency_ms"],
                            "engagement_timing": "post_watch",
                            "economic_value_usd": like_economic["economic_value_usd"],
                            "sentiment_score": random.uniform(0.7, 1.0),
                            "interaction_delay_ms": random.uniform(500, 3000)  # Natural delay before liking
                        })
                    
                    if random.random() < 0.03:  # 3% comment rate
                        realistic_comments = [
                            f"Great {video['category'].lower()} content!",
                            "Really helpful, thanks for sharing",
                            "Love your videos, keep it up!",
                            "This is exactly what I was looking for",
                            "Amazing quality as always",
                            f"Can you make more videos about {video['category'].lower()}?",
                            "Subscribed after watching this!"
                        ]
                        
                        comment_text = random.choice(realistic_comments)
                        content_analysis = analyze_content_interaction(comment_text, user, video)
                        
                        engagement_log.append({
                            "timestamp": current_time.isoformat(),
                            "step": step,
                            "user": user["user_id"],
                            "user_type": "real",
                            "action": "comment",
                            "video_id": video["video_id"],
                            "creator": video["creator"],
                            "comment_text": comment_text,
                            "user_country": user["country"],
                            "device_type": user["device_type"],
                            "network_latency_ms": user["network_profile"]["latency_ms"],
                            
                            # Enhanced content analysis
                            "content_relevance_score": content_analysis["content_relevance_score"],
                            "sentiment_authenticity": content_analysis["sentiment_authenticity"],
                            "context_awareness": content_analysis["context_awareness"],
                            "language_complexity": content_analysis["language_complexity"],
                            "typing_speed_wpm": random.uniform(20, 80),  # Human typing speed
                            "comment_length_chars": len(comment_text),
                            "time_to_compose_seconds": len(comment_text) * random.uniform(0.1, 0.3)
                        })

    # Enhanced bot behavior with sophisticated patterns
    for bot in bots:
        current_hour = current_time.hour
        
        # Check if bot is active during this hour with enhanced temporal patterns
        if current_hour not in bot["activity_hours"]:
            # Some sophisticated bots may still be active occasionally
            if bot["bot_type"] != "sophisticated_bot" or random.random() > 0.1:
                continue
        
        # Apply daily quota limits
        bot_actions_today = len([e for e in engagement_log 
                               if e.get("user") == bot["bot_id"] 
                               and e["timestamp"][:10] == current_time.date().isoformat()])
        
        if bot_actions_today >= bot["daily_quota"]:
            continue
        
        # Coordination detection - track simultaneous bot activity
        time_window = current_time.strftime("%Y-%m-%d %H:%M")
        if time_window not in coordination_tracker:
            coordination_tracker[time_window] = []
        coordination_tracker[time_window].append(bot["bot_id"])
        
        # Detect coordinated activity
        coordinated_activity = len(coordination_tracker[time_window]) > 5  # More than 5 bots active simultaneously
        
        bot_config = bot["behavior_config"]
        bot_type = bot["bot_type"]
        
        # Target specific creators or random content
        if bot["target_creators"]:
            target_videos = [v for v in mockup_videos if v["creator"] in bot["target_creators"]]
        else:
            target_videos = random.sample(mockup_videos, min(3, len(mockup_videos)))
        
        for video in random.sample(target_videos, min(2, len(target_videos))):
            # Bot-specific viewing patterns with enhanced detection
            if random.random() < 0.8:  # High activity rate for bots
                watch_time_range = bot_config["watch_time_range"]
                watch_time = random.uniform(*watch_time_range)
                watch_percentage = watch_time / video["duration_sec"]
                
                # Enhanced behavioral patterns for bots
                pause_events = int(watch_time / 60 * bot["behavioral_profile"]["pause_frequency"])
                seek_events = int(watch_time / 60 * bot["behavioral_profile"]["seek_behavior"])
                volume_changes = int(watch_time / 120 * bot["behavioral_profile"]["volume_adjustments"])
                
                # Calculate detection risk
                detection_risk = calculate_detection_risk(bot, bot["behavioral_profile"], bot["network_profile"])
                
                # Economic impact for bots
                economic_data = calculate_economic_impact(
                    {"action": "view", "watch_percentage": watch_percentage}, 
                    bot
                )
                
                # Add realistic delays for sophisticated bots
                if bot_type == "sophisticated_bot" and random.random() < 0.3:
                    time.sleep(random.uniform(1, 5))
                
                engagement_log.append({
                    "timestamp": current_time.isoformat(),
                    "step": step,
                    "user": bot["bot_id"],
                    "user_type": "bot",
                    "bot_type": bot_type,
                    "action": "view",
                    "video_id": video["video_id"],
                    "creator": video["creator"],
                    "channel_name": video["channel_name"],
                    "title": video["title"],
                    "category": video["category"],
                    "watch_time_sec": watch_time,
                    "watch_percentage": watch_percentage,
                    "bot_country": bot["location"]["country"],
                    "bot_city": bot["location"]["city"],
                    "device_profile": bot["device_profile"]["device"],
                    "user_agent": bot["device_profile"]["user_agent"],
                    "detection_signatures": list(bot["detection_signatures"].keys()),
                    "evasion_techniques": bot["evasion_techniques"],
                    
                    # Enhanced network parameters for bots
                    "network_latency_ms": bot["network_profile"]["latency_ms"],
                    "connection_speed_mbps": bot["network_profile"]["speed_mbps"],
                    "connection_type": bot["network_profile"]["connection_type"],
                    "proxy_detected": bot["network_profile"]["proxy_detected"],
                    "datacenter_ip": bot["network_profile"]["datacenter_ip"],
                    "ip_address": bot["network_profile"]["ip_address"],
                    "suspicious_network_indicators": bot["network_profile"]["suspicious_indicators"],
                    
                    # Enhanced behavioral parameters for bots
                    "pause_events": pause_events,
                    "seek_events": seek_events,
                    "volume_changes": volume_changes,
                    "click_hesitation_ms": bot["behavioral_profile"]["click_hesitation_ms"],
                    "robotic_timing": bot["behavioral_profile"]["robotic_timing"],
                    "perfect_playback": bot["behavioral_profile"]["perfect_playback"],
                    "interaction_naturalness": bot["behavioral_profile"]["interaction_naturalness"],
                    
                    # Enhanced detection parameters
                    "detection_risk_score": detection_risk,
                    "coordinated_activity": coordinated_activity,
                    "coordination_group": bot["coordination_group"],
                    "farm_batch_id": bot["farm_batch_id"],
                    "automation_signatures": bot["automation_signatures"],
                    
                    # Enhanced economic parameters
                    "operation_cost_usd": economic_data["operation_cost_usd"],
                    "revenue_pollution": economic_data["revenue_pollution"],
                    "ad_fraud_impact": economic_data["ad_fraud_impact"],
                    "detection_cost": economic_data["detection_cost"],
                    
                    # Enhanced device fingerprinting
                    "screen_resolution": bot["device_profile"]["screen_resolution"],
                    "timezone": bot["device_profile"]["timezone"],
                    "fingerprint_anomalies": bot["device_profile"]["fingerprint_anomalies"],
                    
                    # Operational metrics
                    "daily_actions_count": bot_actions_today + 1,
                    "account_age_days": (current_time - datetime.fromisoformat(bot["creation_date"])).days,
                    "target_creator_focused": len(bot["target_creators"]) <= 2
                })
                
                # Enhanced bot engagement patterns
                if random.random() < bot_config["like_rate"]:
                    like_economic = calculate_economic_impact({"action": "like"}, bot)
                    
                    engagement_log.append({
                        "timestamp": current_time.isoformat(),
                        "step": step,
                        "user": bot["bot_id"],
                        "user_type": "bot",
                        "bot_type": bot_type,
                        "action": "like",
                        "video_id": video["video_id"],
                        "creator": video["creator"],
                        "bot_country": bot["location"]["country"],
                        "device_profile": bot["device_profile"]["device"],
                        "network_latency_ms": bot["network_profile"]["latency_ms"],
                        "coordinated_activity": coordinated_activity,
                        "detection_risk_score": detection_risk,
                        "operation_cost_usd": like_economic["operation_cost_usd"],
                        "engagement_timing": "immediate" if bot_type != "sophisticated_bot" else random.choice(["immediate", "delayed"]),
                        "click_pattern": "center" if bot["automation_signatures"]["perfect_mouse_movement"] else "natural"
                    })
                
                if random.random() < bot_config["comment_rate"]:
                    comment_text = random.choice(bot_config["typical_comments"])
                    content_analysis = analyze_content_interaction(comment_text, bot, video)
                    
                    # Add detection signatures for generic comments
                    if bot_type in ["view_farm", "subscriber_farm"]:
                        detection_events.append({
                            "timestamp": current_time.isoformat(),
                            "event_type": "generic_comment_detected",
                            "bot_id": bot["bot_id"],
                            "video_id": video["video_id"],
                            "comment": comment_text,
                            "risk_score": detection_risk,
                            "detection_method": "template_matching",
                            "confidence_score": random.uniform(0.7, 0.95)
                        })
                    
                    engagement_log.append({
                        "timestamp": current_time.isoformat(),
                        "step": step,
                        "user": bot["bot_id"],
                        "user_type": "bot",
                        "bot_type": bot_type,
                        "action": "comment",
                        "video_id": video["video_id"],
                        "creator": video["creator"],
                        "comment_text": comment_text,
                        "bot_country": bot["location"]["country"],
                        "device_profile": bot["device_profile"]["device"],
                        "network_latency_ms": bot["network_profile"]["latency_ms"],
                        
                        # Enhanced content analysis for bot comments
                        "content_relevance_score": content_analysis["content_relevance_score"],
                        "template_detected": content_analysis["template_detected"],
                        "generic_response": content_analysis["generic_response"],
                        "language_complexity": content_analysis["language_complexity"],
                        "sentiment_authenticity": content_analysis["sentiment_authenticity"],
                        "detection_risk_score": detection_risk,
                        "coordinated_activity": coordinated_activity,
                        "typing_speed_simulation": random.uniform(100, 200),  # Too fast typing
                        "comment_posting_delay": random.uniform(0.5, 2.0) if bot_type == "sophisticated_bot" else random.uniform(0.1, 0.5)
                    })
                
                if random.random() < bot_config["subscriber_rate"]:
                    subscribe_economic = calculate_economic_impact({"action": "subscribe"}, bot)
                    
                    engagement_log.append({
                        "timestamp": current_time.isoformat(),
                        "step": step,
                        "user": bot["bot_id"],
                        "user_type": "bot",
                        "bot_type": bot_type,
                        "action": "subscribe",
                        "creator": video["creator"],
                        "channel_name": video["channel_name"],
                        "bot_country": bot["location"]["country"],
                        "device_profile": bot["device_profile"]["device"],
                        "network_latency_ms": bot["network_profile"]["latency_ms"],
                        "farm_batch_id": bot["farm_batch_id"],
                        "coordinated_activity": coordinated_activity,
                        "detection_risk_score": detection_risk,
                        "operation_cost_usd": subscribe_economic["operation_cost_usd"],
                        "subscription_without_engagement": bot_type == "subscriber_farm",
                        "account_age_suspicious": (current_time - datetime.fromisoformat(bot["creation_date"])).days < 30
                    })

# Calculate enhanced economic impact with detailed analysis
revenue_analysis = {
    "total_views": len([e for e in engagement_log if e["action"] == "view"]),
    "real_user_views": len([e for e in engagement_log if e["action"] == "view" and e["user_type"] == "real"]),
    "bot_views": len([e for e in engagement_log if e["action"] == "view" and e["user_type"] == "bot"]),
    "estimated_ad_revenue": 0,
    "estimated_creator_revenue": 0,
    "bot_inflation_factor": 0,
    "total_bot_operation_costs": 0,
    "total_detection_costs": 0,
    "revenue_quality_score": 0,
    "network_anomalies_detected": 0,
    "behavioral_anomalies_detected": 0,
    "high_risk_events": 0
}

# Enhanced revenue calculation with quality scoring
total_real_revenue = 0
total_bot_pollution = 0

for video in mockup_videos:
    video_events = [e for e in engagement_log if e.get("video_id") == video["video_id"]]
    
    if video_events and video["monetization_enabled"]:
        for event in video_events:
            if event.get("action") == "view":
                if event["user_type"] == "real":
                    # High-quality revenue from real users
                    revenue = event.get("economic_value_usd", 0)
                    total_real_revenue += revenue
                    revenue_analysis["estimated_ad_revenue"] += revenue
                else:
                    # Bot pollution revenue (much lower value)
                    bot_revenue = event.get("ad_fraud_impact", 0)
                    total_bot_pollution += bot_revenue
                    revenue_analysis["estimated_ad_revenue"] += bot_revenue
                    revenue_analysis["total_bot_operation_costs"] += event.get("operation_cost_usd", 0)

# Calculate enhanced metrics
revenue_analysis["bot_inflation_factor"] = revenue_analysis["bot_views"] / revenue_analysis["total_views"] if revenue_analysis["total_views"] > 0 else 0
revenue_analysis["revenue_quality_score"] = total_real_revenue / (total_real_revenue + total_bot_pollution) if (total_real_revenue + total_bot_pollution) > 0 else 0

# Detection system analysis
high_risk_events = [e for e in engagement_log if e.get("detection_risk_score", 0) > DETECTION_SYSTEM["risk_thresholds"]["high_risk"]]
medium_risk_events = [e for e in engagement_log if DETECTION_SYSTEM["risk_thresholds"]["medium_risk"] < e.get("detection_risk_score", 0) <= DETECTION_SYSTEM["risk_thresholds"]["high_risk"]]

revenue_analysis["high_risk_events"] = len(high_risk_events)
revenue_analysis["medium_risk_events"] = len(medium_risk_events)
revenue_analysis["network_anomalies_detected"] = len([e for e in engagement_log if e.get("proxy_detected") or e.get("datacenter_ip")])
revenue_analysis["behavioral_anomalies_detected"] = len([e for e in engagement_log if e.get("robotic_timing") or e.get("perfect_playback")])

# Enhanced coordination analysis
coordination_analysis = {
    "coordinated_time_windows": len([k for k, v in coordination_tracker.items() if len(v) > 5]),
    "max_simultaneous_bots": max([len(v) for v in coordination_tracker.values()]) if coordination_tracker else 0,
    "coordination_groups": len(set([bot["coordination_group"] for bot in bots])),
    "farm_batches": len(set([bot["farm_batch_id"] for bot in bots]))
}

# Create comprehensive enhanced dataset
simulation_data = {
    "metadata": {
        "simulation_type": "enhanced_realistic_youtube_bot_behavior",
        "timestamp": datetime.now().isoformat(),
        "enhanced_features": [
            "network_forensics",
            "behavioral_micro_patterns", 
            "detection_systems",
            "economic_modeling",
            "coordination_tracking",
            "content_sophistication_analysis",
            "temporal_pattern_analysis"
        ],
        "parameters": {
            "creators": NUM_CREATORS,
            "real_users": NUM_REAL_USERS,
            "bots": NUM_BOTS,
            "content_items": NUM_CONTENT,
            "simulation_steps": SIMULATION_STEPS
        },
        "bot_types": list(BOT_TYPES.keys()),
        "detection_events_count": len(detection_events),
        "enhancement_version": "2.0"
    },
    "creators": creators,
    "content": mockup_videos,
    "real_users": real_users,
    "bots": bots,
    "engagement_log": engagement_log,
    "detection_events": detection_events,
    "revenue_analysis": revenue_analysis,
    "coordination_analysis": coordination_analysis,
    "detection_system_config": DETECTION_SYSTEM,
    "network_patterns": NETWORK_PATTERNS,
    "behavioral_patterns": BEHAVIORAL_PATTERNS,
    "temporal_patterns": TEMPORAL_PATTERNS
}

# Save comprehensive data
import os
os.makedirs("../data", exist_ok=True)

with open("../data/youtube_realistic_simulation.json", "w") as f:
    json.dump(simulation_data, f, indent=2)

with open("../data/youtube_engagement_log_realistic.json", "w") as f:
    json.dump(engagement_log, f, indent=2)

with open("../data/youtube_detection_events.json", "w") as f:
    json.dump(detection_events, f, indent=2)

print(f"Realistic YouTube simulation complete!")
print(f"Total engagement events: {len(engagement_log)}")
print(f"Real user events: {len([e for e in engagement_log if e['user_type'] == 'real'])}")
print(f"Bot events: {len([e for e in engagement_log if e['user_type'] == 'bot'])}")
print(f"Detection events triggered: {len(detection_events)}")
print(f"Bot revenue inflation: {revenue_analysis['bot_inflation_factor']*100:.1f}%")
print(f"Estimated total ad revenue: ${revenue_analysis['estimated_ad_revenue']:.2f}")

# Display bot type distribution
bot_type_counts = {}
for bot in bots:
    bot_type = bot["bot_type"]
    bot_type_counts[bot_type] = bot_type_counts.get(bot_type, 0) + 1

print(f"\nBot type distribution:")
for bot_type, count in bot_type_counts.items():
    print(f"  {bot_type}: {count} bots")

# Save enhanced simulation data
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f"enhanced_youtube_simulation_{timestamp}.json"

with open(output_filename, 'w') as f:
    json.dump(simulation_data, f, indent=2, default=str)

print(f"\nEnhanced simulation data saved to: {output_filename}")
print(f"File size: {len(json.dumps(simulation_data, default=str)) / 1024:.1f} KB")
print(f"Enhanced parameters per event: {len(engagement_log[0]) if engagement_log else 0}")
print(f"Network forensics events: {len([e for e in engagement_log if e.get('network_latency_ms')])}")
print(f"High-risk detection events: {len([e for e in engagement_log if e.get('detection_risk_score', 0) > 0.7])}")

if __name__ == "__main__":
    # Example: scale up by 10x for large-scale simulation
    scale_parameters(scale_factor=10)
