from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    def add_url(self, url, content):
        pass

    @abstractmethod
    def get_url(self, url):
        pass

    @abstractmethod
    def list_urls(self):
        pass
