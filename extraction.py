import requests
from bs4 import BeautifulSoup
import nltk
import operator
import re
import string
import urllib
from bs4 import BeautifulSoup
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

from extra_stopwords import char_stop_words

_stemmer = PorterStemmer()
# try:
#     # For Python 3.0 and later
#     from urllib.request import urlopen
# except ImportError:
#     # Fall back to Python 2's urllib2
#     from urllib2 import urlopen
from urllib import urlopen

URL_KEY = 'url'


class Extraction:
    def __init__(self, history_object):
        self.history_object = history_object

    def title_include(self):
        text = self.history_object["title"]
        final_token = self.tokenize_text(text)
        to_index = []
        for x in final_token:
            to_index.append(x.encode('utf-8'))
        return to_index

    def get_text(self):
        # response = urllib.request.urlopen(x["url"])
        # html = response.read()

        # ensure the history object contains a link/url
        try:
            key = URL_KEY.encode('utf-8')
            url = self.history_object[key]
            if "/logout" in url:
                return
        except:
            print ("No Url Found in Object")
            return

        # check if the page is available
        try:
            # response = urlopen(url)
            # html = response.read()
            # soup = BeautifulSoup(html, "html5lib")
            # text = soup.get_text(strip=True)
            # return text
            source_code = requests.get(url)
            html = source_code.text
            soup = BeautifulSoup(html, "html5lib")
            text = soup.get_text(strip=True)
            final_token = self.tokenize_text(text)
            return self.feature_count(final_token)

        except Exception as e:
            print(e)

        # url = self.url["url"]
        # source_code = requests.get(url)
        # html = source_code.text
        # soup = BeautifulSoup(html, "html5lib")
        # text = soup.get_text(strip=True)
        # return text

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

    def feature_count(self, final_token):
        counter = Counter(final_token)
        most_common = counter.most_common(30)
        related_words_array = self.title_include()
        for i in most_common:
            related_words_array.append(i[0].encode('utf-8'))
        return related_words_array
