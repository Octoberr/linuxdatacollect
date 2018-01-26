# coding:utf-8
import threading
import datetime
import time
from terminal.gethostapdfield import HOSTAPD
class T1:
    def thread2(self):
        count = 0
        while True:
            count += 1
            print 'swm'
            if count == 100:
                break
        return
class T2:
    def thread1(self):
        count = 0
        while True:
            print 'nuonuo'
            count +=1
            if count ==200:
                break
        return
def start():
    t1 = T1()
    t2 = T2()
    thread1 = threading.Thread(target=t1.thread2)
    thread2 = threading.Thread(target=t2.thread1)
    thread1.start()
    thread2.start()
    # thread2.join()
    print datetime.datetime.now(), 'stop the program'
    return
if __name__ == '__main__':
    # python多任务
    # mobi = HOSTAPD()
    # 采集手机信息的一个线程
    # thread1 = threading.Thread(target=mobi.startcollect)
    # 采集网络信息的线程
    # thread2 = threading.Thread(target=t2.start)
    # 开启线程
    # thread1.start()
    # thread1.start()
    # thread2.start()
    # thread1.join()
    # thread2.join()
    # time.sleep(5)
    print datetime.datetime.now(), 'start collect'
    start()