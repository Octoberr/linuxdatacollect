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
            if count == 10:
                break
        return 'hello'
class T2:
    def thread1(self):
        count = 0
        while True:
            print 'nuonuo'
            count +=1
            if count ==20:
                break
        return 'swm'
def start():
    t1 = T1()
    t2 = T2()
    for i in range(0, 3):
        print datetime.datetime.now(), i
        thread1 = threading.ThreadW(target=t1.thread2)
        thread2 = threading.Thread(target=t2.thread1)
        thread1.setDaemon(1)
        thread2.setDaemon(1)
        a = thread1.start()
        b = thread2.start()
        thread2.join()
        thread1.join()
        print a
        print b
        print threading.activeCount()
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