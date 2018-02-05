# coding:utf-8
import os
from subprocess import call, Popen, PIPE
import time
import datetime
"""
控制扫描wifi的server服务
执行shell脚本，kill shell，
执行python脚本，kill py 和log
create by swm 2018/01/24
不再需要操作文件
modify by swm 2018/2/2
"""
fileDir = os.path.dirname(os.path.realpath(__file__))


class CONTROL:

    def __init__(self, seconds):
        self.pypath = os.path.join(fileDir, 'getwifilist.py')
        self.logpath = "/home/execute.log"
        self.shellpath = "/home/getallwifi.sh"
        self.seconds = seconds

    # 运行python脚本抓取数据
    def collectwifilist(self, text):
        from getwifilist import WIFINAME
        wifi = WIFINAME()
        wifilist = wifi.getwifilist(text)
        # print wifilist
        wifi.startcollectinfo(wifilist)
        return
        # call("python {}".format(self.pypath), shell=True)

    # 保存shell的所有输出
    def writeinfotolog(self):
        # call("python {} 2>&1 | tail -1 >{}".format(self.infopath, self.logpath), shell=True)
        # fdout = open(self.logpath, 'a')
        # fderr = open(self.logpath, 'a')
        # 修改为不写入文件对于不是很大的字符串直接存储在内存
        p = Popen(self.shellpath, stderr=PIPE, stdout=PIPE, shell=True)
        stdout, err = p.communicate()
        return err

    # kill shell
    def killshell(self):
        time.sleep(self.seconds)
        call("ps -ef|grep airodump-ng|grep -v grep|cut -c 9-15|xargs kill -s 9", shell=True)
        return

    def writelog(self, log):
        with open(self.logpath, "a") as file:
            file.write(log)
        file.close()

    # 程序运行入口
    def start(self):
        self.writelog("{} Start scan the wifi, wait {}s".format(datetime.datetime.now(), self.seconds))
        # 在写文件前先清除下可能存在的log
        # call("rm -f {}".format(self.logpath), shell=True)
        try:
            text = self.writeinfotolog()
        except:
            log = "{} Wifi failed to start properly, please check whether to open wlan".format(datetime.datetime.now())
            self.writelog(log)
        # 这是非常奇怪的额，明明在写的时候不能执行下一步，但是这个确实能往后面执行
        self.writelog("{} Start insert to mongo.".format(datetime.datetime.now()))
        self.collectwifilist(text)
        return
