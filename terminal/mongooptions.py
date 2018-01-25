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


