# coding:utf-8
import os
from subprocess import call, Popen
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
        self.logpath = "/home/wifi.log"
        self.shellpath = "/home/getallwifi.sh"

    # 运行python脚本抓取数据
    def collectwifilist(self):
        from getwifilist import WIFINAME
        wifi = WIFINAME()
        wifilist = wifi.getwifilist()
        # print wifilist
        wifi.startcollectinfo(wifilist)
        return
        # call("python {}".format(self.pypath), shell=True)

    # 保存shell的所有输出
    def writeinfotolog(self):
        # call("python {} 2>&1 | tail -1 >{}".format(self.infopath, self.logpath), shell=True)
        fdout = open(self.logpath, 'a')
        fderr = open(self.logpath, 'a')
        p = Popen(self.shellpath, stdout=fdout, stderr=fderr, shell=True)
        if p.poll():
            return
        p.wait()
        return

    # kill shell
    def killshell(self):
        call("ps -ef|grep airodump-ng|grep -v grep|cut -c 9-15|xargs kill -s 9", shell=True)

    # 程序运行入口
    def strat(self, seconds):
        print datetime.datetime.now(), "Start scan the wifi, wait {}s".format(seconds)
        # 在写文件前先清除下可能存在的log
        call("rm -f {}".format(self.logpath), shell=True)
        self.writeinfotolog()
        # 这是非常奇怪的额，明明在写的时候不能执行下一步，但是这个确实能往后面执行
        time.sleep(seconds)
        # 结束扫描命令
        self.killshell()
        print datetime.datetime.now(), "Start insert to mongo."
        self.collectwifilist()
        return {"complete": 1}


