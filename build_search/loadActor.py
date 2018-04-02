import json
import mongo_manager
import buildIndex
import time

f=open('actortrackr_export_20171204.json')
line=f.readline()
lineDict=json.loads(line)
actorList=lineDict['actors']

def listToStr(_list):
    listStr = ""
    first=True
    for item in _list:
        if item != ''and not first:
            listStr += ","
        listStr += item.split('\n')[0]
        first=False
    print("the list item is", _list)
    print("transform list to string is ", listStr)
    return listStr

for _actor in actorList:
    #print(actor)
    # print(_actor.keys())
    # print(_actor['_source'])
    # print(_actor['_source'].keys())
    actor=_actor['_source']
    # print(actor['type'])
    _time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    post=mongo_manager.stixThreatActor(
            Name=actor['name'],
            First_Sighting = actor['created_s'],
            Description = actor['description'],
            Criticality = str(actor['criticality']),
            Classification_Family = actor['classification'][0]['family'],
            Classification_ID =actor['classification'][0]['id'],
            TLP = str(actor['tlp']),
            Actor_Types = listToStr(actor['type']),
            Motivations = listToStr(actor['motivation']),
            Aliases = listToStr(actor['alias']),
            Communication_Addresses =actor['communication_address'][0]['value'],
            Financial_Accounts =listToStr(actor['financial_account'][0]['value']),
            Country_Affiliations = listToStr(actor['country_affiliation']),
            Known_Targets = listToStr(actor['known_target']),
            Actor_Suspected_Point_of_Origin = actor['origin'],
            Infrastructure_IPv4s = listToStr(actor['infrastructure']['ipv4']),
            Infrastructure_FQDNs = listToStr(actor['infrastructure']['fqdn']),
            Infrastructure_Action = actor['infrastructure']['action'],
            #Infrastructure_Ownership = actor['infrastructure_ownership'],
            Infrastructure_Status =actor['infrastructure']['status'],
            Infrastructure_Types = actor['infrastructure']['type'][0],
            Detection_Rules = actor['detection_rule'][0]['value'],
            LoginTime=str(_time)
        )
    post.save()
    if buildIndex.document_exist("actor", "Name",actor['name']) == False:
        rep_actor =mongo_manager.stixThreatActor.objects(Name=actor["name"])[0].to_mongo()
        rep_actor = dict(rep_actor)
        id = rep_actor['_id']
        rep_actor.pop('_id', None)
        rep_actor['Name'] = id
        res = buildIndex.post_document("actor", rep_actor)
        print(actor['name']+"is new!")
    else:
        print(actor['name']+"exist!!")

#print(lineDict['actors'])
