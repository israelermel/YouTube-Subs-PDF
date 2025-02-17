from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from urllib.parse import urlparse, parse_qs

class YouTubeCrawler:
    def __init__(self, content_id, content_type='playlist'):
        if content_type == 'playlist':
            self.url = f'https://www.youtube.com/playlist?list={content_id}'
        else:
            self.url = f'https://www.youtube.com/watch?v={content_id}'
        self.driver = None

    def get_chrome_options(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        return chrome_options

    def setup_driver(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=self.get_chrome_options())

    def get_video_ids(self):
        self.setup_driver()
        self.driver.get(self.url)
        time.sleep(15)
        video_ids = []

        if 'playlist' in self.url:
            video_elements = self.driver.find_elements(By.CSS_SELECTOR, 'a.ytd-playlist-video-renderer')
            for video in video_elements:
                url = video.get_attribute('href')
                query = urlparse(url).query
                video_id = parse_qs(query).get('v')
                if video_id:
                    video_ids.append(video_id[0])
        else:
            video_id = parse_qs(urlparse(self.url).query).get('v')
            if video_id:
                video_ids.append(video_id[0])

        self.driver.quit()
        return video_ids