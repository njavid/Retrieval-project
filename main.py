from IR import IR


def string_of_arr(arr):
    mstr = ""
    for i in arr:
        mstr += str(i) + ", "
    return mstr


def get_order(question, valid_choices):
    user_order = input(question)
    if user_order in [str(c) for c in valid_choices]:
        return user_order
    raise Exception('Invalid input!')


if __name__ == '__main__':
    lang = get_order("Hi!\nPlease select language to start! [en,fa]: ", ['en', 'fa'])
    ir = IR(lang)

    while True:
        # try:
            o = get_order('1) Create indexes from files. \n2) Load already existing indexes.\n', [1, 2])
            if o == '1':
                print('Creating indexes ...')
                ir.create_indexes()
            else:
                ir.load()
            break
        # except Exception as e:
        #     print(e)

    while True:
        try:
            order = get_order(
                "What do you want to see?\n1)Your input tokens after preprocess\n"
                "2)See the 15 most frequent token in documents\n"
                "3)Show posting list of a word\n4)Show position of a word in per doc\n"
                "5)Show all word containing a bigram\n"
                "6)Add a new doc to index\n7)delete a doc from index\n"
                "8)Correct your query spelling\n9)Quit\n", range(1, 10))

            if order == "1":
                input_str = input("Give us the text\n")
                print("Your input tokens after preprocess:\n", ir.documents.prepare_text("en", input_str))

            elif order == "2":
                print("The 15 most frequent token in " + lang + " documents:\n", ir.documents.most_frequent)
            elif order == "3":
                input_str = input("Give us the word\n")
                print(ir.get_posting_list(input_str))
            elif order == "4":
                input_str = input("Give us the word\n")
                index = ir.get_posting_list(input_str)
                all_docs = []
                for zone in index:
                    all_docs.extend(index[zone].keys())
                for doc_id in all_docs:
                    if 'body' in index and doc_id in index['body']:
                        print("doc num" + doc_id + " (body) --> " + string_of_arr(index['body'][doc_id]))
                    if 'title' in index and doc_id in index['title:']:
                        print("doc num" + doc_id + " (title) --> " + string_of_arr(index['title'][doc_id]))
            elif order == "5":
                input_str = input("Give us the bigram\n")
                print(string_of_arr([word for word in ir.bigram_indexer.get_posting_list(input_str)]))
            elif order == "6":
                doc_id = input("Give us the doc Id\n")
                title = input("Give us the title\n")
                body = input("Give us the body\n")
                ir.add_document(doc_id, title, body)
                print('done')
            elif order == "7":
                doc_id = input("Give us the doc_id\n")
                ir.delete_document(doc_id)
                print('done')
            elif order == "8":
                query = input("Give us the query\n")
                print(*ir.query(query))
            elif order == "9":
                print("Hope to see you again:)")
                break
        except Exception as e:
            print(str(e))
