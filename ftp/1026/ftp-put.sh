#!/bin/bash

ftp -n <<!
open 192.168.
user testftp ******
binary
cd /opt/yyl/ftp1.0
lcd /opt/yyl/ftp1.0
prompt
mput *
close
bye
!
