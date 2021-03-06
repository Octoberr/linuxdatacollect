# coding:utf-8
"""
create by swm
2018/02/26
"""
import pymongo
import datetime
import time
import json


def getquerydate(today):
    res = []
    client = pymongo.MongoClient(host="192.168.1.213", port=27017)
    db = client.swmdb
    collection = db.wifilist
    # cursor = collection.find({"unixtime": {"$gt": int(today)}}, {"_id": 0}).sort({"unixtime": -1})
    cursor = collection.find({"unixtime": {"$gt": int(today)}}, {"_id": 0}).sort([("unixtime", -1)])
    for el in cursor:
        havedate = datetime.datetime.fromtimestamp(int(el['unixtime'])).strftime('%Y-%m-%d %H:%M:%S')
        el['unixtime'] = havedate
        res.append(el)
    return res


if __name__ == '__main__':
    todayunxi = time.mktime(datetime.date.today().timetuple())
    res = getquerydate(todayunxi)
    # print res
    jsondata = json.dumps(res)
    print jsondata

