# -*- coding:UTF-8 -*-
import platform
import socket
import time
import os


def is_win():
    return 'Windows' in platform.system()


def is_linux():
    return 'Linux' in platform.system()


# 获取linux ip
def get_linux_ip():
    import fcntl  # Linux 下的Python自带模块，win不带
    import struct

    ifname = 'bond0'  # 网口
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])


# 获取本机内网IP
def get_private_ip():
    ip_list = socket.gethostbyname_ex(socket.gethostname())
    # 本机所有内网IP
    ips = ip_list[2]
    return ips[0]


# 获取本机IP
def get_ip():
    if is_win():
        return get_private_ip()
    else:
        return get_linux_ip()


# 轻量级记录日志
def log(msg):
    log_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "/log"
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_file = log_path + "/info.log"

    # 以追加模式打开一个文件，如果文件不存在则创建文件
    log_file = open(log_file, 'a')
    log_file.write(msg + "\n")
    log_file.close()


def read_1(name):
    result = ""

    # 读取资源
    # 'r'表示读取
    # 'w'表示写入
    # 'a'表示添加
    # '+'表示读写
    # 'b'表示2进制访问
    f = open(name, 'rb')

    # 表示读取全部内容
    text = f.read()

    result = ''.join(text)

    f.close()

    return result


def read_2(name):
    s1 = time.clock()

    result = ""
    file = open(name, 'rb')

    while 1:
        data = file.readline(10 * 1024)
        if not data:
            break
        result += ''.join(data)

    e1 = time.clock()
    print "cost time " + str(e1 - s1)
    return result
