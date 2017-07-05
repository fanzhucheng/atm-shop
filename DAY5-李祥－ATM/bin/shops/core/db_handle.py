# -*- coding:utf-8 -*-
__author__ = 'shisanjun'

import os
import sys
import json

from shops.conf import settings
#from shops.core import create_json

file_path=os.path.join(settings.DATABASE.get("path"),settings.DATABASE.get("name"))
shop_file_name="%s.json" %file_path
user_file_name="%s.json" %os.path.join(settings.DATABASE.get("path"),"user")
trade_file_name="%s.json" %os.path.join(settings.DATABASE.get("path"),"trade")

def db_handle():

    if settings.DATABASE.get("engine")=="file_store":
        pass
    else:
        pass


def user_add(account_data):
    name=str(account_data.get("name"))
    tag=False
    user_data={}
    if os.path.isfile(user_file_name):

        with open(user_file_name,'r',encoding="utf-8") as f:
            for line in f:
                data_tmp=json.loads(line.strip())
                if name == data_tmp.get("name"):
                    tag=True
                    break
    if not tag:
        with open(user_file_name,'a',encoding="utf-8") as f:
            json_str=json.dumps(account_data)
            f.write("%s\n" %json_str)
            user_data["name"]=name
            user_data["is_authenticated"]=True
            user_data["user_data"]=json_str
            print("用户名为%s的用户注册成功" %name)
        return user_data
    else:
        print("用户名为%s的用户已存在." %name)

def check_login(name,password):
    name=name.strip()
    user_data={}
    if os.path.isfile(user_file_name):
        with open(user_file_name,'r',encoding="utf-8") as f:
            for line in f:
                data_tmp=json.loads(line.strip())
                if data_tmp.get("name")!=name:
                    continue
                if name == data_tmp.get("name") and str(password)==data_tmp.get("password") :
                    user_data["name"]=name
                    user_data["is_authenticated"]=True
                    user_data["user_data"]=data_tmp
                    return user_data
                else:
                    print("密码不正确")
                    exit()

def shop_lists():
    shop_l=[]
    if os.path.isfile(shop_file_name):
        with open(shop_file_name,'r',encoding="utf-8") as f:
            for line in f:
                shop_l.append(json.loads(line.strip()))

    return shop_l

def trade_cumsue(trade_dict):
    trade_json=json.dumps(trade_dict)
    f=open(trade_file_name,'a',encoding="utf-8")
    f.write("%s\n" %trade_json)
    f.flush()
    f.close()

def show_pay_prdouct(user_data):

    name=user_data.get("name")
    show_cumsue_l=[]
    if os.path.isfile(trade_file_name):
        with open(trade_file_name,'r',encoding="utf-8") as f:
            for line in f:
                trade_tmp=json.loads(line)

                if trade_tmp.get("name")==name:
                    show_cumsue_l.append(trade_tmp)
    return show_cumsue_l