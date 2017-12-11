# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 20:25:56 2017

@author: Vivian
"""
import requests
import json

index_name = "maltest2"
#type_name = "fulltext"
type_name = "exact_match"

def buildIndex(index_name):
    # 使用PUT请求创建一个索引
    res = requests.put("http://localhost:9200/{0}".format(index_name))
    print(res.content.decode('utf8'))
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
    res = requests.post("http://localhost:9200/{0}/{1}/_mapping".format(index_name,"fulltext"), json=data)


def document_exist(url):
    http_template='http://localhost:9200/{0}/{1}/_search?q=url:{2}'.format(index_name,type_name,url)
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
    buildIndex(index_name)

"""
向搜索引擎中加入新文档的索引
"""
def addNewDoc(resList):
    for res in resList:
        resDict=prepare_dict(res)
        post_document(index_name, resDict)

if __name__ == "__main__":
    initial()