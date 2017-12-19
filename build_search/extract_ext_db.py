from mongoengine import *
import redis_manager
import json
import mongo_manager
import buildIndex

connect('monoengine_test', host='localhost', port=27017)
index="indicator"

obj_sub = redis_manager.ParserRedis()
redis_sub = obj_sub.subscribe()
def listen():
    while True:

        msg = json.loads(redis_sub.parse_response()[2])
        if buildIndex.document_exist("indicator"+msg['md5'])==False:
            buildIndex.post_document(index, msg)
        #print(msg)#print(redis_sub.parse_response())
        post = mongo_manager.stixIndicator(ID="indicator"+msg["md5"],IOC_MD5=msg["hash_list"],
                             IOC_Domain=msg["dom_list"],IOC_IPV4=msg["ip_list"],
                             Related_Reports=msg["report_md5"],IOC_URL=msg["url"])
        #print(msg["ip_list"])
        post.save()
def getAllData():
    alldata=mongo_manager.stixIndicator.objects.all()
    #for data in alldata:
        #print(data.to_mongo())
        #print("ID",data.ID,"ip list",data.IOC_IPV4,"related report",data.Related_Reports)
def deleteData():
    alldata = mongo_manager.stixIndicator.objects.all()
    for data in alldata:
        mongo_manager.stixIndicator.delete(data)
        #print("ID", data.ID, "ip list", data.IOC_IPV4, "related report", data.Related_Reports)
listen()
#getAllData()
#deleteData()