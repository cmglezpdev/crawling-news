
# Crawling News

## Authors
 - Alex Sánchez Saez
 - Carlos Manuel González

## Our Project Is a News Page Crawler Our Initial Idea was making a webpage Scrapper for each news Web and process the stacted information for the retrieveral process using the `Vectorial Model` we found some errors in thar approach , so we change some things , for the scrapping and Dom Analysis and Xpath we use a library named `newspaper3k` which makes all the scrapper hardword , so we can focus on the text processing and the information retrieveral , we use `spacy` and `gensim` for that matter , making a summary of the extracted news info and a named entities Analysis , we use `streamlit` to build the ui and found a news database to use in the retrieveral 


## With this project we learn how a web crawler works , to be more precise a `Domain-specific content crawler` we learn how to use nlp libraries such as spacy and gensim and how to use this tools for text processing , we use the vectorial model using tf-idf for the term weight calculus , 

# Definitions
    - TF-IDF (Term Frequency - Inverse Document Frequency)

        **TF-IDF** is a term weighting technique used in information retrieval and text analysis. It assigns weights to the terms in a document to assess their relative importance, considering both their frequency within the document (TF) and their frequency in a set of reference documents (IDF).

        **TF formula:**
        TF(t, d) = (n_t,d) / (∑_w ∈ D(d) n_w,d)
        where:

        * `n_t,d` is the number of times term t appears in document d.
        * `∑_w ∈ D(d) n_w,d` is the sum of the frequencies of all terms in document d.
        * `D(d)` is the set of all unique terms in document d.

        **IDF formula:**
        IDF(t) = log(N / df(t))

 - ## Vector Space Model

      The **Vector Space Model** represents each document as a vector in a high-dimensional space, where each dimension represents a term. The length of the vector reflects the importance of the term in the document.

 - ## Cosine Similarity

       **Cosine Similarity** is used to measure the similarity between two vectors. It is calculated as the cosine of the angle between the vectors. A value of 1 indicates perfect similarity, while a value of 0 indicates complete dissimilarity.

       **Cosine Similarity formula:**
       Cosine Similarity(v1, v2) = cos(θ) = (v1 ⋅ v2) / (||v1|| ||v2||)
        * `v1` and `v2` are the two vectors.
        * `θ` is the angle between the vectors.
        * `||v1||` and `||v2||` are the lengths of the vectors.

# Things to Upgrade :
    - We woud like to improve the information retrieveral step of the process of this crawler , with the knowledge that will be adquired along the course , improve the UI and make it more user friendly and implement another retrieveral model such as Latent Semantic Information (LSI) to make this process or use a more sofisticated analysis of the information adding some other modules to the project such as a periodicly growing database


## Database

The data is a csv with a set of news from cnn website. Dowload the csv file from the [Kaggle](https://www.google.com) and save it in the `src/data/` folder with the name  `cnn_news.csv` 

## Install dependencies

```bash
# install dependencies
python install -m requirements.txt
```


## Execute Project

Navigate to `/src/code/` folder and execute `training.py` script training the _tfidf-model_ with the _cnn data_.

Executing the project
```bash
python ./src
```
Or
```bash
python training.py
```

Navigate to `/src/gui/` and ejectute the the _UI_:

```bash
stremlit run page.py
```

