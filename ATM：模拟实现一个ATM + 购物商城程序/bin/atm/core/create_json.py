# -*- coding:utf-8 -*-
__author__ = 'shisanjun'

import json
import os,sys

#信用卡信息
card_dict={
    "id":None,
    "name":None,
    "passwd":None,
    "credit":None,
    "balance":None,
    "enroll_date":None,
    "expire_date":None,
    "pay_date":None,
    "status":None
}

#商品信息
shops_dict={
    "shop_name":"iphone",
    "price":2999
}

#用户信息
user_dict={
    "name":None,
    "password":None,
    "cardid":None,
    "enroll_date":None
}

#交易信息
trade_dict={
    "name":None,
    "shop_name":None,
    "cardid":None,
    "price":None
}
