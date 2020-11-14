from Documents import EnglishDocuments, PersianDocuments
from Indexers import PositionalIndexer, BigramIndexer


class IR:
    def __init__(self, lang):
        self.lang = lang
        if lang == 'en':
            self.documents = EnglishDocuments("./data/ted_talks.csv")
        else:
            self.documents = PersianDocuments("./data/Persian.xml")
        self.positional_indexer = PositionalIndexer(lang + '-positional-index')
        self.bigram_indexer = BigramIndexer(lang + '-bigram-index')

    def create_indexes(self):
        self.documents.init()
        self.__create_positional_index()
        self.__create_bigram_index()

    def __create_positional_index(self):
        for doc_id in range(len(self.documents.titles)):
            self.positional_indexer.index_document(
                doc_id, self.documents.titles[doc_id], self.documents.bodies[doc_id])
        self.positional_indexer.save()

    def __create_bigram_index(self):
        for doc_id in range(0, len(self.documents.titles)):
            content = self.documents.titles[doc_id] + self.documents.bodies[doc_id]
            self.bigram_indexer.index_document(doc_id, content)
        self.bigram_indexer.save()

    def get_posting_list(self, word):
        return self.positional_indexer.get_posting_list(word)

    def delete_document(self, doc_id):
        tokens = self.documents.pop(doc_id)
        self.positional_indexer.delete_document(doc_id, tokens)
        self.bigram_indexer.delete_document(doc_id, tokens)
        self.positional_indexer.save()
        self.bigram_indexer.save()

    def add_document(self, doc_id, title, body):
        tokenized_title, tokenized_body = self.documents.add(doc_id, title, body)
        self.positional_indexer.index_document(doc_id, tokenized_title, tokenized_body)
        self.bigram_indexer.index_document(doc_id, tokenized_title + tokenized_body)
        self.positional_indexer.save()
        self.bigram_indexer.save()

    def save(self):
        self.positional_indexer.save()
        self.bigram_indexer.save()

    def load(self):
        self.positional_indexer.load()
        self.bigram_indexer.load()