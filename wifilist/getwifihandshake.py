# coding:utf-8
import os
import subprocess
import redis
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
        # self.logpath = "/home/execute.log"
        self.savedatapath = '/home/wifidata/'
        self.mac = mac
        self.ch = ch
        self.wifi = wifi
        # 获得文件的路径
        self.wifihandshake = '/home/wifidata/{}-01.cap'.format(wifi)
        # 保存文件的路径
        self.keepfile = '/home/wifihandshakedata/'
        from terminal.allconfig import conf
        self.r = redis.Redis(host=conf['redishost'], port=conf['redisport'])

    # 保存shell的所有输出
    def writeinfotolog(self, cmd):
        p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        return err

    def delunusefile(self):
        subprocess.call("rm -f /home/wifidata/*", shell=True)

    # 移动获取成功的文件
    def mvfile(self):
        subprocess.call("cp -frap {} {}".format(self.wifihandshake, self.keepfile), shell=True)

    # 接收mac，ch, wifi获取wifihandshakebao，这个程序就只会写log知道泛洪攻击成功
    def starthandshake(self):
        # 在获取握手包前先删除以前的握手包
        self.delunusefile()
        # 开启获取wifi握手包的命令，并将log写入文件，本地获得一个文件
        cmd = 'airodump-ng -c {} --bssid {} -w {} wlan0mon'.format(self.ch, self.mac, self.savedatapath + self.wifi)
        strdata = self.writeinfotolog(cmd)
        re_handshake = re.compile(r'WPA handshake\:.{}'.format(self.mac))
        for line in strdata.splitlines():
            handshake = re_handshake.search(line)
            if handshake:
                GET = True
                # 获取握手包成功后删除wifilog
                break
            else:
                GET = False
                continue
        print "get status", GET
        self.r.hset("handshake", "GET", GET)
        return