# coding:utf-8
from flask import Flask, request, Response
import json
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

app = Flask(__name__)

# from terminal.switch import WEBSWITCH
from terminal.mongooptions import mobidata


@app.route('api/allwlan', methods=['get'])
def getallwlan():
    info = {"wlan": ['wlan0', 'wlan1', 'wlan2']}
    return Response(json.dumps(info), mimetype="application/json")


@app.route('/api/whichwlan', methods=['post'])
def wlanname():
    args = json.loads(request.data)
    wlan = args['wlanname']
    # 改变wlan名字
    info = {"changed": 1}
    return Response(json.dumps(info), mimetype="application/json")


@app.route('/api/start', methods=['post'])
def start():
    args = json.loads(request.data)
    startcode = args['start']
    if int(startcode) == 1:
        # 调用开始函数
        # print 'start the mobi info collection'
        # switch = WEBSWITCH()
        # switch.startallshell()
        info = {"started": 1}
    else:
        info = {"started": 0, "erro": "something wrong with the data."}
    return Response(json.dumps(info), mimetype="applicarion/json")


@app.route('/api/shutdown', methods=['post'])
def stop():
    args = json.loads(request.data)
    stopcode = args['stop']
    if int(stopcode) == 1:
        # 调用停止函数
        # print "stop the mobi info collection"
        # switch = WEBSWITCH()
        # switch.shutdowntheshell()
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
        print("Start at"+ http_server.server_host + ':' + str(http_server.server_port))
        http_server.serve_forever()
    except(KeyboardInterrupt):
        print('Exit......')