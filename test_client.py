#! /usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask, send_from_directory, app
from core.FlaskExtRpcClient import RpcClient

app = Flask(__name__)

rpc_cli = RpcClient(app)


@app.route('/test-zeroRpc')
def test():
    cli = rpc_cli.connection
    word = cli.hello()
    return word


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0', threaded=False)
