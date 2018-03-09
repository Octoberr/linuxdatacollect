# coding:utf-8

"""
控制手机信息搜集的开关
create by swm
2018/03/06
"""
from subprocess import Popen, call
from time import sleep
import threading

from terminal.allconfig import conf



class WEBSWITCH:

    def __init__(self):
        self.hostapdshell = conf['hostapdshell']
        self.dhcpshell = conf['dhcpshell']
        self.routershell = conf['routershell']
        self.hostapdlog = conf['hostapdlog']
        self.dhcplog = conf['dhcplog']

    def starthostadp(self):
        fdout = open(self.hostapdlog, 'a')
        fderr = open(self.hostapdlog, 'a')
        # 修改为不写入文件对于不是很大的字符串直接存储在内存
        p = Popen(self.hostapdshell, stderr=fderr, stdout=fdout, shell=True)
        if p.poll():
            return
        return

    def startdhcp(self):
        fdout = open(self.dhcplog, 'a')
        fderr = open(self.dhcplog, 'a')
        p = Popen(self.dhcpshell, stderr=fderr, stdout=fdout, shell=True)
        if p.poll():
            return
        return

    def startrouter(self):
        p = Popen(self.routershell, shell=True)
        return

    def startallshell(self):
        # 开启与WiFi热点相关的所有数据
    #     thread1 = threading.Thread(target=self.starthostadp)
        self.starthostadp()
        sleep(1)
    #     thread2 = threading.Thread(target=self.startdhcp)
        self.startdhcp()
        sleep(1)
    #     thread3 = threading.Thread(target=self.startrouter)
        self.startrouter()
    #     mobi = HOSTAPD()
    #     thread4 = threading.Thread(target=mobi.startcollect)
    #     # mobi.startcollect()
    #     thread1.start()
    #     sleep(1)
    #     thread2.start()
    #     sleep(1)
    #     thread3.start()
    #     thread4.start()
    #     thread1.join()
    #     thread2.join()
    #     thread3.join()
    #     thread4.join()
        return

    def shutdowntheshell(self, wlanname):
        call("ps -ef|grep hostapd|grep -v grep|cut -c 9-15|xargs kill -s 9", shell=True)
        call("ps -ef|grep dhcp|grep -v grep|cut -c 9-15|xargs kill -s 9", shell=True)
        call("ifconfig {} down".format(wlanname), shell=True)
        return
