# -*- coding: utf-8 -*-
from flask import Flask,render_template,request,jsonify
import requests
import json
import sys
from build_search import mongo_manager
from build_search import buildIndex
from build_search import loadPDF
app=Flask(__name__)
index_name='malextend'
type_name='fulltext'
#2018.3.3 upload
import os
from werkzeug import secure_filename
UPLOAD_FOLDER = 'F:/PythonProjects/ElasticSearchWeb/build_search/uploadFile/'
ALLOWED_EXTENSIONS = set(['pdf'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    para = json.loads(request.form['para'])
    print(request.form)
    length = int(para['len'])
    for i in range(length):
        file = request.files['f'+str(i)]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            loadPDF.uploadFile(UPLOAD_FOLDER+filename,filename,para)
    return str(request.form['para'])
#2018.3.3 upload end


@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/')
def index__():
    return render_template("index.html")
@app.route('/api/index',methods=['POST'])
def stat():
    data=mongo_manager.statistic()
    res = {}
    res['sum'] = []
    res['sum'].append(data["pdf"])
    res['sum'].append(data["other"])
    res['ioc']=data['report']
    res['actor']=data['actor']
    #res['ioc'] = ["www.asd.com","asdkhas.cn","qeqeeq.net","www.asd.com","asdkhas.cn","qeqeeq.net","www.asd.com","asdkhas.cn","qeqeeq.net","asdjds.cd"]
    #res['actor'] = ["www.asd.com","asdkhas.cn","qeqeeq.net","www.asd.com","asdkhas.cn","qeqeeq.net","www.asd.com","asdkhas.cn","qeqeeq.net","yuiyui.du"]
    return json.dumps(res)


@app.route('/api',methods=['POST'])
def index___():
    print(request.form['search[value]'])
    if request.form['search[value]']=='':
        start = int(request.form['start'])
        end=int(request.form['length'])+start
        res=mongo_manager.getAllReportData(start, end)
        #return mongo_manager.getAllReportData(start, end)
    else:
        res=buildIndex.prep_sea_res(request.form['search[value]'])
    res['draw'] = request.form['draw']
    return json.dumps(res)

@app.route('/api/details',methods=['POST'])
def index_details():
    md5 = request.form['md5']
    return mongo_manager.getMD5Data(md5)
@app.route('/actor/details',methods=['POST'])
def index_actor_details():
    name = request.form['md5']
    return json.dumps(mongo_manager.getNameActor(name))

@app.route('/api/details/post',methods=['POST'])
def index_details_post():
    data = request.form['data']
    print("------------------------------------")
    print(data)
    mongo_manager.updateReportData(json.loads(data))
    return ""

@app.route('/actor/details/post',methods=['POST'])
def index_actor_details_post():
    data = request.form['data']
    # print("------------------------------------")
    # print(data)
    mongo_manager.updateActorData(dict(json.loads(data)))
    return ""

@app.route('/actor/details/new',methods=['POST'])
def index_actor_details_new():
    data = request.form['data']
    # print("------------------------------------")
    # print(data)
    mongo_manager.postActors(json.loads(data))
    return ""

@app.route('/manege-list.html')
def index_manage():
    return render_template("manege-list.html")

@app.route('/actor-list.html')
def index_actor():
    return render_template("actor-list.html")

@app.route('/actor',methods=['POST'])
def index_actor_list():
    if request.form['search[value]'] == '':
        start = int(request.form['start'])
        end = int(request.form['length']) + start
        res = mongo_manager.getAllActorData(start, end)
        # return mongo_manager.getAllReportData(start, end)
    else:
        res = buildIndex.searchActor(request.form['search[value]'])
    res['draw'] = request.form['draw']
    return json.dumps(res)
@app.route('/actor/details/search/items',methods=['GET'])
def actor_detail_search_item():
    queryStr=request.args.get("q")
    return json.dumps(buildIndex.queryActorNameList(queryStr))
@app.route('/link',methods=['POST'])
def actor_link():
    data = json.loads(request.form['data'])
    md5=data['report_md5']
    name=data['actor_name']
    mongo_manager.actorAttachRep(name,md5)
    return ""
@app.route('/newlink',methods=['POST'])
def actor_new_link():
    data = json.loads(request.form['data'])
    md5=data['report_md5']
    actor=data['actor']
    mongo_manager.addActAttachRep(actor,md5)
    return ""

@app.route('/audit.html')
def index_audit():
    return render_template("audit.html")

@app.route('/list.html')
def index_():
    return render_template("list.html")

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

@app.route('/upload.html')
def upload():
    return render_template("upload.html")



if __name__=='__main__':
    app.debug=True
    app.run(host='127.0.0.1',port=8989)
