from .base import Crawler

class StaticCrawler(Crawler):
    """
    Implementation of a simple crawler for static HTML using
    requests and BeautifulSoup.
    """
    def extract_content(
        self,
    ):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content)
        return soup.get_text()
