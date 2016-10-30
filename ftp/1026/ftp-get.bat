@echo off


:: 创建 auto_ftp_tmp.cfg 文件
set ftp_file_tmp=auto_ftp_tmp.cfg

:: ----写入以下内容到 auto_ftp_tmp.cfg 文件----

:: ftp连接地址
echo open 192.168.122.1 21>"%ftp_file_tmp%"
:: 用户名
echo testftp>>"%ftp_file_tmp%"
:: 密码
echo ******>>"%ftp_file_tmp%"

:: 查看远程目录
::echo dir>>"%ftp_file_tmp%"

:: 设置 ftp 本地目录
echo lcd D:\test\tmp >>"%ftp_file_tmp%"

:: 查看本地目录
::echo !dir>>"%ftp_file_tmp%"

::二进制传输
echo bin >>"%ftp_file_tmp%"

::下载文件
echo get test.xls>>"%ftp_file_tmp%"

:: 退出ftp
::echo bye >>"%ftp_file_tmp%"

::----写入完毕----

::ftp 执行auto_ftp_tmp.cfg文件
ftp -s:"%ftp_file_tmp%"

::删除auto_ftp_tmp.cfg文件
::del "%ftp_file_tmp%"