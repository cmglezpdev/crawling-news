import spacy
from collections import Counter

nlp = spacy.load('en_core_web_sm') #loading the model

def tokenization(texts): #gets the corpus and separate each doc in tokens

    """
   Separate each document in tokens

    Args:
      texts ([str]):the documents to process

    Returns:
       list[Token]:A list of tokens

    Example:
        >>> texts =["Hello My name Is Crawly","Im a news Crawler"]
        >>> tokenization(texts)
        [[Hello, My, name, Is, Crawly], [I, m, a, news, Crawler]]
    """


    return [[token for token in nlp(text)] for text in texts]

def remove_noise(tokenized_docs):
    """
    Takes an tokenized ser of documents and removes the noise from it (Removes non alphabetical tokens)
    Args:
      tokenized_docs: ([[Token]]):The previously tokenized documents 

    Returns:
       list[Token]:A list of tokens with filtered noise

    Example:
        >>> tokenized_docs = [["Hello", "My", "name", "Is", "Crawly"], ["I", "m", "a", "news", "Crawler"]]

        >>> remove_noise(tokenized_doc)
        [[Hello, My, name, Is, Crawly], [I, m, a, news, Crawler]]
    """
    return [[token for token in tokenized_doc if token.is_alpha] for tokenized_doc in tokenized_docs]

def remove_stopwords(tokenized_docs):
    """
    Removes the stopwords for more clear processing and reduction of the corpus size
    Args:
      tokenized_docs:([[Token]]):an array of tokenized documents

    Returns:
       list[Token]:A list of tokens with stopwords removed

    Example:
        >>> tokenized_docs = [["Hello", "My", "name", "Is", "Crawly"], ["I", "m", "a", "news", "Crawler"]]

        >>> remove_stopwords(tokenized_doc)
        [[Hello, My, name, Is, Crawly], [I, m, a, news, Crawler]]
    """
    return [[token for token in tokens if token.text not in spacy.lang.en.stop_words.STOP_WORDS ]for tokens in tokenized_docs]

def morphological_reduction(tokenized_docs):
    """
    Makes morphological reduction using spacy lemmantization
    Args:
      tokenized_docs ([[Token]]):an array of tokenized documents

    Returns:
       list[Token]:A list of tokens which has been morphologicaly reduced

    Example:
        >>> tokenized_docs = [["Hello", "My", "name", "Is", "Crawly"], ["I", "m", "a", "news", "Crawler"]]

        >>> morphological_reduction(tokenized_doc)
            [['hello', 'my', 'namme', 'be', 'crawly'], ['I', 'm', 'new', 'crawler']]
    """
    return [[token.lemma_ for token in tokens] for tokens in tokenized_docs]

def text_procesation(text,corpus):

    doc = nlp(text)



def filter_tokens_by_occurrence(tokenized_docs, no_below=5, no_above=0.5):
    """

    Filter the Tokens by the number of ocurrences

    Args:
      tokenized_docs:[[Token]] an array of tokenized documents
      no_below: maximun of repetitionss
      no_above: min ammount of reptetitions

    Returns:
       list[Token]:A list of tokens which has been morphologicaly reduced

    Example:
        >>> tokenized_docs = [["Hello", "My", "name", "Is", "Crawly"], ["I", "m", "a", "news", "Crawler"]]

        >>> filtered_docs(tokenized_doc)
            [['hello', 'my', 'namme', 'be', 'crawly'], ['I', 'm', 'new', 'crawler']]
    """
    # Crea un diccionario de frecuencia de tokens
    token_freq = Counter(token for doc in tokenized_docs for token in doc)
    
    # Filtra los tokens según las condiciones dadas
    filtered_docs = []
    for doc in tokenized_docs:
        filtered_tokens = [token for token in doc if no_below <= token_freq[token] <= no_above * len(tokenized_docs)]
        filtered_docs.append(filtered_tokens)
    
    return filtered_docs



def build_vocabulary(dictionary):
    """
    Args:
      dictionary: an array of tokenized documents

    Returns:
       list[Token]:A list of tokens which has been morphologicaly reduced

    Example:
        >>> tokenized_docs = [["Hello", "My", "name", "Is", "Crawly"], ["I", "m", "a", "news", "Crawler"]]

        >>> morphological_reduction(tokenized_doc)
            [['hello', 'my', 'namme', 'be', 'crawly'], ['I', 'm', 'new', 'crawler']]
    """
    tokenized_words = [nlp(word) for word in dictionary]

    word_freq = Counter(token.text.lower() for doc in tokenized_words for token in doc)

    min_freq = 5
    max_vocab = 10000
    filtered_words = [word for word, freq in word_freq.items() if min_freq <= freq <= max_vocab]

    word2id = {word: idx for idx, word in enumerate(filtered_words)}
    id2word = {idx: word for word, idx in word2id.items()}

    return word2id, id2word


print(morphological_reduction(remove_stopwords(remove_noise(tokenization(["Hello My namme Is Crawly","Im a new Crawler"])))))

