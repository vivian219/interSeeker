# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 20:25:56 2017

@author: Vivian
"""
import requests
from elasticsearch import Elasticsearch
import json
#index_name = "actor"
#index_name="indicator"
index_name="report"
#type_name = "fulltext"
type_name = "exact_match"
es=Elasticsearch()
def buildIndex():
    # 使用PUT请求创建一个索引
    #print("build index")
    es.indices.create(index="actor", ignore=400)
    # res = requests.put("http://localhost:9200/{0}".format(index_name))
    # print(res.content.decode('utf8'))
    # 设置分词
    data = {
        type_name: {
                 "_all": {
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_max_word",
                "term_vector": "no",
                "store": "false"
            },
            "properties": {
                "Content": {
                    "type": "text",
                    "analyzer": "ik_max_word",
                    "search_analyzer": "ik_max_word",
                    "include_in_all": "true",
                    "boost": 8
                }
            }
        }
    }
    # res = requests.post("http://localhost:9200/{0}/{1}/_mapping".format(index_name,"fulltext"), json=data)
    # print(res.content.decode('utf8'))

def document_exist(md5):
    http_template='http://localhost:9200/{0}/{1}/_search?q=md5:{2}'.format(index_name,type_name,md5)
    res = json.loads(requests.get(http_template).content.decode('utf8'))
    if "hits" in res.keys():
        if res["hits"]["total"] == 0:
            return False
        else:
            return True
    return False


def post_document(index_name,docDict):
    """
    docDict:ip,domain,hashValue,url
    """
    data=docDict
    print("Doc posted:{0}".format(data))
    # 使用PUT请求将所有文档存入该索引
    res = requests.post("http://localhost:9200/{0}/fulltext".format(index_name),
                  json=data)


def prepare_dict(docStr):
    """
    将结构化信息转换成 ES 需要的字典格式
    :param docStr: 以,分割的结构化信息字符串
    :return: ES 需要的字典格式
    """
    word=docStr.split(",")
    return {"url": word[0], "ip": word[1], "domainName": word[2], "filehash": word[3]}

"""
初始化搜索引擎里的索引,仅需要运行一次即可
"""
def initial():       
    buildIndex()

"""
向搜索引擎中加入新文档的索引
"""
def addNewDoc(resList):
    for res in resList:
        resDict=prepare_dict(res)
        post_document(index_name, resDict)
def queryIndicator(queryStr):
    res=es.search(index="report", body={"query": {"match": {"_all":queryStr}}})
def queryActor(queryStr):
    res=es.search(index="report", body={"query": {"match": {"_all": queryStr}}})
def queryReport(queryStr):
    res=es.search(index="report", body={"query": {"match": {"_all": queryStr}}})
def queryIndex(index,con,queryStr):
    res = es.search(index=index, body={"query": {"match": {con:queryStr}}})
    resList=[]
    for hit in res['hits']['hits']:
        resList.append(hit["_source"])
    return resList
def queryReport(sourceItem,index,queryStr,res):
    for item in sourceItem:
        item_res=queryIndex("report",index,queryStr)
        for _res in item_res:
            res.append(_res)
    return res
def indexDict(dict,index):
    try:
        res=dict[index]
    except:
        res=""
        #print(dict)
    return res
def prep_sea_res(queryStr):
    res={}
    res['draw']=2
    res['recordTotal']=1
    res['recordsFiltered']=1
    resList=queryAll(queryStr)
    data=[]
    for item in resList:
        item_list=[]
        item_list.append(indexDict(item,'md5'))
        item_list.append(indexDict(item,'title'))
        item_list.append(indexDict(item,'time'))
        item_list.append(indexDict(item,'vendors'))
        item_list.append(indexDict(item,'status'))
        item_list.append(indexDict(item,'tlp'))
        data.append(item_list)
    res['data']=data
    return json.dumps(res)
def queryAll(queryStr):
    res=queryIndex("report","_all",queryStr)
    #print(res)
    ind=queryIndex("indicator","_all",queryStr)
    #print(ind)
    res=queryReport(ind,"'report_md5",queryStr,res)
    #print(res)
    # act=queryIndex("actor","_all",queryStr)
    # res=queryReport(act,"")
    return res

def queryAllInfo(index):
    res = es.search(index=index, body={"query": {"match_all": {}}})
    for hit in res['hits']['hits']:
        print(hit['_source'])
if __name__ == "__main__":
    #initial()
    #queryAllInfo("indicator")
    res=queryAll("paper.seebug.org")
    print(res)