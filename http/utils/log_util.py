# -*- coding:UTF-8 -*-
__author__ = 'yyl'

'''
# 使用方法
1.在 py 脚本里 导入
from utils import log_util

2.引用
log_info = log_util.log_info(__name__)
log_err = log_util.log_err(__name__)

#3.使用
log_info.info("...xxx... success")
log_err.error("Error slb :etype %s,info:%s, type(excp), excp)

以上日志默认记录在/logs/auto_info.log，或者 指定 日志文件，步骤2 如下格式
log_info = log_util.log_info(__name__,"t1.log")

'''

import os
import platform
import logging
import logging.handlers

__log_path__ = os.path.abspath(os.path.dirname(__file__)) + "/../logs/"

__log_format_info__ = '%(asctime)s;%(levelname)-8s;%(funcName)-10s;%(message)s'
__log_format_err__ = '%(asctime)s;%(levelname)-8s;%(funcName)s;%(lineno)d;%(message)s'

__default_log_auto__ = 'auto_log.log'
__default_log_auto_debug__ = 'auto_debug.log'
__default_log_auto_info__ = 'auto_info.log'
__default_log_auto_err__ = 'auto_err.log'


def log(name, log_file_name=None):
    if log_file_name:
        log_file = get_log_path() + log_file_name
    else:
        log_file = get_log_path() + __default_log_auto__

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # handler 用于写入到/logs/log.log日志文件
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    # handler 用于 控制台打印
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # 定义handler的输出格式
    formatter = logging.Formatter(__log_format_info__)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 给logger 添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def log_debug(name, log_file_name=None):
    if log_file_name:
        log_file = get_log_path() + log_file_name
    else:
        log_file = get_log_path() + __default_log_auto_debug__

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # handler 用于写入到/logs/debug.log日志文件
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    # handler 用于 控制台打印
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # 定义handler的输出格式
    formatter = logging.Formatter(__log_format_info__)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 给logger 添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def log_info(name, log_file_name=None):
    if log_file_name:
        log_file = get_log_path() + log_file_name
    else:
        log_file = get_log_path() + __default_log_auto_info__

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # handler 用于 按时间写入到不同的日志中写入到/logs/info.log日志文件
    fh = logging.handlers.TimedRotatingFileHandler(log_file, "D", 1, 10)
    fh.setLevel(logging.DEBUG)

    # handler 用于 控制台打印
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # 定义handler的输出格式
    formatter = logging.Formatter(__log_format_info__)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 给logger 添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def log_err(name, log_file_name=None):
    if log_file_name:
        log_file = get_log_path() + log_file_name
    else:
        log_file = get_log_path() + __default_log_auto_err__

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # handler 用于写入到/logs/err.log日志文件
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.ERROR)

    # handler 用于 控制台打印
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # 定义handler的输出格式
    formatter = logging.Formatter(__log_format_err__)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 给logger 添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def get_log_path():
    if is_linux():
        # /var/log/slbtransform/
        # log_path = "/var/log/slbtransform/".replace("/", os.path.sep)
        log_path = __log_path__
    else:
        # ../logs/
        log_path = __log_path__

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    return log_path


def is_win():
    return "Windows" in platform.system()


def is_linux():
    return "Linux" in platform.system()
