#coding = utf8
from fastapi import APIRouter
from pydantic import BaseModel
from enum import Enum
from typing import List
import os
import re
file_name = "/etc/nginx/conf.d/default.conf"

rewrite_app = APIRouter()

"""请求信息的格式"""
class request(BaseModel):
    regular : str = "/"
    path : str = None   # 服务器的路径
    # 给用户的提示模板

"""响应信息"""
class respond(BaseModel):
    handle_res : str = None

class modify(str,Enum):
    add_rewrite = "url重定向添加"



class Re_write():
    def __init__(self,info):
        self.info = info
        self.content = []
        self.already_set = []
        # 读取本地配置文件并赋值给self.content
        self.read_conf()

    def read_conf(self):
        with open(file_name, "r") as f:
            # 把原本文件内容存入数组
            self.content = f.readlines()
            f.close()

    def ret_location(self):
        """返回当前目录的配置区域"""
        line_index = 0  # 匹配到的行号
        flag = False
        rule = "\slocation\s" + "/" + "\s{"  # 正则的规则
        # print("rule:" + rule)
        for index, line in enumerate(self.content):
            # print(index,line)
            # 判断该行是否为该资源的配置块
            if re.search(rule, line):
                flag = True
            if flag == True and re.search("\s}", line):
                return index
        return -1

    def write_conf(self):
        with open(file_name, "w") as f:
            for line in self.content:
                f.write(line)

    def url_rewrite(self):
        respond_info = dict()
        line_index = self.ret_location()
        print(line_index)

        if line_index > 0:
            self.content.insert(line_index + 1, "\n")
            self.content.insert(line_index + 2, f"\tlocation {self.info.regular} " + " {\n")
            self.content.insert(line_index + 3, f"\t\troot {self.info.path};\n")
            self.content.insert(line_index + 4, f"\t\tindex index.html index.htm;\n")
            self.content.insert(line_index + 5, "\t}\n")
        self.write_conf()
        self.restart_nginx(respond_info)
        return  respond_info

    """重启服务器"""
    def restart_nginx(self,respond_info):
        os.system("/usr/sbin/nginx -c /etc/nginx/nginx.conf")
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

@rewrite_app.post("/conf",
               response_model=respond,
               response_model_exclude_unset=True)
def re_write_app(choice:modify,info:request):
    rewrite = Re_write(info=info)
    if choice == "url重定向添加":
        return rewrite.url_rewrite()
