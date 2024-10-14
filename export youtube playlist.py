from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi
import os

# Set the URL of the YouTube playlist and output file name
playlist_url = 'Your Playlist URL'
output_file = 'playlist_transcripts.txt'

# yt-dlp options to fetch video info without downloading
ydl_opts = {
    'quiet': True,
    'extract_flat': 'in_playlist',
}

# Open output file for writing
with open(output_file, 'w', encoding='utf-8') as f:
    with YoutubeDL(ydl_opts) as ydl:
        # Extract playlist info
        playlist_info = ydl.extract_info(playlist_url, download=False)
        for video in playlist_info['entries']:
            video_id = video['id']
            video_title = video.get('title', 'Unknown Title')
            
            # Write the video title
            f.write(f"\nTitle: {video_title}\n")
            f.write("=" * 50 + "\n")

            # Fetch the transcript using YouTubeTranscriptApi
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                
                # Write each line of the transcript
                for line in transcript:
                    f.write(f"{line['text']}\n")
                
                f.write("\n" + "=" * 50 + "\n\n")
                print(f"Transcript for '{video_title}' downloaded successfully.")
            except Exception as e:
                print(f"Could not retrieve transcript for '{video_title}': {e}")
                f.write("Transcript not available.\n")
                f.write("\n" + "=" * 50 + "\n\n")

print(f"All transcripts saved to '{output_file}'")
