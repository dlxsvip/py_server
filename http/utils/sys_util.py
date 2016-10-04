# -*- coding:UTF-8 -*-
import os
import platform
from socket import *


def __is_win__():
    return 'Windows' in platform.system()


def __is_linux__():
    return 'Linux' in platform.system()


def cur_file_ab_path(file):
    path = os.path.abspath(file)
    return path.replace("/", os.path.sep)


# 当前脚本目录路径
def cur_dir_ab_path(file):
    path = os.path.dirname(file).replace("/", os.path.sep)
    return path.replace("/", os.path.sep)


# 当前脚本目录上级目录路径
def par_dir_ab_path(file):
    path = (os.path.dirname(file) + os.path.sep + "..").replace("/", os.path.sep)
    return path.replace("/", os.path.sep)


# 获取本机IP
def __get_ip__():
    if __is_linux__():
        import fcntl  # Linux 下的Python自带模块，win不带
        import struct

        ifname = 'bond0'  # 网口
        s = socket(socket.AF_INET, socket.SOCK_DGRAM)
        return inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])
    else:
        hostname = gethostname()
        return gethostbyname(hostname)


# 获取Linux 分支版本
def __get_linux_v_():
    system_info = platform.linux_distribution()
    print system_info

    if 'Alibaba' in platform.linux_distribution():
        return 'Alibaba'
    elif 'CentOS' in platform.linux_distribution():
        return 'CentOS'
    elif 'Ubuntu' in platform.linux_distribution():
        return 'ubuntu'
    else:
        return 'Other'

