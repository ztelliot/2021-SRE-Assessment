#coding = utf8
from fastapi import APIRouter
from pydantic import BaseModel
from enum import Enum
from typing import List
import os
import re

# 配置文件的地址(需要特别注意修改!!!)
file_name = "/etc/nginx/conf.d/default.conf"

file_app = APIRouter()

# 让用户选择进行哪一种配置
class modify(str,Enum):
    add_proxy = "反向代理增加"
    del_proxy = "反向代理删除"
    search_proxy = "当前反向代理查询"

"""请求信息的格式"""
class request(BaseModel):
    path : str = "/"
    back_server_ip : str = None   # 需要设置反向代理的服务器ip
    # 给用户的提示模板

"""响应信息"""
class respond(BaseModel):
    currunt_set_proxy : List = None
    handle_res : str = None

class Modify():
    def __init__(self,info):
        self.info = info
        self.content = []
        self.already_set = []
        # 读取本地配置文件并赋值给self.content
        self.read_conf()
    
    def check_ip(self,ip):
        # 注意小阔号的位置
        rule = "^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\." \
               + "(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\." \
               + "(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\." \
               + "(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$"

        # 空了就返回0
        if re.search(rule, ip):
            return True
        else:
            return False


    """返回当前目录的配置区域"""
    def ret_location(self):
        line_index = 0  # 匹配到的行号
        rule = "\slocation\s" + self.info.path + "\s{"  # 正则的规则
        # print("rule:" + rule)
        for index, line in enumerate(self.content):
            # print(index,line)
            # 判断该行是否为该资源的配置块
            if re.search(rule, line):
                return index
        return -1

    def read_conf(self):
        with open(file_name, "r") as f:
            # 把原本文件内容存入数组
            self.content = f.readlines()
            f.close()

    def write_conf(self):
        with open(file_name, "w") as f:
            for line in self.content:
                f.write(line)


    def add_proxy(self):
        """变量声明"""
        respond_info = dict()
    
        """先检查ip是否输入正确"""
        if not self.check_ip(self.info.back_server_ip):
            respond_info["handle_res"] = "请输入正确的ip地址"
            return respond_info

        """匹配该网站路径所对应的配置文件区域"""
        line_index = self.ret_location()

        """是否重复添加判断"""
        for i in range(line_index + 1, len(self.content)-1):
            if(re.search("(\s)(proxy_pass\s.*\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{1,5};)",self.content[i])):
                print(self.content[i])
                respond_info["handle_res"] = "proxy is exist,place don't repeat"
                return respond_info
            # 如果匹配到了结尾
            if re.search("\s}",self.content[i]):
                break

        """将反向代理的内容写入文件"""
        self.read_conf()
    
        """ 插入内容 """
        if line_index > 0:
            self.content.insert(line_index + 1, f"\tproxy_pass http://{self.info.back_server_ip}:80;\n")
            self.already_set.append(f"{self.info.back_server_ip}")
        else:
            respond_info["handle_res"] = "Your path is not exist"



        # 将修改好的内容重新写入配置文件
        with open(file_name, "w") as f:
            for line in self.content:
                f.write(line)
    
        # 返回当前配置文件中反向代理的ip
        self.search_proxy_line()

        self.restart_nginx(respond_info)

        respond_info["currunt_set_proxy"] = list(set(self.already_set))  # 去重返回
        if not "handle_res" in respond_info:
            respond_info["handle_res"] = f"Add {self.info.back_server_ip} to conf successfully"
    
        else:
            respond_info["handle_res"] += f"Add {self.info.back_server_ip} to conf successfully"

        # 返回请求体
        return respond_info

    # 查询的范围还要再确定!
    def del_proxy(self):

        respond_info = dict()
        """先检查要删除的ip格式是否正确"""
        # 先读一下配置文件
        self.read_conf()

        if not self.check_ip(self.info.back_server_ip):
            respond_info["handle_res"] = "删除失败,请输入正确的ip地址"
    
        """将反向代理的内容写入文件"""
        # 匹配到传入的ip后将对应行删除
        line_index = self.ret_location()

        # print("搜索长度:",len(self.content))
        """寻找并删除目标ip"""
        # print(f"len is {len(self.content)-1}")
        for i in range(line_index + 1, len(self.content)-1):
            print(i,self.content[i])
            if(re.search(self.info.back_server_ip,self.content[i])): # 匹配到了该ip,就把对应的行给干掉
                del self.content[i]
                respond_info["handle_res"] = f"delete {self.info.back_server_ip} successfully"

            # 如果匹配到了结尾
            if re.search("\s}",self.content[i]):
                if not "handle_res" in respond_info:
                    respond_info["handle_res"] = f"Can't find {self.info.back_server_ip}"
                    break

        """将删除好的内容重新写入配置文件"""
        self.write_conf()
    
        """返回当前的ip"""
        self.search_proxy_line()

        self.restart_nginx(respond_info)

        """返回响应体"""
        respond_info["currunt_set_proxy"] = list(set(self.already_set))  # 去重返回
        return respond_info

    """寻找当前配置文件中的代理ip,赋值给self.already_set"""
    def search_proxy_line(self):
        line_index = self.ret_location()
        # print(line_index)
        self.already_set = []

        for i in range(line_index + 1, len(self.content)):
            rule = "(\s)(proxy_pass\s.*\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{1,5};)"
            if (re.search(rule, self.content[i])):
                self.already_set.append(re.search(rule, self.content[i]).group(2))  # 读出配置文件中的ip部分
            # 如果匹配到了本段的结尾就直接返回
            if (re.match("\s}", self.content[i])):
                break

    def search_proxy(self):
        respond_info = dict()

        self.search_proxy_line()
        respond_info["handle_res"] = "Successfully return"
        respond_info["currunt_set_proxy"] = self.already_set
        return respond_info

    def restart_nginx(self,respond_info):
        if not os.system("/usr/sbin/nginx -s reload"):
            if "handle_res" not in respond_info:
                respond_info["handle_res"] = "Successfully reload "
            else:
                respond_info["handle_res"] += " Successfully reload"

        else:
            if "handle_res" not in respond_info:
                respond_info["handle_res"] = "conf reload filed"
            else:
                respond_info["handle_res"] += " conf reload filed"



@file_app.post("/conf",
               response_model=respond,
               response_model_exclude_unset=True)
def modify_conf(choice:modify,info:request):
    """
    :param choice: 枚举配置操作类型
    :param self.info: 请求体
    :return: 响应体
    """
    m = Modify(info=info)

    if(choice == "反向代理增加"):
        return m.add_proxy()
    elif(choice == "反向代理删除"):
        return  m.del_proxy()
    elif(choice == "当前反向代理查询"):
        return  m.search_proxy()
