
# 📜 YouTube Playlist Transcript Downloader

This script allows you to download transcripts for each video in a YouTube playlist and save them into a single text file. It's particularly useful for content analysis, language learning, or archiving.

---

## 🚀 Features

- **Automatic Transcript Retrieval**: Fetches transcripts for each video in a YouTube playlist.
- **Organized Output**: Saves each video's transcript in a single text file with clear headers.
- **Error Handling**: Notifies if a video transcript isn't available.

---

## 📋 Prerequisites

Ensure you have Python 3 and the required libraries installed.

```bash
pip install yt-dlp youtube-transcript-api
```

---

## 📝 Usage

1. **Set up the Playlist URL**: Update the `playlist_url` variable in the script with the desired YouTube playlist link.
2. **Run the Script**: Execute the script to download transcripts.

```python
from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi
import os

# Set the URL of the YouTube playlist and output file name
playlist_url = 'YOUR_PLAYLIST_URL'
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
```

3. **Check the Output**: After running, find the transcript file named `playlist_transcripts.txt` in the script’s directory.

---

## 📂 Output

Each video's transcript is saved in the `playlist_transcripts.txt` file with:
- **Video Title**: Clearly marked for each section.
- **Transcript Content**: Organized with line breaks for readability.
- **Separator**: Each transcript is separated for easy navigation.

---

## 🛠 Troubleshooting

- **No Transcript Available**: Some videos may not have transcripts, or transcripts may be restricted to manually added captions.
- **Error Handling**: If an error occurs during transcript retrieval, it will be noted in the output file.

---

## 📜 License

This script is available for personal and educational use.

---

Enjoy downloading transcripts! 😄
