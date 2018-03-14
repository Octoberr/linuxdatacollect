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
        wopen = open(self.wifishell, 'w')
        wopen.write(newsrc)
        wopen.close()
        return

    def rename(self, wlanname):
        self.changehostapdconf(wlanname)
        self.changedhcpconf(wlanname)
        return

    def changewificonf(self, name, pwd):
        oldf = open(self.hostapdconf, 'r')
        oldsrc = oldf.read()
        re_name = re.compile(r'(\bssid\=)(.+)')
        re_pwd = re.compile(r'(wpa\_passphrase\=)(.+)')
        name = re_name.sub(r'\1{}'.format(name), oldsrc)
        pwd = re_pwd.sub(r'\1{}'.format(pwd), name)
        oldf.close()
        wopen = open(self.hostapdconf, 'w')
        wopen.write(pwd)
        wopen.close()
        return

# if __name__ == '__main__':
#     import os
#     file = os.path.dirname(os.path.realpath(__file__))
#     hostconf = os.path.join(file, '..', 'script', 'hostapd.conf')
#     # print hostconf
#     src = open(hostconf, 'r')
#     content = src.read()
#     print content
#     re_name = re.compile(r'(\bssid\=)(.+)')
#     re_pwd = re.compile(r'(wpa\_passphrase\=)(.+)')
#     name = re_name.sub(r'\1swm', content)
#     pwd = re_pwd.sub(r'\1adsx123', name)
#     print name
#     print pwd
    # for line in content:
    # name = re_name.search(content)
    # pwd = re_pwd.search(content)
    # if name:
    #     print name.group(2)
    # if pwd:
    #     print pwd.group(2)
    # name = re_name.findall(content)
    # pwd = re_pwd.findall(content)
    # print name
    # print pwd