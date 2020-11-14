
class Compressor:
    def compress(self,index):
        for token in index:
            if 'title' in index[token]:
                doc_ids = [int(doc_id) for doc_id in index[token]['title']]
                doc_ids.sort()
                gaps = [doc_ids[0]]
                for i in range(1,len(doc_ids)):
                    gaps.append(doc_ids[i]-doc_ids[i-1])
                new_index = {self.gamma_code(gaps[i],'c'):index[token]['title'][str(doc_ids[i])] for i in range(0,len(doc_ids))}
                index[token]['title'] = new_index

            if 'text' in index[token]:
                doc_ids = [int(doc_id) for doc_id in index[token]['text']]
                doc_ids.sort()
                gaps = [doc_ids[0]]
                for i in range(1, len(doc_ids)):
                    gaps.append(doc_ids[i] - doc_ids[i - 1])
                new_index = {self.gamma_code(gaps[i],'c'): index[token]['text'][str(doc_ids[i])] for i in range(0, len(doc_ids))}
                index[token]['text'] = new_index

    def decompress(self,index):
        for token in index:
            if 'title' in index[token]:
                doc_ids = [int(doc_id) for doc_id in index[token]['title']]
                doc_ids.sort()
                gaps = [doc_ids[0]]
                for i in range(1, len(doc_ids)):
                    gaps.append(doc_ids[i] + doc_ids[i - 1])
                new_index = {self.gamma_code(gaps[i],'d'): index[token]['title'][str(doc_ids[i])] for i in range(0, len(doc_ids))}
                index[token]['title'] = new_index

            if 'text' in index[token]:
                doc_ids = [int(doc_id) for doc_id in index[token]['text']]
                doc_ids.sort()
                gaps = [doc_ids[0]]
                for i in range(1, len(doc_ids)):
                    gaps.append(doc_ids[i] + doc_ids[i - 1])
                new_index = {self.gamma_code(gaps[i],'d'): index[token]['text'][str(doc_ids[i])] for i in range(0, len(doc_ids))}
                index[token]['text'] = new_index

    def gamma_code(self,num,type):
        if type == 'c':
            print("compress")
        if type == 'd':
            print("decompress")
        return num + 2


    def variable_byte_code(self,num,type):
        if type == 'c':
            print("compress")
        if type == 'd':
            print("decompress")
        return num + 2
