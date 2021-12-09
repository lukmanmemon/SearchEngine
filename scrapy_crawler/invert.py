import jsonlines
import json
import w3lib.html
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Read json file
file_object = open("crawler/spiders/items.json", "r")
json_content = file_object.read()

# Convert json file to list
data_list = json.loads(json_content)

dictionary = {}
stopwords_list = []

# Get stop words and put into list
with open("stopwords.txt", 'r') as file_stopwords:
    for line in file_stopwords:
        stopwords_list.extend(line.split())

ps = PorterStemmer()
# Put terms in dictionary
for content in data_list:
    no_tags_content = w3lib.html.remove_tags(str(content['text']))
    content_tokenized = word_tokenize(no_tags_content)
    for word in content_tokenized:
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
write_file_dict = open("dict.txt","w")
write_file_dict.write( str(sorted_dictionary) )
write_file_dict.close()








