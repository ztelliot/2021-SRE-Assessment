#coding = utf8
from fastapi import FastAPI
from fun import file_app
from fun import rewrite_app


# """接口路由"""
app = FastAPI()  # 主应用
# app.include_router(app_path, prefix="/path_var", tags=["路径变量"])
# app.include_router(app_respond,prefix="/respond",tags=["响应"])
app.include_router(file_app,prefix="/file",tags=["反向代理配置"])
app.include_router(rewrite_app,prefix="/rewrite",tags=["重定向设置"])
