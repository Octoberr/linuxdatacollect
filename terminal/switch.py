# coding:utf-8

"""
控制手机信息搜集的开关
create by swm
2018/03/06
"""
from subprocess import Popen, call
from time import sleep

from terminal.allconfig import conf
from terminal.gethostapdfield import HOSTAPD


class WEBSWITCH:

    def __init__(self):
        self.hostapdshell = '/home/starthostapd.sh'
        self.dhcpshell = '/home/startdhcp.sh'
        self.routershell = '/home/startrouter.sh'
        self.hostapdlog = conf['hostapdlog']
        self.dhcplog = conf['dhcplog']

    def starthostadp(self):
        fdout = open(self.hostapdlog, 'a')
        fderr = open(self.hostapdlog, 'a')
        # 修改为不写入文件对于不是很大的字符串直接存储在内存
        p = Popen(self.hostapdshell, stderr=fderr, stdout=fdout, shell=True)
        if p.poll():
            return
        p.wait()
        return

    def startdhcp(self):
        fdout = open(self.dhcplog, 'a')
        fderr = open(self.dhcplog, 'a')
        p = Popen(self.dhcpshell, stderr=fderr, stdout=fdout, shell=True)
        if p.poll():
            return
        p.wait()
        return

    def startrouter(self):
        p = Popen(self.routershell, shell=True)
        return

    def startallshell(self):
        # 开启与WiFi热点相关的所有数据
        self.starthostadp()
        sleep(1)
        self.startdhcp()
        sleep(1)
        self.startrouter()
        mobi = HOSTAPD()
        mobi.startcollect()
        return

    def shutdowntheshell(self):
        call("ps -ef|grep hostapd|grep -v grep|cut -c 9-15|xargs kill -s 9", shell=True)
        call("ps -ef|grep dhcp|grep -v grep|cut -c 9-15|xargs kill -s 9", shell=True)
        return
