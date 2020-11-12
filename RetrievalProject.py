import csv
import json
from collections import Counter
import nltk
from nltk.stem import PorterStemmer
import xml.etree.ElementTree as ET

english_data_file = "./data/ted_talks.csv"


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


def get_english_documents_data():
    rows = []
    text_dic = {}
    title_dic = {}
    all_tokens = []

    # reading csv file
    with open(english_data_file, encoding="utf8") as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)

    for i in range(1, len(rows)):
        text_dic[i] = en_prepare_text(rows[i][1])
        title_dic[i] = en_prepare_text(rows[i][14])
        all_tokens = all_tokens + text_dic[i] + title_dic[i]

    title_dic, text_dic, f = remove_sw_and_get_most_freq(all_tokens, title_dic, text_dic)

    return title_dic, text_dic, f


def get_persian_documents_data():
    # todo
    print("Not implemented")
    return [], [], 0


def create_indexes(dic):
    index = {}
    for docID in range(1, len(dic)):
        for position in range(len(dic[docID])):
            token = dic[docID][position]
            if token in index:
                if docID in index[token]:
                    index[token][docID].append(position)
                else:
                    index[token][docID] = [position]
            else:
                index[token] = {docID: [position]}

    index_txt = json.dumps(index, indent=4)
    file1 = open("PositionalIndex.txt", "w+")
    file1.write(index_txt)
    file1.close()

    print(index_txt)


# Main method
def main():
    # print("Hi!\nCreating index of documents ...")
    # create_positional_index(get_english_documents())
    while 1:
        order = input(
            "What do you want to see?\n1)Your input tokens after preprocess\n2)See the 15 most frequent token in "
            "documents\n3)show posting list of a word\n4)show position of a word in per doc\n5)show all word "
            "containing a word\n6)add a new doc\n7)delete a doc\n8)quit\n")

        if order == "1":
            language = input("Pick the language:\n1)English\n2)Persian\n")
            if language == "1":
                input_str = input("Give us the text\n")
                print("Your input tokens after preprocess:\n", prepare_text("en", input_str))
            elif language == "2":
                input_str = input("Give us the text\n")
                print("Your input tokens after preprocess:\n", prepare_text("fa", input_str))


        elif order == "2":
            language = input("Pick the language:\n1)English\n2)Persian\n")
            if language == "1":
                _, _, f = get_english_documents_data()
                print("The 15 most frequent token in English documents:\n", f)
            elif language == "2":
                _, _, f = get_persian_documents_data()
                print("The 15 most frequent token in Persian documents:\n", f)

                # print("Top 3 frequent tokens of document ",i+1 , get_docs_most_freq_tokens(documents[i]))
        elif order == "3":
            input_str = input("Give us the word\n")
            print(en_prepare_text(input_str))
        elif order == "4":
            input_str = input("Give us the word\n")
            print(en_prepare_text(input_str))
        elif order == "5":
            input_str = input("Give us the word\n")
            print(en_prepare_text(input_str))
        elif order == "6":
            input_str = input("Give us the word\n")
            print(en_prepare_text(input_str))
        elif order == "7":
            input_str = input("Give us the word\n")
            print(en_prepare_text(input_str))
        elif order == "8":
            print("Hope to see you again:)")
            break
        else:
            print("Invalid input!")


if __name__ == "__main__":
    main()
