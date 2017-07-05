# -*- coding:utf-8 -*-
__author__ = 'shisanjun'

import os,sys
import datetime

from atm.core import create_json
from atm.core import db_handle
from atm.conf import settings
from atm.core.log import logger
from atm.core import auth
from atm.core import transaction


log_access=logger("access")
#log_transaction=logger("transaction")
user_data = {
    'account_id':None,
    'is_authenticated':False,
    'account_data':None

}

def register(user_data):
    """
    注册用户
    """
    while True:
        name=input("请输入您的姓名>>").strip()
        passwd=input("请输入您的密码>>").strip()
        if len(name)==0 or len(passwd)==0:
            print("你的用户名或者密码为空，请重新输入\n")
            continue
        else:break

    enroll_date=datetime.date.today()
    expire_date=datetime.date(enroll_date.year+4,enroll_date.month,enroll_date.day)
    expire_date=expire_date.isoformat()
    enroll_date=enroll_date.isoformat()

    card_json=create_json.card_dict
    card_json["id"]=db_handle.set_id("atm")
    card_json["name"]=name
    card_json["passwd"]=passwd
    card_json["credit"]=settings.TRANSACTION_CREDIT
    card_json["balance"]=settings.TRANSACTION_CREDIT
    card_json["enroll_date"]=enroll_date
    card_json["expire_date"]=expire_date
    card_json["pay_date"]=settings.TRANSACTION_PAY_DAY
    card_json["status"]=0
    db_handle.add(card_json,table_name="atm")

    user_data["account_id"]=card_json["id"]
    user_data["is_authenticated"]=True
    user_data["account_data"]=card_json
    info="""
    ---------------------------------------------
    恭喜姓名为:%s的用户开卡成功
    你的卡号为:%s
    你的信用额度为:%s元
    你的还款日期为每月第%s天
    登陆请使用开号登录
    ---------------------------------------------
    """ %(name,card_json["id"],card_json["credit"],card_json["pay_date"])

    print(info)
    log_access.info("恭喜姓名为[%s]的用户开卡成功，你的卡号为[%s]，" \
                          "你的信用额度为[%s]元,你的还款日期为每月第%s天" \
                         %(name,card_json["id"],card_json["credit"],card_json["pay_date"]))

    return user_data

#用户详细信息查询
@auth.login_required
def query_info(user_data):
    """
    查询用户详情
    """
    if not user_data.get("account_data"):
        user_data=db_handle.db_handle("select atm where id=%s" %user_data.get("account_id"))
    data=user_data.get("account_data")
    info="""
----------用户信息-------------------
    开   号：%s
    姓   名：%s
    信用额度：%s元
    剩余额度：%s元
    注册日期：%s
    过期日期：%s
    每月还款日：%s
--------------------------------------
    """ %(data.get("id"),data.get("name"),data.get("credit"),data.get("balance"), \
          data.get("enroll_date"),data.get("expire_date"),data.get("pay_date"))
    print(info)

    log_access.info("开号为%s的用户，查询了用户信息" %(data.get("id")))

@auth.login_required
def query_info2(user_data):
    """
    用户简要信息查询
    """
    if not user_data.get("account_data"):
        user_data=db_handle.db_handle("select atm where id=%s" %user_data.get("account_id"))
    data=user_data.get("account_data")
    info="姓名为[%s]的用户，开号为[%s]额度金额变为[%s]元" \
          %(data.get("name"),data.get("id"),data.get("balance"))
    print(info)
    log_access.info(info)

@auth.login_required
def query_info_condition(user_data):
    """
    查询用户详情
    """
    account_id=format_input("输入查询信用卡的卡号")
    data=db_handle.db_handle("select * from atm where id=%s" %account_id)
    if not data:
        log_access.error("开号为%s的用户不存在" %(data.get("id")))
        return

    #data=user_data.get("account_data")
    info="""
    ----------用户信息-------------------
    开   号：%s
    姓   名：%s
    信用额度：%s元
    剩余额度：%s元
    注册日期：%s
    过期日期：%s
    每月还款日：%s
    --------------------------------------
    """ %(data.get("id"),data.get("name"),data.get("credit"),data.get("balance"), \
          data.get("enroll_date"),data.get("expire_date"),data.get("pay_date"))
    print(info)

    log_access.info("开号为%s的用户，查询了用户信息" %(data.get("id")))

@auth.login_required
def query_info_condition2(*args):
    """
    查询用户详情
    """
    account_id=args[1]
    data=db_handle.db_handle("select * from atm where id=%s" %account_id)
    if not data:
        log_access.error("开号为%s的用户不存在" %(data.get("id")))
        return

    #data=user_data.get("account_data")
    info="""
    ----------用户信息-------------------
    开   号：%s
    姓   名：%s
    信用额度：%s元
    剩余额度：%s元
    注册日期：%s
    过期日期：%s
    每月还款日：%s
    --------------------------------------
    """ %(data.get("id"),data.get("name"),data.get("credit"),data.get("balance"), \
          data.get("enroll_date"),data.get("expire_date"),data.get("pay_date"))
    print(info)

    log_access.info("开号为%s的用户，查询了用户信息" %(data.get("id")))

@auth.login_required
def withdraw(user_data):
    """
    提现功能
    """
    print("-------提现提示----------------")
    amount=format_input("输入提取的金额")
    user_data=transaction.transactions(user_data,amount,tran_type="withdraw")
    data=user_data.get("account_data")
    if user_data:
        query_info2(user_data)
        log_access.info("姓名为[%s]的用户，开号为[%s]提现[%s]元成功，剩余金额为[%s]元" \
          %(data.get("name"),data.get("id"),amount,data.get("balance")))
    else:
        log_access.info("姓名为[%s]的用户，开号为[%s]提现[%s]元失败" \
          %(data.get("name"),data.get("id"),amount))

    return user_data

@auth.login_required
def repay(user_data):
    """
    还款功能
    """
    print("-------还款提示----------------")
    amount=format_input("输入还款的金额")
    user_data=transaction.transactions(user_data,amount,tran_type="repay")
    data=user_data.get("account_data")
    if user_data:
        query_info2(user_data)
        log_access.info("姓名为[%s]的用户，开号为[%s]还款[%s]元成功，剩余金额为[%s]元" \
          %(data.get("name"),data.get("id"),amount,data.get("balance")))
    else:
        log_access.info("姓名为[%s]的用户，开号为[%s]还款[%s]元失败" \
          %(data.get("name"),data.get("id"),amount))

    return user_data

@auth.login_required
def transfer(user_data):
    """
    转账功能
    """
    print("-------转账提示----------------")
    account_id =format_input("输入转账的账号")
    amount=format_input("输入转账的金额")

    transfer_data=db_handle.db_handle("select * from atm where id=%s" %account_id)
    if transfer_data:

        user_data1=transaction.transactions(user_data,amount,tran_type="transfer")
        if user_data1:
            user_data_new={
                 'account_id':account_id,
                'is_authenticated':False,
                'account_data':transfer_data
            }
            transaction.transactions(user_data_new,amount,tran_type="repay")
            print("开号为[%s]向开号为[%s]转账[%s]元成功" %(user_data1.get("account_id"),account_id,amount))
            log_access.info("开号为[%s]向开号为[%s]转账[%s]元成功" %(user_data1.get("account_id"),account_id,amount))


        else:
            log_access.error("开号为[%s]向开号为[%s]转账[%s]元失败" \
            %(user_data.get("account_id"),account_id,amount,amount))
            print("开号为[%s]向开号为[%s]转账[%s]元失败"  %(user_data.get("account_id"),account_id,amount,amount))


def consume(user_data,amount):
    """
    消费功能
    """
    user_data1=transaction.transactions(user_data,amount,tran_type="consume")
    if user_data1:
        query_info2(user_data1)
        log_access.info("开号为[%s]消费[%s]元" %(user_data1.get("account_id"),amount))
    else:
        log_access.info("开号为[%s]消费[%s]元失败" %(user_data.get("account_id"),amount))
    return user_data

@auth.login_required
def change_credit(*args):
    """
    修改信用额度
    """
    account_id=format_input("输入修改信用卡的卡号")
    account_credit=format_input("输入修改信用额度数")
    data=db_handle.db_handle("select * from atm where id=%s" %account_id)

    if not data:
        log_access.info("开号为[%s]不存在" %(account_id))
        return

    data["credit"]=float(account_credit)
    db_handle.db_handle("update atm where id=%s" %account_id,new_data=data)
    log_access.info("开号为[%s]修改额度为[%s]元" %(account_id,account_credit))
    print("开号为[%s]修改额度为[%s]元" %(account_id,account_credit))


@auth.login_required
def change_pay_day(*args):
    """
    修改还款日期
    """
    account_id=format_input("输入修改信用卡的卡号")
    account_day=format_input("输入修改信用还款日（1-28）")
    data=db_handle.db_handle("select * from atm where id=%s" %account_id)

    if not data:
        log_access.info("开号为[%s]不存在" %(account_id))
        return
    data["pay_date"]=account_day
    db_handle.db_handle("update atm where id=%s" %account_id,new_data=data)

    log_access.info("开号为[%s]修改还款日为[%s]" %(account_id,account_day))
    print("开号为[%s]修改还款日为[%s]" %(account_id,account_day))


@auth.login_required
def not_freeze(*args):
    """
    冻结账户
    """
    account_id=format_input("输入修改信用卡的卡号")

    data=db_handle.db_handle("select * from atm where id=%s" %account_id)

    if not data:
        log_access.info("开号为[%s]不存在" %(account_id))
        return

    data["status"]=1
    db_handle.db_handle("update atm where id=%s" %account_id,new_data=data)
    log_access.info("开号为[%s]已解除冻结" %(account_id))
    print("开号为[%s]已解除冻结" %(account_id))

def freeze(*args):
    """
    冻结账户
    """
    account_id=format_input("输入修改信用卡的卡号")

    data=db_handle.db_handle("select * from atm where id=%s" %account_id)

    if not data:
        log_access.info("开号为[%s]不存在" %(account_id))
        return

    data["status"]=0
    db_handle.db_handle("update atm where id=%s" %account_id,new_data=data)
    log_access.info("开号为[%s]已冻结" %(account_id))
    print("开号为[%s]已冻结" %(account_id))

@auth.login_required
def bill(user_data):

    cardid=user_data.get("account_id")
    bill_list=db_handle.query_bill(cardid)
    if bill_list:
        for line in bill_list:
            print("[%s]开号为[%s]的用户%s金额为[%s],手续费[%s]" \
              %(line.get("action_date"),line.get("id"),line.get("tran_type"),line.get("amount"),line.get("interest")))
    else:
        print("无账单记录")

@auth.login_required
def bill2(user_data):

    cardid=format_input("请输入卡号")
    bill_list=db_handle.query_bill(cardid)
    if bill_list:
        for line in bill_list:
            print("[%s]开号为[%s]的用户%s金额为[%s],手续费[%s]" \
              %(line.get("action_date"),line.get("id"),line.get("tran_type"),line.get("amount"),line.get("interest")))
    else:
        print("无账单记录")

#金额输入
def format_input(output_str):
    while True:
        amount =str(input("%s>>" %output_str).strip())
        if len(amount)==0 or not amount.isdigit():
            print("%s，请重新输入\n")
            continue
        else:break
    return amount

def menu(user_data):
    menu_print1="""
-------------用户管理中心-----------------
        1:查询用户信息
        2：提现
        3：还款
        4：转账
        5:查看账单
        0：退出
---------------------------------------
    """

    menu_func1={
            "1":query_info,
            "2":withdraw,
            "3":repay,
            "4":transfer,
            "5":bill
    }

    menu_print2="""
-------------管理员管理中心---------------------
        1:查询用户信息
        2：提现
        3：还款
        4：转账
        5：添加用户
        6：调整用户信用额度
        7：调整用户还款日期
        8：冻结用户
        9: 解除冻结用户
        10:查看用户账单
        0：退出
----------------------------------------------
    """

    menu_func2={

            "1":query_info_condition,
            "2":withdraw,
            "3":repay,
            "4":transfer,
            "5":register,
            "6":change_credit,
            "7":change_pay_day,
            "8":freeze,
            "9":not_freeze,
            "10":bill2
    }

    if user_data.get("account_id")==1:
        return menu_print2,menu_func2
    else:
        return menu_print1,menu_func1

def interactive(user_data):
    """
    功能访问接口
    """
    while True:
        menu_print,menu_func=menu(user_data)
        print(menu_print)

        num=input("请选择操作>>").strip()

        if num not  in [str(x) for x in range(len(menu_func.keys())+1)]:continue
        if num=="0":break
        #try:
        menu_func[num](user_data)

       # except:
          #  pass


def run():

    menu_print="""
-------------登陆管理-----------------
            1:用户开卡
            2:用户登录
            其他键退出
---------------------------------------
        """
    menu_func={
        "1":register,
        "2":auth.login,
        }

    print(menu_print)
    num=input("请选择操作>>").strip()
    if num in ["1","2"]:
        menu_func[num](user_data)
    else:
        exit()
    if user_data["is_authenticated"] :
        interactive(user_data)
