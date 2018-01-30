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
        self.logpath = "/home/wifi.log"
        self.mongohost = "192.168.1.213"
        self.mongoport = 27017

    def insertintomongo(self, wifilist):
        client = pymongo.MongoClient(self.mongohost, self.mongoport)
        db = client.swmdb
        information = db.wifilist
        information.insert(wifilist)
        print datetime.datetime.now(), 'insert wifidate success'

    def getwifilist(self):
        wifilist = []
        re_start = re.compile(r'BSSID\s+STATION\s+PWR\s+Rate\s+Lost\s+Frames\s+Probe')
        re_end = re.compile(r'BSSID\s+PWR\s+Beacons\s+\#Data\, \#\/s\s+CH\s+MB\s+ENC\s+CIPHER AUTH ESSID')
        copy = False
        with open(self.logpath, 'r') as file:
            for line in reversed(file.readlines()):
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
        # 将信息采集后就可以删除log
        call("rm -f {}".format(self.logpath), shell=True)
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
                try:
                    tmp['ESSID'] = list[-2]
                except:
                    tmp['ESSID'] = 'error code'
                try:
                    self.insertintomongo(tmp)
                except:
                    print '特殊字符串'
                    continue
        print datetime.datetime.now(), "Complete store the info."
        return


# if __name__ == '__main__':
#     wifi = WIFINAME()
#     wifilist = wifi.getwifilist()
#     # print wifilist
#     wifi.startcollectinfo(wifilist)