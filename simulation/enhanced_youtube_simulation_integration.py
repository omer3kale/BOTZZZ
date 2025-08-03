"""
Enhanced YouTube Bot Simulation with Advanced Real-Time Parameters
================================================================

This module integrates the enhanced real-time parameters into the existing YouTube simulation
to create more sophisticated and realistic bot behavior detection and analysis.
"""

import random
import json
import time
import numpy as np
from datetime import datetime, timedelta
import uuid
from enhanced_realtime_parameters import (
    generate_enhanced_user_profile,
    simulate_real_time_event,
    calculate_detection_probability,
    TEMPORAL_PATTERNS,
    ALGORITHM_SIGNALS,
    ECONOMIC_METRICS,
    STREAMING_PARAMETERS
)

# Enhanced simulation parameters with real-time capabilities
ENHANCED_SIMULATION_CONFIG = {
    "real_time_monitoring": True,
    "advanced_detection": True,
    "economic_modeling": True,
    "behavioral_analysis": True,
    "network_forensics": True
}

def enhanced_scale_parameters(scale_factor=1):
    """Enhanced parameter scaling with real-time considerations."""
    global NUM_CREATORS, NUM_REAL_USERS, NUM_BOTS, NUM_CONTENT, SIMULATION_STEPS
    NUM_CREATORS = int(5 * scale_factor)
    NUM_REAL_USERS = int(100 * scale_factor)
    NUM_BOTS = int(20 * scale_factor)
    NUM_CONTENT = int(10 * scale_factor)
    SIMULATION_STEPS = int(50 * scale_factor)
    
    print(f"Enhanced parameters scaled by factor {scale_factor}:")
    print(f"NUM_CREATORS: {NUM_CREATORS}")
    print(f"NUM_REAL_USERS: {NUM_REAL_USERS}")
    print(f"NUM_BOTS: {NUM_BOTS}")
    print(f"NUM_CONTENT: {NUM_CONTENT}")
    print(f"SIMULATION_STEPS: {SIMULATION_STEPS}")
    print(f"Real-time monitoring: {ENHANCED_SIMULATION_CONFIG['real_time_monitoring']}")

# Initialize enhanced parameters
NUM_CREATORS = 5
NUM_REAL_USERS = 100
NUM_BOTS = 20
NUM_CONTENT = 10
SIMULATION_STEPS = 50

def create_enhanced_content_item(creator_info, content_index):
    """Create content with enhanced algorithmic and economic parameters."""
    
    content_types = {
        "gaming": {
            "titles": [f"EPIC Gaming Montage #{content_index}", f"NEW Game Review - Must Watch!"],
            "algorithm_boost": 1.2,  # Gaming content performs well
            "monetization_rate": 0.8,
            "target_demographics": ["13-25", "gaming_enthusiasts"]
        },
        "education": {
            "titles": [f"Learn Programming in 10 Minutes - Tutorial #{content_index}", f"Science Explained Simply"],
            "algorithm_boost": 1.1,
            "monetization_rate": 0.9,
            "target_demographics": ["18-45", "students", "professionals"]
        },
        "entertainment": {
            "titles": [f"Hilarious Compilation #{content_index}", f"Trending Dance Challenge"],
            "algorithm_boost": 1.3,
            "monetization_rate": 0.7,
            "target_demographics": ["13-35", "general_audience"]
        }
    }
    
    content_type = random.choice(list(content_types.keys()))
    type_config = content_types[content_type]
    
    # Enhanced content metadata
    content = {
        "video_id": f"yt_enhanced_{uuid.uuid4().hex[:11]}",
        "creator_id": creator_info["creator_id"],
        "title": random.choice(type_config["titles"]),
        "content_type": content_type,
        "duration_seconds": random.randint(60, 1800),
        "upload_timestamp": (datetime.now() - timedelta(hours=random.randint(1, 168))).isoformat(),
        
        # Algorithm parameters
        "algorithm_signals": {
            "expected_watch_time": random.uniform(0.3, 0.8),  # Percentage of video watched
            "click_through_rate": random.uniform(0.02, 0.12),
            "engagement_velocity": random.uniform(0.1, 2.0),  # Engagement per minute
            "content_quality_score": random.uniform(0.6, 1.0),
            "algorithm_boost_factor": type_config["algorithm_boost"]
        },
        
        # Economic parameters
        "monetization": {
            "enabled": random.random() < type_config["monetization_rate"],
            "cpm_range": (0.5, 8.0),
            "estimated_revenue_per_1k_views": random.uniform(1.0, 5.0),
            "brand_safety_score": random.uniform(0.7, 1.0)
        },
        
        # Real-time metrics (updated during simulation)
        "real_time_metrics": {
            "current_views": 0,
            "current_likes": 0,
            "current_comments": 0,
            "current_shares": 0,
            "watch_time_minutes": 0,
            "unique_viewers": 0,
            "bot_activity_detected": 0,
            "revenue_generated": 0.0
        },
        
        # Target audience for realistic engagement
        "target_demographics": type_config["target_demographics"]
    }
    
    return content

def enhanced_user_behavior_simulation(user_profile, content_item, current_time, global_context):
    """Simulate enhanced user behavior with sophisticated real-time parameters."""
    
    events = []
    user_type = user_profile["user_type"]
    
    # Time-based activity modulation
    hour = current_time.hour
    day_of_week = current_time.strftime("%A").lower()
    
    if user_type == "real":
        # Real user temporal patterns
        activity_multiplier = TEMPORAL_PATTERNS["real_users"]["activity_by_hour"][hour]
        activity_multiplier *= TEMPORAL_PATTERNS["real_users"]["weekly_patterns"][day_of_week]
        
        # Content relevance check
        user_interests = user_profile.get("interests", [])
        content_type = content_item["content_type"]
        relevance_score = 1.0 if content_type in user_interests else 0.3
        
        # Decide if user engages
        engagement_probability = 0.4 * activity_multiplier * relevance_score
        
        if random.random() < engagement_probability:
            # Generate view event with detailed metrics
            watch_duration = simulate_realistic_watch_time(user_profile, content_item)
            
            view_event = simulate_real_time_event(user_profile, content_item, current_time)
            view_event.update({
                "action": "view",
                "watch_duration_seconds": watch_duration,
                "watch_percentage": watch_duration / content_item["duration_seconds"],
                "quality_selected": random.choice(["auto", "720p", "1080p", "480p"]),
                "device_orientation": random.choice(["portrait", "landscape"]) if "mobile" in user_profile["device_profile"]["device_type"] else "landscape",
                "fullscreen_usage": random.random() < 0.4,
                "pause_events": random.randint(0, 3),
                "seek_events": random.randint(0, 2),
                "volume_level": random.uniform(0.3, 1.0),
                "geographic_region": determine_user_region(user_profile),
                "content_discovery_method": random.choice(["recommendations", "search", "trending", "direct"])
            })
            events.append(view_event)
            
            # Secondary engagement based on watch time
            if watch_duration > content_item["duration_seconds"] * 0.5:
                # Like probability increases with watch time
                like_probability = min(0.15, watch_duration / content_item["duration_seconds"] * 0.2)
                if random.random() < like_probability:
                    like_event = simulate_real_time_event(user_profile, content_item, current_time + timedelta(seconds=watch_duration))
                    like_event.update({
                        "action": "like",
                        "engagement_timing": "during_watch" if random.random() < 0.7 else "post_watch",
                        "sentiment_score": random.uniform(0.6, 1.0)
                    })
                    events.append(like_event)
                
                # Comment probability
                if random.random() < 0.08:
                    comment_event = generate_realistic_comment(user_profile, content_item, current_time, watch_duration)
                    events.append(comment_event)
                
                # Subscribe probability (for new content)
                if random.random() < 0.02:
                    subscribe_event = simulate_real_time_event(user_profile, content_item, current_time + timedelta(seconds=watch_duration + 30))
                    subscribe_event.update({
                        "action": "subscribe",
                        "trigger": "content_quality",
                        "subscriber_value_prediction": random.uniform(5.0, 50.0)  # Lifetime value
                    })
                    events.append(subscribe_event)
    
    else:  # Bot behavior
        bot_subtype = user_profile["bot_subtype"]
        
        # Bot-specific activity patterns
        if bot_subtype == "view_farm":
            # High volume, low engagement
            if random.random() < 0.9:  # Very high activity rate
                watch_duration = random.uniform(10, 45)  # Short watches
                
                view_event = simulate_real_time_event(user_profile, content_item, current_time)
                view_event.update({
                    "action": "view",
                    "watch_duration_seconds": watch_duration,
                    "watch_percentage": watch_duration / content_item["duration_seconds"],
                    "bot_signatures": {
                        "linear_playback": True,
                        "no_interaction": True,
                        "consistent_timing": True,
                        "headless_browser_indicators": user_profile["device_profile"].get("headless_markers", False)
                    },
                    "fraud_indicators": {
                        "impossible_user_agent": check_user_agent_validity(user_profile),
                        "datacenter_ip": user_profile["network_profile"]["connection_type"] == "datacenter",
                        "automation_signatures": True
                    }
                })
                events.append(view_event)
        
        elif bot_subtype == "engagement_pod":
            # Coordinated high engagement
            if random.random() < 0.7:
                watch_duration = random.uniform(120, 300)  # Longer watches to appear legitimate
                
                view_event = simulate_real_time_event(user_profile, content_item, current_time)
                view_event.update({
                    "action": "view",
                    "watch_duration_seconds": watch_duration,
                    "watch_percentage": min(1.0, watch_duration / content_item["duration_seconds"]),
                    "coordinated_timing": check_coordinated_behavior(current_time, global_context),
                    "engagement_pod_id": f"pod_{hash(user_profile['user_id']) % 100}"
                })
                events.append(view_event)
                
                # High engagement rates
                if random.random() < 0.9:  # 90% like rate
                    like_event = simulate_real_time_event(user_profile, content_item, current_time + timedelta(seconds=30))
                    like_event.update({
                        "action": "like",
                        "coordinated_timing": True,
                        "engagement_pod_id": f"pod_{hash(user_profile['user_id']) % 100}"
                    })
                    events.append(like_event)
                
                if random.random() < 0.6:  # 60% comment rate
                    comment_event = generate_bot_comment(user_profile, content_item, current_time, bot_subtype)
                    events.append(comment_event)
        
        elif bot_subtype == "subscriber_farm":
            # Focus on subscriptions with minimal engagement
            if random.random() < 0.95:  # Very high subscription rate
                subscribe_event = simulate_real_time_event(user_profile, content_item, current_time)
                subscribe_event.update({
                    "action": "subscribe",
                    "bot_farm_batch_id": f"batch_{current_time.strftime('%Y%m%d%H')}",
                    "minimal_engagement_signature": True,
                    "account_age_suspicious": random.randint(1, 30) if random.random() < 0.8 else random.randint(100, 1000)
                })
                events.append(subscribe_event)
                
                # Minimal view to avoid detection
                if random.random() < 0.3:
                    view_event = simulate_real_time_event(user_profile, content_item, current_time)
                    view_event.update({
                        "action": "view",
                        "watch_duration_seconds": random.uniform(5, 20),
                        "watch_percentage": random.uniform(0.01, 0.1),
                        "subscription_without_engagement_flag": True
                    })
                    events.append(view_event)
        
        elif bot_subtype == "sophisticated_bot":
            # AI-powered human-like behavior
            if random.random() < 0.4:  # Moderate activity to avoid detection
                watch_duration = random.uniform(120, 600)  # Human-like watch times
                
                view_event = simulate_real_time_event(user_profile, content_item, current_time)
                view_event.update({
                    "action": "view",
                    "watch_duration_seconds": watch_duration,
                    "watch_percentage": watch_duration / content_item["duration_seconds"],
                    "simulated_human_behavior": {
                        "pause_events": random.randint(0, 2),
                        "seek_events": random.randint(0, 1),
                        "quality_changes": random.randint(0, 1)
                    },
                    "ai_generated_patterns": {
                        "behavioral_consistency": 0.95,  # Too consistent to be human
                        "decision_timing_uniformity": True,
                        "lack_of_spontaneity": True
                    }
                })
                events.append(view_event)
                
                # AI-generated engagement
                if random.random() < 0.25:
                    like_event = simulate_real_time_event(user_profile, content_item, current_time + timedelta(seconds=watch_duration))
                    like_event.update({
                        "action": "like",
                        "ai_decision_pattern": True
                    })
                    events.append(like_event)
                
                if random.random() < 0.08:
                    comment_event = generate_ai_comment(user_profile, content_item, current_time)
                    events.append(comment_event)
    
    return events

def simulate_realistic_watch_time(user_profile, content_item):
    """Simulate realistic watch time based on user behavior and content quality."""
    
    base_attention_span = user_profile["behavioral_metrics"]["attention_span_minutes"] * 60
    content_duration = content_item["duration_seconds"]
    content_quality = content_item["algorithm_signals"]["content_quality_score"]
    
    # Adjust for content quality
    quality_modifier = 0.5 + (content_quality * 0.5)
    
    # Natural dropoff curve
    max_watch_time = min(base_attention_span * quality_modifier, content_duration)
    
    # Exponential decay for dropoff probability
    dropoff_factor = random.expovariate(1.0 / (max_watch_time / 3))
    actual_watch_time = min(max_watch_time, dropoff_factor)
    
    return max(10, actual_watch_time)  # Minimum 10 seconds

def generate_realistic_comment(user_profile, content_item, current_time, watch_duration):
    """Generate realistic human comment with context awareness."""
    
    content_type = content_item["content_type"]
    watch_percentage = watch_duration / content_item["duration_seconds"]
    
    # Context-aware comment templates
    comment_templates = {
        "gaming": [
            f"That {random.choice(['combo', 'play', 'move'])} at {random.randint(1, int(watch_duration))}:{random.randint(0, 59):02d} was insane!",
            "Your gameplay has really improved since the last video!",
            f"What {random.choice(['settings', 'gear', 'setup'])} are you using for this?",
            "This makes me want to try this game myself"
        ],
        "education": [
            f"Finally understand {random.choice(['this concept', 'this topic', 'how this works'])}! Thanks!",
            "Could you do a video on the advanced version of this?",
            "This is going to help me so much with my project",
            "Great explanation, very clear and concise"
        ],
        "entertainment": [
            f"Lost it at {random.randint(1, int(watch_duration/60))}:{random.randint(0, 59):02d} 😂",
            "How do you come up with this stuff?",
            "This made my day, thank you!",
            "Already shared this with all my friends"
        ]
    }
    
    comment_text = random.choice(comment_templates.get(content_type, ["Great video!", "Thanks for sharing!", "Love your content!"]))
    
    # Add personal touch based on user sophistication
    if user_profile["content_sophistication"]["context_awareness"]:
        if watch_percentage > 0.8:
            comment_text += " Watched the whole thing!"
        elif random.random() < 0.3:
            comment_text += f" (commenting at {int(watch_percentage*100)}% through)"
    
    comment_event = simulate_real_time_event(user_profile, content_item, current_time + timedelta(seconds=watch_duration))
    comment_event.update({
        "action": "comment",
        "comment_text": comment_text,
        "comment_timing": watch_duration,
        "context_relevance_score": user_profile["content_sophistication"]["comment_relevance"],
        "sentiment_analysis": {
            "polarity": random.uniform(0.3, 1.0),  # Positive bias for comments
            "subjectivity": random.uniform(0.4, 0.9),
            "authenticity_score": random.uniform(0.7, 1.0)
        },
        "engagement_quality": "high"
    })
    
    return comment_event

def generate_bot_comment(user_profile, content_item, current_time, bot_subtype):
    """Generate bot comment with detectable patterns."""
    
    generic_comments = [
        "First!", "Nice video!", "Great content!", "Amazing!", "Love this!",
        "Perfect video!", "Awesome work!", "Thanks for sharing!", "So good!", "Keep it up!"
    ]
    
    if bot_subtype == "engagement_pod":
        pod_comments = [
            "This deserves more views!", "Underrated channel!", "Why doesn't this have more likes?",
            "Algorithm needs to push this!", "This should be trending!"
        ]
        comment_text = random.choice(pod_comments)
    else:
        comment_text = random.choice(generic_comments)
    
    comment_event = simulate_real_time_event(user_profile, content_item, current_time)
    comment_event.update({
        "action": "comment",
        "comment_text": comment_text,
        "bot_comment_patterns": {
            "generic_template": True,
            "no_context_awareness": True,
            "timing_suspicion": "immediate_post",
            "language_complexity": "low"
        },
        "detection_signals": {
            "template_match_probability": 0.9,
            "sentiment_authenticity": random.uniform(0.1, 0.4),
            "contextual_relevance": random.uniform(0.0, 0.3)
        },
        "engagement_quality": "low"
    })
    
    return comment_event

def generate_ai_comment(user_profile, content_item, current_time):
    """Generate AI-powered comment that's harder to detect."""
    
    content_type = content_item["content_type"]
    
    # AI-generated comment templates with variables
    ai_templates = {
        "gaming": [
            f"Really enjoyed the strategy you used around the {random.choice(['mid-game', 'late-game', 'early phase'])}",
            f"Your {random.choice(['mechanics', 'decision-making', 'positioning'])} has definitely improved",
            f"Have you considered trying {random.choice(['a different build', 'this strategy', 'that approach'])}?"
        ],
        "education": [
            f"The way you explained {random.choice(['the concept', 'this topic', 'the theory'])} was very clear",
            f"This really helps with understanding {random.choice(['the fundamentals', 'the basics', 'advanced topics'])}",
            f"Looking forward to more content on {random.choice(['this subject', 'related topics', 'similar themes'])}"
        ],
        "entertainment": [
            f"The {random.choice(['editing', 'timing', 'presentation'])} in this video was spot on",
            f"Love how you {random.choice(['approached this', 'handled that', 'executed this idea'])}",
            f"Your {random.choice(['style', 'humor', 'creativity'])} really shines through"
        ]
    }
    
    comment_text = random.choice(ai_templates.get(content_type, [
        "Great content as always!", "Really well done!", "Excellent work on this!"
    ]))
    
    comment_event = simulate_real_time_event(user_profile, content_item, current_time)
    comment_event.update({
        "action": "comment",
        "comment_text": comment_text,
        "ai_generation_markers": {
            "template_variation": True,
            "contextual_insertion": True,
            "grammatical_perfection": True,
            "emotional_distance": True
        },
        "detection_difficulty": "high",
        "engagement_quality": "medium"
    })
    
    return comment_event

def check_coordinated_behavior(current_time, global_context):
    """Check for coordinated timing patterns in bot behavior."""
    
    # Look for unusual clustering of activity
    time_window = timedelta(minutes=5)
    recent_events = [
        event for event in global_context.get("recent_events", [])
        if abs((datetime.fromisoformat(event["timestamp"]) - current_time).total_seconds()) < time_window.total_seconds()
    ]
    
    # Detect suspicious patterns
    if len(recent_events) > 10:  # Too many events in short time
        return True
    
    return False

def check_user_agent_validity(user_profile):
    """Check for impossible or suspicious user agent strings."""
    
    user_agent = user_profile["device_profile"].get("user_agent", "")
    
    # Simple checks for bot signatures
    suspicious_indicators = [
        "HeadlessChrome",
        "PhantomJS",
        "Selenium",
        "WebDriver",
        "automation"
    ]
    
    return any(indicator in user_agent for indicator in suspicious_indicators)

def determine_user_region(user_profile):
    """Determine user's geographic region for content localization."""
    
    # Simple region mapping based on network profile
    connection_type = user_profile["network_profile"]["connection_type"]
    
    if connection_type == "datacenter":
        return random.choice(["datacenter_us_east", "datacenter_eu_west", "datacenter_asia"])
    else:
        return random.choice(["north_america", "europe", "asia_pacific", "south_america", "africa"])

def calculate_economic_impact(events, content_item):
    """Calculate detailed economic impact of engagement events."""
    
    total_revenue = 0.0
    total_costs = 0.0
    
    for event in events:
        if event["user_type"] == "real":
            # Real user value
            if event["action"] == "view":
                watch_percentage = event.get("watch_percentage", 0)
                if watch_percentage > 0.3:  # Monetizable view
                    cpm = random.uniform(*content_item["monetization"]["cpm_range"])
                    revenue = (cpm / 1000) * event.get("economic_value_usd", 0.002)
                    total_revenue += revenue
            
            elif event["action"] == "like":
                total_revenue += 0.001  # Engagement premium
            
            elif event["action"] == "subscribe":
                total_revenue += random.uniform(0.05, 0.20)  # Subscriber value
        
        else:  # Bot
            # Bot costs and negative impact
            total_costs += event.get("operation_cost_usd", 0.001)
            
            # Revenue pollution (ads shown to bots have lower value)
            if event["action"] == "view":
                revenue_pollution = random.uniform(0.0001, 0.0005)
                total_revenue += revenue_pollution  # Much lower than real users
    
    return {
        "total_revenue": total_revenue,
        "total_costs": total_costs,
        "net_impact": total_revenue - total_costs,
        "revenue_quality_score": total_revenue / (total_revenue + total_costs) if (total_revenue + total_costs) > 0 else 0
    }

# Example usage function
def run_enhanced_simulation_demo(scale_factor=0.1):
    """Run a small demo of the enhanced simulation."""
    
    print("=== Enhanced YouTube Bot Simulation Demo ===\n")
    
    # Scale down for demo
    enhanced_scale_parameters(scale_factor)
    
    # Get the scaled values
    global NUM_SIMULATION_STEPS
    if 'NUM_SIMULATION_STEPS' not in globals():
        NUM_SIMULATION_STEPS = int(50 * scale_factor)
    
    # Create enhanced users
    real_users = [generate_enhanced_user_profile("real") for _ in range(NUM_REAL_USERS)]
    bot_users = [generate_enhanced_user_profile("bot") for _ in range(NUM_BOTS)]
    
    # Create enhanced content
    creators = [{"creator_id": f"creator_{i}"} for i in range(NUM_CREATORS)]
    content_items = [create_enhanced_content_item(creators[i % NUM_CREATORS], i) for i in range(NUM_CONTENT)]
    
    # Simulation
    all_events = []
    global_context = {"recent_events": []}
    
    for step in range(NUM_SIMULATION_STEPS):
        current_time = datetime.now() + timedelta(minutes=step * 30)
        
        # Simulate real users
        for user in real_users[:3]:  # Demo with fewer users
            for content in content_items[:2]:  # Demo with fewer content items
                events = enhanced_user_behavior_simulation(user, content, current_time, global_context)
                all_events.extend(events)
                global_context["recent_events"].extend(events)
        
        # Simulate bots
        for bot in bot_users[:2]:  # Demo with fewer bots
            for content in content_items[:2]:
                events = enhanced_user_behavior_simulation(bot, content, current_time, global_context)
                all_events.extend(events)
                global_context["recent_events"].extend(events)
        
        # Keep only recent events in context
        cutoff_time = current_time - timedelta(hours=1)
        global_context["recent_events"] = [
            event for event in global_context["recent_events"]
            if datetime.fromisoformat(event["timestamp"]) > cutoff_time
        ]
    
    # Analysis
    real_events = [e for e in all_events if e["user_type"] == "real"]
    bot_events = [e for e in all_events if e["user_type"] == "bot"]
    
    print(f"Total events generated: {len(all_events)}")
    print(f"Real user events: {len(real_events)}")
    print(f"Bot events: {len(bot_events)}")
    print(f"Bot activity percentage: {len(bot_events)/len(all_events)*100:.1f}%")
    
    # Economic impact
    for content in content_items:
        content_events = [e for e in all_events if e.get("content_id") == content["video_id"]]
        if content_events:
            economic_impact = calculate_economic_impact(content_events, content)
            print(f"\nContent '{content['title'][:30]}...' economic impact:")
            print(f"  Revenue: ${economic_impact['total_revenue']:.4f}")
            print(f"  Costs: ${economic_impact['total_costs']:.4f}")
            print(f"  Net Impact: ${economic_impact['net_impact']:.4f}")
            print(f"  Quality Score: {economic_impact['revenue_quality_score']:.3f}")
    
    # Detection analysis
    detection_events = [e for e in bot_events if e.get("detection_probability", 0) > 0.7]
    print(f"\nHigh-risk bot events detected: {len(detection_events)}")
    
    # Save enhanced data
    enhanced_data = {
        "metadata": {
            "simulation_type": "enhanced_youtube_realtime",
            "timestamp": datetime.now().isoformat(),
            "enhanced_features": list(ENHANCED_SIMULATION_CONFIG.keys())
        },
        "users": {
            "real_users": real_users,
            "bot_users": bot_users
        },
        "content": content_items,
        "events": all_events,
        "global_context": global_context
    }
    
    # Save to file
    import os
    os.makedirs("../data", exist_ok=True)
    
    with open("../data/enhanced_youtube_simulation.json", "w") as f:
        json.dump(enhanced_data, f, indent=2)
    
    print(f"\nEnhanced simulation data saved to: ../data/enhanced_youtube_simulation.json")
    print(f"File size: {len(json.dumps(enhanced_data)) / 1024:.1f} KB")
    
    return enhanced_data

if __name__ == "__main__":
    # Run demo
    enhanced_data = run_enhanced_simulation_demo(scale_factor=0.2)
    
    # Show sample events
    print("\n=== Sample Enhanced Events ===")
    
    sample_real_event = next((e for e in enhanced_data["events"] if e["user_type"] == "real"), None)
    if sample_real_event:
        print("\nSample Real User Event:")
        print(json.dumps(sample_real_event, indent=2))
    
    sample_bot_event = next((e for e in enhanced_data["events"] if e["user_type"] == "bot"), None)
    if sample_bot_event:
        print("\nSample Bot Event:")
        print(json.dumps(sample_bot_event, indent=2))
