# -*- coding:utf-8 -*-
__author__ = 'shisanjun'
import os,sys
import time,datetime

from atm.core import db_handle
from atm.core.log import logger

log_access=logger("access")
user_data = {
    'account_id':None,
    'is_authenticated':False,
    'account_data':None

}

#用户登录装饰器
def login_required(func):
    def wrapper(*args,**kwargs):

        if args[0].get('is_authenticated'):

            func(*args,**kwargs)
        else:
            login(*args)
    return  wrapper

#登陆验证密码和信用卡是否过期
def acc_auth(account,passwd,table_name):
    sql="select * from %s  where account=%s" %(table_name,account)
    data=db_handle.db_handle(sql)
    if data["passwd"]==passwd:
        expire_date_stmap=time.mktime(time.strptime(data["expire_date"],'%Y-%m-%d'))
        if time.time()>expire_date_stmap or data["status"] in [1,2]:
            data["status"]=1
            db_handle.db_handle("update atm where id=%s" %account,new_data=data)
            print("开号为%s的用户,您的信用卡已过期或冻结\n" %data["id"])
            log_access.error("开号为%s的用户,您的信用卡已过期或冻结\n" %data["id"])
            exit()
        else:
            return data
    else:
        log_access.info("开号为%s的用户,您输入的密码不正确\n" %data["id"])


#用户登录认证
def login(user_data):
    login_count=1

    while user_data["is_authenticated"] is  not True and login_count<=3:
        name=input("请输入您的卡号>>").strip()
        passwd=input("请输入您的密码>>")
        if len(name)==0 or len(passwd)==0:
            print("你的卡号或者密码为空，请重新输入\n")
            login_count +=1
            continue

        record=acc_auth(name,passwd,"atm")
        if record:
            user_data["account_id"]=record["id"]
            user_data["is_authenticated"]=True
            user_data["account_data"]=record

            return record

        login_count +=1
    else:
        error="开号为%s的用户,密码已输错3次\n" %(name)
        log_access.error(error)
        exit()

def login_interface(cardid):
    user_data={}
    login_count=1
    while True and login_count<=3:
        passwd=input("请输入信用卡的密码>>")
        if len(passwd)==0:
            print("你的卡号或者密码为空，请重新输入\n")
            login_count +=1
            continue
        record=acc_auth(cardid,passwd,"atm")
        if record:
            user_data["account_id"]=record["id"]
            user_data["is_authenticated"]=True
            user_data["account_data"]=record
            return user_data

        login_count +=1
    else:
        pass