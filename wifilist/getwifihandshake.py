# coding:utf-8
import os
import subprocess
import time
import re
"""
根据传入的mac,ch,wifi名去获取
wifi handshake的握手包
create by swm 2018/1/26
"""


filedir = os.path.dirname(os.path.realpath(__file__))


class HANDSHAKE:

    def __init__(self, mac, ch, wifi):
        # self.hslogpath = os.path.join(filedir, 'routrattack', 'wifihandshake.log')
        self.hslogpath = '/home/wifihandshake.log'
        self.savedatapath = '/home/wifidata/'
        self.mac = mac
        self.ch = ch
        self.wifi = wifi

    # 保存shell的所有输出
    def writeinfotolog(self, cmd):
        # call("python {} 2>&1 | tail -1 >{}".format(self.infopath, self.logpath), shell=True)
        fdout = open(self.hslogpath, 'a')
        fderr = open(self.hslogpath, 'a')
        p = subprocess.Popen(cmd, stdout=fdout, stderr=fderr, shell=True)
        if p.poll():
            return
        p.wait()
        return

    # def follw(self, thefile):
    #     thefile.seek(0, 0)  # Go to the end of the file
    #     while True:
    #         line = thefile.readline()
    #         if not line:
    #             time.sleep(0.1)
    #             continue
    #         yield line

    def killairodump(self):
        subprocess.call("ps -ef|grep airodump-ng|grep -v grep|cut -c 9-15|xargs kill -s 9", shell=True)

    def delthelog(self):
        subprocess.call("rm -rf {}".format(self.hslogpath))

    # 接收mac，ch, wifi获取wifihandshakebao
    def starthandshake(self):
        cmd = 'airodump-ng -c {} --bssid {} -w {} wlan0mon'.format(self.ch, self.mac, self.savedatapath + self.wifi)
        self.writeinfotolog(cmd)
        return

# if __name__ == '__main__':
#     hand = HANDSHAKE()
#     hand.gethandshake('50:2B:73:F4:35:F1', 7, 'swm')