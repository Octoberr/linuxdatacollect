# coding:utf-8
import threading
import datetime
from terminal.gethostapdfield import HOSTAPD


if __name__ == '__main__':
    # python多任务
    mobi = HOSTAPD()
    # 采集手机信息的一个线程
    thread1 = threading.Thread(target=mobi.startcollect)
    # 采集网络信息的线程
    # thread2 = threading.Thread(target=t2.start)
    # 开启线程
    # thread1.start()
    thread1.start()
    # thread2.start()
    thread1.join()
    # thread2.join()
    print datetime.datetime.now(), 'start collect'
