# coding:utf-8
import threading
from flask import Flask, request, Response, send_from_directory, make_response
import json
import gevent.monkey
from gevent.pywsgi import WSGIServer
import redis
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
        control = CONTROL(seconds)
        thread1 = threading.Thread(target=control.start)
        thread2 = threading.Thread(target=control.killshell)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        info = {"complete": 1}
    else:
        info = {"complete": 0, "error": "something wrong with you!"}
    return Response(json.dumps(info), mimetype="application/json")


@app.route('/api/handshake', methods=['post'])
def collecthandshake():
    args = json.loads(request.data)
    handshake = HANDSHAKE(args['mac'], int(args['ch']), args['wifi'])
    router = ROUTE(args['mac'])
    t1 = threading.Thread(target=handshake.starthandshake)
    t2 = threading.Thread(target=router.start)
    t1.start()
    t2.start()
    t2.join()
    t1.join()
    from terminal.allconfig import conf
    r = redis.Redis(host=conf['redishost'], port=conf['redisport'])
    get = r.hget("handshake", "GET")
    if get:
        handshake.mvfile()
        info = {"complete": 1}
    else:
        info = {"complete": 0, "error": "Failed get wifi handshake"}
    r.delete("handshake")
    return Response(json.dumps(info), mimetype="application/json")


@app.route('/api/download/<wifi>', methods=['GET'])
def download(wifi):
    filepath = '/home/wifihandshakedata/'
    filename = '{}-01.cap'.format(wifi)
    # 中文
    response = make_response(send_from_directory(directory=filepath, filename=filename, as_attachment=True))
    # except:
    #     info = {"complete": 0, "error": "No such file, scan wifi failed"}
    #     return Response(json.dumps(info), mimetype="application/json")
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