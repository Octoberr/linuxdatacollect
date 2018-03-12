# coding:utf-8
"""
使用iwconfig获取插入的网卡
create by swm
2018/03/07
"""
import re
from subprocess import Popen, PIPE

from terminal.allconfig import conf


class IWWIFI:

    def __init__(self):
        self.shell = 'iwconfig'
        self.hostapdconf = conf['hostapdconf']
        self.dhcpsh = conf['dhcpshell']
        self.wifishell = conf['wifishell']

    def getallname(self):
        p = Popen('iwconfig', stdout=PIPE, stderr=PIPE, shell=True)
        out, err = p.communicate()
        re_wlanname = re.compile(r'wlan\d')
        wlanname = re_wlanname.findall(out)
        return wlanname

    def changehostapdconf(self, wlanname):
        oldf = open(self.hostapdconf, 'r')
        oldsrc = oldf.read()
        re_wlanname = re.compile(r'wlan\d')
        newsrc = re_wlanname.sub(r'{}'.format(wlanname), oldsrc)
        oldf.close()
        wopen = open(self.hostapdconf, 'w')
        wopen.write(newsrc)
        wopen.close()
        return

    def changedhcpconf(self, wlanname):
        oldf = open(self.dhcpsh, 'r')
        oldsrc = oldf.read()
        re_wlanname = re.compile(r'wlan\d')
        newsrc = re_wlanname.sub(r'{}'.format(wlanname), oldsrc)
        oldf.close()
        wopen = open(self.dhcpsh, 'w')
        wopen.write(newsrc)
        wopen.close()
        return

    def changwifishell(self, wlanname):
        oldf = open(self.wifishell, 'r')
        oldsrc = oldf.read()
        re_wlanname = re.compile(r'wlan\d')
        newsrc = re_wlanname.sub(r'{}'.format(wlanname), oldsrc)
        oldf.close()
        wopen = open(self.dhcpsh, 'w')
        wopen.write(newsrc)
        wopen.close()
        return

    def rename(self, wlanname):
        self.changehostapdconf(wlanname)
        self.changedhcpconf(wlanname)
        return