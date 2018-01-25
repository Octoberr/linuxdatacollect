# coding:utf-8
"""
读取hostapd的log，并且将结果缓存在redis
create by swm
2018/01/16
"""
import time
import re
import redis

from terminal.allconfig import conf
from terminal import mongooptions as mongo


class HOSTAPD:

    def __init__(self):
        self.r = redis.Redis(host=conf['redishost'], port=conf['redisport'])

    def follw(self, thefile):
        thefile.seek(0, 2)  # Go to the end of the file
        while True:
            line = thefile.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line

    def getmobilfactory(self, devicemac):
        dhcpfile = open(conf['dhcplog'], "r").read()
        re_factory = re.compile(r'{}.\((.*?)\)'.format(devicemac))
        factory = re_factory.findall(dhcpfile)[0]
        return factory

    def startcollect(self):
        re_connect = re.compile(r'AP-STA-CONNECTED.(\S+\:\S+\:\S+\:\S+\:\S+\:\S+)')
        re_disconnect = re.compile(r'AP-STA-DISCONNECTED.(\S+\:\S+\:\S+\:\S+\:\S+\:\S+)')
        logfile = open(conf['hostapdlog'], "r")
        loglines = self.follw(logfile)
        for line in loglines:
            connect = re_connect.search(line)
            if connect:
                name = connect.group(1)
                # 上线时间
                connecttime = int(time.time())
                self.r.hset(name, "onlinetime", connecttime)
                self.r.hset(name, "devicemac", name)
                continue
            disconnect = re_disconnect.search(line)
            if disconnect:
                name = disconnect.group(1)
                # 根据devicemac在dhcp.log中寻找生产产商
                factory = self.getmobilfactory(name)
                self.r.hset(name, "factory", factory)
                disconnecttime = int(time.time())
                # 下线时间
                self.r.hset(name, "offlinetime", disconnecttime)
                mobiinfo = self.r.hgetall(name)
                # 上网的时间，单位为s,转换为int相减上
                mobiinfo['nettime'] = int(mobiinfo['offlinetime']) - int(mobiinfo['onlinetime'])
                mongo.insertmoibiinfo(mobiinfo)
                # 删除redis中已经存储在了mongodb的信息
                self.r.delete(name)
                continue
