from .base import Crawler
import requests
from bs4 import BeautifulSoup

class StaticCrawler(Crawler):
    """
    Implementation of a simple crawler for static HTML using
    requests and BeautifulSoup.
    """
    def extract_content(
        self,
    ):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, features="html.parser")
        return soup.get_text()
