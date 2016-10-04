# -*- coding:UTF-8 -*-
''' http 服务端 '''

import os
import time
import urllib2
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler


# 日志类
class MyLog:
    # 静态属性，通过MyLog.log_file 直接调用,也可以 self.log_file调用
    log_file = os.path.abspath(os.path.dirname(__file__)) + os.path.sep + "http.log"

    def __init__(self):
        pass

    # 静态方法 可以 MyLog.log()直接调用,也可以 self.log()调用
    @staticmethod
    def log(msg):
        # 以追加模式打开一个文件，如果文件不存在则创建文件
        log_file = open(MyLog.log_file, 'a')
        log_file.write(msg + "\n")
        log_file.close()


# http 消息处理 handler
class MyHandler(BaseHTTPRequestHandler):
    rel_host = 'http://192.168.0.12/open/services?'

    def do_GET(self):
        print self.path
        print self.headers

        # date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        self._request = False

        if self._request:
            # 真实的去请求地址
            req = urllib2.Request('%s%s' % (self.rel_host, self.path))
            MyLog.log("%s http request :%s" % (time.strftime('%Y-%m-%d %H:%M:%S'), self.get_json_tmp()))

            rsp = urllib2.urlopen(req)
            content = rsp.read()

            self.sent_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(content)

            MyLog.log("%s http response :%s" % (time.strftime('%Y-%m-%d %H:%M:%S'), content))
        else:
            MyLog.log("%s http request :%s" % (time.strftime('%Y-%m-%d %H:%M:%S'), self.rel_host + self.path))

            # 返回模拟数据
            self.send_response(200)
            self.send_header('Content-type', 'text/html');
            self.end_headers()

            # self.wfile.write(self.get_html_tmp())
            self.wfile.write(self.get_json_tmp())

            MyLog.log("%s http response :%s" % (time.strftime('%Y-%m-%d %H:%M:%S'), self.get_json_tmp()))

    do_POST = do_GET
    do_DELETE = do_GET
    do_PUT = do_GET

    @staticmethod
    def get_html_tmp():
        return """<!DOCTYPE HTML>
        <html lang="utf-8>
        <head>
            <meta charset="UTF-8">
            <title></title>
        </head>
        <body>
            <p> this is get!</p>
        </bode>
        </html>
        """

    @staticmethod
    def get_json_tmp():
        return '''
        {
            "code":200,
            "msg":"successful",
            "data":{
                "vm_name":"test-1",
                "vm_ip":"192.168.0.12"
            }
        }
        '''


# http 服务 类
class MyHttpServer:
    def __init__(self):
        # 默认端口
        self.port = 8012
        self.http_server = None

    def start(self, port=None):
        if port:
            # 传端口 则使用端口参数，否则继续使用默认端口
            self.port = port

        # http 服务端  IP 端口,'' 表示本机IP
        self.http_server = HTTPServer(('', self.port), MyHandler)

        # date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        MyLog.log("%s http server start :%d" % (time.strftime('%Y-%m-%d %H:%M:%S'), self.port))

        # 接受消息
        self.http_server.serve_forever()

    def stop(self):
        if self.http_server:
            self.http_server.socket.close()
            MyLog.log("%s http server stop :%d" % (time.strftime('%Y-%m-%d %H:%M:%S'), self.port))


if __name__ == '__main__':

    http_server = MyHttpServer()
    try:
        http_server.start()
    except Exception as e:
        MyLog.log('type:%s, info:%s', type(e), e)
        http_server.stop()
