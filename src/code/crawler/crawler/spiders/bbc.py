from typing import Any, Iterable
import scrapy
import time
from scrapy import Request
from scrapy.http import Response
import json


class BBCSpider(scrapy.Spider):
    name = 'bbc'

    def start_requests(self) -> Iterable[Request]:
        urls = ['https://www.bbc.com/worklife/article/20240214-ai-recruiting-hiring-software-bias-discrimination', 'https://www.bbc.com/news']

        for url in urls:
            # wait 3 second to avoid being blocked
            time.sleep(3)
            yield scrapy.Request(url=url, meta={'playwright': True})

    def parse(self, response: Response, **kwargs: Any) -> Any:
        microdata = response.xpath('//script[@type="application/ld+json"]/text()').get()
        content = response.css('section[data-component="text-block"] p::text').getall()
        data:dir = json.loads(microdata)
        ignore_microdatas = ['WebPage']
    
        article = None
        if data['@type'] not in ignore_microdatas:
            if data['@type'] == 'ReportageNewsArticle':
                article = {
                    'url': response.url,
                    'title': data['headline'],
                    'published': data['datePublished'],
                    'description': data['description'],
                    'authors': [author['name'].replace('By ', '') for author in data['author']],
                    'images': [data['thumbnailUrl']],
                    'content': content
                }
                
            elif data['@type'] == 'NewsArticle':
                article = {
                    'url': response.url,
                    'title': data['headline'],
                    'published': data['datePublished'],
                    'description': data['description'],
                    'authors': [data['author']['name']],
                    'images': data['image'],
                    'content': content
                }
    
        if article is not None:
            yield article

        hrefs = set(response.css('a::attr(href)').getall())
        filtered = [link for link in list(hrefs) if 'http' not in link]

        for link in filtered:
            # wait 3 second to avoid being blocked
            time.sleep(3)
            yield response.follow(link, callback=self.parse)
