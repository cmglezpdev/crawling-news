from typing import Any, Iterable
import scrapy
import time
from datetime import datetime
from scrapy import Request
from scrapy.http import Response
import json
import queue


class CNNSpider(scrapy.Spider):
    name = 'cnn'
    domain = 'https://www.cnn.com/'
    urls = queue.PriorityQueue()

    def start_requests(self) -> Iterable[Request]:
        self.urls.put((1, 'https://www.cnn.com/2024/02/16/politics/takeaways-donald-trump-fraud-ruling/index.html'))
    
        while self.urls.empty is False:
            _, url = self.urls.get()    
            # wait 3 second to avoid being blocked
            time.sleep(3)
            yield scrapy.Request(url=url, meta={'playwright': True})


    def parse(self, response: Response, **kwargs: Any) -> Any:
        microdata = response.xpath('//script[@type="application/ld+json"]/text()').get()
        data:dir = json.loads(microdata)
        ignore_microdatas = ['WebPage', 'CollectionPage', 'VideoObject', 'Product']
    
        article = None
        if data['@type'] not in ignore_microdatas:
            if data['@type'] == 'NewsArticle':
                article = {
                    'url': response.url,
                    'title': data['headline'],
                    'published': data['datePublished'],
                    'description': data['description'],
                    'authors': [author['name'] for author in data['author']],
                    'images': [data['thumbnailUrl']],
                    'content': data['articleBody']
                }
                
        if article is not None:
            yield article

        hrefs = set(response.css('a::attr(href)').getall())
        for link in list(hrefs):
            if self.is_external_page(link) or self.ignore_page(link):
                continue
            
            if self.is_news_page(link):
                self.urls.put((1, link))
            else:
                self.urls.put((0, link))
            
        while self.urls.empty is False:
            _, url = self.urls.get()    
            # wait 3 second to avoid being blocked
            time.sleep(3)
            yield response.follow(url, callback=self.parse)


    def is_external_page(self, url: str):
        return url.startswith('http') and url.startswith(self.domain) is False

    def is_news_page(self, url:str) -> bool:
        clear_url = url
        if url.startswith(f'{self.domain}/'):
            clear_url = clear_url.replace(self.domain, '')
        
        tokens = clear_url.split('/')
        
        if len(tokens) < 4: # year/month/day/<more...>
            return False        

        [year, month, day] = tokens
        try:
            datetime(year, month, day)
            return True
        except ValueError:
            return False
    
    def ignore_page(self, url: str):
        ignore_pages = [
            'https://www.cnn.com/interactive/', '/interactive/',
            'https://www.cnn.com/cnn-underscored/', '/cnn-underscored/',
            'https://www.cnn.com/video/', '/video/',
            'https://www.cnn.com/audio/', '/audio/',
            'https://www.cnn.com/live-tv/', '/live-tv/'
        ]
    
        for pages in ignore_pages:
            if pages.startswith(pages):
                return True
        
        return False