#!/usr/bin/python
# -*- coding:UTF-8 -*-

from Mm import *

# 当前脚本所在的目录
__cur_path__ = os.path.abspath(os.path.dirname(__file__))

# 当前脚本所在目录的父级目录
__par_path__ = os.path.dirname(__cur_path__)


def jia_m():
    pc = Mm()

    p = __par_path__ + "/src/s"
    txt = util.read_1(p)

    mm_txt = pc.encrypt(txt)

    p_o = __par_path__ + "/src/1"
    util.write_1(p_o, mm_txt)


def jie_m():
    pc = Mm()

    p = __par_path__ + "/src/1"
    txt = util.read_1(p)

    mm_txt = pc.decrypt(txt)

    p_o = __par_path__ + "/src/2"
    util.write_1(p_o, mm_txt)


def main():
    pc = Mm('keyskeyskeyskeys')  # 初始化密钥
    e = pc.encrypt("00000")
    d = pc.decrypt(e)
    print e, d

if __name__ == '__main__':
    jia_m()
    main()
    jie_m()