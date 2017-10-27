import nltk
import csv
from nltk.stem.porter import *
from nltk.corpus import wordnet
import requests
import itertools
import os
import json
voc = []
for doc in os.listdir("data/")[0:2]:
	print(doc)
	if doc.endswith(".json"):
		with open("data/"+doc) as f:
			voc +=[x["token"] for x in json.loads(requests.post("http://localhost:9200/moviefindr/_analyze", data={"tokenizer":"standard","filter":"lowercase","text":json.load(f)["body"]}).text)["tokens"]]

##TOKENIZE EVERYTHING
csvfile = open('Synonyms.csv', 'w')
csvwriter = csv.writer(csvfile, delimiter=',')
for word in voc:
    for syn in wordnet.synsets(word):
    	syn2 = syn.name().split('.', 1 )[0]
    	if syn2 != word:
    		print([word, syn.name().split('.', 1 )[0]])
        	csvwriter.writerow([word, syn.name().split('.', 1 )[0]])