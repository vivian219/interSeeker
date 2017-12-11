# -*- coding: utf-8 -*-
from flask import Flask,render_template,request,jsonify
import requests
import json

app=Flask(__name__)
index_name='maltest2'
type_name='fulltext'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search',methods=['POST'])
def search_text():
    query=request.form['query']
    field=request.form['field']
    infos=search(field,query,index_name,type_name)
    return jsonify(infos)

def search(field,query,index_str,type_str):
    http_template='http://localhost:9200/{0}/{1}/_search?q={2}:{3}'.format(index_str,type_str,field,query)
    print(http_template)
    res = json.loads(requests.get(http_template).content.decode('utf8'))
    new_list = []
    if "hits" in res.keys():
        for item in res["hits"]["hits"]:
            new_list.append(item["_source"])
    print(new_list)
    return new_list
'''
def hello_world():
    return 'Hello World!'
'''
if __name__=='__main__':
    app.debug=True
    app.run(host='127.0.0.1',port=8989)