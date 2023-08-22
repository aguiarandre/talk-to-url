from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    def add_url(self, url, content):
        "Add URL"
        pass

    @abstractmethod
    def get_url(self, url):
        "Given the URL, return its content"
        pass

    @abstractmethod
    def list_urls(self):
        "Return a list the indexed URLs"
        pass

    @abstractmethod
    def add_embeddings(self, text, embedding):
        "Add text along with its associated embedding vectors"
        pass

    @abstractmethod
    def get_embeddings(self, text):
        "Retrieve the embedding for a given text"
        pass
