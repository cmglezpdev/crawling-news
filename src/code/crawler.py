from newspaper import Article

class Crawler:
    """
    @params
    url(str):  New's url
    html(str): Html page
    _title(str): New's title
    _top_image(str): Principal image
    _authors(list[str]): New's authors
    _publish_date(str): New's publish date
    _content(str): New's content
    _description(str): New's description
    """
    
    def __init__(self, url: str) -> None:
        if url is None:
            raise Exception('The url must has a value')
    
        self.url = url
        self._article = Article(url)
        self._title = None
        self._top_image = None
        self._authors = []
        self._publish_date = None
        self._content = None
        self._description = None
        self._html = None
        
    def download(self):
        self._article.download()
        self._article.parse()
        self._html = self._article.html
        
    @property
    def title(self):
        if self._title: 
            return self._title
        if not self._html:
            self.download()
        self._title = self._article.title
        return self._title
        
    @property
    def top_image(self):
        if self._top_image: 
            return self._top_image
        if not self._html:
            self.download()
        self._top_image = self._article.top_image
        return self._top_image
    
    @property
    def authors(self):
        if self._authors: 
            return self._authors
        if not self._html:
            self.download()    
        self._authors = self._article.authors
        return self._authors
        
    @property
    def publish_date(self):
        if self._publish_date: 
            return self._publish_date
        if not self._html:
            self.download()
        self._publish_date = self._article.publish_date
        return self._publish_date
        
    @property
    def content(self):
        if self._content: 
            return self._content
        if not self._html:
            self.download()
        self._content = self._article.text
        return self._content
        
    @property
    def description(self):
        if self._description: 
            return self._description
        if not self._html:
            self.download()
        self._description = self._article.meta_description
        return self._description

    
# crawl = Crawler('https://www.bbc.com/news/business-68254587')

# print(crawl.title)
# print(crawl.authors)
# print(crawl.publish_date)
# print(crawl.content)
# print(crawl.top_image)
# print(crawl.description)