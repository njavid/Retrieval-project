import csv
import json
from collections import Counter

import nltk
from hazm import *
from lxml.etree import parse
from nltk.stem import PorterStemmer

english_data_path = ".\\data\\ted_talks.csv"
persian_data_path = ".\\data\\Persian.xml"

def prepare_text(language, text):
    tokens = []
    if language == "en":
        tokens = en_prepare_text(text)
    else:
        print("Todo")

    return tokens


def en_prepare_text(content):
    # remove all punctuation marks and tokenizing
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(content)

    # stemming
    ps = PorterStemmer()
    s_tokens = [ps.stem(x) for x in tokens]

    return s_tokens


def fa_prepare_text(content):
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


def remove_sw_and_get_most_freq(tokens_list, title_dictionary, text_dictionary):
    c = Counter(tokens_list)
    most_frequent = c.most_common(55)
    stop_words = most_frequent[:40]

    # print(stop_words)

    for docID in range(1, len(title_dictionary) + 1):
        for (sw, f) in stop_words:
            title_dictionary[docID] = [i for i in title_dictionary[docID] if i != sw]
            text_dictionary[docID] = [i for i in text_dictionary[docID] if i != sw]

    # return processed dictionary and the top 15
    return title_dictionary, text_dictionary, most_frequent[40:]


def read_english_docs(title, text, tokens):
    rows = []
    # reading csv file
    with open(english_data_path, encoding="utf8") as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)

    for i in range(1, len(rows)):
        text[i] = en_prepare_text(rows[i][1])
        title[i] = en_prepare_text(rows[i][14])
        tokens = tokens + text[i] + title[i]

    return title, text, tokens


def read_persian_docs(title, text, tokens):
    tree = parse(persian_data_path)
    ns = {"wiki": "http://www.mediawiki.org/xml/export-0.10/"}
    titles = tree.xpath("//wiki:title//text()", namespaces=ns)
    texts = tree.xpath("//wiki:text//text()", namespaces=ns)

    for i in range(1, len(titles)):
        text[i] = fa_prepare_text(texts[i])
        title[i] = fa_prepare_text(titles[i])
        tokens = tokens + text[i] + title[i]

    return title, text, tokens


def get_documents_data(language):
    text_dic = {}
    title_dic = {}
    all_tokens = []

    if language == "en":
        title_dic, text_dic, all_tokens = read_english_docs(title_dic, text_dic, all_tokens)
    else:
        title_dic, text_dic, all_tokens = read_persian_docs(title_dic, text_dic, all_tokens)

    title_dic, text_dic, f = remove_sw_and_get_most_freq(all_tokens, title_dic, text_dic)

    return title_dic, text_dic, f


def create_indexes(dic, language):
    title_dic, text_dic = dic[0], dic[1]
    print(text_dic)

    #   positional index
    index = {}
    for docID in range(1, len(title_dic)+1):
        #   text index :
        for position in range(0, len(text_dic[docID])):
            token = text_dic[docID][position]
            if token in index:
                if docID in index[token]:
                    if 'text' in index[token][docID]:
                        index[token][docID]['text'].append(position)
                    else:
                        index[token][docID]['text'] = position
                else:
                    index[token][docID] = {'text': [position]}
            else:
                index[token] = {docID: {'text': [position]}}

        #   title index :
        for position in range(0, len(title_dic[docID])):
            token = title_dic[docID][position]
            if token in index:
                if docID in index[token]:
                    if 'title' in index[token][docID]:
                        index[token][docID]['title'].append(position)
                    else:
                        index[token][docID]['title'] = [position]
                else:
                    index[token][docID] = {'title': [position]}
            else:
                index[token] = {docID: {'title': [position]}}

    save_data(index,language,'positional')

    #   bigram index :
    for docID in range(1, len(title_dic) + 1):
        text_dic[docID].extend(title_dic[docID])
    index = {}
    for docID in range(1, len(text_dic) + 1):
        for token in text_dic[docID]:
            for i in range(len(token)-1):
                bi = token[i:i+2]
                if bi in index :
                    if token in index[bi]:
                        index[bi][token] += 1
                    else :
                        index[bi][token] = 1
                else:
                    index[bi] = {token: 1}


    save_data(index,language,'bigram')


def get_positional_posting_list(word,language,index_type):
    index = load_data(language,index_type)
    if word in index:
        return index[word]
    return {}


def string_of_arr(arr):
    mstr = ""
    for i in arr :
        mstr+=str(i)+" , "
    return mstr


def load_data(language,index_type):
    f = open(language + "-" + index_type + "-index.txt", "r")
    index_text = f.read()
    f.close()
    index = json.loads(index_text)
    # if index_type == 'positional' :
        # todo encode index
    return index


def save_data(data,language,index_type):
    # if index_type == 'positional' :
    # todo encode index
    index_txt = json.dumps(data, indent=4)
    file2 = open(language + "-"+index_type+"-index.txt", "w+")
    file2.write(index_txt)
    file2.close()
    print(index_txt)


def delete_from_index(docId,language):
    bigram_index = load_data(language,'bigram')
    positional_index = load_data(language,'positional')
    # update positional:
    #   todo


def add_doc_to_index(doc_id,text,title,language):
    prepared_title = prepare_text(language,title)
    prepared_text = prepare_text(language,text)
    bigram_index = load_data(language,"bigram")
    positional_index = load_data(language,"positional")

    for position in range(0, len(prepared_text)):
        token = prepared_text[position]
        if token in positional_index:
            if doc_id in positional_index[token]:
                if 'text' in positional_index[token][doc_id]:
                    positional_index[token][doc_id]['text'].append(position)
                else:
                    positional_index[token][doc_id]['text'] = position
            else:
                positional_index[token][doc_id] = {'text': [position]}
        else:
            positional_index[token] = {doc_id: {'text': [position]}}

    for position in range(0, len(prepared_title)):
        token = prepared_title[position]
        if token in positional_index:
            if doc_id in positional_index[token]:
                if 'title' in positional_index[token][doc_id]:
                    positional_index[token][doc_id]['title'].append(position)
                else:
                    positional_index[token][doc_id]['title'] = position
            else:
                positional_index[token][doc_id] = {'title': [position]}
        else:
            positional_index[token] = {doc_id: {'title': [position]}}

#todo bi
    save_data(positional_index,language,'positional')
    save_data(bigram_index,language,'bigram')


# Main method
def main():
    print("Hi!\nCreating index of documents ...")
    create_indexes(get_documents_data('en'), 'en')
    # create_indexes(get_documents_data('fa'),'fa')

    while 1:
        order = input(
            "What do you want to see?\n1)Your input tokens after preprocess\n"
            "2)See the 15 most frequent token in documents\n"
            "3)show posting list of a word\n4)show position of a word in per doc\n"
            "5)show all word containing a bigram\n"
            "6)add a new doc to index\n7)delete a doc from index\n8)quit\n")

        if order == "1":
            language = input("Pick the language:\n1)English\n2)Persian\n")
            if language == "1":
                input_str = input("Give us the text\n")
                print("Your input tokens after preprocess:\n", prepare_text("en", input_str))
            elif language == "2":
                input_str = input("Give us the text\n")
                print("Your input tokens after preprocess:\n", prepare_text("fa", input_str))

        elif order == "2":
            language = input("Which language ? 'fa' or 'en' ?")
            _,_, f = get_documents_data(language)
            print("The 15 most frequent token in "+language+" documents:\n", f)

            # print("Top 3 frequent tokens of document ",i+1 , get_docs_most_freq_tokens(documents[i]))
        elif order == "3":
            input_str = input("Give us the word\n")
            language = input("Which language ? 'fa' or 'en' ?")
            print(get_positional_posting_list(input_str,language,"positional"))
        elif order == "4":
            input_str = input("Give us the word\n")
            language = input("Which language ? 'fa' or 'en' ?")
            index = get_positional_posting_list(input_str, language,"positional")
            for docId in index :
                if 'text' in index[docId] :
                    print("doc num"+docId +" (text) --> "+ string_of_arr(index[docId]['text']))
                if 'title' in index[docId] :
                    print("doc num"+docId +" (title) --> "+ string_of_arr(index[docId]['title']))
        elif order == "5":
            input_str = input("Give us the bigram\n")
            language = input("Which language ? 'fa' or 'en' ?")
            print(string_of_arr([word for word in get_positional_posting_list(input_str,language,"bigram")]))
        elif order == "6":
            doc_id = input("Give us the doc Id\n")
            title = input("Give us the title\n")
            text = input("Give us the text\n")
            language = input("Which language ? 'fa' or 'en' ?")
            add_doc_to_index(doc_id,title,text,language)
            print('done')
        elif order == "7":
            doc_id = input("Give us the doc_id\n")
            language = input("Which language ? 'fa' or 'en' ?")
            delete_from_index(doc_id,language)
            print('done')
        elif order == "8":
            print("Hope to see you again:)")
            break
        else:
            print("Invalid input!")


if __name__ == "__main__":
    main()
