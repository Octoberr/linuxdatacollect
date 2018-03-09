# coding:utf-8
"""
获取wifi list
存入mongodb
create by swm
2018/1/23
"""

import re
import pymongo
import datetime
import time
from subprocess import call
# 外部引用


class WIFINAME:

    def __init__(self):
        self.logpath = "/home/execute.log"
        self.mongohost = "192.168.1.138"
        self.mongoport = 27017

    def insertintomongo(self, wifilist):
        try:
            client = pymongo.MongoClient(self.mongohost, self.mongoport)
        except:
            self.writelog('{} canot connect mongodb'.format(datetime.datetime.now()))
        db = client.swmdb
        information = db.wifilist
        try:
            information.insert(wifilist)
        except:
            wifilist['ESSID'] = 'errorcode'
            information.insert(wifilist)
            self.writelog("{} error code, have replace".format(datetime.datetime.now()))
        return

    def writelog(self, log):
        with open(self.logpath, "a") as file:
            file.write(log)
        file.close()

    def getwifilist(self, text):
        wifilist = []
        re_start = re.compile(r'BSSID\s+STATION\s+PWR\s+Rate\s+Lost\s+Frames\s+Probe')
        re_end = re.compile(r'BSSID\s+PWR\s+Beacons\s+\#Data\, \#\/s\s+CH\s+MB\s+ENC\s+CIPHER AUTH ESSID')
        copy = False
        # 倒着读字符串，找到符合条件的行加入列表然后再筛选
        for line in reversed(text.splitlines()):
            start = re_start.search(line)
            end = re_end.search(line)
            if start:
                copy = True
                continue
            elif end:
                copy = False
                if len(wifilist) > 0:
                    break
            elif copy:
                wifilist.append(line)
        # 将信息采集后就可以删除log,不在需要log
        # call("rm -f {}".format(self.logpath), shell=True)
        return wifilist

    def startcollectinfo(self, wifilist):
        for line in wifilist:
            # 空格分割
            str = line.split(' ')
            # 去除空字符串
            list = filter(None, str)
            if len(list) <= 1:
                continue
            else:
                tmp = {}
                tmp['BSSID'] = list[0]
                tmp['PWR'] = list[1]
                tmp['Beacons'] = list[2]
                tmp['Data'] = list[3]
                tmp['s'] = list[4]
                tmp['CH'] = list[5]
                tmp['MB'] = list[6]
                tmp['unixtime'] = int(time.time())
                tmp['ESSID'] = list[-1]
                self.insertintomongo(tmp)
        self.writelog("{} Complete store the info.".format(datetime.datetime.now()))
        return


# if __name__ == '__main__':
#     wifi = WIFINAME()
#     wifilist = wifi.getwifilist()
#     # print wifilist
#     wifi.startcollectinfo(wifilist)