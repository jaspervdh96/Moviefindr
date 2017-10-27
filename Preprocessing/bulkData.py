import sys
import json
import io
import elasticsearch
import os
import elasticsearch.helpers

HOST = 'http://localhost:9200/'
es = elasticsearch.Elasticsearch(hosts=[HOST], timeout=120)

def default_dict(data):
    if data["Response"] != "False":
        return {'_index': 'moviefindr', '_type': 'document', '_source': data}
    else:
        return False

actions = (default_dict(json.loads(io.open('data/'+f, "r", encoding='ISO-8859-1').read())) for f in os.listdir('data') if f.endswith('.json'))
for x in elasticsearch.helpers.streaming_bulk(es, (x for x in actions if x), chunk_size=5):
    print(x)