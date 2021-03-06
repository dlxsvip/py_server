# -*- coding:UTF-8 -*-

'''
参考来源 http://blog.csdn.net/menglei8625/article/details/7513653

安装模块
pip install pyyaml

'''

import yaml
import os
import sys
from ftplib import FTP

# 当前脚本所在的目录
__cur_path__ = os.path.abspath(os.path.dirname(__file__))

# 当前脚本所在目录的父级目录
__par_path__ = os.path.dirname(__cur_path__)

# ftp 配置文件
__ftp_cfg__ = __par_path__ + "/conf/ftp.yaml".replace("/", os.path.sep)

# 设置缓冲块大小
__buf_size__ = 1024

file_list = []


def login(ip, port, name, pwd):
    if not port:
        port = 21

    ftp = FTP()
    # 打开调试级别2，显示详细信息;0为关闭调试信息
    ftp.set_debuglevel(2)

    try:
        # 连接
        ftp.connect(ip, port)
        debug_print('成功连接到 %s' % ip)
        # 登录，如果匿名登录则用空串代替即可
        ftp.login(name, pwd)
        debug_print('成功登录到 %s' % ip)
        # 显示ftp服务器欢迎信息
        debug_print(ftp.getwelcome())
    except:
        print "连接或登录失败"

    return ftp


def ftp_ups(ftp, local_files, remote_dir='./'):
    try:
        # 在ftp 服务器的 根目下 创建子目录
        ftp.mkd(remote_dir)
    except:
        debug_print('目录已存在 %s' % remote_dir)

    for item in local_files:
        ftp_up(ftp, item, remote_dir)


def ftp_up(ftp, local_file, remote_dir):
    # if is_same_size(ftp,local_file,remote_file):
    #     debug_print('跳过[相等]: %s' % local_file)
    #     return

    # cd 到 ftp 服务器的根目录下的 remote_dir 子目录目录
    ftp.cwd(remote_dir)

    # 以读模式在本地打开文件
    file_handler = open(local_file, 'rb')
    # 上传文件
    ftp.storbinary('STOR %s' % os.path.basename(local_file), file_handler, __buf_size__)
    file_handler.close()

    # cd 到 上级目录
    ftp.cwd('..')
    print "ftp up %s OK" % local_file


def ftp_down_dir(ftp, local_dir='./', remote_dir='./'):
    try:
        # cd 到 服务器目录
        ftp.cwd(remote_dir)
    except:
        debug_print('目录%s不存在，继续...' % remote_dir)

    debug_print('切换至目录 %s' % ftp.pwd())

    # 创建本地目录
    if not os.path.isdir(local_dir):
        os.makedirs(local_dir)

    ftp.dir(get_file_list)
    # print(file_list)
    for item in file_list:
        file_type = item[0]
        file_name = item[1]
        local = os.path.join(local_dir, file_name)
        if file_type == 'd':
            ftp_down_dir(ftp, local, file_name)
        elif file_type == '-':
            ftp_down(ftp, file_name, local_dir)

    ftp.cwd('..')
    debug_print('返回上层目录 %s' % ftp.pwd())


def ftp_down(ftp, down_file, local_dir):
    # 以写模式在本地打开 local_dir + down_file 文件
    file_handler = open(local_dir + down_file, 'wb')
    # 接收服务器上文件并写入本地文件
    ftp.retrbinary('RETR %s' % os.path.basename(down_file), file_handler.write, __buf_size__)
    file_handler.close()
    print "ftp down %s OK" % down_file


def get_file_name(line):
    pos = line.rfind(':')
    while line[pos] != ' ':
        pos += 1

    while line[pos] == ' ':
        pos += 1

    file_arr = [line[0], line[pos:]]
    return file_arr


def get_file_list(line):
    ret_arr = []
    file_arr = get_file_name(line)
    if file_arr[1] not in ['.', '..']:
        file_list.append(file_arr)


def is_same_size(ftp, local_file, remote_file):
    try:
        remote_file_size = ftp.size(remote_file)
    except:
        remote_file_size = -1

    try:
        local_file_size = os.path.getsize(local_file)
    except:
        local_file_size = -1

    debug_print('lo:%d  re:%d' % (local_file_size, remote_file_size), )
    if remote_file_size == local_file_size:
        return 1
    else:
        return 0


def download_file(ftp, local_file, remote_file):
    if is_same_size(ftp, local_file, remote_file):
        debug_print('%s 文件大小相同，无需下载' % local_file)
        return
    else:
        debug_print('>>>>>>>>>>>>下载文件 %s ... ...' % local_file)
        ftp_down(ftp, local_file)


def upload_file(ftp, local_file, remote_file):
    if not os.path.isfile(local_file):
        return
    if is_same_size(ftp, local_file, remote_file):
        debug_print('跳过[相等]: %s' % local_file)
        return
    ftp_ups(ftp, local_file)


def debug_print(s):
    print (s)


def main(argv):
    # len(argv)

    # 读取配置文件
    if not os.path.exists(__ftp_cfg__):
        print "not exist %s" % __ftp_cfg__

    ftp_date = yaml.load(file(__ftp_cfg__))

    # 登录FTP
    ftp_entity = login(ftp_date['ip'], ftp_date['port'], ftp_date['name'], ftp_date['pwd'])

    if ftp_date['method'] == 'put':
        ftp_ups(ftp_entity, ftp_date['put_files'], ftp_date['remote_dir'])
    elif ftp_date['method'] == 'get':
        ftp_down_dir(ftp_entity, ftp_date['local_dir'], ftp_date['remote_dir'])

    # 关闭调试模式
    ftp_entity.set_debuglevel(0)
    # 退出FTP
    ftp_entity.quit()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
