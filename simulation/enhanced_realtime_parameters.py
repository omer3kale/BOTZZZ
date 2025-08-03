"""
Enhanced Real-Time Parameters for Bot Simulation
==============================================

This module contains additional parameters that can be integrated into the YouTube bot simulation
to create more realistic and comprehensive real-time data patterns.
"""

import random
import json
from datetime import datetime, timedelta
import uuid

# NETWORK BEHAVIOR PARAMETERS
NETWORK_PATTERNS = {
    "real_users": {
        "connection_types": [
            {"type": "fiber", "speed_mbps": (100, 1000), "latency_ms": (5, 15), "weight": 0.3},
            {"type": "cable", "speed_mbps": (25, 300), "latency_ms": (10, 30), "weight": 0.4},
            {"type": "mobile_5g", "speed_mbps": (50, 500), "latency_ms": (15, 40), "weight": 0.2},
            {"type": "mobile_4g", "speed_mbps": (5, 50), "latency_ms": (30, 80), "weight": 0.1}
        ],
        "session_patterns": {
            "session_duration_minutes": (5, 120),
            "videos_per_session": (1, 8),
            "break_probability": 0.3,
            "return_probability": 0.6
        }
    },
    "bots": {
        "connection_types": [
            {"type": "datacenter", "speed_mbps": (100, 1000), "latency_ms": (1, 5), "weight": 0.6},
            {"type": "residential_proxy", "speed_mbps": (20, 100), "latency_ms": (15, 50), "weight": 0.3},
            {"type": "mobile_proxy", "speed_mbps": (10, 50), "latency_ms": (50, 150), "weight": 0.1}
        ],
        "suspicious_patterns": {
            "identical_connection_speed": True,
            "consistent_low_latency": True,
            "simultaneous_connections": True,
            "unusual_bandwidth_usage": True
        }
    }
}

# TEMPORAL BEHAVIOR PATTERNS
TEMPORAL_PATTERNS = {
    "real_users": {
        "activity_by_hour": {
            0: 0.1, 1: 0.05, 2: 0.03, 3: 0.02, 4: 0.02, 5: 0.03,
            6: 0.1, 7: 0.2, 8: 0.3, 9: 0.4, 10: 0.5, 11: 0.6,
            12: 0.7, 13: 0.6, 14: 0.5, 15: 0.6, 16: 0.7, 17: 0.8,
            18: 0.9, 19: 1.0, 20: 0.9, 21: 0.8, 22: 0.6, 23: 0.3
        },
        "weekly_patterns": {
            "monday": 0.8, "tuesday": 0.9, "wednesday": 0.9, "thursday": 0.9,
            "friday": 1.0, "saturday": 1.1, "sunday": 1.0
        },
        "seasonal_variations": {
            "winter": 1.2, "spring": 1.0, "summer": 0.8, "fall": 1.1
        }
    },
    "bots": {
        "activity_patterns": [
            {"type": "24/7_farm", "variation": 0.1, "peak_hours": None},
            {"type": "business_hours", "variation": 0.3, "peak_hours": [9, 17]},
            {"type": "night_shift", "variation": 0.2, "peak_hours": [22, 6]},
            {"type": "coordinated_burst", "variation": 0.8, "burst_duration": 30}
        ]
    }
}

# ADVANCED DEVICE FINGERPRINTING
DEVICE_FINGERPRINTS = {
    "real_devices": [
        {
            "device_type": "smartphone",
            "brand": "iPhone",
            "model": "iPhone 14 Pro",
            "os": "iOS 16.5",
            "screen_resolution": "1179x2556",
            "pixel_density": 460,
            "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15",
            "hardware_features": ["touch_id", "face_id", "accelerometer", "gyroscope", "magnetometer"],
            "installed_apps": ["YouTube", "Safari", "Instagram", "TikTok"],
            "battery_level_variation": True,
            "network_switching": True
        },
        {
            "device_type": "laptop",
            "brand": "Apple",
            "model": "MacBook Pro M2",
            "os": "macOS 13.4",
            "screen_resolution": "1512x982",
            "pixel_density": 227,
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "hardware_features": ["webcam", "microphone", "bluetooth", "wifi"],
            "browser_plugins": ["flash", "pdf_viewer", "ad_blocker"],
            "screen_usage_patterns": ["fullscreen_videos", "multi_tab_browsing"]
        }
    ],
    "bot_devices": [
        {
            "device_type": "emulated_android",
            "suspicious_indicators": [
                "missing_hardware_sensors",
                "identical_screen_resolution",
                "consistent_battery_level",
                "no_installed_apps_variation",
                "unrealistic_performance_metrics"
            ],
            "emulator_signatures": ["BlueStacks", "NoxPlayer", "LDPlayer", "MEmu"],
            "virtual_machine_indicators": True
        },
        {
            "device_type": "headless_browser",
            "suspicious_indicators": [
                "missing_graphics_acceleration",
                "no_user_interaction_events",
                "automated_mouse_movement",
                "predictable_timing_patterns"
            ],
            "automation_tools": ["Selenium", "Puppeteer", "Playwright"],
            "headless_markers": True
        }
    ]
}

# BEHAVIORAL MICRO-PATTERNS
MICRO_BEHAVIORS = {
    "real_users": {
        "viewing_patterns": {
            "pause_frequency": (0.1, 0.4),  # Times per video
            "seek_behavior": (0.05, 0.2),   # Scrubbing frequency
            "volume_adjustments": (0.02, 0.1),
            "fullscreen_usage": (0.3, 0.7),
            "speed_changes": (0.01, 0.05)   # Playback speed modifications
        },
        "interaction_timing": {
            "click_delay_ms": (200, 2000),
            "scroll_speed_px_ms": (1, 5),
            "typing_speed_wpm": (20, 80),
            "mouse_movement_natural": True
        },
        "attention_patterns": {
            "tab_switching_frequency": (0.1, 0.5),
            "background_tab_duration": (30, 300),  # seconds
            "return_to_video_probability": 0.7
        }
    },
    "bots": {
        "automated_patterns": {
            "consistent_timing": True,
            "no_pause_behavior": True,
            "linear_playback_only": True,
            "no_volume_adjustment": True,
            "identical_interaction_timing": True
        },
        "detection_signatures": {
            "mouse_movement_linear": True,
            "click_timing_robotic": True,
            "no_human_hesitation": True,
            "perfect_center_clicks": True
        }
    }
}

# GEOLOCATION AND VPN PATTERNS
GEO_PATTERNS = {
    "real_users": {
        "location_consistency": True,
        "timezone_alignment": True,
        "regional_content_preferences": True,
        "language_country_match": True,
        "local_trending_awareness": True
    },
    "bots": {
        "vpn_indicators": [
            "datacenter_ip_ranges",
            "location_language_mismatch",
            "timezone_inconsistency",
            "rapid_location_changes",
            "commercial_vpn_providers"
        ],
        "proxy_patterns": [
            "residential_proxy_farms",
            "rotating_ip_addresses",
            "geolocation_spoofing",
            "dns_leak_indicators"
        ]
    }
}

# CONTENT INTERACTION SOPHISTICATION
CONTENT_SOPHISTICATION = {
    "real_users": {
        "content_understanding": {
            "comment_relevance_score": (0.7, 1.0),
            "context_awareness": True,
            "topic_continuation": True,
            "emotional_responses": True,
            "personal_references": True
        },
        "discovery_patterns": {
            "recommendation_following": 0.6,
            "search_usage": 0.4,
            "direct_channel_access": 0.3,
            "trending_exploration": 0.2,
            "playlist_creation": 0.1
        }
    },
    "bots": {
        "content_patterns": {
            "generic_responses": True,
            "keyword_stuffing": True,
            "template_based_comments": True,
            "no_context_awareness": True,
            "repetitive_phrases": True
        },
        "targeting_behavior": {
            "specific_creator_focus": True,
            "keyword_based_discovery": True,
            "no_organic_exploration": True,
            "algorithmic_gaming_intent": True
        }
    }
}

# ECONOMIC IMPACT PARAMETERS
ECONOMIC_METRICS = {
    "revenue_streams": {
        "ad_revenue_cpm": {
            "real_views": {"min": 0.5, "max": 8.0, "average": 2.5},
            "bot_views": {"min": 0.1, "max": 0.3, "average": 0.15}  # Lower value
        },
        "engagement_premiums": {
            "high_engagement_multiplier": 1.5,
            "subscriber_value_multiplier": 2.0,
            "comment_engagement_multiplier": 1.3
        }
    },
    "cost_structures": {
        "bot_operation_costs": {
            "view_farm_cost_per_1k": 0.50,
            "engagement_pod_cost_per_1k": 2.00,
            "subscriber_farm_cost_per_1k": 1.50,
            "sophisticated_bot_cost_per_1k": 5.00
        },
        "detection_costs": {
            "content_moderation_cost": 0.10,  # per engagement
            "ai_detection_cost": 0.05,
            "human_review_cost": 1.00
        }
    }
}

# PLATFORM-SPECIFIC ALGORITHM SIGNALS
ALGORITHM_SIGNALS = {
    "youtube_ranking_factors": {
        "watch_time_weight": 0.35,
        "engagement_rate_weight": 0.25,
        "click_through_rate_weight": 0.20,
        "session_duration_weight": 0.15,
        "freshness_weight": 0.05
    },
    "bot_impact_on_algorithm": {
        "artificial_watch_time_boost": True,
        "engagement_manipulation": True,
        "recommendation_pollution": True,
        "trending_manipulation": True,
        "creator_economy_distortion": True
    }
}

# DETECTION SYSTEM PARAMETERS
DETECTION_SYSTEMS = {
    "ml_detection_features": [
        "behavioral_clustering",
        "device_fingerprint_analysis",
        "network_pattern_recognition",
        "temporal_anomaly_detection",
        "content_interaction_analysis",
        "cross_platform_correlation"
    ],
    "detection_accuracy": {
        "view_farm_detection": 0.85,
        "engagement_pod_detection": 0.75,
        "subscriber_farm_detection": 0.90,
        "sophisticated_bot_detection": 0.45
    },
    "false_positive_rates": {
        "aggressive_detection": 0.15,
        "balanced_detection": 0.08,
        "conservative_detection": 0.03
    }
}

# REAL-TIME STREAMING PARAMETERS
STREAMING_PARAMETERS = {
    "live_metrics": {
        "concurrent_viewers": {
            "real_growth_pattern": "exponential_with_decay",
            "bot_growth_pattern": "linear_burst",
            "peak_retention_real": 0.6,
            "peak_retention_bot": 0.95
        },
        "chat_interaction": {
            "real_chat_rate": (0.1, 0.3),  # messages per minute per viewer
            "bot_chat_rate": (0.05, 0.8),
            "message_complexity_real": "high_variation",
            "message_complexity_bot": "template_based"
        }
    },
    "buffering_patterns": {
        "real_users": {
            "buffer_events_per_hour": (0, 3),
            "buffer_duration_seconds": (2, 15),
            "quality_adjustments": True
        },
        "bots": {
            "buffer_events_per_hour": (0, 0),  # Minimal buffering
            "perfect_connection_indicators": True,
            "no_quality_adjustments": True
        }
    }
}

# SOCIAL PROOF MANIPULATION
SOCIAL_PROOF_PARAMETERS = {
    "engagement_cascades": {
        "like_momentum": {
            "real_threshold": 100,  # Likes needed for organic growth
            "bot_artificial_boost": 500,  # Artificial starting point
            "cascade_multiplier": 1.3
        },
        "comment_influence": {
            "top_comment_visibility_impact": 2.5,
            "bot_comment_positioning": "strategic_early_placement",
            "sentiment_manipulation": True
        }
    },
    "subscriber_psychology": {
        "social_proof_threshold": 1000,  # Subscriber count for credibility
        "bot_subscriber_front_loading": True,
        "inactive_subscriber_detection": 0.7  # Percentage that can be detected
    }
}

def generate_enhanced_user_profile(user_type="real"):
    """Generate enhanced user profile with all new parameters."""
    
    if user_type == "real":
        # Network behavior
        connection = random.choices(
            NETWORK_PATTERNS["real_users"]["connection_types"],
            weights=[c["weight"] for c in NETWORK_PATTERNS["real_users"]["connection_types"]]
        )[0]
        
        # Device fingerprint
        device = random.choice(DEVICE_FINGERPRINTS["real_devices"])
        
        # Behavioral patterns
        viewing = MICRO_BEHAVIORS["real_users"]["viewing_patterns"]
        interaction = MICRO_BEHAVIORS["real_users"]["interaction_timing"]
        
        return {
            "user_id": f"real_{uuid.uuid4().hex[:8]}",
            "user_type": "real",
            "network_profile": {
                "connection_type": connection["type"],
                "speed_mbps": random.uniform(*connection["speed_mbps"]),
                "latency_ms": random.uniform(*connection["latency_ms"]),
                "isp": random.choice(["Comcast", "Verizon", "AT&T", "Charter", "Local ISP"])
            },
            "device_profile": device,
            "behavioral_metrics": {
                "pause_frequency": random.uniform(*viewing["pause_frequency"]),
                "seek_behavior": random.uniform(*viewing["seek_behavior"]),
                "click_delay_ms": random.uniform(*interaction["click_delay_ms"]),
                "typing_speed_wpm": random.uniform(*interaction["typing_speed_wpm"]),
                "attention_span_minutes": random.uniform(5, 45)
            },
            "content_sophistication": {
                "comment_relevance": random.uniform(0.7, 1.0),
                "context_awareness": True,
                "emotional_responses": True
            },
            "economic_value": {
                "ad_revenue_multiplier": random.uniform(0.8, 1.2),
                "engagement_quality": random.uniform(0.7, 1.0)
            }
        }
    
    else:  # bot
        # Bot-specific suspicious patterns
        connection = random.choices(
            NETWORK_PATTERNS["bots"]["connection_types"],
            weights=[c["weight"] for c in NETWORK_PATTERNS["bots"]["connection_types"]]
        )[0]
        
        device = random.choice(DEVICE_FINGERPRINTS["bot_devices"])
        bot_type = random.choice(["view_farm", "engagement_pod", "subscriber_farm", "sophisticated_bot"])
        
        return {
            "user_id": f"bot_{bot_type}_{uuid.uuid4().hex[:8]}",
            "user_type": "bot",
            "bot_subtype": bot_type,
            "network_profile": {
                "connection_type": connection["type"],
                "speed_mbps": random.uniform(*connection["speed_mbps"]),
                "latency_ms": random.uniform(*connection["latency_ms"]),
                "suspicious_indicators": NETWORK_PATTERNS["bots"]["suspicious_patterns"]
            },
            "device_profile": device,
            "behavioral_anomalies": {
                "consistent_timing": True,
                "no_human_hesitation": True,
                "automated_patterns": True,
                "detection_risk_score": random.uniform(0.3, 0.9)
            },
            "content_sophistication": {
                "comment_relevance": random.uniform(0.1, 0.4),
                "generic_responses": True,
                "template_based": True
            },
            "economic_impact": {
                "operation_cost_per_1k": ECONOMIC_METRICS["cost_structures"]["bot_operation_costs"][f"{bot_type}_cost_per_1k"],
                "revenue_pollution_factor": random.uniform(0.1, 0.3)
            }
        }

def calculate_detection_probability(user_profile):
    """Calculate probability of bot detection based on profile."""
    if user_profile["user_type"] == "real":
        return 0.02  # False positive rate
    
    bot_type = user_profile["bot_subtype"]
    base_detection = DETECTION_SYSTEMS["detection_accuracy"][f"{bot_type}_detection"]
    
    # Adjust based on sophistication
    risk_score = user_profile["behavioral_anomalies"]["detection_risk_score"]
    
    return base_detection * risk_score

def simulate_real_time_event(user_profile, content_item, current_time):
    """Simulate a real-time engagement event with enhanced parameters."""
    
    event = {
        "timestamp": current_time.isoformat(),
        "user_id": user_profile["user_id"],
        "user_type": user_profile["user_type"],
        "content_id": content_item["video_id"],
        "network_latency_ms": user_profile["network_profile"]["latency_ms"],
        "connection_speed_mbps": user_profile["network_profile"]["speed_mbps"],
        "device_fingerprint": {
            "screen_resolution": user_profile["device_profile"].get("screen_resolution"),
            "user_agent": user_profile["device_profile"].get("user_agent"),
            "hardware_features": user_profile["device_profile"].get("hardware_features", [])
        }
    }
    
    if user_profile["user_type"] == "bot":
        event.update({
            "bot_subtype": user_profile["bot_subtype"],
            "detection_probability": calculate_detection_probability(user_profile),
            "suspicious_indicators": user_profile["device_profile"].get("suspicious_indicators", []),
            "operation_cost_usd": user_profile["economic_impact"]["operation_cost_per_1k"] / 1000
        })
    else:
        event.update({
            "behavioral_naturalness_score": random.uniform(0.7, 1.0),
            "content_relevance_score": user_profile["content_sophistication"]["comment_relevance"],
            "economic_value_usd": random.uniform(0.001, 0.008)  # Per engagement
        })
    
    return event

# EXAMPLE USAGE FUNCTIONS
def demonstrate_enhanced_parameters():
    """Demonstrate the enhanced parameters in action."""
    
    print("=== Enhanced Real-Time Parameters Demo ===\n")
    
    # Generate sample profiles
    real_user = generate_enhanced_user_profile("real")
    bot_user = generate_enhanced_user_profile("bot")
    
    print("Real User Profile Sample:")
    print(json.dumps(real_user, indent=2))
    print("\n" + "="*50 + "\n")
    
    print("Bot User Profile Sample:")
    print(json.dumps(bot_user, indent=2))
    print("\n" + "="*50 + "\n")
    
    # Simulate events
    current_time = datetime.now()
    sample_content = {"video_id": "sample_video_123"}
    
    real_event = simulate_real_time_event(real_user, sample_content, current_time)
    bot_event = simulate_real_time_event(bot_user, sample_content, current_time)
    
    print("Real User Event Sample:")
    print(json.dumps(real_event, indent=2))
    print("\n" + "="*50 + "\n")
    
    print("Bot User Event Sample:")
    print(json.dumps(bot_event, indent=2))

if __name__ == "__main__":
    demonstrate_enhanced_parameters()
