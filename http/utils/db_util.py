#!/home/tops/bin/python2.7
# -*- coding:UTF-8 -*-
__author__ = 'yyl'

import json
import os
import yaml

import MySQLdb

host_master = ""
port_master = 0
database_master = ""
user_master = ""
password_master = ""

# 当前脚本父级路径
parent_dir = os.path.dirname(os.path.abspath(__file__))


# 打印全局变量
def test():
    print host_master, port_master, database_master, user_master, password_master


# 执行SQL
def execute(sql):
    con = None
    try:
        con = MySQLdb.connect(host=host_master, port=port_master, db=database_master, user=user_master,
                              passwd=password_master)
        cur = con.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()

        return data
    finally:
        if con:
            con.close()


# 更新
def update(sql):
    updated_row = 0
    con = None
    try:
        con = MySQLdb.connect(host=host_master, port=port_master, db=database_master, user=user_master,
                              passwd=password_master)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        updated_row = cur.rowcount
        cur.close()
    finally:
        if con:
            con.close()
    return updated_row


# 插入
def insert(sql, value):
    con = None
    try:
        con = MySQLdb.connect(host=host_master, port=port_master, db=database_master, user=user_master,
                              passwd=password_master)
        cur = con.cursor()
        cur.execute(sql, value)
        # 提交
        con.commit()

        cur.close()
    except MySQLdb.Error as e:
        print e
        # 回滚
        con.rollback()
    finally:
        if con:
            con.close()


# 批量插入
def batch_insert(sql, values):
    con = None
    try:
        con = MySQLdb.connect(host=host_master, port=port_master, db=database_master, user=user_master,
                              passwd=password_master)
        cur = con.cursor()
        cur.executemany(sql, values)

        # 提交
        con.commit()

        cur.close()
    except MySQLdb.Error as e:
        print e
        # 回滚
        con.rollback()
    finally:
        if con:
            con.close()


def load(conf_file, type='json'):
    file_path = os.path.abspath(conf_file)
    if not os.path.isfile(file_path):
        raise Exception('File not exist. %s' % file_path)

    # 字符串转化成函数执行
    # yf = eval('''%s.load(open(conf_file,'r'))''' % type)

    if type == 'json':
        yf = json.load(open(conf_file, 'r'))
    elif type == 'yaml':
        yf = yaml.load(open(conf_file, 'r'))
    else:
        raise Exception("Invalid file type %s " % type)
    # print yf

    for key in yf.keys():
        globals()[key] = yf[key]
    # print globals()

    return yf


# 本地数据库初始化
def init_local_db():
    cnf = "../conf/db.yaml".replace("/", os.path.sep)

    if not os.path.exists(cnf):
        cnf = "%s/../conf/db.yaml".replace("/", os.path.sep) % parent_dir

    conf_db_master = load(cnf, 'yaml')
    # print type(conf_db_master), conf_db_master

    # 先声明全局变量 在赋值
    global host_master, port_master, database_master, user_master, password_master
    db = conf_db_master['db_local']
    host_master = str(db['db_host'])
    port_master = int(db['db_port'])
    database_master = str(db['db_database'])
    user_master = str(db['db_user'])
    password_master = str(db['db_password'])


# 初始化数据库
def init(op_cfg):
    # 先声明全局变量 在赋值
    global host_master, port_master, database_master, user_master, password_master
    db = op_cfg['database']
    host_master = str(db['t_host'])
    port_master = int(db['t_port'])
    database_master = str(db['t_db'])
    user_master = str(db['t_user'])
    password_master = str(db['t_passwd'])
