# -*- coding:UTF-8 -*-
import time
import json
import requests
import logging

logger = logging.getLogger(__name__)


# 获取cookie，用来进行会话保持
def get_cookie(ip, port, retry=10):
    url = "http://%s:%s" % (ip, port)
    cookies = None
    while retry > 0:
        try:
            rsp = requests.get(url, timeout=5)
            code = rsp.status_code
            cookies = rsp.cookies
            if code == 200:
                break
        except Exception as e:
            logger.error('type:%s, info:%s', type(e), e)
        finally:
            time.sleep(1)
            retry -= 1
    return cookies


# 会话保持，带cookie请求
def http_with_cookie(ip, port, cookie, retry=10):
    url = "http://%s:%s" % (ip, port)
    rsp = None
    while retry > 0:
        try:
            rsp = requests.get(url, cookies=cookie, timeout=5)
            code = rsp.status_code
            if code == 200:
                break
        except Exception as e:
            logger.error('type:%s, info:%s', type(e), e)
        finally:
            time.sleep(1)
            retry -= 1
    return rsp


def http(ip, port, pm, method='GET', retry=10):
    rsp = None
    url = "http://%s:%s/%s" % (ip, port, pm)
    print url
    while retry > 0:
        try:
            if method == 'POST':
                rsp = requests.post(url, timeout=3000)
            elif method == 'PUT':
                requests.put(url, timeout=3000)
            elif method == 'DELETE':
                requests.delete(url, timeout=3000)
            elif method == 'GET':
                rsp = requests.get(url, timeout=3000)
            else:
                rsp = requests.get(url, timeout=3000)

            if rsp.status_code == 200:
                break
        except Exception as e:
            logger.error('%d, type:%s, info:%s', retry, type(e), e)
        finally:
            time.sleep(1)
            retry -= 1

    return rsp
