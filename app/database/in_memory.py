from .base import Database


class InMemoryDB(Database):
    def __init__(
        self,
    ):
        self.in_memory_db = {}

    def add_url(self, url, content):
        self.in_memory_db[url] = content

    def get_url(self, url):
        return self.in_memory_db.get(url)

    def list_urls(self):
        return self.in_memory_db.keys()
