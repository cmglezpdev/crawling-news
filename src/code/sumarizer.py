import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest

def new_generatesumarize(text):

        nlp = spacy.load('en_core_web_sm') #loading the model

        doc = nlp(text) #preocessing the text

# print(len(list(doc.sents))) #initial sentences

        keywords = []
        stop_words = list(STOP_WORDS) #getting the stop_words
        pos_tag = ['PROPN','ADJ','NOUN','VERB'] #sentence recognition tags
        for token in doc:
            if token.text in stop_words or token.text in punctuation:
                continue
            if token.pos_ in pos_tag: #si es alguno de los tags de oracion
                keywords.append(token.text)#se agrega a las palabras clave

#este proceso elimina adjetivos y palabras descriptoras innecesarias

        freq_word = Counter(keywords) #saca las palabras mas usadas en el texto (de las palabras claves)
# print(freq_word.most_common(5))
#da un array de tuplas de palabras , palabra y frecuencia

        max_freq = Counter(keywords).most_common(1)[0][1] #da la frecuencia de aparicion de las palabras

        for word in freq_word.keys():
            freq_word[word] = (freq_word[word]/max_freq)#normalizando las frecuencias
# print(freq_word.most_common(5))


        sent_strength ={}#calcular la fuerza de las oraciones en base a la relevancia de sus palabras

        for sent in doc.sents:
            for word in sent:
                if word.text in freq_word.keys():#se tienen encuenta solo las palabras frecuentes , el resto tienen relevancia 0
                    if sent in sent_strength.keys():#si ya tiene asignado valor se le suma
                         sent_strength[sent]+=freq_word[word.text]
                    else:
                        sent_strength[sent]=freq_word[word.text]

# print(sent_strength)

        sumarized_sentences = nlargest(3,sent_strength,key=sent_strength.get)

# print(sumarized_sentences)


#convirtiendo el resumen en un string

        final_sentences = [w.text for w in sumarized_sentences]

        final_text = ''.join(final_sentences)

        return final_text
