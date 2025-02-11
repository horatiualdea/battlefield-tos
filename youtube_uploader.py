import os
import pickle
import json
import random
from datetime import datetime
import shutil
import pytz
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from moviepy.editor import VideoFileClip

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
LOG_FILE = "upload_log.json"

def authenticate_youtube_api():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    youtube = build("youtube", "v3", credentials=creds)
    return youtube

def get_video_length(video_file):
    video = VideoFileClip(video_file)
    return video.duration

def save_upload_log(video_file, video_id):
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

def upload_video_to_youtube(video_file, title, description, tags=None):
    title = f"{title} #Shorts"
    
    video_length = get_video_length(video_file)
    if video_length > 60:
        print("❗ The video exceeds 60 seconds and won't be uploaded as a YouTube Short.")
        return False

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": "20",
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }

    youtube = authenticate_youtube_api()
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(video_file, chunksize=-1, resumable=True),
    )
    
    response = request.execute()
    print(f"✅ Video uploaded as YouTube Short! Video ID: {response['id']}")

    save_upload_log(video_file, response["id"])  # Save log

    return True
