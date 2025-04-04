import os
import time

# Set your video folder path
VIDEO_FOLDER = "output"

# Get all .mp4 files sorted by last modified time
videos = sorted(
    [f for f in os.listdir(VIDEO_FOLDER) if f.endswith(".mp4")],
    key=lambda f: os.path.getmtime(os.path.join(VIDEO_FOLDER, f))
)

# Rename files to video1.mp4, video2.mp4, ...
for index, filename in enumerate(videos, start=1):
    old_path = os.path.join(VIDEO_FOLDER, filename)
    new_filename = f"video{index}.mp4"
    new_path = os.path.join(VIDEO_FOLDER, new_filename)

    os.rename(old_path, new_path)
    print(f"Renamed: {filename} → {new_filename}")

print("All files renamed successfully!")
