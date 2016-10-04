# -*- coding:UTF-8 -*-

import os
import util
import codecs

# 当前脚本所在的目录
__path__ = os.path.abspath(os.path.dirname(__file__))
# __path__ = os.path.realpath(os.path.dirname(__file__))

# 当前脚本所在目录的父级目录
__dir_path__ = os.path.dirname(__path__)

# 输出到文本
__file_path__ = __path__ + os.path.sep + "file"

# True 作为黑名单拦截, False 作为白名单通过
__black_list__ = True

# 文件格式名单 : "" 代表没有后缀名的文件
__file_suffix__ = ["", ".bat", ".pptx", ".docx"]

# 目录名单
__ignore_dir__ = ["lib", "html", "log"]


# 获取文件列表
def get_file_list(path, file_list):
    if os.path.isfile(path):
        # 文件

        # 文件后缀
        suffix = os.path.splitext(path)[1]

        # 替换掉 绝对路径的前缀
        path = path.replace(__dir_path__, "")

        if __black_list__:
            # 不在黑名单 -- 放行
            if suffix.lower() not in __file_suffix__:
                file_list.append(path.decode('gbk'))
        else:
            # 在白名单 -- 放行
            if suffix.lower() in __file_suffix__:
                file_list.append(path.decode('gbk'))

        # 用 gbk 解析,用utf-8存储
        util.log(path.decode('gbk').encode('utf-8'))
    elif os.path.isdir(path):
        # 目录
        for item in os.listdir(path):
            # 如果需要忽略某些文件夹，使用以下代码
            # print item.decode('gbk')
            if __black_list__:
                # 在黑名单 -- 拦截
                if item.lower() in __ignore_dir__:
                    continue
            else:
                # 不在白名单 -- 拦截
                if item.lower() not in __ignore_dir__:
                    continue

            new_dir = os.path.join(path, item)
            get_file_list(new_dir, file_list)
    else:
        print "Error ", path

    return file_list


def write_in_file(file_path, file_list):
    # 'r'：只读（缺省。如果文件不存在，则抛出错误）
    # 'w'：只写（如果文件不存在，则自动创建文件）
    # 'a'：附加到文件末尾
    # 'r+'：读写
    src_file = codecs.open(file_path, "w", "utf-8")

    txt = ""
    for i in file_list:
        txt += i + "\n"

    src_file.write(txt)

    src_file.close()


def print_file_list(file_list):
    for item in file_list:
        print item

    print "total", len(file_list)


def main():
    # 获取共享文件列表
    util.log("==========文件资源=======================")
    f_list = get_file_list(__dir_path__, [])
    util.log("==========total:%-3s====================" % len(f_list))
    # 写入共享文件
    write_in_file(__file_path__, f_list)

    # 打印共享的文件列表
    # print_file_list(f_list)

# if __name__ == '__main__':
#    main()
