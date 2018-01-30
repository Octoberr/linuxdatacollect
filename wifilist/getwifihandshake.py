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
        # 获得文件的路径
        self.wifihandshake = '/home/wifidata/{}-01.cap'.format(wifi)
        # 保存文件的路径
        self.keepfile = '/home/wifihandshakedata/'

    # 保存shell的所有输出
    def writeinfotolog(self, cmd):
        fdout = open(self.hslogpath, 'a')
        fderr = open(self.hslogpath, 'a')
        p = subprocess.Popen(cmd, stdout=fdout, stderr=fderr, shell=True)
        if p.poll():
            return
        p.wait()
        return

    def delthelog(self):
        subprocess.call("rm -f {}".format(self.hslogpath), shell=True)

    def delunusefile(self):
        subprocess.call("rm -f /home/wifidata/*", shell=True)

    # 移动获取成功的文件
    def mvfile(self):
        subprocess.call("cp -frap {} {}".format(self.wifihandshake, self.keepfile), shell=True)

    # 接收mac，ch, wifi获取wifihandshakebao，这个程序就只会写log知道泛洪攻击成功
    def starthandshake(self):
        # 开启获取wifi握手包的命令，并将log写入文件，本地获得一个文件
        cmd = 'airodump-ng -c {} --bssid {} -w {} wlan0mon'.format(self.ch, self.mac, self.savedatapath + self.wifi)
        # 在写入文件前删除可能存在的文件
        self.delthelog()
        self.writeinfotolog(cmd)
        return