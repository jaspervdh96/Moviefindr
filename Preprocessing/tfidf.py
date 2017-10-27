from sklearn.feature_extraction.text import TfidfVectorizer
import json
import os
import io


tfidf = TfidfVectorizer(input='content', max_df=0.7, sublinear_tf=True)
tfidfmatrix = tfidf.fit_transform(json.loads(io.open('TextFolder/'+f, "r", encoding='ISO-8859-1').read())["body"] for f in os.listdir('TextFolder') if f.endswith('.json'))

vectors = tfidfmatrix.toarray().tolist()
names = tfidf.get_feature_names()
ids = [json.loads(io.open('TextFolder/'+f, "r", encoding='ISO-8859-1').read()).get("imdbID", "onzin") for f in os.listdir('TextFolder') if f.endswith('.json')]

vectordict = dict(zip(ids, vectors))
vectordict["names"] = names

for x in vectordict:
    with open('tfidf/'+x+'.json', "w") as f:
        f.write(json.dumps(vectordict[x]))
