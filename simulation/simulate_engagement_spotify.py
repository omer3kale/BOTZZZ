import random
import json
import time
from datetime import datetime, timedelta

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

# Spotify engagement probabilities
REAL_PLAY_PROB = 0.3
BOT_PLAY_PROB = 0.8
REAL_LIKE_PROB = 0.05
BOT_LIKE_PROB = 0.4
REAL_PLAYLIST_ADD_PROB = 0.02
BOT_PLAYLIST_ADD_PROB = 0.25
REAL_FOLLOW_PROB = 0.01
BOT_FOLLOW_PROB = 0.3

# Economic factors for Spotify
SPOTIFY_PAY_PER_STREAM = 0.003  # $0.003 per stream (average)
PREMIUM_USER_RATIO = 0.45  # 45% of users are premium
BOT_PREMIUM_RATIO = 0.8  # Bots often use premium accounts to avoid ads

# Generate artists and tracks
artists = [f"artist_{i}" for i in range(NUM_ARTISTS)]
tracks = []

# Mockup Spotify track details
for i in range(NUM_TRACKS):
    track = {
        "track_id": f"sp_{i:06d}",
        "artist": artists[i % NUM_ARTISTS],
        "title": f"Track {i}",
        "album": f"Album {i // 3}",  # Multiple tracks per album
        "genre": random.choice(["Pop", "Rock", "Hip-Hop", "Electronic", "Jazz", "Classical", "Country", "R&B"]),
        "duration_ms": random.randint(120000, 360000),  # 2-6 minutes
        "release_date": f"2025-{random.randint(1, 7):02d}-{random.randint(1, 31):02d}",
        "popularity_score": random.randint(1, 100),
        "explicit": random.choice([True, False]),
        "streams": random.randint(1000, 10000000),
        "monthly_listeners": random.randint(500, 5000000)
    }
    tracks.append(track)

# Simulate users
real_users = []
for i in range(NUM_REAL_USERS):
    user = {
        "user_id": f"user_{i}",
        "subscription": "premium" if random.random() < PREMIUM_USER_RATIO else "free",
        "country": random.choice(["US", "DE", "UK", "FR", "ES", "IT", "CA", "AU", "NL", "SE"]),
        "age_group": random.choice(["13-17", "18-24", "25-34", "35-44", "45-54", "55+"]),
        "listening_hours_per_day": random.uniform(0.5, 8.0)
    }
    real_users.append(user)

bots = []
for i in range(NUM_BOTS):
    bot = {
        "bot_id": f"bot_{i}",
        "subscription": "premium" if random.random() < BOT_PREMIUM_RATIO else "free",
        "country": random.choice(["US", "DE", "UK", "FR", "ES"]),  # Bots often in major markets
        "streaming_pattern": random.choice(["aggressive", "moderate", "stealth"]),
        "target_artists": random.sample(artists, random.randint(1, 5)),
        "streams_per_hour": random.randint(50, 500)
    }
    bots.append(bot)

# Mockup device/platform profiles
device_profiles = [
    {"platform": "mobile_android", "user_agent": "Spotify/8.7.0 Android/11"},
    {"platform": "mobile_ios", "user_agent": "Spotify/8.7.0 iOS/15.0"},
    {"platform": "desktop_windows", "user_agent": "Spotify/1.1.84 Windows/10"},
    {"platform": "desktop_mac", "user_agent": "Spotify/1.1.84 Darwin/21.0"},
    {"platform": "web_player", "user_agent": "Mozilla/5.0 Spotify Web Player"},
    {"platform": "smart_speaker", "user_agent": "Spotify Connect"},
]

# Engagement log
engagement_log = []
economic_log = []

print("Starting Spotify bot simulation...")

for step in range(SIMULATION_STEPS):
    # Real users behavior
    for user in real_users:
        # Users don't engage with every track every step
        active_tracks = random.sample(tracks, random.randint(1, min(10, len(tracks))))
        
        for track in active_tracks:
            # Stream probability
            if random.random() < REAL_PLAY_PROB:
                # Simulate realistic listening duration
                listen_duration = random.randint(30000, track["duration_ms"])  # At least 30 seconds
                is_complete_play = listen_duration >= (track["duration_ms"] * 0.8)  # 80% completion
                
                engagement_log.append({
                    "timestamp": datetime.now().isoformat(),
                    "step": step,
                    "user": user["user_id"],
                    "user_type": "real",
                    "action": "stream",
                    "track_id": track["track_id"],
                    "artist": track["artist"],
                    "title": track["title"],
                    "album": track["album"],
                    "genre": track["genre"],
                    "duration_ms": track["duration_ms"],
                    "listen_duration_ms": listen_duration,
                    "completion_rate": listen_duration / track["duration_ms"],
                    "is_complete_play": is_complete_play,
                    "user_subscription": user["subscription"],
                    "user_country": user["country"],
                    "platform": random.choice(device_profiles)["platform"]
                })
                
                # Economic calculation for real streams
                if is_complete_play:  # Only complete plays generate revenue
                    revenue = SPOTIFY_PAY_PER_STREAM
                    if user["subscription"] == "premium":
                        revenue *= 1.5  # Premium streams pay more
                    
                    economic_log.append({
                        "timestamp": datetime.now().isoformat(),
                        "step": step,
                        "track_id": track["track_id"],
                        "artist": track["artist"],
                        "user_type": "real",
                        "revenue_generated": revenue,
                        "subscription_type": user["subscription"],
                        "country": user["country"]
                    })
            
            # Like probability
            if random.random() < REAL_LIKE_PROB:
                engagement_log.append({
                    "timestamp": datetime.now().isoformat(),
                    "step": step,
                    "user": user["user_id"],
                    "user_type": "real",
                    "action": "like",
                    "track_id": track["track_id"],
                    "artist": track["artist"],
                    "title": track["title"],
                    "user_subscription": user["subscription"],
                    "user_country": user["country"]
                })
            
            # Playlist add probability
            if random.random() < REAL_PLAYLIST_ADD_PROB:
                engagement_log.append({
                    "timestamp": datetime.now().isoformat(),
                    "step": step,
                    "user": user["user_id"],
                    "user_type": "real",
                    "action": "playlist_add",
                    "track_id": track["track_id"],
                    "artist": track["artist"],
                    "title": track["title"],
                    "playlist_name": f"My Playlist {random.randint(1, 5)}",
                    "user_subscription": user["subscription"]
                })

    # Bot behavior
    for bot in bots:
        device_profile = random.choice(device_profiles)
        
        # Bots focus on their target artists
        target_tracks = [t for t in tracks if t["artist"] in bot["target_artists"]]
        if not target_tracks:
            target_tracks = random.sample(tracks, min(5, len(tracks)))
        
        # Aggressive streaming pattern
        streams_this_step = random.randint(1, 20) if bot["streaming_pattern"] == "aggressive" else random.randint(1, 5)
        
        for _ in range(streams_this_step):
            track = random.choice(target_tracks)
            
            # Bots have high streaming probability
            if random.random() < BOT_PLAY_PROB:
                # Bot listening patterns (often shorter or artificial)
                if bot["streaming_pattern"] == "stealth":
                    # Stealth bots try to mimic real behavior
                    listen_duration = random.randint(30000, track["duration_ms"])
                else:
                    # Aggressive bots might have shorter listening times
                    listen_duration = random.randint(30000, min(120000, track["duration_ms"]))
                
                is_complete_play = listen_duration >= 30000  # Spotify's 30-second rule
                
                engagement_log.append({
                    "timestamp": datetime.now().isoformat(),
                    "step": step,
                    "user": bot["bot_id"],
                    "user_type": "bot",
                    "action": "stream",
                    "track_id": track["track_id"],
                    "artist": track["artist"],
                    "title": track["title"],
                    "album": track["album"],
                    "genre": track["genre"],
                    "duration_ms": track["duration_ms"],
                    "listen_duration_ms": listen_duration,
                    "completion_rate": listen_duration / track["duration_ms"],
                    "is_complete_play": is_complete_play,
                    "bot_subscription": bot["subscription"],
                    "bot_country": bot["country"],
                    "bot_pattern": bot["streaming_pattern"],
                    "platform": device_profile["platform"],
                    "user_agent": device_profile.get("user_agent", "")
                })
                
                # Economic calculation for bot streams
                if is_complete_play:
                    revenue = SPOTIFY_PAY_PER_STREAM
                    if bot["subscription"] == "premium":
                        revenue *= 1.5
                    
                    economic_log.append({
                        "timestamp": datetime.now().isoformat(),
                        "step": step,
                        "track_id": track["track_id"],
                        "artist": track["artist"],
                        "user_type": "bot",
                        "revenue_generated": revenue,
                        "subscription_type": bot["subscription"],
                        "country": bot["country"],
                        "bot_pattern": bot["streaming_pattern"]
                    })
            
            # Bot likes (high probability)
            if random.random() < BOT_LIKE_PROB:
                engagement_log.append({
                    "timestamp": datetime.now().isoformat(),
                    "step": step,
                    "user": bot["bot_id"],
                    "user_type": "bot",
                    "action": "like",
                    "track_id": track["track_id"],
                    "artist": track["artist"],
                    "title": track["title"],
                    "bot_subscription": bot["subscription"],
                    "bot_pattern": bot["streaming_pattern"]
                })
            
            # Random delay to avoid detection
            if random.random() < 0.1:
                time.sleep(random.uniform(0.1, 1.0))

# Calculate economic impact summary
total_real_revenue = sum(entry["revenue_generated"] for entry in economic_log if entry["user_type"] == "real")
total_bot_revenue = sum(entry["revenue_generated"] for entry in economic_log if entry["user_type"] == "bot")
total_real_streams = len([entry for entry in engagement_log if entry["user_type"] == "real" and entry["action"] == "stream" and entry.get("is_complete_play", False)])
total_bot_streams = len([entry for entry in engagement_log if entry["user_type"] == "bot" and entry["action"] == "stream" and entry.get("is_complete_play", False)])

economic_summary = {
    "simulation_parameters": {
        "real_users": NUM_REAL_USERS,
        "bots": NUM_BOTS,
        "tracks": NUM_TRACKS,
        "steps": SIMULATION_STEPS
    },
    "revenue_analysis": {
        "total_real_revenue": round(total_real_revenue, 4),
        "total_bot_revenue": round(total_bot_revenue, 4),
        "bot_revenue_percentage": round((total_bot_revenue / (total_real_revenue + total_bot_revenue)) * 100, 2) if (total_real_revenue + total_bot_revenue) > 0 else 0,
        "revenue_per_real_stream": round(total_real_revenue / total_real_streams, 4) if total_real_streams > 0 else 0,
        "revenue_per_bot_stream": round(total_bot_revenue / total_bot_streams, 4) if total_bot_streams > 0 else 0
    },
    "stream_analysis": {
        "total_real_streams": total_real_streams,
        "total_bot_streams": total_bot_streams,
        "bot_stream_percentage": round((total_bot_streams / (total_real_streams + total_bot_streams)) * 100, 2) if (total_real_streams + total_bot_streams) > 0 else 0
    }
}

# Create data directory if it doesn't exist
import os
os.makedirs("../data", exist_ok=True)

# Save engagement log
with open("../data/spotify_engagement_log.json", "w") as f:
    json.dump(engagement_log, f, indent=2)

# Save economic analysis
with open("../data/spotify_economic_log.json", "w") as f:
    json.dump(economic_log, f, indent=2)

# Save economic summary
with open("../data/spotify_economic_summary.json", "w") as f:
    json.dump(economic_summary, f, indent=2)

print(f"Spotify simulation complete!")
print(f"Total engagement events logged: {len(engagement_log)}")
print(f"Total economic events logged: {len(economic_log)}")
print(f"Bot revenue percentage: {economic_summary['revenue_analysis']['bot_revenue_percentage']}%")
print(f"Bot stream percentage: {economic_summary['stream_analysis']['bot_stream_percentage']}%")

if __name__ == "__main__":
    # Example: scale up by 5x for large-scale simulation
    scale_parameters(scale_factor=5)
