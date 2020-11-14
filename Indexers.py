import json


class Indexer:

    def __init__(self, name):
        self.index = {}
        self.name = name

    def save(self):
        file = open(self.name + ".json", "w+", encoding='utf-8')
        index_str = json.dumps(self.index, indent=4)
        file.write(index_str)
        file.close()

    def load(self):
        try:
            file = open(self.name + ".json", "r", encoding='utf-8')
            index_text = file.read()
            file.close()
            self.index = json.loads(index_text)
        except FileNotFoundError:
            raise Exception('Indexes have not been created yet!')


class PositionalIndexer(Indexer):

    def index_document(self, doc_id, title, body):
        self.index_with_zone(doc_id, 'title', title)
        self.index_with_zone(doc_id, 'body', body)

    def index_with_zone(self, doc_id, zone, content):
        for position in range(len(content)):
            token = content[position]
            if token not in self.index:
                self.index[token] = {}

            if zone in self.index[token]:
                if doc_id in self.index[token][zone]:
                    self.index[token][zone][doc_id].append(position)
                else:
                    self.index[token][zone][doc_id] = [position]
            else:
                self.index[token][zone] = {doc_id: [position]}
        # Changed order of doc_id and zone

    def get_posting_list(self, word):
        if word in self.index:
            return self.index[word]
        return {}

    def delete_document(self, doc_id, tokens):
        for token in tokens:
            if token in self.index:
                for zone in self.index[token]:
                    if doc_id in self.index[token][zone]:
                        self.index[token][zone].pop(doc_id)


class BigramIndexer(Indexer):

    def index_document(self, doc_id, tokenized_content):
        for token in tokenized_content:
            for i in range(len(token) - 1):
                bi = token[i:i + 2]
                if bi in self.index:
                    if token in self.index[bi]:
                        self.index[bi][token] += 1
                    else:
                        self.index[bi][token] = 1
                else:
                    self.index[bi] = {token: 1}
        # TODO: where is the posting list?!

    def delete_document(self, doc_id, tokenized_content):
        for token in tokenized_content:
            for i in range(len(token) - 1):
                bi = token[i:i + 2]
                if bi in self.index:
                    if token in self.index[bi]:
                        self.index[bi][token] -= 1

    def get_posting_list(self, word):
        if word in self.index:
            return self.index[word]
        return {}
