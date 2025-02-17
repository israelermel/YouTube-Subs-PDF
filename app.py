from flask import Flask, request, render_template, send_file, after_this_request
import zipfile
import os
import logging
from web.LoggerConfig import LoggerConfig
from web.YouTubeCrawler import YouTubeCrawler
from web.YouTubeSubtitleToPDF import YouTubeSubtitleToPDF
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize logging configuration
LoggerConfig()

# Directory to store the zip files
ZIP_DIR = 'zips'

# Ensure the directory exists
os.makedirs(ZIP_DIR, exist_ok=True)


def get_unique_zip_filename(base_name='subtitles'):
    index = 1
    while True:
        zip_filename = os.path.join(ZIP_DIR, f'{base_name}_{index}.zip')
        if not os.path.exists(zip_filename):
            return zip_filename
        index += 1


def create_pdf_files(video_ids, languages):
    converter = YouTubeSubtitleToPDF()
    pdf_filenames = []

    for video_id in video_ids:
        output_filename = f'{video_id}.pdf'.replace('_', '')
        logging.debug(f'Creating PDF for video ID: {video_id}')
        converter.fetch_and_create_pdf(video_id=video_id, languages=languages, output_filename=output_filename)
        if os.path.exists(f'data/{output_filename}'):
            pdf_filenames.append(f'data/{output_filename}')
        else:
            logging.error(f'Failed to create PDF for video ID: {video_id}')

    return pdf_filenames

def create_zip_file(pdf_filenames):
    zip_filename = get_unique_zip_filename()
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for pdf_filename in pdf_filenames:
            zipf.write(pdf_filename, os.path.basename(pdf_filename))
            os.remove(pdf_filename)  # Remove the PDF file after adding it to the zip
    return zip_filename


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        logging.debug(f'Request form data: {request.form}')
        content_type = request.form.get('content_type')
        content_id = request.form.get('content_id')
        language = request.form.get('language')

        if not content_type or not content_id or not language:
            return 'Bad Request: Missing form data', 400

        languages = [language]

        if content_type == 'playlist':
            logging.debug(f'Fetching video IDs for playlist: {content_id}')
            crawler = YouTubeCrawler(content_id, content_type)
            video_ids = crawler.get_video_ids()
            logging.debug(f'Fetched video IDs: {video_ids}')
        else:
            logging.debug(f'Using single video ID: {content_id}')
            video_ids = [content_id]
            logging.debug(f'Video IDs: {video_ids}')

        logging.debug(f'Creating PDFs for video IDs: {video_ids} with languages: {languages}')
        pdf_filenames = create_pdf_files(video_ids, languages)
        logging.debug(f'PDFs created: {pdf_filenames}')

        if not pdf_filenames:
            return 'No PDFs were created. Please check the logs for more details.'

        logging.debug('Creating zip file')
        zip_filename = create_zip_file(pdf_filenames)
        logging.debug(f'Zip file created: {zip_filename}')

        # Return the zip file for download
        return send_file(zip_filename, as_attachment=True)

    return render_template('index.html')


@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(ZIP_DIR, filename)

    @after_this_request
    def remove_file(response):
        try:
            os.remove(file_path)
        except Exception as error:
            logging.error(f'Error removing file: {error}')
        return response

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)