import os
from web.PDFCreator import PDFCreator
from web.YouTubeSubtitleFetcher import YouTubeSubtitleFetcher


class YouTubeSubtitleToPDF:
    def __init__(self):
        pass

    def fetch_subtitles(self, video_id, languages=["pt"]):
        fetcher = YouTubeSubtitleFetcher(video_id, languages)
        return fetcher.get_full_text()

    def create_pdf(self, text, output_filename="output.pdf"):
        output_path = os.path.join("data", output_filename)
        pdf_creator = PDFCreator()
        pdf_creator.create_pdf(text, output_path)

    def fetch_and_create_pdf(self, video_id, languages=["pt"], output_filename="output.pdf"):
        subtitles_text = self.fetch_subtitles(video_id, languages)
        self.create_pdf(subtitles_text, output_filename)