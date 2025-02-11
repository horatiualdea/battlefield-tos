import os
import json
import requests
import time
from datetime import datetime
import pytz

# TikTok API Credentials
ACCESS_TOKEN = "YOUR_TIKTOK_ACCESS_TOKEN"  # Replace with your TikTok API access token
UPLOAD_ENDPOINT = "https://open-api.tiktok.com/video/upload/"
PUBLISH_ENDPOINT = "https://open-api.tiktok.com/video/publish/"

LOG_FILE = "upload_log.json"

def get_file_size(file_path):
    """Returns file size in bytes."""
    return os.path.getsize(file_path)

def save_upload_log(video_file, video_id):
    """Appends upload details to the JSON log file."""
    log_entry = {
        "video_file": os.path.basename(video_file),
        "upload_time": datetime.now(pytz.timezone("Europe/Bucharest")).strftime("%Y-%m-%d %H:%M:%S"),
        "video_id": video_id
    }

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            try:
                logs = json.load(file)
            except json.JSONDecodeError:
                logs = []
    else:
        logs = []

    logs.append(log_entry)

    with open(LOG_FILE, "w", encoding="utf-8") as file:
        json.dump(logs, file, indent=4)

def upload_video_to_tiktok(video_file, title, description):
    """Uploads a video to TikTok via the official API."""
    print(f"🚀 Uploading {video_file} to TikTok...")

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    # Step 1: Upload the video file
    with open(video_file, "rb") as file:
        files = {"video": file}
        response = requests.post(UPLOAD_ENDPOINT, headers=headers, files=files)

    if response.status_code != 200:
        print(f"❌ TikTok upload failed! Response: {response.text}")
        return False

    upload_data = response.json()
    video_id = upload_data.get("data", {}).get("video_id")

    if not video_id:
        print("❌ No video_id returned from TikTok.")
        return False

    print(f"✅ Video uploaded to TikTok, video_id: {video_id}")

    # Step 2: Publish the video with metadata
    publish_payload = {
        "video_id": video_id,
        "title": title,
        "description": description
    }

    publish_response = requests.post(PUBLISH_ENDPOINT, headers=headers, json=publish_payload)

    if publish_response.status_code != 200:
        print(f"❌ Failed to publish video. Response: {publish_response.text}")
        return False

    print(f"✅ Video published successfully on TikTok! 🎉")

    # Log the successful upload
    save_upload_log(video_file, video_id)

    return True
