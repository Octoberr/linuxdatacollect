# coding:utf-8
from flask import Flask, request, Response
import json
import gevent.monkey
from gevent.pywsgi import WSGIServer
import threading
from time import sleep
gevent.monkey.patch_all()

app = Flask(__name__)

from terminal.switch import WEBSWITCH
from terminal.mongooptions import mobidata
from terminal.getallwifiname import IWWIFI
from terminal.gethostapdfield import HOSTAPD


@app.route('/api/allwlan', methods=['get'])
def getallwlan():
    iw = IWWIFI()
    info = {}
    wlanlist = iw.getallname()
    if len(wlanlist) == 0:
        info['wlan'] = wlanlist
        info['err'] = 'no wlan find, please check the mechine'
    else:
        info['wlan'] = wlanlist
    # info = {"wlan": ['wlan0', 'wlan1', 'wlan2']}
    return Response(json.dumps(info), mimetype="application/json")


@app.route('/api/whichwlan', methods=['post'])
def wlanname():
    args = json.loads(request.data)
    wlan = args['wlanname']
    # 改变wlan名字
    iw = IWWIFI()
    iw.rename(wlan)
    info = {"changed": 1}
    return Response(json.dumps(info), mimetype="application/json")


@app.route('/api/wificonf', methods=['post'])
def wificonf():
    args = json.loads(request.data)
    name = args['name']
    pwd = args['pwd']
    # 改变热点名字和密码
    iw = IWWIFI()
    iw.changewificonf(name, pwd)
    info = {"changed": 1}
    return Response(json.dumps(info), mimetype="application/json")


@app.route('/api/start', methods=['post'])
def start():
    args = json.loads(request.data)
    startcode = args['start']
    if int(startcode) == 1:
        # 调用开始函数
        # print 'start the mobi info collection'
        switch = WEBSWITCH()
        thread1 = threading.Thread(target=switch.startallshell)
        mobi = HOSTAPD()
        thread2 = threading.Thread(target=mobi.startcollect)
        thread1.start()
        thread2.start()
        # thread1.join()
        # thread2.join()
        info = {"started": 1}
    else:
        info = {"started": 0, "erro": "something wrong with the data."}
    return Response(json.dumps(info), mimetype="applicarion/json")


@app.route('/api/shutdown', methods=['post'])
def stop():
    args = json.loads(request.data)
    stopcode = args['stop']
    stopwlan = args['wlanname']
    if int(stopcode) == 1:
        # 调用停止函数
        # print "stop the mobi info collection"
        switch = WEBSWITCH()
        switch.shutdowntheshell(stopwlan)
        info = {"stopcode": 1}
    else:
        info = {"stopcode": 0, "erro": "something wrong with the data."}
    return Response(json.dumps(info), mimetype="application/json")


@app.route('/api/mobiinfo', methods=['get'])
def querymobidata():
    data = json.dumps(mobidata())
    return Response(data, mimetype="application/json")


if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 8015), app)
    try:
        print("Start at" + http_server.server_host + ':' + str(http_server.server_port))
        http_server.serve_forever()
    except(KeyboardInterrupt):
        print('Exit......')