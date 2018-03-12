# coding:utf-8
"""
mongodb options
create by swm
2018/1/15
"""
import pymongo
import datetime
from terminal.allconfig import conf


# 将tshark获取的数据存入mongodb
def insertintoterminal(terminal):
    client = pymongo.MongoClient(host=conf['mongohost'], port=conf['mongoport'])
    db = client.swmdb
    information = db.terminal
    information.insert(terminal)
    print datetime.datetime.now(), 'insert terminal success'


# 后面再增加其他方法
def insertmoibiinfo(mobi):
    client = pymongo.MongoClient(host=conf['mongohost'], port=conf['mongoport'])
    db = client.swmdb
    information = db.mobi
    information.insert(mobi)
    print datetime.datetime.now(), 'insert mobi success'


# 查询手机信息
def mobidata():
    res = []
    client = pymongo.MongoClient(host=conf['mongohost'], port=conf['mongoport'])
    db = client.swmdb
    mobi = db.mobi
    # 1升序，-1降序
    cursor = mobi.find({}, {"_id": 0}).sort("onlinetime", -1)
    for el in cursor:
        online = datetime.datetime.fromtimestamp(int(el['onlinetime'])).strftime('%Y-%m-%d %H:%M:%S')
        offline = datetime.datetime.fromtimestamp(int(el['offlinetime'])).strftime('%Y-%m-%d %H:%M:%S')
        el['onlinetime'] = online
        el['offlinetime'] = offline
        res.append(el)
    return res


