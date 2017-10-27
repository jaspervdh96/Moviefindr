import requests
import json

synlist = []

with open('Synonyms.csv') as f:
    syns = f.readlines()
    for x in syns:
        s = json.loads(requests.get("http://localhost:9200/test/_analyze", data=json.dumps({"analyzer":"my_analyzer","text": x.replace(',', ' ')})).text)
        test = [x["token"] for x in s["tokens"]]

        if len(test) > 1:
            synlist.append(", ".join(list(set(test))))
            print(test)
            
base = {"settings":{"analysis":{}},"mappings" : {"document" : {"properties" : {"body" : { "type" : "string", "analyzer" : "my_analyzer" }}}}}

#analyzer = {"my_analyzer":{"tokenizer":"standard","filter":["standard","lowercase","my_stemmer", "my_syn_filter"]}}
#stemmer = {"type":"stemmer","name":"english"}
#synonyms = {"type": "synonym", "synonyms": synlist}

#base["settings"]["analysis"]["filter"] = {"my_stemmer": stemmer, "my_syn_filter": synonyms}
#base["settings"]["analysis"]["analyzer"] = analyzer

#result = requests.put("http://localhost:9200/moviefindr", data=json.dumps(base)).text
#print(result)


with open('syn.txt', "w") as f:
    for x in synlist:
        f.write(x+'\n')