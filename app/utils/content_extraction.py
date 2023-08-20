import requests
from bs4 import BeautifulSoup


class WebsiteCrawler:
    def __init__(self, website_url):
        self.url = website_url

    def extract_content(
        self,
    ):
        response = requests.get(self.url)

        soup = BeautifulSoup(response.content)
        content = soup.get_text()
        return content
