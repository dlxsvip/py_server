# -*- coding:UTF-8 -*-
__author__ = 'yyl'

import logging
import subprocess
import paramiko

logger = logging.getLogger(__name__)


def exe_cmd_local(cmd):
    """  本机 执行 shell  命令 """
    assert cmd not in ['', None]
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    std_out, std_err = process.communicate()

    if process.stdin:
        process.stdin.close()
    if process.stdout:
        process.stdout.close()
    if process.stderr:
        process.stderr.close()

    return process.returncode, std_out, std_err


def exe_cmd_remote(ip, cmd):
    """ 远程执行 shell 命令 """
    assert ip not in ['', None]
    assert cmd not in ['', None]
    cmd_line = 'ssh %s %s' % (ip, cmd)
    process = subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    std_out, std_err = process.communicate()

    if process.stdin:
        process.stdin.close()
    if process.stdout:
        process.stdout.close()
    if process.stderr:
        process.stderr.close()

    return process.returncode, std_out, std_err



def ssh_1(ip, port, username, pwd, timeout=5):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, pwd, timeout)
    stdin, stdout, stderr = ssh.exec_command("ls -l")
    return stdin, stdout, stderr



def ssh_1():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("10.0.x.x", 22, "ubuntu", "ubuntu", timeout=5)
    stdin, stdout, stderr = ssh.exec_command("ls -l")
    print stdout.read()
    ssh.close()

def ssh_31():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # 直接使用密码登陆不上去
    #ssh.connect("114.xxx.xx.xx", 22, "root", "pwd", timeout=5, allow_agent=False, look_for_keys=False)

    # 使用 私钥 登陆（前提，公钥已经放到了Linux服务端）
    # ssh.connect("139.xx.x.xx", 22, "root", key_filename="../../../cert/id_rsa_2048")
    ssh.connect("114.xx.xx.xxx", 22, "root", key_filename="../../../cert/id_rsa_2048")

    stdin, stdout, stderr = ssh.exec_command("ls -l")
    print stdout.read()
    ssh.close()
