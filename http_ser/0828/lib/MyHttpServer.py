# -*- coding:UTF-8 -*-
''' http 服务端 '''

import os
import socket
import SocketServer

import dir
import util
from MyHandler import *
from MyTcpHandler import *


class MyHttpServer:
    # 当前脚本所在的目录
    __cur_path__ = os.path.abspath(os.path.dirname(__file__))

    # 当前脚本所在目录的父级目录
    __par_path__ = os.path.dirname(__cur_path__)

    def __init__(self):
        self.http_server = None
        self.port = 8080
        self.buffer_size = 1024 * 2
        self.close = False

    def start(self, port=None):
        if port:
            self.port = port

        p_ip = util.get_ip()
        util.log("%s start http server  -- %s:%d" % (time.strftime('%Y-%m-%d %H:%M:%S'), p_ip, self.port))
        print "start http server  -- %s:%d" % (p_ip, self.port)

        self.http_server = SocketServer.ThreadingTCPServer(('', self.port), MyTcpHandler)
        self.http_server.serve_forever()

    def stop(self):
        self.close = True
        if self.http_server:
            self.http_server.close()
            print "stop http server -- port:%d" % self.port
            util.log("%s stop http server  -- port:%d" % (time.strftime('%Y-%m-%d %H:%M:%S'), self.port))


if __name__ == '__main__':
    server = MyHttpServer()

    # 生成文件列表
    dir.main()

    # 启动服务
    server.start()
