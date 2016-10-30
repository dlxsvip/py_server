# -*- coding:UTF-8 -*-

# pip install pyftpdlib
import time

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

import util


class FtpServer:

    def __init__(self):
        self.port = 21

        # dir = os.getcwd()

        if util.is_win():
            dir = "D:\\test"
        else:
            dir = "/opt"

        util.log("ftp分享 %s" % dir)

        # 新建一个用户组
        self.authorizer = DummyAuthorizer()

        # 将用户名，密码，指定目录，权限 添加到里面

        # self.authorizer.add_user("testftp", "******", dir, perm="elr")     # elr   只读权限
        self.authorizer.add_user("testftp", "******", dir, perm="elradfmw")  # adfmw 写权限
        # 这个是添加匿名用户,任何人都可以访问，如果去掉的话，需要输入用户名和密码，可以自己尝试
        # self.authorizer.add_anonymous(dir)

    def start(self, port=None):
        if port:
            self.port = port

        p_ip = util.get_ip()

        handler = FTPHandler
        handler.authorizer = self.authorizer

        ftp_server = FTPServer((p_ip, self.port), handler)

        # 最大连接数
        ftp_server.max_cons = 10

        # 每个ip最大连接限制
        ftp_server.max_cons_per_ip = 3
        # ftp://localhost:21/
        print "start ftp server  -- ftp://%s:%d" % (p_ip, self.port)
        util.log("%s ftp http server  -- ftp://%s:%d" % (time.strftime('%Y-%m-%d %H:%M:%S'), p_ip, self.port))

        # 启动
        ftp_server.serve_forever()


if __name__ == '__main__':
    ftp = FtpServer()
    ftp.start()
