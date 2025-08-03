import random
import json
import time
import numpy as np
from datetime import datetime, timedelta
import uuid

def scale_parameters(scale_factor=1):
    """Scale simulation parameters for large-scale streaming generation."""
    global NUM_ARTISTS, NUM_REAL_USERS, NUM_BOTS, NUM_TRACKS, SIMULATION_STEPS
    NUM_ARTISTS = int(NUM_ARTISTS * scale_factor)
    NUM_REAL_USERS = int(NUM_REAL_USERS * scale_factor)
    NUM_BOTS = int(NUM_BOTS * scale_factor)
    NUM_TRACKS = int(NUM_TRACKS * scale_factor)
    SIMULATION_STEPS = int(SIMULATION_STEPS * scale_factor)
    print(f"Spotify Parameters scaled by factor {scale_factor}:")
    print(f"NUM_ARTISTS: {NUM_ARTISTS}")
    print(f"NUM_REAL_USERS: {NUM_REAL_USERS}")
    print(f"NUM_BOTS: {NUM_BOTS}")
    print(f"NUM_TRACKS: {NUM_TRACKS}")
    print(f"SIMULATION_STEPS: {SIMULATION_STEPS}")

# Spotify-specific simulation parameters
NUM_ARTISTS = 10
NUM_REAL_USERS = 200
NUM_BOTS = 50
NUM_TRACKS = 25
SIMULATION_STEPS = 100

# Real Spotify bot patterns based on industry research
SPOTIFY_BOT_TYPES = {
    "stream_farm": {
        "description": "Basic stream farming operation",
        "behavior": {
            "play_duration_range": (30, 45),  # Just over Spotify's 30-second threshold
            "skip_rate": 0.95,  # Skip after minimum time
            "playlist_interaction": 0.02,
            "like_rate": 0.01,
            "follow_rate": 0.005,
            "repeat_rate": 0.8,  # High repeat streaming
            "daily_streams": (500, 2000)
        },
        "detection_signatures": {
            "minimal_play_time": True,
            "high_skip_rate": True,
            "repetitive_patterns": True,
            "no_user_interaction": True,
            "ip_clustering": True
        }
    },
    "playlist_manipulation": {
        "description": "Playlist placement and manipulation bots",
        "behavior": {
            "play_duration_range": (60, 180),  # Longer to seem natural
            "skip_rate": 0.3,
            "playlist_interaction": 0.9,  # High playlist activity
            "like_rate": 0.4,
            "follow_rate": 0.6,
            "repeat_rate": 0.2,
            "daily_streams": (100, 500)
        },
        "detection_signatures": {
            "coordinated_playlist_adds": True,
            "burst_activity_patterns": True,
            "similar_music_taste": True,
            "account_creation_timing": True
        }
    },
    "premium_farm": {
        "description": "Premium account streaming farms for higher payouts",
        "behavior": {
            "play_duration_range": (120, 300),  # Full song completion
            "skip_rate": 0.1,
            "playlist_interaction": 0.3,
            "like_rate": 0.2,
            "follow_rate": 0.1,
            "repeat_rate": 0.4,
            "daily_streams": (200, 800)
        },
        "detection_signatures": {
            "premium_account_clustering": True,
            "payment_method_patterns": True,
            "geographic_anomalies": True,
            "usage_pattern_similarities": True
        }
    },
    "sophisticated_ai": {
        "description": "AI-powered human-like streaming behavior",
        "behavior": {
            "play_duration_range": (45, 240),  # Variable listening
            "skip_rate": 0.25,  # More human-like
            "playlist_interaction": 0.15,
            "like_rate": 0.08,
            "follow_rate": 0.03,
            "repeat_rate": 0.15,
            "daily_streams": (50, 300)
        },
        "detection_signatures": {
            "ai_behavior_patterns": True,
            "consistent_randomness": True,
            "lack_of_emotional_variation": True,
            "scheduled_activity": True
        }
    }
}

# Real device profiles used by Spotify bots
REAL_SPOTIFY_BOT_DEVICES = [
    {
        "platform": "android_farm",
        "device_model": "Samsung Galaxy A10",
        "os_version": "Android 9.0",
        "app_version": "8.6.84.1119",
        "user_agent": "Spotify/8.6.84 Android/28 (Samsung SM-A105F)",
        "fingerprint_anomalies": ["identical_device_specs", "emulator_traces", "root_detection_bypass"]
    },
    {
        "platform": "ios_farm", 
        "device_model": "iPhone 8",
        "os_version": "iOS 14.8",
        "app_version": "8.6.84",
        "user_agent": "Spotify/8.6.84 iOS/14.8 (iPhone10,4)",
        "fingerprint_anomalies": ["jailbreak_indicators", "modified_system_files", "automation_frameworks"]
    },
    {
        "platform": "desktop_headless",
        "device_model": "Generic Linux",
        "os_version": "Ubuntu 20.04",
        "app_version": "1.1.84.716",
        "user_agent": "Spotify/1.1.84 Linux/5.4.0",
        "fingerprint_anomalies": ["headless_browser", "missing_audio_devices", "virtual_machine"]
    },
    {
        "platform": "residential_proxy",
        "device_model": "Windows Desktop",
        "os_version": "Windows 10",
        "app_version": "1.1.84.716", 
        "user_agent": "Spotify/1.1.84 Windows/10.0",
        "fingerprint_anomalies": ["proxy_leaks", "geolocation_mismatch", "connection_timing"]
    }
]

# Generate realistic artists with different profiles
artists = []
for i in range(NUM_ARTISTS):
    genres = ["Pop", "Hip-Hop", "Electronic", "Rock", "Jazz", "Classical", "Country", "R&B", "Indie", "Latin"]
    primary_genre = random.choice(genres)
    
    # Artist tier affects bot targeting
    artist_tier = random.choices(
        ["emerging", "mid-tier", "major"],
        weights=[50, 35, 15]  # Most artists are emerging
    )[0]
    
    if artist_tier == "emerging":
        monthly_listeners = random.randint(100, 10000)
        total_streams = random.randint(1000, 100000)
        bot_target_likelihood = 0.8  # High likelihood of being botted
    elif artist_tier == "mid-tier":
        monthly_listeners = random.randint(10000, 500000)
        total_streams = random.randint(100000, 5000000)
        bot_target_likelihood = 0.4
    else:  # major
        monthly_listeners = random.randint(500000, 50000000)
        total_streams = random.randint(5000000, 1000000000)
        bot_target_likelihood = 0.1  # Less likely to need bots
    
    artist = {
        "artist_id": f"artist_{uuid.uuid4().hex[:8]}",
        "name": f"{primary_genre}Artist{i}",
        "primary_genre": primary_genre,
        "secondary_genres": random.sample([g for g in genres if g != primary_genre], random.randint(0, 2)),
        "tier": artist_tier,
        "monthly_listeners": monthly_listeners,
        "total_streams": total_streams,
        "follower_count": random.randint(monthly_listeners // 10, monthly_listeners),
        "verified": artist_tier in ["mid-tier", "major"] and random.random() > 0.3,
        "label": random.choice(["Independent", "Major Label", "Indie Label"]) if artist_tier != "emerging" else "Independent",
        "bot_target_likelihood": bot_target_likelihood,
        "payout_per_stream": random.uniform(0.003, 0.007),  # Artist-specific rates
        "countries_popular": random.sample(["US", "UK", "DE", "FR", "ES", "BR", "MX", "CA", "AU"], random.randint(1, 5))
    }
    artists.append(artist)

# Generate realistic tracks with metadata
tracks = []
for i in range(NUM_TRACKS):
    artist = artists[i % NUM_ARTISTS]
    
    # Track characteristics based on genre
    genre_characteristics = {
        "Pop": {"duration_range": (180, 240), "energy": "high", "tempo_range": (120, 140)},
        "Hip-Hop": {"duration_range": (180, 300), "energy": "high", "tempo_range": (70, 100)},
        "Electronic": {"duration_range": (240, 480), "energy": "high", "tempo_range": (128, 140)},
        "Rock": {"duration_range": (200, 360), "energy": "high", "tempo_range": (110, 150)},
        "Jazz": {"duration_range": (300, 600), "energy": "medium", "tempo_range": (60, 120)},
        "Classical": {"duration_range": (600, 1800), "energy": "low", "tempo_range": (60, 100)}
    }
    
    char = genre_characteristics.get(artist["primary_genre"], {"duration_range": (180, 240), "energy": "medium", "tempo_range": (100, 120)})
    
    release_date = datetime.now() - timedelta(days=random.randint(1, 365))
    
    track = {
        "track_id": f"spotify:track:{uuid.uuid4().hex[:22]}",
        "artist_id": artist["artist_id"],
        "artist_name": artist["name"],
        "title": f"Track {i} - {artist['primary_genre']} Song",
        "album": f"Album {i // 3}",  # Multiple tracks per album
        "genre": artist["primary_genre"],
        "secondary_genres": artist["secondary_genres"],
        "duration_ms": random.randint(char["duration_range"][0] * 1000, char["duration_range"][1] * 1000),
        "tempo_bpm": random.randint(*char["tempo_range"]),
        "energy_level": char["energy"],
        "release_date": release_date.isoformat(),
        "isrc": f"US{random.randint(100, 999)}{random.randint(10, 99)}{random.randint(10000, 99999)}",
        "explicit": random.choice([True, False]),
        "popularity_score": random.randint(1, 100),
        "total_streams": random.randint(1000, max(1000, artist["total_streams"] // 5)),
        "countries_available": ["US", "UK", "DE", "FR", "ES", "BR", "MX", "CA", "AU", "NL", "SE"],
        "playlist_additions": random.randint(0, 10000),
        "likes": random.randint(10, 50000),
        "artist_tier": artist["tier"],
        "bot_target_probability": artist["bot_target_likelihood"]
    }
    tracks.append(track)

# Generate realistic users with listening patterns
real_users = []
for i in range(NUM_REAL_USERS):
    subscription_type = random.choices(
        ["free", "premium", "family", "student"],
        weights=[40, 35, 15, 10]
    )[0]
    
    # User demographics affect listening behavior
    demographics = random.choice([
        {"age": "13-17", "primary_genres": ["Pop", "Hip-Hop", "Electronic"], "daily_hours": random.uniform(2, 6)},
        {"age": "18-24", "primary_genres": ["Hip-Hop", "Electronic", "Indie"], "daily_hours": random.uniform(3, 8)},
        {"age": "25-34", "primary_genres": ["Pop", "Rock", "Indie"], "daily_hours": random.uniform(2, 5)},
        {"age": "35-44", "primary_genres": ["Rock", "Jazz", "Classical"], "daily_hours": random.uniform(1, 4)},
        {"age": "45+", "primary_genres": ["Jazz", "Classical", "Country"], "daily_hours": random.uniform(1, 3)}
    ])
    
    user = {
        "user_id": f"user_{uuid.uuid4().hex[:12]}",
        "subscription_type": subscription_type,
        "age_group": demographics["age"],
        "primary_genres": demographics["primary_genres"],
        "country": random.choice(["US", "DE", "UK", "FR", "ES", "BR", "MX", "CA", "AU", "NL", "SE"]),
        "language": random.choice(["en", "de", "fr", "es", "pt", "nl"]),
        "daily_listening_hours": demographics["daily_hours"],
        "device_preference": random.choice(["mobile", "desktop", "both"]),
        "playlist_count": random.randint(5, 50),
        "following_count": random.randint(10, 200),
        "account_age_days": random.randint(30, 2000),
        "premium_since": (datetime.now() - timedelta(days=random.randint(30, 800))).isoformat() if subscription_type != "free" else None,
        "listening_pattern": random.choice(["morning", "commute", "work", "evening", "night", "weekend"]),
        "discovery_behavior": random.choice(["explorer", "loyalist", "mainstream"])
    }
    real_users.append(user)

# Generate sophisticated bots with realistic patterns
bots = []
for i in range(NUM_BOTS):
    bot_type = random.choice(list(SPOTIFY_BOT_TYPES.keys()))
    bot_config = SPOTIFY_BOT_TYPES[bot_type]
    device_profile = random.choice(REAL_SPOTIFY_BOT_DEVICES)
    
    # Bot farm operation details
    farm_locations = [
        {"country": "BD", "city": "Dhaka", "cost_per_stream": 0.0005},
        {"country": "PK", "city": "Lahore", "cost_per_stream": 0.0007},
        {"country": "ID", "city": "Jakarta", "cost_per_stream": 0.0008},
        {"country": "PH", "city": "Manila", "cost_per_stream": 0.0006},
        {"country": "VN", "city": "Ho Chi Minh", "cost_per_stream": 0.0009},
        {"country": "NG", "city": "Lagos", "cost_per_stream": 0.0004},
        {"country": "IN", "city": "Mumbai", "cost_per_stream": 0.0003}
    ]
    
    farm_location = random.choice(farm_locations)
    
    # Target selection based on bot type and artist vulnerability
    vulnerable_artists = [a for a in artists if a["bot_target_likelihood"] > 0.5]
    if bot_type == "stream_farm" and vulnerable_artists:
        target_artists = random.sample(vulnerable_artists, random.randint(1, min(3, len(vulnerable_artists))))
    elif bot_type == "playlist_manipulation":
        # Target mid-tier artists for playlist manipulation
        mid_tier_artists = [a for a in artists if a["tier"] == "mid-tier"]
        if mid_tier_artists:
            target_artists = random.sample(mid_tier_artists, random.randint(1, min(2, len(mid_tier_artists))))
        else:
            target_artists = random.sample(artists, random.randint(1, min(2, len(artists))))
    else:
        target_artists = random.sample(artists, random.randint(1, min(2, len(artists))))
    
    subscription_type = "premium" if bot_type == "premium_farm" else random.choice(["free", "premium"])
    
    bot = {
        "bot_id": f"bot_{bot_type}_{uuid.uuid4().hex[:8]}",
        "bot_type": bot_type,
        "bot_description": bot_config["description"],
        "subscription_type": subscription_type,
        "farm_location": farm_location,
        "device_profile": device_profile,
        "behavior_config": bot_config["behavior"],
        "detection_signatures": bot_config["detection_signatures"],
        "target_artists": [a["artist_id"] for a in target_artists],
        "target_tracks": [],  # Will be populated based on target artists
        "daily_stream_quota": random.randint(*bot_config["behavior"]["daily_streams"]),
        "creation_date": (datetime.now() - timedelta(days=random.randint(1, 180))).isoformat(),
        "activity_schedule": random.choice([
            list(range(24)),  # 24/7 operation
            list(range(6, 22)),  # Day shift
            list(range(22, 24)) + list(range(0, 6))  # Night shift
        ]),
        "proxy_rotation_enabled": random.choice([True, False]),
        "account_warming_period": random.randint(1, 30),  # Days to appear natural
        "evasion_techniques": random.sample([
            "randomized_timing", "human_behavior_simulation", "playlist_diversification",
            "geographic_distribution", "device_fingerprint_spoofing", "session_management"
        ], random.randint(2, 4)),
        "payment_method": random.choice(["stolen_cards", "virtual_cards", "gift_cards", "cryptocurrency"]) if subscription_type == "premium" else None
    }
    
    # Populate target tracks based on target artists
    for artist_id in bot["target_artists"]:
        artist_tracks = [t for t in tracks if t["artist_id"] == artist_id]
        bot["target_tracks"].extend([t["track_id"] for t in artist_tracks])
    
    bots.append(bot)

# Engagement simulation with realistic streaming patterns
engagement_log = []
economic_log = []
detection_events = []

print("Starting realistic Spotify bot simulation...")
print(f"Bot types: {[bot['bot_type'] for bot in bots]}")

for step in range(SIMULATION_STEPS):
    current_time = datetime.now() + timedelta(hours=step * 0.5)  # 30-minute intervals
    current_hour = current_time.hour
    
    # Real user streaming behavior
    for user in real_users:
        # Activity based on listening pattern
        is_active = False
        activity_probability = 0.1  # Base probability
        
        if user["listening_pattern"] == "morning" and 6 <= current_hour <= 10:
            activity_probability = 0.7
        elif user["listening_pattern"] == "commute" and (7 <= current_hour <= 9 or 17 <= current_hour <= 19):
            activity_probability = 0.8
        elif user["listening_pattern"] == "work" and 9 <= current_hour <= 17:
            activity_probability = 0.6
        elif user["listening_pattern"] == "evening" and 18 <= current_hour <= 23:
            activity_probability = 0.8
        elif user["listening_pattern"] == "night" and (0 <= current_hour <= 2 or 22 <= current_hour <= 24):
            activity_probability = 0.5
        
        if random.random() > activity_probability:
            continue
        
        # Select tracks based on user preferences
        preferred_tracks = [t for t in tracks if t["genre"] in user["primary_genres"]]
        if not preferred_tracks:
            preferred_tracks = random.sample(tracks, min(5, len(tracks)))
        
        session_length = random.randint(1, 8)  # Songs per session
        for _ in range(session_length):
            track = random.choice(preferred_tracks)
            
            # Realistic listening behavior
            full_duration = track["duration_ms"]
            
            # Listen duration based on user engagement
            if user["discovery_behavior"] == "explorer":
                listen_duration = random.uniform(30000, full_duration)  # More exploratory
            elif user["discovery_behavior"] == "loyalist":
                listen_duration = random.uniform(full_duration * 0.7, full_duration)  # Full songs
            else:  # mainstream
                listen_duration = random.uniform(45000, full_duration * 0.8)
            
            is_complete_play = listen_duration >= 30000  # Spotify's threshold
            completion_rate = listen_duration / full_duration
            
            engagement_log.append({
                "timestamp": current_time.isoformat(),
                "step": step,
                "user": user["user_id"],
                "user_type": "real",
                "action": "stream",
                "track_id": track["track_id"],
                "artist_id": track["artist_id"],
                "artist_name": track["artist_name"],
                "title": track["title"],
                "genre": track["genre"],
                "duration_ms": full_duration,
                "listen_duration_ms": listen_duration,
                "completion_rate": completion_rate,
                "is_complete_play": is_complete_play,
                "user_subscription": user["subscription_type"],
                "user_country": user["country"],
                "user_age_group": user["age_group"],
                "platform": user["device_preference"]
            })
            
            # Revenue calculation for complete plays
            if is_complete_play:
                base_payout = 0.003  # Base rate
                if user["subscription_type"] == "premium":
                    payout = base_payout * 1.5
                elif user["subscription_type"] == "family":
                    payout = base_payout * 1.3
                elif user["subscription_type"] == "student":
                    payout = base_payout * 1.2
                else:  # free
                    payout = base_payout * 0.7
                
                economic_log.append({
                    "timestamp": current_time.isoformat(),
                    "step": step,
                    "track_id": track["track_id"],
                    "artist_id": track["artist_id"],
                    "user_type": "real",
                    "revenue_generated": payout,
                    "subscription_type": user["subscription_type"],
                    "country": user["country"],
                    "completion_rate": completion_rate
                })
            
            # Additional engagement actions
            if completion_rate > 0.8:  # Liked the song
                if random.random() < 0.1:  # 10% like rate
                    engagement_log.append({
                        "timestamp": current_time.isoformat(),
                        "step": step,
                        "user": user["user_id"],
                        "user_type": "real",
                        "action": "like",
                        "track_id": track["track_id"],
                        "artist_id": track["artist_id"],
                        "user_subscription": user["subscription_type"]
                    })
                
                if random.random() < 0.05:  # 5% playlist add rate
                    engagement_log.append({
                        "timestamp": current_time.isoformat(),
                        "step": step,
                        "user": user["user_id"],
                        "user_type": "real",
                        "action": "playlist_add",
                        "track_id": track["track_id"],
                        "artist_id": track["artist_id"],
                        "playlist_name": f"User Playlist {random.randint(1, user['playlist_count'])}"
                    })

    # Bot streaming behavior with sophisticated patterns
    for bot in bots:
        if current_hour not in bot["activity_schedule"]:
            continue
        
        # Daily quota management
        bot_streams_today = len([e for e in engagement_log 
                               if e.get("user") == bot["bot_id"] 
                               and e["timestamp"][:10] == current_time.date().isoformat()
                               and e["action"] == "stream"])
        
        if bot_streams_today >= bot["daily_stream_quota"]:
            continue
        
        bot_config = bot["behavior_config"]
        bot_type = bot["bot_type"]
        
        # Select target tracks
        if bot["target_tracks"]:
            available_tracks = [t for t in tracks if t["track_id"] in bot["target_tracks"]]
        else:
            available_tracks = tracks
        
        streams_this_session = random.randint(1, min(10, len(available_tracks)))
        
        for _ in range(streams_this_session):
            if bot_streams_today >= bot["daily_stream_quota"]:
                break
            
            track = random.choice(available_tracks)
            
            # Bot-specific listening patterns
            duration_range = bot_config["play_duration_range"]
            listen_duration = random.uniform(duration_range[0] * 1000, duration_range[1] * 1000)
            
            # Ensure minimum for payout but add bot-like patterns
            if bot_type == "stream_farm":
                # Stream farms barely meet minimum
                listen_duration = random.uniform(30100, 35000)  # Just over 30 seconds
            elif bot_type == "premium_farm":
                # Premium farms play longer for legitimacy
                listen_duration = min(listen_duration, track["duration_ms"])
            
            is_complete_play = listen_duration >= 30000
            completion_rate = listen_duration / track["duration_ms"]
            
            engagement_log.append({
                "timestamp": current_time.isoformat(),
                "step": step,
                "user": bot["bot_id"],
                "user_type": "bot",
                "bot_type": bot_type,
                "action": "stream",
                "track_id": track["track_id"],
                "artist_id": track["artist_id"],
                "artist_name": track["artist_name"],
                "title": track["title"],
                "genre": track["genre"],
                "duration_ms": track["duration_ms"],
                "listen_duration_ms": listen_duration,
                "completion_rate": completion_rate,
                "is_complete_play": is_complete_play,
                "bot_subscription": bot["subscription_type"],
                "bot_country": bot["farm_location"]["country"],
                "bot_city": bot["farm_location"]["city"],
                "device_profile": bot["device_profile"]["platform"],
                "user_agent": bot["device_profile"]["user_agent"],
                "detection_signatures": list(bot["detection_signatures"].keys()),
                "evasion_techniques": bot["evasion_techniques"]
            })
            
            bot_streams_today += 1
            
            # Revenue calculation for bot streams
            if is_complete_play:
                base_payout = 0.003
                if bot["subscription_type"] == "premium":
                    payout = base_payout * 1.5
                else:
                    payout = base_payout * 0.7
                
                economic_log.append({
                    "timestamp": current_time.isoformat(),
                    "step": step,
                    "track_id": track["track_id"],
                    "artist_id": track["artist_id"],
                    "user_type": "bot",
                    "bot_type": bot_type,
                    "revenue_generated": payout,
                    "subscription_type": bot["subscription_type"],
                    "country": bot["farm_location"]["country"],
                    "completion_rate": completion_rate,
                    "cost_per_stream": bot["farm_location"]["cost_per_stream"]
                })
            
            # Detection events based on bot behavior
            if bot_type == "stream_farm" and completion_rate < 0.2:
                detection_events.append({
                    "timestamp": current_time.isoformat(),
                    "event_type": "minimal_play_time_detected",
                    "bot_id": bot["bot_id"],
                    "track_id": track["track_id"],
                    "completion_rate": completion_rate,
                    "risk_score": random.uniform(0.8, 0.95)
                })
            
            # Bot engagement actions
            if random.random() < bot_config["like_rate"]:
                engagement_log.append({
                    "timestamp": current_time.isoformat(),
                    "step": step,
                    "user": bot["bot_id"],
                    "user_type": "bot",
                    "bot_type": bot_type,
                    "action": "like",
                    "track_id": track["track_id"],
                    "artist_id": track["artist_id"],
                    "bot_country": bot["farm_location"]["country"]
                })
            
            if random.random() < bot_config["playlist_interaction"]:
                engagement_log.append({
                    "timestamp": current_time.isoformat(),
                    "step": step,
                    "user": bot["bot_id"],
                    "user_type": "bot",
                    "bot_type": bot_type,
                    "action": "playlist_add",
                    "track_id": track["track_id"],
                    "artist_id": track["artist_id"],
                    "playlist_name": f"Bot Playlist {random.randint(1, 10)}"
                })
            
            # Add small delays for sophisticated bots
            if bot_type == "sophisticated_ai" and random.random() < 0.2:
                time.sleep(random.uniform(0.5, 2.0))

# Calculate comprehensive economic analysis
total_real_revenue = sum(e["revenue_generated"] for e in economic_log if e["user_type"] == "real")
total_bot_revenue = sum(e["revenue_generated"] for e in economic_log if e["user_type"] == "bot")
total_bot_costs = sum(e.get("cost_per_stream", 0) for e in economic_log if e["user_type"] == "bot")

real_streams = len([e for e in engagement_log if e["user_type"] == "real" and e["action"] == "stream" and e.get("is_complete_play", False)])
bot_streams = len([e for e in engagement_log if e["user_type"] == "bot" and e["action"] == "stream" and e.get("is_complete_play", False)])

economic_summary = {
    "simulation_parameters": {
        "artists": NUM_ARTISTS,
        "real_users": NUM_REAL_USERS,
        "bots": NUM_BOTS,
        "tracks": NUM_TRACKS,
        "steps": SIMULATION_STEPS
    },
    "revenue_analysis": {
        "total_real_revenue": round(total_real_revenue, 4),
        "total_bot_revenue": round(total_bot_revenue, 4),
        "total_bot_costs": round(total_bot_costs, 4),
        "bot_profit": round(total_bot_revenue - total_bot_costs, 4),
        "bot_roi": round(((total_bot_revenue - total_bot_costs) / total_bot_costs) * 100, 2) if total_bot_costs > 0 else 0,
        "bot_revenue_percentage": round((total_bot_revenue / (total_real_revenue + total_bot_revenue)) * 100, 2) if (total_real_revenue + total_bot_revenue) > 0 else 0
    },
    "stream_analysis": {
        "total_real_streams": real_streams,
        "total_bot_streams": bot_streams,
        "bot_stream_percentage": round((bot_streams / (real_streams + bot_streams)) * 100, 2) if (real_streams + bot_streams) > 0 else 0
    },
    "detection_analysis": {
        "total_detection_events": len(detection_events),
        "detection_rate": round((len(detection_events) / bot_streams) * 100, 2) if bot_streams > 0 else 0,
        "most_detected_bot_type": max([e.get("bot_type", "") for e in engagement_log if e.get("user_type") == "bot"], key=lambda x: [e.get("bot_type") for e in detection_events].count(x)) if detection_events else None
    }
}

# Create comprehensive realistic dataset
realistic_data = {
    "metadata": {
        "simulation_type": "realistic_spotify_bot_behavior",
        "timestamp": datetime.now().isoformat(),
        "description": "Sophisticated Spotify bot simulation with real-world behavior patterns",
        "bot_types_simulated": list(SPOTIFY_BOT_TYPES.keys()),
        "detection_events": len(detection_events)
    },
    "artists": artists,
    "tracks": tracks,
    "real_users": real_users,
    "bots": bots,
    "engagement_log": engagement_log,
    "economic_log": economic_log,
    "detection_events": detection_events,
    "economic_summary": economic_summary
}

# Save comprehensive realistic data
import os
os.makedirs("../data", exist_ok=True)

with open("../data/spotify_realistic_simulation.json", "w") as f:
    json.dump(realistic_data, f, indent=2)

with open("../data/spotify_engagement_log_realistic.json", "w") as f:
    json.dump(engagement_log, f, indent=2)

with open("../data/spotify_economic_log_realistic.json", "w") as f:
    json.dump(economic_log, f, indent=2)

with open("../data/spotify_detection_events.json", "w") as f:
    json.dump(detection_events, f, indent=2)

print(f"Realistic Spotify simulation complete!")
print(f"Total engagement events: {len(engagement_log)}")
print(f"Real user streams: {real_streams}")
print(f"Bot streams: {bot_streams}")
print(f"Bot stream percentage: {economic_summary['stream_analysis']['bot_stream_percentage']}%")
print(f"Bot revenue percentage: {economic_summary['revenue_analysis']['bot_revenue_percentage']}%")
print(f"Bot ROI: {economic_summary['revenue_analysis']['bot_roi']}%")
print(f"Detection events: {len(detection_events)}")
print(f"Detection rate: {economic_summary['detection_analysis']['detection_rate']}%")

# Display bot type distribution and economics
bot_type_analysis = {}
for bot in bots:
    bot_type = bot["bot_type"]
    if bot_type not in bot_type_analysis:
        bot_type_analysis[bot_type] = {"count": 0, "streams": 0, "revenue": 0, "costs": 0}
    
    bot_type_analysis[bot_type]["count"] += 1
    bot_type_analysis[bot_type]["streams"] += len([e for e in engagement_log 
                                                  if e.get("user") == bot["bot_id"] 
                                                  and e["action"] == "stream"])
    bot_type_analysis[bot_type]["revenue"] += sum([e["revenue_generated"] for e in economic_log 
                                                  if e.get("user_type") == "bot" 
                                                  and e.get("bot_type") == bot_type])
    bot_type_analysis[bot_type]["costs"] += sum([e.get("cost_per_stream", 0) for e in economic_log 
                                                if e.get("user_type") == "bot" 
                                                and e.get("bot_type") == bot_type])

print(f"\nBot Type Analysis:")
for bot_type, analysis in bot_type_analysis.items():
    profit = analysis["revenue"] - analysis["costs"]
    roi = (profit / analysis["costs"] * 100) if analysis["costs"] > 0 else 0
    print(f"  {bot_type}:")
    print(f"    Count: {analysis['count']} bots")
    print(f"    Streams: {analysis['streams']}")
    print(f"    Revenue: ${analysis['revenue']:.4f}")
    print(f"    Costs: ${analysis['costs']:.4f}")
    print(f"    Profit: ${profit:.4f}")
    print(f"    ROI: {roi:.1f}%")

if __name__ == "__main__":
    # Example: scale up by 5x for large-scale simulation
    scale_parameters(scale_factor=5)
