from .static import StaticCrawler
from enum import Enum

class CrawlerType(Enum):
    STATIC = "static"
    DYNAMIC = "dynamic"

class CrawlerFactory:
    @staticmethod
    def create_crawler(crawler_type: CrawlerType, website_url: str, *args, **kwargs):
        if crawler_type == CrawlerType.STATIC:
            return StaticCrawler(website_url, *args, **kwargs)
        else:
            raise NotImplementedError("This crawler is not implemented.")
