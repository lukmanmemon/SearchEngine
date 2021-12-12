import json
import w3lib.html
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import pickle

def invert(testMode=False, testFilePath=""):
    
    if testMode:
        testFilePath += "/"
        file_object = open(testFilePath + "items.json", "r")
    else:
        # Read json file
        file_object = open("items.json", "r")
    json_content = file_object.read()
    file_object.close()
    # Convert json file to list
    data_list = json.loads(json_content)

    description_list = []
    url_list = []
    content_list = []
    title_list = []
    dictionary = {}
    stopwords_list = []


    # Get stop words and put into list
    with open("stopwords.txt", 'r') as file_stopwords:
        for line in file_stopwords:
            stopwords_list.extend(line.split())

    # Create lists with web page content, titles, URLs and descriptions
    for content in data_list:
        no_tags_content = w3lib.html.remove_tags(str(content['text']))
        tokenized_content = word_tokenize(no_tags_content)
        content_list.append(tokenized_content)

        title = ' '.join(content['title'])
        title_list.append(title)

        url = content['url']
        url_list.append(url)

        try:
            description = content['metadata']['opengraph'][0]['properties'][4][1]
        except IndexError:
            description = "No description available"
            
        description_list.append(description)

    ps = PorterStemmer()
    # Put terms in dictionary
    for content in content_list:
        for word in content:
            stripped_word = word.strip().lower()
            # Apply porter stemming to term
            stripped_word = ps.stem(stripped_word)

            if stripped_word.isalnum() and stripped_word not in stopwords_list:
                if stripped_word in dictionary:
                    dictionary[stripped_word] += 1
                else:
                    dictionary[stripped_word] = 1

    # Sort dictionary items
    dictionary_items = dictionary.items()
    sorted_items = sorted(dictionary_items)

    # List of tuples to dictionary 
    sorted_dictionary = {k:v for k,v in sorted_items}

    # Open txt file and write dictionary to it
    write_file_dict = open(testFilePath + "dict.txt","w")
    write_file_dict.write( str(sorted_dictionary) )
    write_file_dict.close()

    # Add terms to postings list with ID, TF, positions
    postings_list = {}
    id = 0
    tf_counter = {}

    for content in content_list:
        for line in content:

            for word in word_tokenize(line):
                # Apply porter stemming to term
                term = ps.stem(word.strip().lower())
                if term.isalnum() and term not in stopwords_list:
                    if term in tf_counter:
                        tf_counter[term] = tf_counter[term] + 1
                    else:
                        tf_counter[term] = 1
                    
                    if term not in postings_list:
                        postings_list[term] = {id: [title_list[id], url_list[id], tf_counter[term]]}

                    if term in postings_list and id not in postings_list[term].keys():
                        postings_list[term][id] = [title_list[id], url_list[id], tf_counter[term]]

                    if term in postings_list and id in postings_list[term].keys():
                        postings_list[term][id] = [title_list[id], url_list[id], tf_counter[term]]

        id = id + 1
        for key in tf_counter:
            tf_counter[key] = 0

    # Open txt file and write postings list to it
    write_file_postings = open(testFilePath + "postings.txt","w", encoding='utf-8')
    write_file_postings.write( str(postings_list) )
    write_file_postings.close()
    
    # Dump the vars to be used by the search program to provide speed/efficiency when searching through the documents
    with open(testFilePath + 'InvertVariableStore.pckl', 'wb') as dumped_vars:
        pickle.dump([stopwords_list, data_list, url_list, title_list, description_list], dumped_vars)
    
    if testMode:
        return [stopwords_list, data_list, url_list, title_list, description_list]


if __name__ == "__main__":
    invert();