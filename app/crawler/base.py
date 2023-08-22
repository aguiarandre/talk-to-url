from urllib import parse

class Crawler:
    def __init__(self, website_url):

        self.url = website_url
        self._normalize_url()
        self._sanitize_url()

    def extract_content(self) -> str:
        "Extracts the content of the website and output it in text format."
        pass

    def _sanitize_url(self, ) -> None:
        """
        Sanitises URLs so as to help avoiding db injections.
        """
        # self.url = parse.quote(self.url, safe='/')

    def _normalize_url(self, ) -> None:
        parsed_url = parse.urlparse(self.url)

        # Normalize the scheme and hostname to lowercase
        scheme = parsed_url.scheme.lower()
        netloc = parsed_url.netloc.lower()

        # Reconstruct the normalized URL
        normalized_url = parse.urlunparse((scheme, netloc, parsed_url.path, parsed_url.params,
                                    parsed_url.query, parsed_url.fragment))

        self.url = normalized_url
