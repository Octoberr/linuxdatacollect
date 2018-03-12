# coding:utf-8

"""
选择网卡， 更改shell脚本内容
create by swm
2018/03/12
"""
from subprocess import call


class SWITCH:

    def stopwifi(self, wlanname):
        call('airmon-ng stop {}mon'.format(wlanname), shell=True)
        info = {"stoped": 1}
        return info