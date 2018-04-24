from gensim.models import Word2Vec

# read data and normalize it

import re
from gensim.parsing import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from string import punctuation
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity
from e.state import State

import pickle


class Model:
    # max = 0

    def __init__(self):


        w2v = []

        texts = [r"../data/carroll-alice.txt",
                 r"../data/melville-moby_dick.txt",
                 r"../data/edgeworth-parents.txt",
                 r"../data/austen-emma.txt",
                 r"../data/whitman-leaves.txt",
                 ]

        for text in texts:
            paragraphs = open(text, 'r').read().split('\n')
            for par in paragraphs:
                if not par:
                    continue
                if par == '\n' or par == '':
                    continue
                par = re.sub('[\[\]()]+', '', par)
                w2v.append(par)

        self.vectorizer = TfidfVectorizer(stop_words=ENGLISH_STOP_WORDS)

        try:
            with open('model1.pkl'.format(20), 'rb') as input:
                model = pickle.load(input)
        except:
            with open('model1.pkl'.format(20), 'wb') as output:
                model = self.vectorizer
                pickle.dump(model, output, pickle.HIGHEST_PROTOCOL)

        self.vexts = self.vectorizer.fit_transform(w2v)

        try:
            with open('model.pkl'.format(20), 'rb') as input:
                model = pickle.load(input)
        except:
            with open('model.pkl'.format(20), 'wb') as output:
                model = self
                pickle.dump(model, output, pickle.HIGHEST_PROTOCOL)




    def check_time(self, query):
        cosine = cosine_similarity(self.vectorizer.transform(["event time"]), self.vectorizer.transform([query]))
        cosine1 = cosine_similarity(self.vectorizer.transform(["In which time event will be"]), self.vectorizer.transform([query]))
        cosine2 = cosine_similarity(self.vectorizer.transform(["In what time"]), self.vectorizer.transform([query]))

        print('time',cosine, ' ' , cosine1, ' ', cosine2)

        if cosine >= cosine1 and cosine >= cosine2:
            amax = cosine[0].argmax()
            return cosine[0][amax]
        elif cosine1 > cosine and cosine1 > cosine2:
            amax = cosine1[0].argmax()
            return cosine1[0][amax]
        else:
            amax = cosine2[0].argmax()
            return cosine2[0][amax]


    def check_price(self, query):
        cosine = cosine_similarity(self.vectorizer.transform(["price of the event"]), self.vectorizer.transform([query]))
        cosine1 = cosine_similarity(self.vectorizer.transform(["cost of the event"]),
                                    self.vectorizer.transform([query]))
        cosine2 = cosine_similarity(self. vectorizer.transform(["How much event "]), self.vectorizer.transform([query]))
        print('price',cosine, ' ' , cosine1, ' ', cosine2)

        if cosine >= cosine1 and cosine >= cosine2:
            amax = cosine[0].argmax()
            return cosine[0][amax]
        elif cosine1 >= cosine and cosine1 >= cosine2:
            amax = cosine1[0].argmax()
            return cosine1[0][amax]
        else:
            amax = cosine2[0].argmax()
            return cosine2[0][amax]

    def check_place(self, query):
        cosine = cosine_similarity(self.vectorizer.transform(["event place"]), self.vectorizer.transform([query]))
        cosine1 = cosine_similarity(self.vectorizer.transform(["where will the event take place"]),
                                    self.vectorizer.transform([query]))
        cosine2 = cosine_similarity(self.vectorizer.transform(["Where are the event?"]), self.vectorizer.transform([query]))

        print('place',cosine, ' ' , cosine1, ' ', cosine2)

        if cosine >= cosine1 and cosine >= cosine2:
            amax = cosine[0].argmax()
            return cosine[0][amax]
        elif cosine1 >= cosine and cosine1 >= cosine2:
            amax = cosine1[0].argmax()
            return cosine1[0][amax]
        else:
            amax = cosine2[0].argmax()
            return cosine2[0][amax]

    def found_max(self, query):
        max = 0
        c_time = self.check_time(query)
        c_price = self.check_price(query)
        c_place = self.check_place(query)
        if c_time >= c_place and c_time >= c_price :
            max = c_time
        elif c_place >= c_price and c_place >= c_time:
            max = c_place
        elif c_price >= c_place and c_price >= c_time:
            max = c_price
        return max

    def check_section(self, query):

        m = self.found_max(query)
        # print('m',m)
        if m < 0.3:
            return State.FACT_SECTION
        elif m == self.check_price(query):
            return State.COST_SECTION
        elif m == self.check_place(query):
            return State.PLACE_SECTION
        else:
            return State.TIME_SECTION

    def get_tagger(limit=20):
        tagger = None
        try:
            with open('tagger.model{}.pkl'.format(limit), 'rb') as input:
                tagger = pickle.load(input)
        except:
            with open('tagger.model{}.pkl'.format(limit), 'wb') as output:
                # tagger = Tagger(DataParser(limit))
                pickle.dump(tagger, output, pickle.HIGHEST_PROTOCOL)
        return tagger
