import csv
import json
from collections import Counter
import nltk
from nltk.stem import PorterStemmer

english_data_file = "./data/ted_talks.csv"


def en_prepare_text(content):
    # remove all punctuation marks
    tokenizer = nltk.RegexpTokenizer(r"\w+")

    # tokenizing
    tokens = tokenizer.tokenize(content)

    # stemming
    ps = PorterStemmer()
    s_tokens = [ps.stem(x) for x in tokens]

    # removing stop words(words with more than 12 percent frequency)

    tonkens_freq = list(Counter(s_tokens).items())

    l = len(s_tokens)
    output = [token for (token, f) in tonkens_freq if (f / l) < 0.12]

    return output


def get_english_documents():
    rows = []
    dic = {}

    # reading csv file 
    with open(english_data_file, encoding="utf8") as csvfile:
        # creating a csv reader object 
        csvreader = csv.reader(csvfile)

        # extracting each data row one by one 
        for row in csvreader:
            rows.append(row)

    for i in range(1, len(rows)):
        dic[i] = (en_prepare_text(rows[i][14] + " " + rows[i][1]))

    return dic


def get_docs_most_freq_tokens(tokens):
    c = Counter(tokens)
    return c.most_common(3)


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
            "What do you want to see?\n1)Your input tokens after preprocess\n2)see term frequency in "
            "documents\n3)show posting list of a word\n4)show position of a word in per doc\n5)show all word "
            "containing a word\n6)add a new doc\n7)delete a doc\n")

        if order == "1":
            input_str = input("Give us the text\n")
            print(en_prepare_text(input_str))
        elif order == "2":
            documents = get_english_documents()
            j = 1
            for doc in documents:
                print("Top 3 tokens of document number ", j, get_docs_most_freq_tokens(documents[doc]))
                j += 1
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
        else:
            print("Invalid input!")


if __name__ == "__main__":
    main()
