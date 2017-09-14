#! /usr/bin/env python
# -*- coding: utf-8 -*-
import threading

import zerorpc

import traceback

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

global_data = threading.local()
RPC_URI = ['tcp://127.0.0.1:5007']

class RpcClient(zerorpc.Client):
    def __init__(self, app=None, auto_close=False):
        self.app = app
        if app is not None and auto_close:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('RPC_CLI', ':memory:')
        # Use the newstyle teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def connect(self):
        if not hasattr(global_data, "cli"):
            global_data.cli = zerorpc.Client(connect_to=RPC_URI)
            print ' global_data.cli  zerorpc.Client connect_to ', RPC_URI
        else:
            test = global_data.cli.is_alive()
            if not test:
                try:
                    global_data.cli.close()
                except Exception, e:
                    traceback.print_exc()
                global_data.cli = zerorpc.Client(connect_to=RPC_URI)
                print ' global_data.cli  zerorpc.Client connect_to ', RPC_URI
            else:
                pass
        return global_data.cli

    def connect2(self):
        return zerorpc.Client(connect_to=RPC_URI,timeout=60, heartbeat=30)

    def __del__(self):
        if hasattr(global_data, "cli"):
            try:
                print ' global_data.cli  zerorpc.Client __del__  close'
                global_data.cli.close()
            except Exception, e:
                traceback.print_exc()

    def teardown(self, exception):
        '''
        每次连接完毕都会关闭cli，消耗会比较大
        :param exception:
        :return:
        '''
        ctx = stack.top
        if hasattr(ctx, 'rpc_cli'):
            print "DEL RPC CLIENT"
            ctx.rpc_cli.close()

    @property
    def connection(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'rpc_cli'):
                # ctx.rpc_cli = self.connect2()
                ctx.rpc_cli = self.connect()
            return ctx.rpc_cli
