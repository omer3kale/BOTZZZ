import random
import json
import time

def scale_parameters(scale_factor=1):
    """Scale simulation parameters for large-scale engagement generation."""
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
REAL_LIKE_PROB = 0.07
BOT_LIKE_PROB = 0.6
REAL_COMMENT_PROB = 0.03
BOT_COMMENT_PROB = 0.35
REAL_SHARE_PROB = 0.02
BOT_SHARE_PROB = 0.25
REAL_SAVE_PROB = 0.01
BOT_SAVE_PROB = 0.15

# Generate creators and content
creators = [f"creator_{i}" for i in range(NUM_CREATORS)]
content = [f"content_{i}" for i in range(NUM_CONTENT)]

# Mockup Instagram post details
mockup_posts = []
for i in range(NUM_CONTENT):
    post = {
        "post_id": f"ig_{i:06d}",
        "creator": creators[i % NUM_CREATORS],
        "caption": f"Instagram Post {i} caption.",
        "hashtags": [f"#insta{i}", f"#creator{(i % NUM_CREATORS)}"],
        "media_type": random.choice(["image", "video", "carousel"]),
        "upload_date": f"2025-07-{random.randint(1, 31):02d}",
        "likes": random.randint(50, 20000),
        "comments": random.randint(5, 3000),
        "shares": random.randint(1, 1000),
        "saves": random.randint(1, 5000)
    }
    mockup_posts.append(post)

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
            post_details = mockup_posts[idx]
            # Simulate Instagram engagement by real users
            if random.random() < REAL_LIKE_PROB:
                engagement_log.append({
                    "step": step,
                    "user": user,
                    "type": "real",
                    "action": "like",
                    "content": item,
                    "post_id": post_details["post_id"],
                    "creator": post_details["creator"],
                    "caption": post_details["caption"],
                    "hashtags": post_details["hashtags"],
                    "media_type": post_details["media_type"],
                    "upload_date": post_details["upload_date"]
                })
            # Simulate comments by real users
            if random.random() < REAL_COMMENT_PROB:
                engagement_log.append({
                    "step": step,
                    "user": user,
                    "type": "real",
                    "action": "comment",
                    "content": item,
                    "comment_text": f"Nice post! [{user}]",
                    "post_id": post_details["post_id"],
                    "creator": post_details["creator"],
                    "caption": post_details["caption"],
                    "hashtags": post_details["hashtags"],
                    "media_type": post_details["media_type"],
                    "upload_date": post_details["upload_date"]
                })
            # Simulate shares by real users
            if random.random() < REAL_SHARE_PROB:
                engagement_log.append({
                    "step": step,
                    "user": user,
                    "type": "real",
                    "action": "share",
                    "content": item,
                    "post_id": post_details["post_id"],
                    "creator": post_details["creator"],
                    "caption": post_details["caption"],
                    "hashtags": post_details["hashtags"],
                    "media_type": post_details["media_type"],
                    "upload_date": post_details["upload_date"]
                })
            # Simulate saves by real users
            if random.random() < REAL_SAVE_PROB:
                engagement_log.append({
                    "step": step,
                    "user": user,
                    "type": "real",
                    "action": "save",
                    "content": item,
                    "post_id": post_details["post_id"],
                    "creator": post_details["creator"],
                    "caption": post_details["caption"],
                    "hashtags": post_details["hashtags"],
                    "media_type": post_details["media_type"],
                    "upload_date": post_details["upload_date"]
                })
    for bot in bots:
        device_profile = random.choice(bot_devices)
        # Bots only engage with a random subset of content per step
        content_indices = random.sample(range(len(content)), k=random.randint(1, len(content)))
        for idx in content_indices:
            item = content[idx]
            post_details = mockup_posts[idx]
            # Random delay to simulate human-like timing
            if random.random() < 0.05:
                time.sleep(random.uniform(0.01, 0.1))
            # Simulate Instagram engagement by bots
            if random.random() < BOT_LIKE_PROB:
                engagement_log.append({
                    "step": step,
                    "user": bot,
                    "type": "bot",
                    "action": "like",
                    "content": item,
                    "post_id": post_details["post_id"],
                    "creator": post_details["creator"],
                    "caption": post_details["caption"],
                    "hashtags": post_details["hashtags"],
                    "media_type": post_details["media_type"],
                    "upload_date": post_details["upload_date"],
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
                    "comment_text": f"Great post! [{bot}]",
                    "post_id": post_details["post_id"],
                    "creator": post_details["creator"],
                    "caption": post_details["caption"],
                    "hashtags": post_details["hashtags"],
                    "media_type": post_details["media_type"],
                    "upload_date": post_details["upload_date"],
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
                    "post_id": post_details["post_id"],
                    "creator": post_details["creator"],
                    "caption": post_details["caption"],
                    "hashtags": post_details["hashtags"],
                    "media_type": post_details["media_type"],
                    "upload_date": post_details["upload_date"],
                    "device": device_profile["device"],
                    "user_agent": device_profile["user_agent"]
                })
            # Simulate saves by bots
            if random.random() < BOT_SAVE_PROB:
                engagement_log.append({
                    "step": step,
                    "user": bot,
                    "type": "bot",
                    "action": "save",
                    "content": item,
                    "post_id": post_details["post_id"],
                    "creator": post_details["creator"],
                    "caption": post_details["caption"],
                    "hashtags": post_details["hashtags"],
                    "media_type": post_details["media_type"],
                    "upload_date": post_details["upload_date"],
                    "device": device_profile["device"],
                    "user_agent": device_profile["user_agent"]
                })

# Save engagement log
with open("../data/engagement_log_instagram.json", "w") as f:
    json.dump(engagement_log, f, indent=2)

print(f"Instagram simulation complete. {len(engagement_log)} engagement events logged.")

if __name__ == "__main__":
    # Example: scale up by 10x for large-scale simulation
    scale_parameters(scale_factor=10)
