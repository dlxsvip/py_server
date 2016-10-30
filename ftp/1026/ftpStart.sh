#!/bin/bash

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

