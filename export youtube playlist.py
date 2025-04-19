from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi
import argparse


class YouTubePlaylistTranscriptDownloader:
    def __init__(self, playlist_url, output_file, markdown_links=False):
        self.playlist_url = playlist_url
        self.output_file = output_file
        self.markdown_links = markdown_links
        self.ydl_opts = {
            "quiet": True,
            "extract_flat": "in_playlist",
        }

    def fetch_playlist_info(self):
        """Fetch playlist information using yt-dlp."""
        with YoutubeDL(self.ydl_opts) as ydl:
            return ydl.extract_info(self.playlist_url, download=False)

    def fetch_transcript(self, video_id):
        """Fetch transcript for a given video ID."""
        try:
            return YouTubeTranscriptApi.get_transcript(video_id)
        except Exception as e:
            print(f"Could not retrieve transcript for video ID '{video_id}': {e}")
            return None

    def write_transcript(self, file, video_title, transcript):
        """Write the transcript to the output file."""
        file.write(f"\nTitle: {video_title}\n")
        file.write("=" * 50 + "\n")
        if transcript:
            for line in transcript:
                file.write(f"{line['text']}\n")
        else:
            file.write("Transcript not available.\n")
        file.write("\n" + "=" * 50 + "\n\n")

    def process_playlist(self):
        """Process the playlist and save transcripts to the output file."""
        playlist_info = self.fetch_playlist_info()
        print("\nProcessing Playlist:\n" + "=" * 50)
        with open(self.output_file, "w", encoding="utf-8") as file:
            for index, video in enumerate(playlist_info["entries"], start=1):
                video_id = video["id"]
                video_title = video.get("title", "Unknown Title")
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                if self.markdown_links:
                    print(f"[{video_title}]({video_url})")
                else:
                    print(f"{index}. {video_title}")
                transcript = self.fetch_transcript(video_id)
                self.write_transcript(file, video_title, transcript)
        print("\n" + "=" * 50 + f"\nAll transcripts saved to '{self.output_file}'\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download YouTube playlist transcripts."
    )
    parser.add_argument(
        "playlist_url",
        help="URL of the YouTube playlist",
        nargs="?",
        default="https://www.youtube.com/playlist?list=PLyqSpQzTE6M8Pp2Z8kOAVyoSbw1UOPWQY",
    )
    parser.add_argument(
        "output_file",
        help="File to save the transcripts",
        nargs="?",
        default="transcripts.txt",
    )
    parser.add_argument(
        "--markdown-links",
        action="store_true",
        help="Print video titles with links in markdown format",
    )

    args = parser.parse_args()

    downloader = YouTubePlaylistTranscriptDownloader(
        args.playlist_url, args.output_file, markdown_links=args.markdown_links
    )
    downloader.process_playlist()
