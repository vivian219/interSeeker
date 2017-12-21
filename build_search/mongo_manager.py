from mongoengine import *
import json
import buildIndex

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
    Actors=StringField()
    Related_Reports=StringField(required=True)
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
    TLP=StringField()
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

connect('mongo_engine_db', host='localhost', port=27017)
def getAllReportData(start,end):
    allReport=stixReport.objects.order_by('Date')
    requiredData=allReport[start:end]
    requiredlist=[]
    data={}
    #data["draw"]="2"
    data["recordsTotal"]=len(requiredData)
    data[ "recordsFiltered"]=len(requiredData)
    for item in requiredData:
        #print(item.to_mongo)
        # print(item.ID)
        print(item.to_mongo())
        #print(item)
        _dict=dict(item.to_mongo())
        #print(_dict)
        _list=getReportList(_dict)
        #print("id",_dict['ID'])
        requiredlist.append(_list)
        #print(_list)
    data["data"]=requiredlist
    #print(json.dumps(data))
    return data
    #print(json.dumps(requiredlist))
def getReportList(_dict):
    _list = []
    _list.append(getIndexData('_id', _dict))
    _list.append(getIndexData("Title", _dict))
    _list.append(getIndexData("Date", _dict))
    _list.append(getIndexData("vendors", _dict))
    _list.append(getIndexData('Status', _dict))
    _list.append(getIndexData('TLP', _dict))
    return _list
def getIndexData(index,_dict):
    try:
        data=_dict[index]
    except:
        data=""
    return data

def getMD5Data(md5):
    _report=stixReport.objects(ID=md5)
    ind=stixIndicator.objects(Related_Reports=md5)
    report=dict(_report[0].to_mongo())
    report_list=getReportList(report)
    #report_list[0]=md5
    merge_dict={}
    merge_dict['report']=report_list
    merge_dict['labels']=getIndexData('Tag',report)
    merge_dict['abstract']=getIndexData('Abstract',report)
    urls=[]
    for _ind in ind:
        ind_dict={}
        __ind = dict(_ind.to_mongo())
        ind_dict["id"]=getIndexData("_id",__ind)
        ind_dict["url"]=getIndexData('IOC_URL',__ind)
        ind_dict["md5"]= getIndexData('IOC_MD5', __ind)
        ind_dict["domains"]=getIndexData('IOC_Domain', __ind)
        ind_dict["ipv4"]=getIndexData('IOC_IPV4', __ind)
        ind_dict["actors"]=getIndexData('Actors', __ind)
        ind_dict["reports"]= getIndexData('Related_Reports', __ind)
        urls.append(ind_dict)
        #print(ind_dict)
        #_b.update(json.loads(a))
        # for item in _ind:
        #     print("item",)
    merge_dict["urls"]=urls
    try:
        desc=_report[0].Description
    except:
        desc=""
    try:
        actors=_report[0].Actors
    except:
        actors=""
    merge_dict["desc"]=desc
    merge_dict["actors"]=actors
    #print(json.dumps(merge_dict))
    return json.dumps(merge_dict)
def updateReport(report,labels,abstract,desc,actors):
    id=report[0]
    rep_obj = stixReport.objects(ID=id)
    rep_obj.update(Title=report[1])
    rep_obj.update(Date=report[2])
    rep_obj.update(vendors=report[3])
    rep_obj.update(Status=report[4])
    rep_obj.update(TLP=report[5])
    rep_obj.update(Tag=labels)
    rep_obj.update(Abstract=abstract)
    rep_obj.update(Description=desc)
    rep_obj.update(Actors=actors)
    # print(actors)
    # print(desc)
def updateIndicator(ind):
    id=ind['id']
    ind_obj = stixIndicator.objects(ID=id)
    ind_obj.Related_Reports=ind['reports']
    ind_obj.update(IOC_URL=ind['url'])
    ind_obj.update(IOC_MD5=ind['md5'])
    ind_obj.update(IOC_Domain=ind['domains'])
    ind_obj.update(IOC_IPV4=ind['ipv4'])
    ind_obj.update(Actors=ind['actors'])
    #print(ind['actors'])
def updateData(data):
    report=data["report"]
    labels=data["labels"]
    abstract=data["abstract"]
    #urls=data['urls']
    desc=data['desc']
    actors=data['actors']
    updateReport(report,labels,abstract,desc,actors)
    temp =stixReport.objects(ID=report[0])
    rep_data= stixReport.objects(ID=report[0])[0].to_mongo()
    buildIndex.updateData(report[0],dict(rep_data))
    # for url in urls:
    #     updateIndicator(url)
getAllReportData(0,5)
#getMD5Data("1d7ae8f7f5e5f0ce0171c021be32976c")
"""
updateData(
{
  "report": [
    "1d7ae8f7f5e5f0ce0171c021be32976c",
    "\u57fa\u7840\u8bbe\u65bd\u9493\u9c7c new",
    "20171218-5",
    " new",
    " new",
    " new"
  ],
  "labels": "\u57fa\u7840\u8bbe\u65bd; \u9493\u9c7c new",
  "abstract": "\u5b89\u5168\u5382\u5546\u601d\u79d1Talos\u7814\u7a76\u56e2\u961f\u53d1\u5e03\u9488\u5bf9\u57fa\u7840\u8bbe\u65bd\u7684\u9493\u9c7c\u6d3b\u52a8\u7684\u5206\u6790\u62a5\u544a\u3002\u81ea2017\u5e745\u6708\uff0cTalos\u5df2\u7ecf\u89c2\u5bdf\u5230\u9488\u5bf9\u6b27\u6d32\u548c\u7f8e\u56fd\u7684\u57fa\u7840\u8bbe\u65bd\u548c\u80fd\u6e90\u516c\u53f8\u7684\u9493\u9c7c\u653b\u51fb\u3002\u90ae\u4ef6\u9644\u4ef6\u672c\u8eab\u5e76\u4e0d\u542b\u6709\u6076\u610f\u4ee3\u7801\uff0c\u4f46\u9644\u4ef6\u8bd5\u56fe\u901a\u8fc7SMB\u670d\u52a1\u8fde\u63a5\u4e0b\u8f7d\u6a21\u677f\u6587\u4ef6\uff0c\u8be5\u6a21\u677f\u6587\u4ef6\u53ef\u4ee5\u4e0b\u8f7d\u5176\u4ed6\u6076\u610f\u8d1f\u8f7d\uff0c\u4ee5\u6b64\u9759\u9ed8\u6536\u96c6\u7528\u6237\u7684\u51ed\u636e\u3002 new",
  "urls": [
    {
      "id": "2daac820a83f7dbbc86efa4fe0dbf054",
      "url": " http://blog.talosintelligence.com/2017/07/template-injection.html",
      "md5": "['ac6c1df3895af63b864bb33bf30cb31059e247443ddb8f23517849362ec94f08 new', 'b02508baf8567e62f3c0fd14833c82fb24e8ba4f0dc84aeb7690d9ea83385baa', '93cd6696e150caf6106e6066b58107372dcf43377bf4420c848007c10ff80bc9', '3d6eadf0f0b3fb7f996e6eb3d540945c2d736822df1a37dcd0e25371fa2d75a0']",
      "domains": "['www.blogblog.com new', 'apis.google.com', 'blog.talosintelligence.com', 'www.google-analytics.com', 'www.talosintelligence.com', '3.bp.blogspot.com', 'www.blogger.com']",
      "ipv4": "[ new]",
      "actors": "new",
      "reports": "1d7ae8f7f5e5f0ce0171c021be32976c"
    }
  ],
  "desc": " new",
  "actors": " new"
}

)
"""