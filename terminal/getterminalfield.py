# coding:utf-8
"""
1、读取文件
2、正则表达式提取信息
3、生成字段插入数据库
create by swm
2018/1/15
"""
import os
import re
import time
import datetime

from terminal.allconfig import conf
from terminal.mongooptions import insertintoterminal

class ANALYSIS:

    def getallthefilename(self, directorypath):
        allfilenames = []
        for root, dirs, files in os.walk(directorypath):
            for filename in files:
                # print(filename)
                allfilenames.append(filename)
        return allfilenames

    # 跟踪文件，定位为文件最后一行
    def follw(self, thefile):
        thefile.seek(0, 2)  # Go to the end of the file
        while True:
            line = thefile.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line

    def storeinformation(self, infotime):
        # 创建字典暂存信息
        info = {}
        info['logtime'] = infotime
        insertintoterminal(info)

    def startcollectinformation(self):
        # 信号强度
        # 数据包
        # 匹配当前时间
        re_time = re.compile(r'(\S{3}) (\d{2})\, (\d{4}) (\d{2})\:(\d{2})\:(\d{2})')
        logfile = open(conf['terminal'], "r")
        loglines = self.follw(logfile)
        for line in loglines:
            logtime = re_time.match(line)
            # datetime
            origintime = datetime.datetime(int(logtime.group(3)), conf[logtime.group(1)], int(logtime.group(2)), int(logtime.group(4)),
                                           int(logtime.group(5)), int(logtime.group(6)))
            # 存入数据库采用unix time的整形
            unixtime = int(time.mktime(origintime.timetuple()))
            # 最后调用存储的方法
            self.storeinformation(unixtime)

