FROM nginx
LABEL author = "lzd"
# 环境变量
ENV HTML_ROOT = "/var/www/html/"  
WORKDIR "/usr/share/nginx"  

# 安装软件
RUN apt update && apt install -y vim && apt install -y net-tools



COPY ./index.html ${HTML_ROOT}/html/ 
# 安装python环境和包
COPY ./conf.sh ./ 
COPY ./Miniconda3-py37_4.9.2-Linux-x86_64.sh ./ 
COPY ./conda.sh	./ 
COPY ./myserver /etc/nginx/myserver

RUN bash -c "/bin/echo -e '\nyes\n\nyes' | bash Miniconda3-py37_4.9.2-Linux-x86_64.sh"
RUN bash conda.sh 

# 暴露端口
EXPOSE 80:80 8000:8000
#

# 用脚本执行CMD传来的命令
ENTRYPOINT ["./conf.sh"]
