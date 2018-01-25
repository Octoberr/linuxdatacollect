# coding:utf-8

from flask import Flask, request, Response
import json
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()
# 内部引用
from wifilist.startwifiserver import CONTROL
app = Flask(__name__)


@app.route('/api/startcollect', methods=['post'])
def starttheserver():
    args = json.loads(request.data)
    if args['start'] == 1:
        control = CONTROL()
        control.strat()
        orderinfo = {"complete": 1}
    return Response(json.dumps(orderinfo), mimetype="application/json")


if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 8014), app)
    try:
        print("Start at " + http_server.server_host +
              ':' + str(http_server.server_port))
        http_server.serve_forever()
    except(KeyboardInterrupt):
        print('Exit...')