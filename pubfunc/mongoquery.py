import pymongo
import datetime


class MONGO:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def getquerydate(self, aircarfNo):
        client = pymongo.MongoClient(host=self.host, port=self.port)
        db = client.swmdb
        eagleyedates = db.runtest
        cursor = eagleyedates.find({"Info.fno": aircarfNo}, {"Info.Date": 1}).sort("Info.Date", -1).limit(1)
        for el in cursor:
            havedate = datetime.datetime.strptime(el["Info"]['Date'], "%Y-%m-%dT%H:%M:%S").date()
            return havedate

    def insertintomongo(self, flightdata):
        client = pymongo.MongoClient(host=self.host, port=self.port)
        db = client.swmdb
        eagleyedates = db.runtest
        eagleyedates.insert(flightdata)
        print(datetime.datetime.now(), 'insert mongodb success')