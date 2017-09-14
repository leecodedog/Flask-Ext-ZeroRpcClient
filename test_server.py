#! /usr/bin/env python
# -*- coding: utf-8 -*-

import zerorpc
import os
import time


class RpcServer(object):
    """docstring for TestRpcServer"""

    def __init__(self):
        super(RpcServer, self).__init__()

    @staticmethod
    def hello():
        return "hello world"

    @staticmethod
    def is_alive():
        return True


def get_localtime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


if __name__ == '__main__':
    urls = 'tcp://127.0.0.1:5007'
    s = zerorpc.Server(RpcServer())
    s.bind(urls)
    print get_localtime(), 'start Parser RPC  Server s1', urls, 'pid :', os.getpid()
    s.run()
