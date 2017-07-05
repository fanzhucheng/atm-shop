# -*- coding:utf-8 -*-
__author__ = 'shisanjun'


import time,datetime
import json

from atm.core.main import consume,repay
from atm.core.auth import login_interface
from shops.core import db_handle
from shops.core import auth
from shops.core.log import logger

logger_shop=logger()

user_data = {
    'name':None,
    'is_authenticated':False,
    'user_data':None

}

def register(user_data):
    """
    用户注册
    :return:
    """
    while True:
        name=input("请输入用户名>>").strip()
        password=input("请输入密码>>").strip()
        cardid=input("请输入信用卡号>>").strip()
        if len(name)==0 or password==0 or len(cardid)==0:
            print("用户名或者密码或者信用卡号为空")
            continue
        else:break
    user_dict={}
    today=datetime.date.today().isoformat()
    user_dict["name"]=name
    user_dict["password"]=password
    user_dict["cardid"]=cardid
    user_dict["enroll_date"]=today
    user_data1=db_handle.user_add(user_dict)
    if user_data1:
        logger_shop.info("用户[%s]于[%s]注册成功" %( user_dict["name"],user_dict["enroll_date"]))
        return user_data1
    else:
        logger_shop.info("用户[%s]已存在" %( user_dict["name"]))
        return  user_data


@auth.login_required
def trade(user_data):

    trade_shops=[]
    trade_shop_sucess=[]
    while True:
        shop_l=db_handle.shop_lists()

        print("商品信息如下:")
        print("------------")
        for i,v in enumerate(shop_l):
            print(i,v.get("shop_name"),v.get("price"))

        num=input("请选择购买商品序号，q查看购物车，b退出>>").strip()
        if num=='b':break
        if num=='q':
            print("购物车里商品好下：")
            for i in trade_shops:
                print("商品名称：%s,价格为:%s" %(i[0],i[1]))

        if num not in [str(x) for x in range(len(shop_l))]:continue
        else:
            shop_name=shop_l[int(num)].get("shop_name")
            amount=shop_l[int(num)].get("price")

            cartid=user_data.get("user_data").get("cardid")
            while True:
                choice=input("1:立即支付,2:加入购物车>>").strip()
                if choice not  in ["1","2"]:continue
                else:break

            trade_shops.append((shop_name,amount))
            if choice=="1":
                shop_amount_tmp=0
                for i in trade_shops:
                    shop_amount_tmp+=float(i[1])
                trade_data=login_interface(cartid)

                trade_data_tmp=consume(trade_data,shop_amount_tmp)

                if trade_data_tmp:
                    for i in trade_shops:
                        shop_name_tmp=i[0]
                        shop_amount_tmp=i[1]
                        trade_shop_sucess.append((shop_name_tmp,shop_amount_tmp))


                    trade_shops=[]

    trade_dict={}
    trade_dict["name"]=user_data.get("name")
    trade_dict["trade_time"]=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    if len(trade_shop_sucess):
        print("成功购买的商品如下:")
        print("-"*30)
        for i in trade_shop_sucess:
            print("商品名称：%s,价格为:%s" %(i[0],i[1]))
            trade_dict["shop_name"]=str(i[0])
            trade_dict["price"]=str(i[1])
            db_handle.trade_cumsue(trade_dict)
            logger_shop.info("[%s]用户[%s]成功购买[%s]价格为[%s]元" \
                %(trade_dict["trade_time"],trade_dict["name"],trade_dict["shop_name"],trade_dict["price"]))

@auth.login_required
def shop_info(user_data):
    shop_2=db_handle.shop_lists()
    print("商品信息如下:")
    print("------------")
    for i,v in enumerate(shop_2):
        print(i,v.get("shop_name"),v.get("price"))
    return shop_2

@auth.login_required
def shop_cumsue(user_data):

    shop_l=db_handle.show_pay_prdouct(user_data)

    for trade_dict in shop_l:
        print("[%s]用户[%s]购买商品[%s]价格为[%s]元" \
              %(trade_dict.get("trade_time"),trade_dict.get("name"),\
                trade_dict.get("shop_name"),trade_dict.get("price")))
        logger_shop.info("[%s]用户[%s]购买商品[%s]价格为[%s]元" \
              %(trade_dict.get("trade_time"),trade_dict.get("name"),\
                trade_dict.get("shop_name"),trade_dict.get("price")))

def shop_repay(user_data):
    cartid=user_data.get("user_data").get("cardid")
    trade_data=login_interface(cartid)

    credit_account=float(trade_data.get("account_data").get("credit"))
    balance_acccount=float(trade_data.get("account_data").get("balance"))
    if credit_account>balance_acccount:
        account=credit_account-balance_acccount
        print("需要还款金额为[%s]" %account)
        repay(trade_data)

def exit1(*args):

    exit()

def interactive(user_data):

    while True:
        menu_print="""
-------------购物操作-----------------
        1:查看商品
        2：开始购物
        3：查看已购商品
        4：还信用卡
        0：退出
-------------------------------------
        """

        menu_func={
            "0":exit1,
            "1":shop_info,
            "2":trade,
            "3":shop_cumsue,
            "4":shop_repay
            }

        print(menu_print)

        num=input("请选择操作>>").strip()
        if len(num)==0 or num not  in [str(x) for x in range(0,5)]:continue
        menu_func[num](user_data)

def run():
    while True:
        menu_print="""
-------商品购物-------------
       1:注册用户
       2:用户登录
       其他键退出
---------------------------
        """
        menu_func1={
       "1":register,
        "2":auth.login
        }
        print(menu_print)
        num=input("请选择操作>>").strip()
        if num in ["1","2"]:

            user_data_tmp=menu_func1[num](user_data)
            if user_data_tmp:
                if user_data_tmp["is_authenticated"] :
                    interactive(user_data_tmp)
        else:break
