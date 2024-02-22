# Crawling News


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

