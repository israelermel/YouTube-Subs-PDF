from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

class YouTubeSubtitleFetcher:
    def __init__(self, video_id, languages=["en"]):
        self.video_id = video_id
        self.languages = languages

    def fetch_subtitles(self):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id=self.video_id, languages=self.languages)
            return transcript
        except TranscriptsDisabled:
            print(f"Subtitles are disabled for the video {self.video_id}")
            return None

    def get_full_text(self):
        transcript = self.fetch_subtitles()
        if transcript is None:
            return ""
        return " ".join([entry['text'] for entry in transcript])