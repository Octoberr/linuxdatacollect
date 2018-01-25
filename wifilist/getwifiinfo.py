# coding:utf-8

"""
获取wifi信息并写入文件
create by swm 2018/1/25
"""

from subprocess import call
import datetime
import time


class INFO:

    def __init__(self):
        self.shellpath = "/home/getallwifi.sh"
        self.logpath = "/home/wifi.log"

    def startshell(self):
        # 执行脚本前先清理下log文件
        call("rm -rf {}".format(self.logpath), shell=True)
        print "start the shell"
        # 执行脚本
        call(self.shellpath, shell=True)

    # kill shell
    def killshell(self):
        call("ps -ef|grep airodump-ng|grep -v grep|cut -c 9-15|xargs kill -s 9", shell=True)

    # 结束循环后kill自己,并且删除log文件
    def killmyself(self):
        call("ps -ef|grep getwifiinfo.py|grep -v grep|cut -c 9-15|xargs kill -s 9", shell=True)

    def strat(self):
        self.startshell()
        print datetime.datetime.now(), "Start scan the wifi, wait 10s"
        time.sleep(10)
        # 结束shell
        self.killshell()
        print datetime.datetime.now(), "Have writen log to file"
        self.killmyself()


if __name__ == '__main__':
    print " start"
    info = INFO()
    info.strat()
