from mongoengine import *
import json
import buildIndex
import time

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
    LoginTime=StringField()
    Related_Reports=StringField(required=True)
class stixReport(Document):
    ID=StringField(required=True,primary_key=True)
    Title=StringField()
    Abstract=StringField()
    Tag=StringField()
    URL=StringField()
    vendors=StringField()
    Status=StringField()
    Date=StringField()
    Description=StringField()
    TLP=StringField()
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
    Source=StringField()
    LoginTime = StringField()

class stixThreatActor(Document):
    Name=StringField(required=True,primary_key=True)
    First_Sighting=StringField()
    Description=StringField()
    Criticality=StringField()
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
    LoginTime = StringField()
class Event(Document):
    Event_id=StringField()
    Event_time=StringField()

connect('mongo_engine_db', host='localhost', port=27017)
def getAllReportData(start,end):
    allReport=stixReport.objects.order_by('Date')
    if end==-1:
        end=len(allReport)
    requiredData=allReport[start:end]
    requiredlist=[]
    data={}
    #data["draw"]="2"
    data["recordsTotal"]=len(allReport)
    data[ "recordsFiltered"]=len(allReport)
    for item in requiredData:
        #print(item.to_mongo)
        # print(item.ID)
        #print(item.to_mongo())
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
    _list.append(getIndexData('Source',_dict))
    return _list
def getAllActorData(start,end):
    allActor = stixThreatActor.objects.order_by('Name')
    if end>len(allActor):
        end=len(allActor)
    requiredData = allActor[start:end]
    data = {}
    data["recordsTotal"] = len(allActor)
    data["recordsFiltered"] = len(allActor)
    dataList=[]
    for item in requiredData:
        itemList=[]
        #print(item.to_mongo())
        # print(item)
        _dict = dict(item.to_mongo())
        itemList.append(_dict['_id'])
        itemList.append(_dict['First_Sighting'])
        itemList.append(_dict['Criticality'])
        itemList.append(_dict['Classification_Family'])
        itemList.append(_dict['TLP'])
        itemList.append(_dict['LoginTime'])
        #requiredlist.append(_dict)
        dataList.append(itemList)
        # print(_list)
    data["data"] = dataList
    return data
def getActorNameList():
    allActor = stixThreatActor.objects.order_by('Name')
    for item in allActor:
        _dict = dict(item.to_mongo())

def getNameActor(name):
    actor=stixThreatActor.objects(Name=name)[0].to_mongo()
    #print(actor)
    return dict(actor)
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
        if desc==None:
            desc=""
    except:
        desc=""
    try:
        actors=_report[0].Actors
        if actors==None:
            actors=""

    except:
        actors=""
    actorList=[]
    if actors!="":
        _actorList=actors.split(";")
        for item in _actorList:
            actorList.append([item])

    merge_dict["desc"]=desc
    merge_dict["actors"]=actorList
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
def updateReportData(data):
    report=data["report"]
    labels=data["labels"]
    abstract=data["abstract"]
    #urls=data['urls']
    desc=data['desc']
    actors=data['actors']
    updateReport(report,labels,abstract,desc,actors)
    rep_data= stixReport.objects(ID=report[0])[0].to_mongo()
    buildIndex.updateReportData(report[0],dict(rep_data))
    # for url in urls:
    #     updateIndicator(url)
def updateActorData(data):
    stixThreatActor.objects(Name=data['name']).delete()
    # print("a"+str(a))
    # a.delete()
    postActors(data)
    act_data = stixThreatActor.objects(Name=data['name'])[0].to_mongo()
    buildIndex.updateActorData(dict(act_data))

def postActors(data):
    _time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    post=stixThreatActor(
        Name=data['name'],
        First_Sighting = data['first_sighting'],
        Description = data['description'],
        Criticality = data['criticality'],
        Classification_Family = data['classification_family'],
        Classification_ID =data['classification_id'],
        TLP = data['tlp'],
        Actor_Types = data['actor_types'],
        Motivations = data['motivations'],
        Aliases = data['aliases'],
        Communication_Addresses =data['communication_addresses'],
        Financial_Accounts =data['financial_accounts'],
        Country_Affiliations = data['country_affiliations'],
        Known_Targets = data['known_targets'],
        Actor_Suspected_Point_of_Origin = data['actor_suspected_point_of_origin'],
        Infrastructure_IPv4s = data['infrastructure_ipv4s'],
        Infrastructure_FQDNs = data['infrastructure_fqdns'],
        Infrastructure_Action = data['infrastructure_action'],
        Infrastructure_Ownership = data['infrastructure_ownership'],
        Infrastructure_Status =data['infrastructure_status'],
        Infrastructure_Types = data['infrastructure_types'],
        Detection_Rules = data['detection_rules'],
        LoginTime=str(_time)
    )
    post.save()
    if buildIndex.document_exist("actor", "Name",data['name']) == False:
        rep_data =stixThreatActor.objects(Name=data["name"])[0].to_mongo()
        rep_data = dict(rep_data)
        id = rep_data['_id']
        rep_data.pop('_id', None)
        rep_data['Name'] = id
        res = buildIndex.post_document("actor", rep_data)
        print(data['name']+"is new!")
    else:
        print(data['name']+"exist!!")
def actorAttachRep(actorName,reportMd5):
    report=stixReport.objects(ID=reportMd5)[0]
    actors=report['Actors']
    #print("post new actor",actors)
    if actors==None:
        reportActors=actorName
    else:
        actorList=actors.split(";")
        #print("actorList",actorList)
        if actorName not in actorList:
            reportActors=report.Actors+";"+actorName
            #print("if ",reportActors)
        else:
            reportActors = report.Actors
            #print("else",reportActors)
    report.update(Actors=reportActors)

    rep_data = stixReport.objects(ID=reportMd5)[0].to_mongo()
    buildIndex.updateReportData(reportMd5,dict(rep_data))
def addActAttachRep(actor,reportMd5):
    postActors(actor)
    actorAttachRep(actor['name'],reportMd5)
def deleteData():
    stixThreatActor.objects().delete()
    stixReport.objects().delete()
    stixIndicator.objects().delete()
def statistic():
    allReport = stixReport.objects.order_by('-LoginTime')
    #allIndicator=stixIndicator.objects.order_by('-LoginTime')
    allActor=stixThreatActor.objects.order_by('-LoginTime')
    #print("all actor",allActor)
    pdfObj=0
    otherObj=0
    data={}
    for _report in allReport:
        report=dict(_report.to_mongo())
        try:
            if report["Source"]=="pdf":
                pdfObj+=1
            elif report["Source"]=="txt" or report["Source"]=="excel":
                otherObj+=1
        except:
            pass
    reportList=[]
    actorList=[]
    reportLen=0
    actorLen=0
    if len(allReport)<10:
        reportLen=len(allReport)
    else:
        reportLen=10

    if len(allActor)<10:
        actorLen=len(allActor)
    else:
        actorLen=10
    #print("actor len",actorLen)
    _reportList=allReport[0:reportLen]
    _actorList=allActor[0:actorLen]
    for _report in _reportList:
        __report=dict(_report.to_mongo())
        reportList.append(__report['Title'])
    for _actor in _actorList:
        __actor=dict(_actor.to_mongo())
        #print(__actor)
        actorList.append(__actor['_id'])
    data["pdf"]=pdfObj
    data["other"]=otherObj
    data["report"]=reportList
    data["actor"]=actorList
    return data
data=statistic()
print(data['report'])
print(data['actor'])
#deleteData()
#print(getAllActorData(0,1))
#print(getNameActor('APT10'))
#print(getMD5Data("66029002775c24ed3287fa6b1cc175b9"))
#getAllReportData(0,5)
#getMD5Data("1d7ae8f7f5e5f0ce0171c021be32976c")