# coding:utf-8
import threading
from flask import Flask, request, Response, send_from_directory, make_response
import json
import gevent.monkey
from gevent.pywsgi import WSGIServer
import time
import re
gevent.monkey.patch_all()
# 内部引用
from wifilist.startwifiserver import CONTROL
from wifilist.getwifihandshake import HANDSHAKE
from wifilist.routeattack import ROUTE
app = Flask(__name__)


@app.route('/api/startcollect', methods=['post'])
def starttheserver():
    args = json.loads(request.data)
    # 类型强转确保int
    seconds = int(args['seconds'])
    if int(args['start']) == 1:
        control = CONTROL()
        orderinfo =control.strat(seconds)
    return Response(json.dumps(orderinfo), mimetype="application/json")


@app.route('/api/handshake', methods=['post'])
def collecthandshake():
    args = json.loads(request.data)
    t1 = HANDSHAKE(args['mac'], int(args['ch']), args['wifi'])
    t2 = ROUTE(args['mac'])
    re_handshake = re.compile(r'WPA handshake\:.{}'.format(args['mac']))
    GET = True
    count = 0
    while GET:
        count += 1
        if count > 3:
            orderinfo = {"complete": 0}
            break
        t1.delunusefile()
        thread1 = threading.Thread(target=t1.starthandshake)
        thread2 = threading.Thread(target=t2.strat)
        thread1.start()
        thread2.start()
        # 等待线程执行结束
        thread1.join()
        thread2.join()
        logfile = open(t1.hslogpath, "r")
        loglines = logfile.readlines()
        for line in loglines:
            handshake = re_handshake.search(line)
            if handshake:
                GET = False
                # 获取握手包成功后删除wifilog
                break
            else:
                continue
    else:
        t1.delthelog()
        t1.mvfile()
        orderinfo = {"complete": 1}
    # 最后保存文件
    return Response(json.dumps(orderinfo), mimetype="application/json")


@app.route('/api/download/<wifi>', methods=['GET'])
def download(wifi):
    filepath = '/home/wifihandshakedata/'
    filename = '{}-01.cap'.format(wifi)
    # 中文
    response = make_response(send_from_directory(directory=filepath, filename=filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response


if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 8014), app)
    try:
        print("Start at " + http_server.server_host +
              ':' + str(http_server.server_port))
        http_server.serve_forever()
    except(KeyboardInterrupt):
        print('Exit...')