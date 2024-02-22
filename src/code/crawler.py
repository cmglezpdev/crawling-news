from newspaper import Article
from .sumarizer import new_generatesumarize
from .new import New
from .named_entities_identifier import named_entities_searcher

class Crawler:
    """
    Process the url, extracting all necessary and interesting data from the page.
    For asegure correct data, the url must be a news url
    
    Params:
        url (str): The user of the new
        
    Properties:
        data (New): Is a New instance that represent the data extracted from the url

    """
    
    def __init__(self, url: str) -> None:
        if url is None:
            raise Exception('The url must has a value')
        
        self._article = Article(url)
            
            
    def process_page(self) -> None:
        self._article.download()
        self._article.parse()
        self._data = New(
            url=self._article.url,
            title=self._article.title,
            top_image=self._article.top_image,
            authors=self._article.authors,
            publish_date=self._article.publish_date,
            content=self._article.text,
            description=self._article.meta_description,
            summary=new_generatesumarize(self._article.text),
            named_entities=named_entities_searcher(self._article.text)
        )
        
    @property
    def data(self) -> New:
        if self._data:
            return self._data
        
        self.process_page()
        return self._data
                 
