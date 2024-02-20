from newspaper import Article
import sumarizer

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
    _summary(str): Short summary of the new's content
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
        self._summary = None
        
    def download(self):
        self._article.download()
        self._article.parse()
        self._html = self._article.html
        self._title = self._article.title
        self._top_image = self._article.top_image
        self._authors = self._article.authors
        self._publish_date = self._article.publish_date
        self._content = self._article.text
        self._description = self._article.meta_description
        self._summary  = sumarizer.new_generatesumarize(self._content)
        
    @property
    def title(self):
        return self._title
        
    @property
    def top_image(self):
        return self._top_image
    
    @property
    def authors(self):
        return self._authors
        
    @property
    def publish_date(self):
        return self._publish_date
        
    @property
    def content(self):
        return self._content
        
    @property
    def description(self):
        return self._description

    @property
    def summary(self):
        return self._summary
    
    
# crawl = Crawler('https://www.bbc.com/news/business-68254587')
# crawl.download()

# print(crawl.title)
# print(crawl.authors)
# print(crawl.publish_date)
# print(crawl.content)
# print(crawl.top_image)
# print(crawl.description)
# print(crawl.summary)