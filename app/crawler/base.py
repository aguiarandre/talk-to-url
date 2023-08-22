import requests
from bs4 import BeautifulSoup
from urllib import parse

class Crawler:
    def __init__(self, website_url):
        self.url = self._normalize_url(self._sanitize(website_url))

    def extract_content(self) -> str:
        "Extracts the content of the website and output it in text format."
        pass

    def _sanitize_url(website_url: str) -> None:
        """
        Sanitises URLs so as to help avoiding db injections.
        """
        return parse.quote(website_url, safe='/')

    def _normalize_url(website_url: str) -> None:
        parsed_url = urlparse(self.url)

        # Normalize the scheme and hostname to lowercase
        scheme = parsed_url.scheme.lower()
        netloc = parsed_url.netloc.lower()

        # Reconstruct the normalized URL
        normalized_url = urlunparse((scheme, netloc, parsed_url.path, parsed_url.params,
                                    parsed_url.query, parsed_url.fragment))

        return normalized_url
