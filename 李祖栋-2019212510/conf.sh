#!/bin/bash

#cat > /etc/nginx/conf.d/www.conf<<EOF
#server{
#	server_name ${SERVER_NAME-www.lzd.com};
#	listen ${SER_IP:-0.0.0.0}:${SER_PORT:-80};
#	root ${DOC_ROOT:-/var/share/nginx/html/};
#}
#EOF
# 启动python环境
export  PATH="/home/gaoxiang/miniconda3/bin:"$PATH
source ~/.bashrc
source activate

cd /etc/nginx/myserver
/usr/sbin/nginx -g "daemon off;" &
uvicorn --host 0.0.0.0 main:app

# 以主进程的方式执行nginx命令(一定要有双引号)
#exec "$@"

while [[ true ]]; do
    sleep 1
done
