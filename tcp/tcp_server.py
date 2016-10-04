#!/usr/bin/python
# -*- coding:UTF-8 -*-
__author__ = 'yyl'
import os
import optparse
import time
from socket import *

# 当前脚本所在目录
__path__ = os.path.split(os.path.realpath(__file__))[0]
log = "tcp.log"


class TcpServer:
    def __init__(self):
        self.tcp_server = None
        self.buffer_size = 1024
        # 默认端口
        self.port = 10011

    # 启动服务
    def start(self, port=None):
        if port:
            # 修改默认端口
            self.port = port

        date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        print 'tcp server start '
        self.write_log("%s tcp server start :%d" % (date_time, self.port))

        # 为空监听任意IP  监听端口
        address = ('', self.port)

        # SOCK_STREAM 面向连接(tcp)
        self.tcp_server = socket(AF_INET, SOCK_STREAM)

        # 绑定地址（host,port）到套接字， 在AF_INET下,以元组（host,port）的形式表示地址。
        self.tcp_server.bind(address)

        self.tcp_server.listen(5)  # 设置最大连接数，超过后排队
        while True:
            # 被动接受TCP客户端连接,(阻塞式)等待连接的到来
            tcp_client, client_addr = self.tcp_server.accept()
            while True:
                # 接受的消息 1024字节的 data 数据
                data = tcp_client.recv(1024)
                if data:
                    date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    print date_time, client_addr, ':', data
                    self.write_log("%s %s request:%s" % (date_time, client_addr, data))
                    break

            # 向客户端 发送 hello 信息
            tcp_client.send("hello")
            self.write_log("%s %s response:hello" % (date_time, client_addr))

    # 关闭服务端
    def stop(self):
        if self.tcp_server is not None:
            date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.tcp_server.close()
            self.write_log("%s tcp server close" % date_time)

    @staticmethod
    def parse_options():
        usage = '\n %prog [options] '
        usage += '\n -h,--help   show help and exit'
        parser = optparse.OptionParser(usage=usage, version='1.0 v')

        # 解析测试例自定义参数
        parser.add_option('--port', dest='port', action='store', default=10011, help='server port')

        parser.add_option('--start', dest='start', action='store_true', help='start server')
        parser.add_option('--stop', dest='stop', action='store_true', help='stop server')

        opts, args = parser.parse_args()

        return parser, opts, args

    # 记日志
    @staticmethod
    def write_log(msg):
        path_file = "%s/%s" % (__path__, log)
        # 以追加模式打开一个文件，如果文件不存在则创建文件
        log_file = open(path_file, 'a')
        log_file.write(msg + "\n")
        log_file.close()


if __name__ == '__main__':
    tcp_server = TcpServer()

    parser, opts, args = tcp_server.parse_options()
    print parser, opts, args

    if opts.start:
        if opts.port.isdigit():
            tcp_server.start(int(opts.port))
        else:
            tcp_server.start()
    elif opts.stop:
        tcp_server.stop()
    else:
        tcp_server.start()
