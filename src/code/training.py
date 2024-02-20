import spacy
import pandas as pd
import gensim
import json

# load spacy lagunage architecture
nlp = spacy.load("en_core_web_sm")

# load documents
df = pd.read_csv('../data/cnn_news.csv')
news = []
for _, row in df.head(200).iterrows():
    news.append({
        'title': row['Headline'],
        'author': row['Author'],
        'url': row['Url'],
        'content': row['Article text'],
        'date': row['Date published'],
    })


tokenized_docs = [] # docs tokens
lemmantized_docs = []
dictionary = {}
vocabulary = []
corpus = []
tfidf_model: gensim.models.TfidfModel = None

print("Tokenizando los documentos...")
# tokenization
tokenized_docs = [[token for token in nlp(doc['content'])] for doc in news]

print("Eliminando el ruido del los token y las stopword...")
# remove_noise and stop_words
tokenized_docs = [
    [token for token in doc if token.is_alpha and not token.is_stop] 
    for doc in tokenized_docs
]

print("Lemantizando los documentos")
# lemmatization of the documents
lemmantized_docs = [[token.lemma_ for token in doc] for doc in tokenized_docs]

print("Creando el diccionario con las frecuencias de las palabras...")
# dictionary with words frecuencies
dictionary = gensim.corpora.Dictionary(lemmantized_docs)
print("Eliminando palabras raras...")
dictionary.filter_extremes(no_below=5, no_above=0.5)
aux_filtered_lemmas = [word for _, word in dictionary.iteritems()]
tokenized_docs = [
    [token for token in doc if token.lemma_ in aux_filtered_lemmas]
    for doc in tokenized_docs
]
lemmantized_docs = [[token.lemma_ for token in doc] for doc in tokenized_docs]

print("Guardando los ids del vocabulario...")
# save the vocabulary
vocabulary = list(dictionary.token2id.keys())

print("Guardando la representacion del vector con Word on Bow...")
corpus = [dictionary.doc2bow(doc) for doc in lemmantized_docs]
print("Creando el tfidf model con el corpus...")
tfidf_model = gensim.models.TfidfModel(corpus)
print("Guardando la representación vectorial del corpus...")
vector_repr = [tfidf_model[doc] for doc in corpus]

tfidf_model.save('../model/tfidf_model')
dictionary.save('../model/dictionary')
with open('../model/docs_vec_repr.json', 'w') as f:
    f.write(json.dumps(vector_repr))
