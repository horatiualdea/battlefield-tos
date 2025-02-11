import os
import random
import schedule
import time
import shutil
import pytz
from datetime import datetime
from youtube_uploader import upload_video_to_youtube
from tiktok_uploader import upload_video_to_tiktok

# Flags to enable/disable uploads
UPLOAD_TO_YOUTUBE = True
UPLOAD_TO_TIKTOK = False

# Define multiple sets of metadata
METADATA_OPTIONS = [
    {
        "title": "🎯 Insane Headshot Compilation! Quick Kills in BF2042",
        "description": "🔥 Some of my best Battlefield 2042 headshots in this insane compilation! Who needs a scope? 💀 #Shorts #Battlefield2042 #Gaming",
        "tags": ["#Shorts", "Battlefield 2042", "Headshot", "Gaming", "FPS", "BF2042 Highlights"]
    },
    {
        "title": "⚡ Fastest Sniper Kills Ever? Battlefield 2042 Madness!",
        "description": "💥 Quick reflexes and insane aim! These sniper kills in Battlefield 2042 are absolutely nuts. Watch till the end! #Shorts #BF2042 #FPS",
        "tags": ["#Shorts", "Battlefield 2042", "Sniper", "Epic Gaming Moments", "Quickscopes"]
    },
]

def generate_video_metadata():
    return random.choice(METADATA_OPTIONS)

def upload_daily_video():
    folder_path = "videos_to_post"
    posted_folder_path = "posted_videos"

    video_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]
    
    if not video_files:
        print("❗ No videos found in the 'videos_to_post' folder. Stopping the script.")
        return False

    video_file = os.path.join(folder_path, random.choice(video_files))
    title, description, tags = generate_video_metadata().values()

    uploaded = False

    if UPLOAD_TO_YOUTUBE:
        print("📺 Uploading to YouTube...")
        if upload_video_to_youtube(video_file, title, description, tags):
            uploaded = True

    if UPLOAD_TO_TIKTOK:
        print("🎵 Uploading to TikTok...")
        if upload_video_to_tiktok(video_file, title, description):
            uploaded = True

    if uploaded:
        posted_video_path = os.path.join(posted_folder_path, os.path.basename(video_file))
        shutil.move(video_file, posted_video_path)
        print(f"✅ Video moved to 'posted_videos' folder: {posted_video_path}")

    return uploaded

def get_best_posting_time():
    romania_tz = pytz.timezone("Europe/Bucharest")
    now = datetime.now(romania_tz)
    
    day_of_week = now.weekday()
    
    if day_of_week < 5:
        post_time = random.choice(["12:00", "18:00"])
    else:
        post_time = random.choice(["10:00", "15:00"])
    
    return post_time

def schedule_upload():
    while True:
        post_time = get_best_posting_time()
        print(f"✅ Scheduled upload for {post_time} Romanian time.")

        schedule.every().day.at(post_time).do(upload_daily_video)
        
        schedule.run_pending()
        
        if not upload_daily_video():
            break
        
        time.sleep(60)

if __name__ == "__main__":
    schedule_upload()
