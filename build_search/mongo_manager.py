from mongoengine import *
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

connect('monoengine_test', host='localhost', port=27017)
def getAllReportData(start,end):
    allReport=stixReport.objects.order_by('Date')
    requiredData=allReport[start:end]
    requiredlist=[]
    data={}
    data["draw"]="2"
    data["recordsTotal"]=37
    data[ "recordsFiltered"]=37
    for item in requiredData:
        #print(item.to_mongo)
        print(item.ID)
        print(item.to_mongo())

        #print(item)
        _dict=dict(item.to_mongo())
        print(_dict)
        _list=getReportList(_dict)
        #print("id",_dict['ID'])
        requiredlist.append(_list)
        #print(_list)
    data["data"]=requiredlist
    #print(json.dumps(data))
    return json.dumps(data)
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
        ind_dict["url"]=getIndexData('IOC_URL',__ind)
        ind_dict["md5"]= getIndexData('IOC_MD5', __ind)
        ind_dict["domains"]=getIndexData('IOC_Domain', __ind)
        ind_dict["ipv4"]=getIndexData('IOC_IPV4', __ind)
        ind_dict["actors"]=getIndexData('Actors', __ind)
        ind_dict["reports"]= getIndexData('Related_Reports', __ind)
        urls.append(ind_dict)
        print(ind_dict)
        #_b.update(json.loads(a))
        # for item in _ind:
        #     print("item",)
    merge_dict["urls"]=urls
    try:
        desc=_report.Description
    except:
        desc=""
    try:
        actors=_report.Actors
    except:
        actors=""
    merge_dict["desc"]=desc
    merge_dict["actors"]=actors
    #print(json.dumps(merge_dict))
    return json.dumps(merge_dict)
#getAllReportData(0,5)
getMD5Data("1d7ae8f7f5e5f0ce0171c021be32976c")