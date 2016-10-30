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

:: 在远程目录的根目录下创建 tmp 目录
echo mkdir tmp>>"%ftp_file_tmp%"

:: 进入 tmp目录
echo cd tmp>>"%ftp_file_tmp%"

:: 设置 ftp 本地目录
echo lcd D:\test >>"%ftp_file_tmp%"

:: 查看本地目录
::echo !dir>>"%ftp_file_tmp%"

:: 批量上传 关闭交互
echo Prompt >>"%ftp_file_tmp%"

:: 二进制传输
echo bin >>"%ftp_file_tmp%"

:: 显示进度
echo hash>>"%ftp_file_tmp%"

:: 批量上传文件
echo mput *.xls>>"%ftp_file_tmp%"

:: 删除远程主机tmp目录下所有文件
::echo delete *.* >>"%ftp_file_tmp%"

:: 返回上级目录
::echo cd .. >>"%ftp_file_tmp%"

:: 删除远程主机tmp目录
::echo mrdir tmp >>"%ftp_file_tmp%"


:: 退出ftp
::echo bye >>"%ftp_file_tmp%"


::----写入完毕----

::ftp 执行auto_ftp_tmp.cfg文件
ftp -s:"%ftp_file_tmp%"

::删除auto_ftp_tmp.cfg文件
del "%ftp_file_tmp%"

