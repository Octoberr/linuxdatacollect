# coding:utf-8
import threading
from flask import Flask, request, Response
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
    seconds = args['seconds']
    if args['start'] == 1:
        # control = CONTROL()
        # control.strat(seconds)
        time.sleep(seconds)
        orderinfo = {"complete": 1}
    return Response(json.dumps(orderinfo), mimetype="application/json")


@app.route('/api/handshake', methods=['post'])
def collecthandshake():
    args = json.loads(request.data)
    t1 = HANDSHAKE(args['mac'], args['ch'], args['wifi'])
    t2 = ROUTE(args['mac'])
    re_handshake = re.compile(r'WPA handshake\:.{}'.format(args['mac']))
    GET = True
    while GET:
        thread1 = threading.Thread(target=t1.starthandshake)
        thread2 = threading.Thread(target=t2.strat)
        thread1.start()
        thread2.start()
        logfile = open(t1.hslogpath, "r")
        loglines = logfile.readlines()
        for line in loglines:
            handshake = re_handshake.search(line)
            if handshake:
                GET = False
                t1.delthelog()
                orderinfo = {"complete": 1}
                break
            else:
                t1.delunusefile()
                time.sleep(0.5)
                GET = True
    return Response(json.dumps(orderinfo), mimetype="application/json")


if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 8014), app)
    try:
        print("Start at " + http_server.server_host +
              ':' + str(http_server.server_port))
        http_server.serve_forever()
    except(KeyboardInterrupt):
        print('Exit...')