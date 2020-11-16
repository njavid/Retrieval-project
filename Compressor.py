class Compressor:
    def compress(self, index):
        for token in index:
            if 'title' in index[token]:
                doc_ids = [int(doc_id) for doc_id in index[token]['title']]
                doc_ids.sort()
                gaps = [doc_ids[0]]
                for i in range(1, len(doc_ids)):
                    gaps.append(doc_ids[i] - doc_ids[i - 1])
                new_index = {self.gamma_code(gaps[i], 'c'): index[token]['title'][str(doc_ids[i])] for i in
                             range(0, len(doc_ids))}
                index[token]['title'] = new_index

            if 'body' in index[token]:
                doc_ids = [int(doc_id) for doc_id in index[token]['body']]
                doc_ids.sort()
                gaps = [doc_ids[0]]
                for i in range(1, len(doc_ids)):
                    gaps.append(doc_ids[i] - doc_ids[i - 1])
                new_index = {self.gamma_code(gaps[i], 'c'): index[token]['body'][str(doc_ids[i])] for i in
                             range(0, len(doc_ids))}
                index[token]['body'] = new_index

    def decompress(self, index):
        for token in index:
            if 'title' in index[token]:
                doc_ids = [int(doc_id) for doc_id in index[token]['title']]
                doc_ids.sort()
                gaps = [doc_ids[0]]
                for i in range(1, len(doc_ids)):
                    gaps.append(doc_ids[i] + doc_ids[i - 1])
                new_index = {self.gamma_code(gaps[i], 'd'): index[token]['title'][str(doc_ids[i])] for i in
                             range(0, len(doc_ids))}
                index[token]['title'] = new_index

            if 'body' in index[token]:
                doc_ids = [int(doc_id) for doc_id in index[token]['body']]
                doc_ids.sort()
                gaps = [doc_ids[0]]
                for i in range(1, len(doc_ids)):
                    gaps.append(doc_ids[i] + doc_ids[i - 1])
                new_index = {self.gamma_code(gaps[i], 'd'): index[token]['body'][str(doc_ids[i])] for i in
                             range(0, len(doc_ids))}
                index[token]['body'] = new_index

    @staticmethod
    def gamma_code(num, type):
        if type == 'c':
            binary = bin(num)[2:]
            return '1' * (len(binary) - 1) + '0' + binary[1:]
        if type == 'd':
            num_str = str(num)
            index = num_str.find('0')
            return int('1' + num_str[index + 1:], 2)
        return None

    @staticmethod
    def variable_byte_code(num, type):
        if type == 'c':
            binary = bin(num)[2:]
            s = len(binary)
            res = ""
            while s > 7:
                res = '1' + binary[s - 7: s] + res
                s -= 7
            res = '0' * (8 - s) + binary[0:s] + res
            return res

        if type == 'd':
            num_str = str(num)
            s = len(num_str) - 8
            binary = ""
            while num_str[s] != '0':
                binary = num_str[s + 1: s + 8] + binary
                s -= 8
            index = num_str[s + 1:s + 8].find("1")
            binary = num_str[s + 1 + index:s + 8] + binary
            return int(binary, 2)

        return None
