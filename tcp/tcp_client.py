#!/usr/bin/python
# -*- coding:UTF-8 -*-
import subprocess

__author__ = 'yyl'

import os
import time
import optparse
from socket import *
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

buffer_size = 1024


def parse_options():
    usage = '\n %prog [options] '
    usage += '\n -h,--help   show help and exit'
    parser = optparse.OptionParser(usage=usage, version='1.0 v')

    # 解析测试例自定义参数
    parser.add_option('--port', dest='port', action='store', default=10011, help='server port')

    parser.add_option('--start', dest='start', action='store_true', help='start server')
    parser.add_option('--stop', dest='stop', action='store_true', help='stop server')

    # python xxx.py --port=80 --start  ss ww
    # 会被解析成
    # opts={'start': True, 'stop': None, 'port': '80'}
    # args = [ss,ww]
    opts, args = parser.parse_args()

    return parser, opts, args


def ping_ip(ip):
    # cmd = ["ping", "-q", "-c 2", "-r", ip]
    cmd = "ping -q -c 2 -r %s" % ip
    ping = subprocess.Popen(cmd, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print ping.stdout.readline()

    info = os.system("ping %s" % ip)
    print info


def tcp_connect(host, port, retry=10):
    data = ''
    while retry > 0:
        try:
            # AF_INET IPV4, SOCK_STREAM 面向连接
            tcp_client = socket(AF_INET, SOCK_STREAM)
            tcp_client.settimeout(3)
            # 主动初始化TCP服务器连接
            tcp_client.connect((host, port))
            # 发送TCP数据
            tcp_client.send("你好，服务端")
            # 接受TCP数据
            data = tcp_client.recv(buffer_size)
            if data:
                break
        except Exception as e:
            print e, retry
        finally:
            tcp_client.close()
            time.sleep(0.5)
            retry -= 1
    return data


if __name__ == '__main__':
    parser, opts, args = parse_options()
    print parser, opts, args

    if opts.start:
        ss = "%s" %opts
        print ss
        print tcp_connect('10.189.93.138', 10011, 10)
    elif opts.stop:
        print "stop"
    else:
        print tcp_connect('127.0.0.1', 10011, 10)

        # print tcp_connect('localhost', 10011, 10)

        # ping_ip('10.32.165.8')
        # print tcp_connect('10.32.165.8', 10011, 10)