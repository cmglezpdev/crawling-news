from crawler import Crawler
from new import New
import gensim
import spacy
import json
import pandas as pd

nlp = spacy.load('en_core_web_sm')
tfidf_model: gensim.models.TfidfModel = gensim.models.TfidfModel.load("../model/tfidf_model")

dictionary: gensim.corpora.Dictionary = gensim.corpora.Dictionary.load("../model/dictionary")

docs_vec_repr:list[list[tuple]] = []
with open("../model/docs_vec_repr.json", "r") as f:
    docs_vec_repr:list[list[tuple]] = json.loads(f.read())

documents:list[New] = []
cnn_data_df = pd.read_csv('../data/cnn_news.csv')

for _, row in cnn_data_df.head(200).iterrows():
    documents.append(New(
        url=row['Url'],
        title=row['Headline'],
        authors=row['Author'],
        content=row['Article text'],
        publish_date=row['Date published'],
        description=row['Description'],
        top_image='',
        summary=row['Description']
    ))



def process_query(url: str) -> tuple[New, list[tuple[New, float]]]:
    if not url:
        return
    
    crawl = Crawler(url)
    crawl.process_page()
    
    query = crawl.data.content
    print("Tokenizando los documentos...")
    tokenized = [token for token in nlp(query)]
    tokenized = [token for token in tokenized if token.is_alpha and not token.is_stop]
    print('Hallando la representacion del vector...')
    query_bow = dictionary.doc2bow([token.lemma_ for token in tokenized])    
    query_vector = tfidf_model[query_bow]
    
    print('Calculando la distancia coseno con el resto de los documentos...')
    cosine_distance = [
        (index, gensim.matutils.cossim(query_vector, vector)) for index, vector in enumerate(docs_vec_repr)
    ]
    print('Tomando los 10 documentos mas similares...')
    sorted_cosine_distance = sorted(cosine_distance, key=lambda x: x[1], reverse=True)
    filtered_docs = list(filter(lambda x: x[1] > 0, sorted_cosine_distance[:10]))
    news = [(
        New(
            url=documents[doc[0]].url,
            title=documents[doc[0]].title,
            authors=documents[doc[0]].authors,
            content=documents[doc[0]].content,
            publish_date=documents[doc[0]].publish_date,
            description=documents[doc[0]].description,
            top_image='',
            summary=documents[doc[0]].description
        ), doc[1]) for doc in filtered_docs]

    return (
        crawl.data, # new of the url 
        news # the most similary news
    )
