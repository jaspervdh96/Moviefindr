import json
import os
from collections import Counter
import io


json_data = []
for x in (json.loads(io.open('data/'+f, "r", encoding='ISO-8859-1').read()) for f in os.listdir('data') if f.endswith('.json')):
    if "Genre" in x:
        json_data += x["Genre"].split(', ')

print([str(x[0]) for x in Counter(json_data).most_common(22)])