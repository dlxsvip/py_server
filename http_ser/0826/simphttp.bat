@echo off



:: 不显示窗口
start pythonw ./lib/dir.py

:: 显示窗口
:: start python -m SimpleHTTPServer 80
start python ./lib/simp_http.py

exit