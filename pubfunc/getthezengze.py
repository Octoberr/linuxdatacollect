# coding:utf-8
"""
正则表达式匹配测试
create by SWM
2017/12/29
increase mongoquery interface
2018/01/04
"""
import re
import json
import datetime
import pymongo
from config import mongo
import os
import time
fileDir = os.path.dirname(os.path.realpath(__file__))


# 获得一个文件夹下所有可读文件的列表
# def getallthefilename(directorypath):
#     allfilenames = []
#     for root, dirs, files in os.walk(directorypath):
#         for filename in files:
#             # print(filename)
#             allfilenames.append(filename)
#     return allfilenames


# mongodb数据库localhost，集合terminal
def insertintoterminal(spiderdata):
    client = pymongo.MongoClient(host=mongo['host'], port=mongo['port'])
    db = client.swmdb
    information = db.terminal
    information.insert(spiderdata)
    print(datetime.datetime.now(), 'insert terminal success')


# mongodb数据库localhost，集合wifi
# def insertintowifi(spiderdata):
#     client = pymongo.MongoClient(host=mongo['host'], port=mongo['port'])
#     db = client.swmdb
#     information = db.wifi
#     information.insert(spiderdata)
#     print(datetime.datetime.now(), 'insert wifi success')


# def selectsomething(arg1, arg2, arg3, arg4):
#     client = pymongo.MongoClient(host=mongo['host'], port=mongo['port'])
#     db = client.swmdb
#     information = db.saveoutfile
#     # 迭代器
#     cursor = information.find({"arg": arg1}, {"arg": 1}).sort("arg", -1).limit(1)
#     while True:
#         data = next(cursor)
#         if something:
#             return data
    # for el in cursor:
    #     havedate = datetime.datetime.strptime(el["Info"]['Date'], "%Y-%m-%dT%H:%M:%S").date()
    #     return havedate


def getthephoneinformation(filepath):
    # re_connect = re.compile(r'AP-STA-CONNECTED.(\S+\:\S+\:\S+\:\S+\:\S+\:\S+)')
    # re_disconnect = re.compile(r'AP-STA-DISCONNECTED.(\S+\:\S+\:\S+\:\S+\:\S+\:\S+)')

    #匹配当前时间
    re_time = re.compile(r'(\S{3}) (\d{2})\, (\d{4}) (\d{2})\:(\d{2})\:(\d{2})')
    # re_time = re.compile(r'\d{4}.\d{2}\:\d{2}\:\d{2}')
    # 匹配具有标识的字符串，如abc=****;
    # re_usragen = re.compile(r'User-Agent=\S+;')  # User-Agent=(.*?);
    # re_usragen = re.compile(r'User-Agent=(.*?);')  # User-Agent=(.*?);
    # 匹配qq邮箱
    # re_mailcount = re.compile(r'[\d]+@[\w.]+')
    # 匹配qq号,数字9位到13位
    # re_qqnumber = re.compile(r'\d{9,10}')
    # 匹配ip地址
    # re_ipnumber = re.compile(r'\d+\.\d+\.\d+\.\d+')
    # 匹配mac地址
    # re_mac = re.compile(r'\S+\:\S+\:\S+\:\S+\:\S+\:\S+')
    # 匹配gif图片
    # [\w.]+[\d.]\.gif 字母加数字
    # re_gif = re.compile(r'[\S.]+\.gif')
    # 匹配网站
    # re_net = re.compile(r'[\w.]+\.com|[\w.]+\.cn')
    file = open(filepath, "r").readlines()
    for line in file:
        fac = re_time.match(line)
        print fac.group(3)
        break
    # with open(filepath, "r") as file:
    # lines = file.read()
    # fac = re_time.findall(file)
    # print fac
    conf = {}
    conf['Jan'] = 1
    conf['Feb'] = 2
    conf['Mar'] = 3
    conf['Apr'] = 4
    conf['May'] = 5
    conf['Jun'] = 6
    conf['Jul'] = 7
    conf['Aug'] = 8
    conf['Sep'] = 9
    conf['Oct'] = 10
    conf['Nov'] = 11
    conf['Dec'] = 12
    origintime = datetime.datetime(int(fac.group(3)), conf[fac.group(1)], int(fac.group(2)), int(fac.group(4)), int(fac.group(5)), int(fac.group(6)))
    # unixtime = time.(int(fac[2]), conf[fac[0]], int(fac[1]), int(fac[3]), int(fac[4]), int(fac[5]))
    unixtime = int(time.mktime(origintime.timetuple()))
    print unixtime
    print origintime
        # for line in lines:
        #     connect = re_connect.search(line)
        #     # discon = re_disconnect.match(line)
        #     if connect:
        #         print connect.group(1)
        #     disconnect = re_disconnect.search(line)
        #     if disconnect:
        #         print disconnect.group(1)
        #         print type(disconnect.group(1))
            # print connect
#             nowtime = re_time.findall(line)
#             usragent = re_usragen.findall(line)
#             email = re_mailcount.findall(line)
#             qq = re_qqnumber.findall(line)
#             ip = re_ipnumber.findall(line)
#             mac = re_mac.findall(line)
#             gif = re_gif.findall(line)
#             net = re_net.findall(line)
#             tmp['tmie'] = nowtime
#             tmp['usragent'] = usragent
#             tmp['email'] = email
#             tmp['qq'] = qq
#             tmp['ip'] = ip
#             tmp['macaddress'] = mac
#             tmp['gifsources'] = gif
#             tmp['netaddress'] = net
#             with open('outpufile.json', 'a') as outfile:
#                 json.dump(tmp, outfile)
#             insertintomongo(tmp)
# 终端采集数据
# def theterminaldata():
#     term = {}
#     # 设备mac
#     term['device_mac'] =
#     # 厂商
#     term['company'] =
#     # 上网时间
#     term['on_net_time'] =
#     # 离开时间
#     term['off_net_time'] =
#     # 信号强度
#     term['signal_strength']=
#     # 数据包
#     term['data_pack'] =

# def thewifidata():
#     wifi = {}
#     # mac
#     wifi['bssid'] =
#     # essid wifi名称
#     wifi['essid'] =
#     # rssi 信号强度
#     wifi['rssi'] =
#     # 握手包
#     wifi['handshake_data'] =
#     # CH 频段
#     wifi['CH']=
#     # MB 带宽
#     wifi['MB']=
#     # ENC加密体系
#     wifi['ENC']=
#     #CIPHER加密算法
#     wifi['CIPHER']=

if __name__ == '__main__':
    log = os.path.join(fileDir, '..', 'script', 'teminal.log')
    getthephoneinformation(log)