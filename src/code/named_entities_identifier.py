import spacy

nlp = spacy.load('en_core_web_sm')

def named_entities_searcher(text):
    doc = nlp(text)

    return doc.ents
