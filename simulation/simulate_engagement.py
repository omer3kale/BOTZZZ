import random
import json
import time

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

# Engagement probabilities
REAL_LIKE_PROB = 0.05
BOT_LIKE_PROB = 0.5
REAL_COMMENT_PROB = 0.02
BOT_COMMENT_PROB = 0.3
REAL_SHARE_PROB = 0.01
BOT_SHARE_PROB = 0.2

# Generate creators and content
creators = [f"creator_{i}" for i in range(NUM_CREATORS)]
content = [f"content_{i}" for i in range(NUM_CONTENT)]

# Mockup YouTube video details
mockup_videos = []
for i in range(NUM_CONTENT):
    video = {
        "video_id": f"yt_{i:06d}",
        "creator": creators[i % NUM_CREATORS],
        "title": f"YouTube Video {i}",
        "tags": [f"tag{i}", f"creator{(i % NUM_CREATORS)}"],
        "duration_sec": random.randint(60, 3600),
        "category": random.choice(["Music", "Gaming", "Education", "Vlog", "Tech", "Comedy"]),
        "description": f"This is a mockup description for YouTube Video {i}.",
        "upload_date": f"2025-07-{random.randint(1, 31):02d}",
        "views": random.randint(1000, 1000000),
        "likes": random.randint(100, 50000),
        "dislikes": random.randint(0, 5000),
        "comments": random.randint(10, 5000)
    }
    mockup_videos.append(video)

# Simulate users
real_users = [f"user_{i}" for i in range(NUM_REAL_USERS)]
bots = [f"bot_{i}" for i in range(NUM_BOTS)]

# Mockup device/user-agent profiles for bots
bot_devices = [
    {"device": "Android", "user_agent": "Dalvik/2.1.0 (Linux; U; Android 10)"},
    {"device": "iPhone", "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"},
    {"device": "Windows", "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    {"device": "Mac", "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
]

# Engagement log
engagement_log = []

for step in range(SIMULATION_STEPS):
    for user in real_users:
        for idx, item in enumerate(content):
            video_details = mockup_videos[idx]
            # Simulate YouTube engagement by real users
            if random.random() < REAL_LIKE_PROB:
                engagement_log.append({
                    "step": step,
                    "user": user,
                    "type": "real",
                    "action": "like",
                    "content": item,
                    "video_id": video_details["video_id"],
                    "creator": video_details["creator"],
                    "title": video_details["title"],
                    "tags": video_details["tags"],
                    "duration_sec": video_details["duration_sec"],
                    "category": video_details["category"],
                    "description": video_details["description"],
                    "upload_date": video_details["upload_date"]
                })
            # Simulate views by real users
            engagement_log.append({
                "step": step,
                "user": user,
                "type": "real",
                "action": "view",
                "content": item,
                "video_id": video_details["video_id"],
                "creator": video_details["creator"],
                "title": video_details["title"],
                "tags": video_details["tags"],
                "duration_sec": video_details["duration_sec"],
                "category": video_details["category"],
                "description": video_details["description"],
                "upload_date": video_details["upload_date"]
            })
            # Simulate comments by real users
            if random.random() < REAL_COMMENT_PROB:
                engagement_log.append({
                    "step": step,
                    "user": user,
                    "type": "real",
                    "action": "comment",
                    "content": item,
                    "comment_text": f"Awesome video! [{user}]",
                    "video_id": video_details["video_id"],
                    "creator": video_details["creator"],
                    "title": video_details["title"],
                    "tags": video_details["tags"],
                    "duration_sec": video_details["duration_sec"],
                    "category": video_details["category"],
                    "description": video_details["description"],
                    "upload_date": video_details["upload_date"]
                })
            # Simulate shares by real users
            if random.random() < REAL_SHARE_PROB:
                engagement_log.append({
                    "step": step,
                    "user": user,
                    "type": "real",
                    "action": "share",
                    "content": item,
                    "video_id": video_details["video_id"],
                    "creator": video_details["creator"],
                    "title": video_details["title"],
                    "tags": video_details["tags"],
                    "duration_sec": video_details["duration_sec"],
                    "category": video_details["category"],
                    "description": video_details["description"],
                    "upload_date": video_details["upload_date"]
                })
    for bot in bots:
        device_profile = random.choice(bot_devices)
        # Bots only engage with a random subset of content per step
        content_indices = random.sample(range(len(content)), k=random.randint(1, len(content)))
        for idx in content_indices:
            item = content[idx]
            video_details = mockup_videos[idx]
            # Random delay to simulate human-like timing
            if random.random() < 0.05:
                time.sleep(random.uniform(0.01, 0.1))
            # Simulate YouTube engagement by bots
            if random.random() < BOT_LIKE_PROB:
                engagement_log.append({
                    "step": step,
                    "user": bot,
                    "type": "bot",
                    "action": "like",
                    "content": item,
                    "video_id": video_details["video_id"],
                    "creator": video_details["creator"],
                    "title": video_details["title"],
                    "tags": video_details["tags"],
                    "duration_sec": video_details["duration_sec"],
                    "category": video_details["category"],
                    "description": video_details["description"],
                    "upload_date": video_details["upload_date"],
                    "device": device_profile["device"],
                    "user_agent": device_profile["user_agent"]
                })
            # Simulate views by bots
            engagement_log.append({
                "step": step,
                "user": bot,
                "type": "bot",
                "action": "view",
                "content": item,
                "video_id": video_details["video_id"],
                "creator": video_details["creator"],
                "title": video_details["title"],
                "tags": video_details["tags"],
                "duration_sec": video_details["duration_sec"],
                "category": video_details["category"],
                "description": video_details["description"],
                "upload_date": video_details["upload_date"],
                "device": device_profile["device"],
                "user_agent": device_profile["user_agent"]
            })
            # Simulate comments by bots
            if random.random() < BOT_COMMENT_PROB:
                engagement_log.append({
                    "step": step,
                    "user": bot,
                    "type": "bot",
                    "action": "comment",
                    "content": item,
                    "comment_text": f"Great video! [{bot}]",
                    "video_id": video_details["video_id"],
                    "creator": video_details["creator"],
                    "title": video_details["title"],
                    "tags": video_details["tags"],
                    "duration_sec": video_details["duration_sec"],
                    "category": video_details["category"],
                    "description": video_details["description"],
                    "upload_date": video_details["upload_date"],
                    "device": device_profile["device"],
                    "user_agent": device_profile["user_agent"]
                })
            # Simulate shares by bots
            if random.random() < BOT_SHARE_PROB:
                engagement_log.append({
                    "step": step,
                    "user": bot,
                    "type": "bot",
                    "action": "share",
                    "content": item,
                    "video_id": video_details["video_id"],
                    "creator": video_details["creator"],
                    "title": video_details["title"],
                    "tags": video_details["tags"],
                    "duration_sec": video_details["duration_sec"],
                    "category": video_details["category"],
                    "description": video_details["description"],
                    "upload_date": video_details["upload_date"],
                    "device": device_profile["device"],
                    "user_agent": device_profile["user_agent"]
                })

# Save engagement log
with open("../data/engagement_log.json", "w") as f:
    json.dump(engagement_log, f, indent=2)

print(f"Simulation complete. {len(engagement_log)} engagement events logged.")

if __name__ == "__main__":
    # Example: scale up by 10x for large-scale simulation
    scale_parameters(scale_factor=10)
