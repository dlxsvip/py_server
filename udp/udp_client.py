#!/usr/bin/python
# -*- coding:UTF-8 -*-
__author__ = 'yy'

import os
import time
from socket import *
import struct

buffer_size = 1024


def udp_connect(ip, port, msg, retry=10):
    data = ''
    address = (str(ip), int(port))

    # 设置给定套接字选项的值。
    # udp_client.setsockopt(SOL_SOCKET, SO_RCVTIMEO, struct.pack('LL', 1, 0))
    while retry > 0:
        try:
            # SOCK_DGRAM 面向非链接
            udp_client = socket(AF_INET, SOCK_DGRAM)
            udp_client.settimeout(5)
            # 发送UDP数据
            udp_client.sendto(msg, address)

            # 接受UDP数据
            data, service_addr = udp_client.recvfrom(buffer_size)
            if data:
                break
        except Exception as e:
            print "error", retry
        finally:
            udp_client.close()
            time.sleep(0.5)
            retry -= 1
    return data


if __name__ == '__main__':
    # print udp_connect('localhost', 10000, "你好，服务端", 10)
    # print udp_connect('10.189.94.207', 8888, "你好，服务端", 10)
    print udp_connect('127.0.0.1', 10010, "你好，服务端", 10)
