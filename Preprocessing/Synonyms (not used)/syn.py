import nltk
import csv
from nltk.stem.porter import *
from nltk.corpus import wordnet
import nltk
import requests
import itertools
import os
import json
import re

voc = []
for doc in os.listdir("TextFolder/"):
    print(doc)
    if doc.endswith(".json"):
        with open("TextFolder/"+doc) as f:
            voc +=[x.lower() for x in nltk.tokenize.word_tokenize(json.load(f)["body"]) if re.match(r'\w+', x)]
voc = list(set(voc))
##TOKENIZE EVERYTHING
csvfile = open('Synonyms.csv', 'w')
csvwriter = csv.writer(csvfile, delimiter=',')
for word in voc:
    syns = wordnet.synsets(word)
    if len(syns)>0:
        csvwriter.writerow(list(set([word]+[x.name().split('.', 1 )[0] for x in syns])))
