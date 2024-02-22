
class New:
    """
    The class that represent a new 
    
    Params:
        url(str):  New's url
        title(str): New's title
        top_image(str): Principal image
        authors(list[str]): New's authors
        publish_date(str): New's publish date
        content(str): New's content
        description(str): New's description
        summary(str): Short summary of the new's content
    """
    
    def __init__(self, url: str, title: str, 
                 top_image: str, authors: str, 
                 publish_date: str, content: str, 
                 description: str, summary: str,
                 named_entities: list[tuple[str, str]] = []) -> None:
        
        self._url = url
        self._title = title
        self._top_image = top_image
        self._authors = authors
        self._publish_date = publish_date
        self._content = content
        self._description = description
        self._summary = summary
        self._named_entities = named_entities
   
    @property
    def url(self):
        return self._url
   
    @property
    def title(self):
        return self._title
    
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
    
    @property
    def named_entities(self):
        return self._named_entities
