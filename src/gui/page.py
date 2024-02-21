import streamlit as st
import pandas as pd
import gensim
import spacy
import json
from crawler import Crawler
from new import New

if "query" not in st.session_state:
    st.session_state['query'] = ""

if "docs_showed" not in st.session_state:
    st.session_state['docs_showed'] = []

if "tfidf_model" not in st.session_state:
    st.session_state['tfidf_model'] = gensim.models.TfidfModel.load("../model/tfidf_model")

if "dictionary" not in st.session_state:
    st.session_state['dictionary'] = gensim.corpora.Dictionary.load("../model/dictionary")

if "docs_vec_repr" not in st.session_state:
    with open("../model/docs_vec_repr.json", "r") as f:
        st.session_state['docs_vec_repr'] = json.loads(f.read())

if "documents" not in st.session_state:
    st.session_state['documents'] = []
    df = pd.read_csv('../data/cnn_news.csv')
    
    for _, row in df.head(200).iterrows():
        st.session_state['documents'].append(New(
            url=row['Url'],
            title=row['Headline'],
            authors=row['Author'],
            content=row['Article text'],
            publish_date=row['Date published'],
            description=row['Description'],
            top_image='',
            summary=row['Description']
        ))

nlp = spacy.load('en_core_web_sm')
tfidf_model: gensim.models.TfidfModel = st.session_state.tfidf_model
dictionary: gensim.corpora.Dictionary = st.session_state.dictionary
docs_vec_repr:list[list[tuple]] = st.session_state.docs_vec_repr
documents:list[New] = st.session_state.documents


st.write(
"""
# Check news from different sources 
"""
)


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


input_side, button_side = st.columns([0.8, 0.2])
with input_side:
    st.text_input("Input a new's url", placeholder="https://webnews.com/....", key="query")

with button_side:
    st.write('<style> .button-container { display: flex; flex-direction: column; align-items: center; justify-content: flex-end; height: 90%; } </style>', unsafe_allow_html=True)
    st.write('<div class="button-container">', unsafe_allow_html=True)
    st.button('Search', key="search_button")
    st.write('</div>', unsafe_allow_html=True)


if st.session_state.search_button and st.session_state.query:
    print("Procesando la consulta...")
    article, news = process_query(st.session_state.query)
    
    if len(news) > 0:        
        st.caption("#### The provided new")
        st.markdown(f"""
            ##### [{article.title}]({article.url})
            **{', '.join(article.authors)}** | {article.publish_date}
        """)
        st.write(article.summary)
        st.write("\n\n\n")
            
        st.divider()
        st.caption("#### Suggestions")
        for new, relevance in news:
            st.caption(f"RELEVANCE: {round(relevance, 4)}")
            st.markdown(f"""
                ##### [{new.title}]({new.url})
                **{new.authors}** | {new.publish_date}
                
                {new.description}
            """)
            st.write("\n\n\n")
            st.divider()
    else:
        st.image('not-found.jpeg', use_column_width=True)