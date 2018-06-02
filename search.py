import os
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from extra_stopwords import char_stop_words
from fileIO import FileIO
import thread
_stemmer = PorterStemmer()


class Search:
    def __init__(self, query):
        self.query = query
        self.results = []

    def fine_tune(self):
        mod_text = self.tokenize_text(self.query)
        clean_text = []
        for i in mod_text:
            clean_text.append(i.encode('utf-8'))
        self.clean_text = clean_text

    def tokenize_text(self, text):
        tokens = [t for t in text.split()]
        stem = self.stem_tokens(self.clean_tokens(tokens), _stemmer)
        return stem

    def clean_tokens(self, tokens):
        clean_words = tokens[:]
        en_stop_words = stopwords.words('english') + char_stop_words
        clean_words = [word for word in tokens if word not in en_stop_words]
        return clean_words

    def stem_tokens(self, tokens, stemmer):
        stemmed = []
        stemmed = [stemmer.stem(token) for token in tokens]
        return stemmed

    def check_words(self, target):
        new_target = []
        if target:
            for i in target:
                new_target.append(i.encode('utf-8'))
            results_url = [i for e in self.clean_text for i in new_target if e in i]
            return len(results_url)

    def multiple_search(self, file):
        path = 'search_index'
        indices = FileIO(path + '/' + file).read_file()["indices"]
        for object in indices:
            if self.check_words(object["word_index"]) > 0:
                self.results.append(object)

    def search(self):
        path = 'search_index'
        for file in os.listdir(path):
            if file.endswith(".json") or file.endswith(".txt"):
                indices = FileIO(path + '/' + file).read_file()["indices"]
                for object in indices:
                    print object["word_index"]
                    if self.check_words(object["word_index"]) > 0:
                        self.results.append(object)

    def get_results(self):
        return list(self.results)


if __name__ == '__main__':
    search = Search("preach jehovah's witnesses php")
    search.fine_tune()
    search.search()
    print search.get_results()
