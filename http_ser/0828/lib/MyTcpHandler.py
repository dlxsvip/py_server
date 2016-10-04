#!/usr/bin/python
# -*- coding:UTF-8 -*-

# SocketServer 多线程并发
import SocketServer
import util
import urllib
import os


# 继承BaseRequestHandler基类，然后必须重写handle方法，并且在handle方法里实现与客户端的所有交互
class MyTcpHandler(SocketServer.BaseRequestHandler):
    # 当前脚本所在的目录
    __cur_path__ = os.path.abspath(os.path.dirname(__file__))

    # 当前脚本所在目录的父级目录
    __par_path__ = os.path.dirname(__cur_path__)

    def handle(self):
        while True:
            # 接收1024字节数据
            data = self.request.recv(1024)
            if not data:
                continue

            method = data.split(' ')[0]
            uri = data.split(' ')[1]

            print method, uri

            if method == "GET":
                self.get(uri)
            elif method == "POST":
                form = data.split('\r\n')
                # self.post(uri, form)
                pass
            elif method == "PUT":
                # self.put()
                pass
            elif method == "DELETE":
                # self.delete()
                pass
            else:
                print method, " not support"

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

        status = MyTcpHandler.__code_status__(code)

        util.log(status)
        print status

        c_type = MyTcpHandler.__context_type__(suffix)
        tmp_hd = "HTTP/1.1 %s \r\nContext-Type:%s \r\nServer: Python version 1.0\r\nContext-Length:" % (status, c_type)

        return tmp_hd

    def get(self, uri):
        # 转换成请求的绝对路径
        if uri == '/':
            # 返回 默认 index 页面
            abs_path = (self.__par_path__ + '/html/index.html').replace("/", os.path.sep)
        else:
            abs_path = (self.__par_path__ + urllib.unquote(uri)).replace("/", os.path.sep)

        # 处理路径里的汉字 导致os.path.exists 不生效问题
        new_path = ''.join(x.decode('utf-8') for x in abs_path.split())

        # 资源后缀
        suffix = os.path.splitext(abs_path)[1].lower()

        print new_path
        if os.path.isfile(new_path):
            # 获取文件大小
            file_size = os.path.getsize(new_path)
            header = self.response_header(200, suffix)
        else:
            # 文件也有可能不存在
            header = self.response_header(404, suffix)
            self.request.send(header)
            return

        # 读取资源
        f = file(new_path, 'rb')
        send_size = 0
        while not file_size == send_size:
            if file_size - send_size > 1024*10:
                data = f.read(1024*10)
                send_size += 1024*10
            else:
                data = f.read(file_size - send_size)
                send_size += (file_size - send_size)

            txt = "%s %d \n\n%s\n\n" % (header, file_size, data)
            self.request.send(data)
            print file_size, send_size
        else:
            print '-----send file"%s done------' % new_path
            f.close()
