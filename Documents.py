import copy
import csv
from abc import abstractmethod
from collections import Counter

import nltk
from hazm import *
from lxml.etree import parse
from nltk.stem import PorterStemmer


class Documents:

    def __init__(self, path):
        self.path = path
        self.docs = {}
        self.titles = []
        self.bodies = []
        self.all_tokens = []
        self.most_frequent = []

    def init(self):
        title_dict, body_dict, all_tokens = self.read_documents()
        title_dict, body_dict, most_frequent = self.remove_sw_and_get_most_freq(all_tokens, title_dict, body_dict)

        self.titles = title_dict
        self.bodies = body_dict
        self.all_tokens = all_tokens
        self.most_frequent = most_frequent

    def prepare_text(self, doc_id, text):
        tokens = self.extract_tokens(text)
        if doc_id in self.docs:
            self.docs[str(doc_id)].extend(copy.deepcopy(tokens))
        else:
            self.docs[str(doc_id)] = copy.deepcopy(tokens)

        # TODO: there was a todo here for persian :-?
        return tokens

    def pop(self, doc_id):
        if doc_id not in self.docs:
            raise Exception('Document id does not exist.')
        res = self.docs[doc_id]
        self.docs.pop(doc_id)
        return res

    def add(self, doc_id, title, body):
        if doc_id in self.docs:
            raise Exception('Document id already exist.')
        return self.prepare_text(doc_id, title), self.prepare_text(doc_id, body)  # TODO remove stop words

    @staticmethod
    def remove_sw_and_get_most_freq(tokens_list, title_dict, body_dict):
        c = Counter(tokens_list)
        most_frequent = c.most_common(55)
        stop_words = most_frequent[:40]

        for doc_id in range(len(title_dict)):
            for (sw, f) in stop_words:
                title_dict[doc_id] = [token for token in title_dict[doc_id] if token != sw]
                body_dict[doc_id] = [token for token in body_dict[doc_id] if token != sw]

        # return processed dictionary and the top 15
        return title_dict, body_dict, most_frequent[40:]

    @abstractmethod
    def read_documents(self):
        pass

    @abstractmethod
    def extract_tokens(self, content):
        pass


class EnglishDocuments(Documents):

    def read_documents(self):
        bodies, titles, tokens = [], [], []
        rows = []
        # reading csv file
        with open(self.path, encoding="utf8") as csvfile:
            # creating a csv reader object
            csv_reader = csv.reader(csvfile)

            # extracting each data row one by one
            for row in csv_reader:
                rows.append(row)
        rows = rows[1:]
        for doc_id, row in enumerate(rows):
            bodies.append(self.prepare_text(doc_id, row[1]))
            titles.append(self.prepare_text(doc_id, row[14]))
            tokens = tokens + bodies[doc_id] + titles[doc_id]

        return titles, bodies, tokens

    def extract_tokens(self, content):
        # remove all punctuation marks and tokenizing
        tokenizer = nltk.RegexpTokenizer(r"\w+")
        tokens = tokenizer.tokenize(content)

        # stemming
        ps = PorterStemmer()
        res = [ps.stem(x) for x in tokens]

        return res


class PersianDocuments(Documents):

    def read_documents(self):
        bodies, titles, tokens = [], [], []
        tree = parse(self.path)
        ns = {"wiki": "http://www.mediawiki.org/xml/export-0.10/"}
        titles = tree.xpath("//wiki:title//text()", namespaces=ns)
        bodies = tree.xpath("//wiki:text//text()", namespaces=ns)

        for i in range(1, len(titles)):
            bodies[i] = self.prepare_text(i, texts[i])
            titles[i] = self.prepare_text(i, titles[i])
            tokens = tokens + bodies[i] + titles[i]

        return titles, bodies, tokens

    def extract_tokens(self, content):
        # normalize
        normalizer = Normalizer()
        content = normalizer.normalize(content)

        # tokenizing and removing punctuation marks
        tokenizer = nltk.RegexpTokenizer(r"\w+")
        tokens = tokenizer.tokenize(content)

        # stemming
        stemmer = Stemmer()
        res = [stemmer.stem(x) for x in tokens]

        return res
