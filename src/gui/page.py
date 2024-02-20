import streamlit as st
import pandas as pd
import gensim
import spacy
import json

if "query" not in st.session_state:
    st.session_state['query'] = ""

if "docs_showed" not in st.session_state:
    st.session_state['docs_showed'] = []

if "tfidf_model" not in st.session_state:
    st.session_state['tfidf_model'] = gensim.models.TfidfModel.load("model/tfidf_model")

if "dictionary" not in st.session_state:
    st.session_state['dictionary'] = gensim.corpora.Dictionary.load("model/dictionary")

if "docs_vec_repr" not in st.session_state:
    with open("model/docs_vec_repr.json", "r") as f:
        st.session_state['docs_vec_repr'] = json.loads(f.read())

if "documents" not in st.session_state:
    st.session_state['documents'] = []
    df = pd.read_csv('data/cnn_news.csv')
    
    for _, row in df.head(200).iterrows():
        st.session_state['documents'].append({
            'title': row['Headline'],
            'author': row['Author'],
            'url': row['Url'],
            'content': row['Article text'],
            'date': row['Date published'],
            'description': row['Description']
        })

nlp = spacy.load('en_core_web_sm')
tfidf_model: gensim.models.TfidfModel = st.session_state.tfidf_model
dictionary: gensim.corpora.Dictionary = st.session_state.dictionary
docs_vec_repr:list[list[tuple]] = st.session_state.docs_vec_repr
documents:list[dict] = st.session_state.documents


st.write(
"""
# Check news from different sources 
"""
)



@st.cache_data
def process_query(query: str):
    st.write("Haz escrito: ", query)
    if not query:
        return

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
    print(sorted_cosine_distance)
    return list(filter(lambda x: x[1] > 0, sorted_cosine_distance[:10]))
    
    
    
    
    


st.text_input("Input a query", placeholder="Type here...", key="query")

if st.session_state.query:
    print("Procesando la consulta...")
    docs = process_query(st.session_state.query)
    
    if len(docs) > 0:
        for doc in docs:
            st.caption(f"Document Relevance: {round(doc[1], 4)}")
            st.markdown(f"""
                ##### [{documents[doc[0]]['title']}]({documents[doc[0]]['url']})
                **{documents[doc[0]]['author']}** | {documents[doc[0]]['date']}
                
                {documents[doc[0]]['description']}
            """)
            st.write("\n\n\n")
            st.divider()
    else:
        st.image('not-found.jpeg', use_column_width=True)