import os
import time
import datetime
from googleapiclient.discovery import build # type: ignore
from googleapiclient.http import MediaFileUpload# type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow# type: ignore

# Authenticate YouTube API
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
credentials = flow.run_local_server(port=0)
youtube = build("youtube", "v3", credentials=credentials)

# Video folder path
VIDEO_FOLDER = "output"
videos = sorted([f for f in os.listdir(VIDEO_FOLDER) if f.startswith("video") and f.endswith(".mp4")], 
                key=lambda x: int(x.replace("video", "").replace(".mp4", "")))  # Sort numerically

# Metadata
TITLE_TEMPLATE = "Code Crusade - Episode {}"
DESCRIPTION = """Code Crusade Shorts - Master coding in seconds! 🚀🔥
#coding #shorts #CodeCrusade"""
TAGS = ["coding", "programming", "CodeCrusade", "developer", "software", "shorts"]

# Start scheduling from tomorrow at 9 AM UTC
upload_time = datetime.datetime.utcnow() + datetime.timedelta(days=1, hours=9)

def upload_video(file_path, scheduled_time, episode_num):
    """Uploads a video with scheduling"""
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": TITLE_TEMPLATE.format(episode_num),
                "description": DESCRIPTION,
                "tags": TAGS,
                "categoryId": "28",  # Science & Technology
            },
            "status": {
                "privacyStatus": "private",  # Required for scheduling
                "publishAt": scheduled_time.isoformat() + "Z",  # UTC format
                "selfDeclaredMadeForKids": False  # Ensures correct settings
            }
        },
        media_body=media
    )

    response = request.execute()
    print(f"Uploaded {file_path}: {response['id']} - Scheduled for {scheduled_time}")

# Upload 2 videos per day until all are scheduled
for i in range(0, len(videos), 2):
    file1 = os.path.join(VIDEO_FOLDER, videos[i])
    upload_video(file1, upload_time, i + 1)

    # Schedule next video for the same day at 3 PM UTC
    upload_time += datetime.timedelta(hours=6)  

    # Check if there's another video left for today
    if i + 1 < len(videos):
        file2 = os.path.join(VIDEO_FOLDER, videos[i + 1])
        upload_video(file2, upload_time, i + 2)

    # Move to the next day at 9 AM UTC
    upload_time += datetime.timedelta(days=1, hours=-6)

    time.sleep(5)  # Avoid hitting API rate limits

print("All videos scheduled!")
