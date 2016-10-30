#!/bin/bash

# 消除win平台的回车换行符
# sed -i -e 's/\r$//' your_script.sh

helpFun(){
cat<<help
    usage:$0  [start|stop|restart|status]
help
}

ftpFun(){
    python ./lib/start_ftp.py $1
}

case "$1" in
	start)
		ftpFun start;;
	stop)
		ftpFun stop;;
	restart)
		ftpFun restart;;
	status)
		ftpFun status;;
	-h|help)
	    helpFun ;;
	 *)
		exit 0;;
esac

