# -*- coding:utf-8 -*-
__author__ = 'shisanjun'


from shops.core import db_handle

#用户登录装饰器
def login_required(func):
    def wrapper(*args,**kwargs):

        if args[0].get('is_authenticated'):
             func(*args,**kwargs)
        else:
            login(*args)
    return  wrapper


def login(user_data):
    #用户登录

    while True:
        name=input("请输入用户名>>").strip()
        password=input("请输入密码>>").strip()
        if len(name)==0 or len(password)==0:continue
        else:break

    return  db_handle.check_login(name,password)


