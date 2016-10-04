#!/usr/bin/python
# -*- coding:UTF-8 -*-
__author__ = 'wb-yyl187231'

import os
import time
import optparse
from socket import *

# 当前脚本所在目录
__path__ = os.path.split(os.path.realpath(__file__))[0]
log = "udp.log"


class UdpServer:
    # 构造函数，初始化参数
    def __init__(self, port=None):
        self.port = 10010  # 服务默认端口
        self.buffer_size = 1024

        self.udp_service = None

    def start(self, port=None):
        if port:
            # 修改默认端口
            self.port = port

        date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print "%s udp server start :%d" % (date_time, self.port)
        self.write_log("%s udp server start :%d" % (date_time, self.port))

        # SOCK_DGRAM 面向非链接(udp)
        self.udp_service = socket(AF_INET, SOCK_DGRAM)
        self.udp_service.bind(('', self.port))

        while True:
            # 接受 UDP 数据
            data, client_addr = self.udp_service.recvfrom(self.buffer_size)

            if data:
                date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                print date_time, client_addr, ':', data
                self.write_log("%s %s request:%s" % (date_time, client_addr, data))

            # 发送 UDP hello 数据
            self.udp_service.sendto('hello', client_addr)
            self.write_log("%s %s response:hello" % (date_time, client_addr))

    def stop(self):
        if self.udp_service is not None:
            date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # 关闭服务端
            self.udp_service.close()
            self.write_log("%s udp server close" % date_time)

    # 记日志
    @staticmethod
    def write_log(msg):
        path_file = "%s/%s" % (__path__, log)
        # 以追加模式打开一个文件，如果文件不存在则创建文件
        log_file = open(path_file, 'a')
        log_file.write(msg + "\n")
        log_file.close()

    # 静态方法 解析参数
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


if __name__ == '__main__':
    udp_service = UdpServer()
    parser, opts, args = udp_service.parse_options()
    print parser, opts, args

    if opts.start:
        if opts.port.isdigit():
            udp_service.start(int(opts.port))
        else:
            udp_service.start()
    elif opts.stop:
        udp_service.stop()
    else:
        udp_service.start()
