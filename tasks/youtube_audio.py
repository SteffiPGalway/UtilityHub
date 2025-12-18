from pytubefix import YouTube
from pytubefix.cli import on_progress
import os

def download_youtube_video(url, output_path="downloads", filename=None):
    yt = YouTube(url, on_progress_callback=on_progress)

    # Get highest resolution video
    video_stream = yt.streams.get_highest_resolution()

    # Default filename = video title
    if filename is None:
        filename = yt.title.replace(" ", "_").replace("/", "_") + ".mp4"

    os.makedirs(output_path, exist_ok=True)
    out_file = video_stream.download(output_path=output_path, filename=filename)

    return out_file
