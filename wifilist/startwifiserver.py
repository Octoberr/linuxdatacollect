# coding:utf-8
import os
from subprocess import call
import time
import datetime
"""
控制扫描wifi的server服务
执行shell脚本，kill shell，
执行python脚本，kill py 和log
create by swm 2018/01/24
"""
fileDir = os.path.dirname(os.path.realpath(__file__))


class CONTROL:

    def __init__(self):
        self.pypath = os.path.join(fileDir, 'getwifilist.py')
        self.infopath = os.path.join(fileDir, 'getwifiinfo.py')
        self.logpath = "/home/wifi.log"

    # 运行python脚本抓取数据
    def collectwifilist(self):
        call("python {}".format(self.pypath), shell=True)

    def writeinfotolog(self):
        call("python {} 2>&1 | tail -1 > {}".format(self.infopath, self.logpath), shell=True)

    # 程序运行入口
    def strat(self):
        print datetime.datetime.now(), "Start scan the wifi, wait 10s"
        self.writeinfotolog()
        time.sleep(11)
        self.collectwifilist()
        print datetime.datetime.now(), "Start insert to mongo."

