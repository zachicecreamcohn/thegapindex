from get_data import gap, oldnavy, banana, athleta
from database import insert_product

def getGapData(cid, pageId, depId):
    data = gap(cid, pageId, depId)
    return data

def getOldnavyData(cid, pageId, depId):
    data = oldnavy(cid, pageId, depId)
    return data

def getBananaData(cid, pageId, depId):
    data = banana(cid, pageId, depId)
    return data

def getAthletaData(cid):
    data = athleta(cid)
    return data


cids_and_depIds = [
    {"cid": "1158705", "depId": "136"},
    {"cid":  "1152219", "depId": "75"},

]

cids = ["1025878","1032080","1038916","1031353","89745", "1170247","1017102","1032096", ]

for cid in cids:
    page = 0
    continue_trying = True
    while (continue_trying):
        try:
            data = getAthletaData(cid)
            for i in data:
                insert_product(i)
            page += 1
        except Exception as e:
            print(e)
            continue_trying = False
            continue
    

