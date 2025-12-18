from pytubefix import YouTube
from pytubefix.cli import on_progress
import os

def download_youtube_video(url, output_path="downloads", filename=None, audio_only=False):
    """
    Download a YouTube video (or audio) using pytubefix.

    Args:
        url (str): YouTube video URL
        output_path (str): Folder to save downloads
        filename (str): Optional custom filename
        audio_only (bool): If True, download only audio

    Returns:
        str: Full path to downloaded file, or None if failed
    """
    try:
        yt = YouTube(url, on_progress_callback=on_progress)

        # Choose stream
        if audio_only:
            stream = yt.streams.filter(only_audio=True).first()
        else:
            stream = yt.streams.get_highest_resolution()

        if stream is None:
            print("No stream available for this video.")
            return None

        # Default filename
        if filename is None:
            safe_title = yt.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
            extension = "mp3" if audio_only else "mp4"
            filename = f"{safe_title}.{extension}"

        # Ensure output folder exists
        os.makedirs(output_path, exist_ok=True)

        out_file = stream.download(output_path=output_path, filename=filename)
        return out_file

    except Exception as e:
        print(f"Download failed: {str(e)}")
        return None
