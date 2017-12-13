from mongoengine import *
import redis_manager
import json

class stixIndicator(Document):
    ID=StringField(required=True,primary_key=True)
    IOC_MD5=StringField(required=True)
    IOC_SHA1=StringField()
    IOC_EMAIL=StringField()
    IOC_SHA256=StringField()
    IOC_String=StringField()
    IOC_URL=StringField()
    IOC_Domain=StringField(required=True)
    IOC_IPV4=StringField(required=True)
    Related=StringField()
    Actors=StringField()
    Related_Reports=StringField(required=True)

connect('monoengine_test', host='localhost', port=27017)

obj_sub = redis_manager.ParserRedis()
redis_sub = obj_sub.subscribe()
def listen():
    while True:
        #print(redis_sub.parse_response())
        msg = json.loads(redis_sub.parse_response()[2])
        post = stixIndicator(ID="indicator"+msg["md5"],IOC_MD5=msg["hash_list"],
                             IOC_Domain=msg["dom_list"],IOC_IPV4=msg["ip_list"],
                             Related_Reports=msg["report_md5"])
        print(msg["ip_list"])
        post.save()
def getAllData():
    alldata=stixIndicator.objects.all()
    for data in alldata:
        print("ID",data.ID,"ip list",data.IOC_IPV4,"related report",data.Related_Reports)
def deleteData():
    alldata = stixIndicator.objects.all()
    for data in alldata:
        stixIndicator.delete(data)
        #print("ID", data.ID, "ip list", data.IOC_IPV4, "related report", data.Related_Reports)
#listen()
getAllData()
#deleteData()