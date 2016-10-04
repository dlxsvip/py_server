# -*- coding:UTF-8 -*-
__author__ = 'yyl'

import os
import platform
import subprocess


def is_win():
    return "Windows" in platform.system()


def is_linux():
    return "Linux" in platform.system()


# 保存到文件
def ipconfig():
    txt = os.getcwd() + os.path.sep + "test.txt"
    handle = open(r'%s' % txt, 'wt')
    subprocess.Popen(['ipconfig', '-all'], stdout=handle)


# 保存到变量中
def ipconfig2():
    if is_linux():
        process = subprocess.Popen(['ifconfig'], shell=True)
        std_out, std_err = process.communicate()
    else:
        process = subprocess.Popen(['ipconfig', '-all'], shell=True)
        std_out, std_err = process.communicate()
    print std_out, std_err


def echo():
    x = subprocess.check_output(["echo", "Hello World!"], shell=True)
    print x


def ls():
    if is_win():
        x = subprocess.call(["dir"], shell=True)
    else:
        x = subprocess.call(["ls", "-l"], shell=True)
    print x


# 显示test.txt里内容
def type_1():
    y = subprocess.check_output(["type", "test.txt"], shell=True)
    print y


type_1()