# coding:utf-8

"""
结束死循环式的攻击
反正就是结束攻击
"""
from subprocess import call


class SHUTDOWN:
    def __init__(self, wlanname):
        self.wlanname = wlanname

    def attackover(self):
        call("ps -ef|grep airodump-ng|grep -v grep|cut -c 9-15|xargs kill -s 9", shell=True)
        call('airmon-ng stop {}mon'.format(self.wlanname))
        return


if __name__ == '__main__':
    shuwdown = SHUTDOWN('wlan1')
    shuwdown.attackover()