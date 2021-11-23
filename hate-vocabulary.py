"""
Created on Tue Nov 23 15:48:03 2021

@author: Irene Lopez

Collect all hate vocabulary in english from Hatebase: https://hatebase.org/
Code adapted from: https://github.com/DanielJDufour/hatebase#get-all-arabic-vocabulary
"""

import json
from hatebase import HatebaseAPI

key = "ABC" # this depends on user

hatebase = HatebaseAPI({"key": key, "debug":True})
filters = {"language": "eng"}
format = "json"

# initialize list for all vocabulary entry dictionaries
en_vocab = []
response = hatebase.getVocabulary(filters=filters, format=format)
pages = response["number_of_pages"]

# fill the vocabulary list with all entries of all pages
# this might take some time...
for page in range(1, pages+1):
    filters["page"] = str(page) 
    response = hatebase.getVocabulary(filters=filters, format=format)
    en_vocab.append(response["result"])

# dump into json file for later use
with open("hate_vocabulary.json", "w", encoding="utf8") as file:
    json.dump(en_vocab, file)
