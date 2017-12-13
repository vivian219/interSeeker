from mongoengine import *
import redis_manager
import json
class stixReport(Document):
    ID=StringField(required=True,primary_key=True)
    Title=StringField(required=True)
    Abstract=StringField(required=True)
    Tag=StringField(required=True)
    URL=StringField(required=True)
    vendors=StringField()
    Status=StringField()
    Date=StringField(required=True)
    Description=StringField()
    TLP=IntField()
    Related=ListField(StringField())
    Actors=StringField()
    STIX2_Attack=StringField()
    Pattern=StringField()
    STIX2_Campaign=StringField()
    STIX2_Course_of_Action=StringField()
    STIX2_Identity=StringField()
    STIX2_Intrusion_Set=StringField()
    STIX2_Malware=StringField()
    STIX2_Observed_Data=StringField()
    STIX2_Tool=StringField()
    STIX2_Vulnerability=StringField()


class stixThreatActor(Document):
    Name=StringField(required=True,primary_key=True)
    First_Sighting=StringField()
    Description=StringField()
    Criticality=IntField()
    Classification_Family=StringField()
    Classification_ID=StringField()
    TLP=StringField()
    Actor_Types=StringField()
    Motivations=StringField()
    Aliases=StringField()
    Communication_Addresses=StringField()
    Financial_Accounts=StringField()
    Country_Affiliations=StringField()
    Known_Targets=StringField()
    Actor_Suspected_Point_of_Origin=StringField()
    Infrastructure_IPv4s=StringField()
    Infrastructure_FQDNs=StringField()
    Infrastructure_Action=StringField()
    Infrastructure_Ownership=StringField()
    Infrastructure_Status=StringField()
    Infrastructure_Types=StringField()
    Detection_Rules=StringField()

connect('monoengine_test',host='localhost',port=27017)

obj_sub=redis_manager.TxtRedis()
redis_sub=obj_sub.subscribe()
'''
msg format
        self.md5=_md5
        self.content=_content
        self.time = _txt.time
        self.title = _txt.title
        self.abstract = _txt.abstract
        self.tag = _txt.tag
        self.urlList = _txt.urlList
'''
def listen():
    while True:
        msg=json.loads(redis_sub.parse_response()[2])
        print(msg)
        post=stixReport(ID=msg["md5"],Title=msg["title"],Abstract=msg["abstract"],Tag=msg["tag"],URL=msg["urlList"],Date=msg["time"])
        post.save()
        print('save')
#listen()
def getAllData():
    alldata=stixReport.objects.all()
    for data in alldata:
        print("title",data.Title,"abstract",data.Abstract)
getAllData()
# class Post(Document):
#     title=StringField(required=True,max_length=200)
#     content=StringField(required=True)
#     author=StringField(required=True)
#     published=DateTimeField(default=datetime.datetime.now)
# class Post_doc(Document):
#     url=StringField(required=True,unique=True)
#     content=StringField(required=True)
# class Post_fileContxt(Document):
#     url=StringField(required=True,unique=True)
#     content=StringField(required=True)
# def contentToFile(url,content):
#     try:
#         post=Post_fileContxt(url,content)
#         post.save()
#     except:
#         print(url)

#post2=Post_doc(url='127.0.0.1',content='djifjdi')
# post3=Post_doc(url='url1',content='url1-content')
# post4=Post_doc(url='url2',content='url2-content')
# post5=Post_doc(url='url3',content='url3-content')
# post1=Post(
#     title='Sample Post',
#     content='Some engaging content',
#     author='Scott'
# )
#post2.save()
# post3.save()
# post4.save()
# post5.save()
# #print(post2.url)
# for post in Post_fileContxt.objects:
#     print('url'+post.url)
#     print('content'+post.content)
    #print('content'+post.content.strip())
# doc2=Post_doc.objects(url='url1')
# for post in doc2:
#     print(post.content)
# print(doc2.content)
# post1.title='A Better Post Title'
# post1.save()
# print(post1.title)
# post3=Post_doc(
#     url='127.0.0.1',
#     content='djifjdifdf'
# )
# post3.save()

# print(post3.url)