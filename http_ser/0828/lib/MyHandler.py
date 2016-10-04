# -*- coding:UTF-8 -*-

import os
import threading
import time
import urllib

import util


class MyHandler(threading.Thread):
    # 当前脚本所在的目录
    __cur_path__ = os.path.abspath(os.path.dirname(__file__))

    # 当前脚本所在目录的父级目录
    __par_path__ = os.path.dirname(__cur_path__)

    def __init__(self, http_client, client_address, header, num):
        threading.Thread.__init__(self)

        self.http_client = http_client
        self.client_address = client_address
        self.header = header
        self.thread_num = num

    # 重写 run 方法
    def run(self):
        print "Thread Object(%d),Time:%s" % (self.thread_num, time.strftime('%Y-%m-%d %H:%M:%S'))

        method = self.header.split(' ')[0]
        uri = self.header.split(' ')[1]
        # print method
        # print uri

        # req_list = header.split('\n')
        # print "请求头列表", req_list
        # req = req_list[0]
        # parm_list = req.split(' ')
        # print parm_list  # ['GET', '/', 'HTTP/1.1\r'] ,['GET', '/html/index.html', 'HTTP/1.1\r']
        # GET POST ...
        # method = parm_list[0]
        # print method
        # uri = parm_list[1]
        # print uri

        if method == "GET":
            req = self.get(self.client_address, uri)
        elif method == "POST":
            form = self.header.split('\r\n')
            req = self.post(uri, form)
        elif method == "PUT":
            req = self.put()
        elif method == "DELETE":
            req = self.delete()
        else:
            req = self.get(self.client_address, uri)

        # util.log("%s %s %s \n%s" % (time.strftime('%Y-%m-%d %H:%M:%S'), client_address[0], 'response: ', req))
        # print time.strftime('%Y-%m-%d %H:%M:%S'), client_address[0], 'response: ', req

        # 向客户端返回请求的资源
        self.http_client.send(req)

        # 关闭客户端
        self.http_client.close()
        # print client_address[0], "close"

    def get(self, client_address, uri):
        print time.strftime('%Y-%m-%d %H:%M:%S'), client_address[0], 'request : ', urllib.unquote(uri)
        util.log("%s %s %s %s" % (time.strftime('%Y-%m-%d %H:%M:%S'), client_address[0], 'request : ',
                                  urllib.unquote(uri)))

        # 转换成请求的绝对路径
        if uri == '/':
            # 返回 默认 index 页面
            abs_path = (self.__par_path__ + '/html/index.html').replace("/", os.path.sep)
        else:
            abs_path = (self.__par_path__ + urllib.unquote(uri)).replace("/", os.path.sep)

        util.log("%s %s %s %s" % (time.strftime('%Y-%m-%d %H:%M:%S'), client_address[0], 'response: ', abs_path))
        print time.strftime('%Y-%m-%d %H:%M:%S'), client_address[0], 'response: ', abs_path

        req = self.get_response(abs_path)

        return req

    def post(self, uri, form):
        idx = form.index('')  # Find the empty line
        entry = form[idx:]  # Main content of the request
        value = entry[-1].split('=')[-1]
        print value

        req = self.post_response(uri)
        return req

    def put(self):
        req = self.response("")
        return req

    def delete(self):
        req = self.response("")
        return req

    @staticmethod
    def __code_status__(code):
        if code == 200:
            status = "200 OK "
        elif code == 400:  # 由于客户端请求有语法错误，不能被服务器所理解。
            status = "400 Bad Request "
        elif code == 401:  # 请求未经授权。这个状态代码必须和WWW-Authenticate报头域一起使用
            status = "401 Unauthonzed "
        elif code == 403:  # 服务器收到请求，但是拒绝提供服务。服务器通常会在响应正文中给出不提供服务的原因
            status = "403 Forbidden "
        elif code == 404:  # 请求的资源不存在
            status = "404 Not Found "
        elif code == 500:  # 服务器发生不可预期的错误
            status = "500 Internal Server Error "
        elif code == 503:  # 服务器当前不能够处理客户端的请求，在一段时间之后，服务器可能会恢复正常
            status = "503 Service Unavailable "
        else:
            status = "404 Not Found "

        return status

    @staticmethod
    def __context_type__(suffix):
        if suffix in [".html", ".htm", ".htx"]:
            c_type = "text/html;charset=utf-8"
        elif suffix in [".js"]:
            c_type = "application/javascript"
        elif suffix in [".css"]:
            c_type = "text/css"
        elif suffix in [".ico"]:
            c_type = "image/x-icon"
        elif suffix in [".gif"]:
            c_type = "image/gif"
        elif suffix in [".jpeg"]:
            c_type = "image/jpeg"
        elif suffix in [".png"]:
            c_type = "image/png"
        elif suffix in [".jpg"]:
            c_type = "image/jpg"
        else:
            c_type = "text/html;charset=utf-8"

        return c_type

    @staticmethod
    def response_header(code, suffix):

        status = MyHandler.__code_status__(code)

        util.log(status)
        print status

        c_type = MyHandler.__context_type__(suffix)
        tmp_hd = "HTTP/1.1 %s \r\nContext-Type:%s \r\nServer: Python version 1.0\r\nContext-Length:" % (status, c_type)

        return tmp_hd

    @staticmethod
    def get_response(abs_path):

        # 资源后缀
        suffix = os.path.splitext(abs_path)[1].lower()

        # 处理路径里的汉字 导致os.path.exists 不生效问题
        new_path = ''.join(x.decode('utf-8') for x in abs_path.split())
        if os.path.exists(new_path):
            header = MyHandler.response_header(200, suffix)
        else:
            header = MyHandler.response_header(404, suffix)
            return header

        # 读取资源
        txt_str = util.read_2(new_path)

        txt = "%s %d \n\n%s\n\n" % (header, len(txt_str), txt_str)

        return txt

    @staticmethod
    def post_response(header, abs_path):
        source = abs_path.replace("/", os.path.sep)

        print source
        # 读取资源
        txt_str = util.read_1(source)

        return "%s %d \n\n%s\n\n" % (header, len(txt_str), txt_str)
