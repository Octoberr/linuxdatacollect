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
        print datetime.datetime.now(), 'insert terminal success'

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
        return wifilist

    # 结束循环后kill自己,并且删除log文件
    def killmyself(self):
        call("rm -rf {}".format(self.logpath), shell=True)
        call("ps -ef|grep startwifiserver.py|grep -v grep|cut -c 9-15|xargs kill -s 9", shell=True)

    def startcollectinfo(self, wifilist):
        for line in wifilist:
            str = line.split(' ')
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
                tmp['ESSID'] = list[-2]
                self.insertintomongo(tmp)
        print datetime.datetime.now(), "Complete store the info."
        self.killmyself()


if __name__ == '__main__':
    wifi = WIFINAME()
    wifilist = wifi.getwifilist()
    # print wifilist
    wifi.startcollectinfo(wifilist)