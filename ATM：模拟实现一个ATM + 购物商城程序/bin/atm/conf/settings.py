# -*- coding:utf-8 -*-
__author__ = 'shisanjun'

import os
import logging

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE={
    "engine":"file_store",
    "name":"atm",
    "path":"%s" %os.path.join(BASE_DIR,"db")
}

#日志等级:DEBUG,INFO,WARNING,ERROR,CRITICAL
LOG_LEVEL=logging.INFO

#transaction交易日志,access操作日志
LOG_FILE={
    "transaction":"transaction.log",
    "access":"access.log"
}

#设置信用卡默认额度和还款日期
TRANSACTION_CREDIT=15000
TRANSACTION_PAY_DAY=22

#设置手续费
TRANSACTION_TYPE = {
    'repay':{'action':'plus', 'interest':0},
    'withdraw':{'action':'minus', 'interest':0.05},
    'transfer':{'action':'minus', 'interest':0.05},
    'consume':{'action':'minus', 'interest':0},

}











