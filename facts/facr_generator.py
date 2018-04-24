from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity
from random import randint

class FactGenerator():
    def __init__(self):
        facts = []
        with open('../data/test.txt', "r", encoding="utf-8") as inp:
            facts = inp.readlines()
        vectorizer = TfidfVectorizer(stop_words=ENGLISH_STOP_WORDS.union(["fact", "tell", "about"]))
        vects = vectorizer.fit_transform(facts)

        self.facts = facts
        self.vectorizer = vectorizer
        self.vects = vects

    def best_fact(self, query):
        cosine = cosine_similarity(self.vectorizer.transform([query]), self.vects)
        amax = cosine[0].argmax()
        return self.facts[amax], cosine[0][amax]

    def random_fact(self, lst=None):
        if lst is None:
            lst = self.facts
        return lst[randint(0, len(lst) - 1)]