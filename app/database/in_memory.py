from .base import Database

class InMemoryDB(Database):
    """
    InMemoryDB is a simple implementation of a dictionary used
    to store the contents of the website URLs
    """
    def __init__(
        self,
    ):
        self.in_memory_db = {}
        self.embedding_map = {}

    def add_url(self, url, content):
        self.in_memory_db[url] = content

    def get_url(self, url):
        return self.in_memory_db.get(url)

    def list_urls(self):
        return self.in_memory_db.keys()

    def add_embeddings(self, text, embedding):
        self.embedding_map[text] = embedding

    def get_embeddings(self, text):
        return self.embedding_map.get(text)
