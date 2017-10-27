import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import json
import elasticsearch
import io
import re


# config Flask app
app = Flask('MovieFindr')
app.config.update(dict(
    SECRET_KEY='dfgdfssr234rwefherwk543tr',
))
app.config.from_envvar('FLASK_SETTINGS', silent=True)

# config elastic search
HOST = 'http://localhost:9200/'
es = elasticsearch.Elasticsearch(hosts=[HOST])


# route for home page
@app.route('/')
def index():
    return render_template('home.html')

# route for search API
@app.route('/search', methods=["POST"])
def search():
	
	# only POST requests allowed
    if request.method == 'POST':
        
        # get the POST data
        data = request.form
        genres = json.loads(data["genres"]) if "genres" in data else []
        query = data["query"]
        person = data["person"]
        match_phrase = True if data["match_phrase"] == "true" else False
        
        # get upperbound for date and parse to integer
        if data["upperDate"] != "":
            u = re.search(r'\d+', data["upperDate"])
            upperDate = int(u.group())
        else:
            upperDate = ""
        
        # get lowerbound for date and parse to integer
        if data["lowerDate"] != "":
            l = re.search(r'\d+', data["lowerDate"])
            lowerDate = int(l.group())
        else:
            lowerDate = ""
        
        # base query
        q = {"query": {"bool": {"must": [], "filter": []}}}
        
        # add query for the script body according to data
        if query != "":
            if match_phrase:
                q["query"]["bool"]["must"].append({"match_phrase": {"body": query}})
            else:
                q["query"]["bool"]["must"].append({"match":{"body": query}})
        else:
            q["query"]["bool"]["must"].append({"match_all": {}})
        
        # add query for genres if present
        if genres:
            q["query"]["bool"]["filter"].append({"terms": {"Genre": [x.lower() for x in genres]}})
        
        # add query for persons involved if present
        if person != "":
            q["query"]["bool"]["must"].append({"dis_max": {"queries": [{"match": {"Director": person}}, {"match": {"Writer": person}},{"match": {"Actors": person}}]}})
        
        # add query for year of release if present
        if upperDate != "" and lowerDate != "":
            q["query"]["bool"]["filter"].append({"range": {"Year": {"lte": upperDate, "gte": lowerDate}}})
        elif upperDate != "":
            q["query"]["bool"]["filter"].append({"range": {"Year": {"lte": upperDate}}})
        elif lowerDate != "":
            q["query"]["bool"]["filter"].append({"range": {"Year": {"gte": lowerDate}}})
        
        # execute the actual search
        search = elasticsearch.Elasticsearch.search(es, index="moviefindr", doc_type="document", _source_exclude=['body'],\
                                                    body=q, size=12)

        # if there are hits, generate the data for timeline and wordcloud
        if search["hits"]["total"] > 0:
            
            # get the words for TF-IDF vectors
            names = json.loads(io.open("/var/www/MovieFindr/MovieFindr/tfidf/names.json", "r", encoding='ISO-8859-1').read())
            
            # get the TF-IDF vectors for the movies found and merge them
            tfidfs = [json.loads(io.open("/var/www/MovieFindr/MovieFindr/tfidf/"+x["_source"]["imdbID"]+".json", "r", encoding='ISO-8859-1').read()) for x in search["hits"]["hits"]]
            summed = sorted([(x, names[i]) for i, x in enumerate(map(sum, zip(*tfidfs)))], reverse=True, key=lambda x: x[0])[:30]
            
            # put in right format and add to search results
            results = [{"text": x[1], "size": x[0]} for x in summed]
            search["hits"]["tfidf"] = results
            
            # generate data for timeline and add to search results
            search["hits"]["timeline"] = {"events": [{"start_date":{"year": int(re.search(r'\d+', x["_source"]["Year"]).group())}, "text":{"headline": x["_source"]["Title"], "text": x["_source"]["Plot"]}} for x in search["hits"]["hits"]]}
        
        # return results
        return json.dumps(search)

# route for detail page
@app.route('/detail')
def detail():
	
	# get the id from GET request
    id = request.args["id"]

    # search for id
    get = elasticsearch.Elasticsearch.get(es, index="moviefindr", doc_type="document", id=id)
    
    # return search data with template
    return render_template('detail.html', data=get)

# possibility to run development server
if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)