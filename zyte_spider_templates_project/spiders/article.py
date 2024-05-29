from typing import Any, Dict, Iterable

from pydantic import BaseModel
from scrapy import Request
from scrapy_poet import DummyResponse
from scrapy_spider_metadata import Args
from zyte_common_items import Article, ArticleNavigation
from zyte_spider_templates.params import (
    GeolocationParam,
    MaxRequestsParam,
    UrlParam,
)
from zyte_spider_templates.spiders.base import BaseSpider


class ArticleSpiderParams(
    MaxRequestsParam,
    GeolocationParam,
    UrlParam,
    BaseModel,
):
    pass


class ArticleSpider(Args[ArticleSpiderParams], BaseSpider):
    name = "article"
    metadata: Dict[str, Any] = {
        "title": "Articles",
        "description": "Template for spiders that extract website articles.",
    }

    def start_requests(self) -> Iterable[Request]:
        yield Request(url=self.args.url, callback=self.parse_navigation)

    def parse_navigation(
        self, response: DummyResponse, navigation: ArticleNavigation
    ) -> Iterable[Request]:
        for request in navigation.items or []:
            yield request.to_scrapy(callback=self.parse_article)
        if navigation.nextPage:
            yield navigation.nextPage.to_scrapy(callback=self.parse_navigation)
        for request in navigation.subCategories or []:
            yield request.to_scrapy(callback=self.parse_navigation)

    def parse_article(
        self, response: DummyResponse, article: Article
    ) -> Iterable[Article]:
        yield article
