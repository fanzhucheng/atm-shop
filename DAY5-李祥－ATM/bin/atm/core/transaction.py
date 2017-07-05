# -*- coding:utf-8 -*-
__author__ = 'shisanjun'


import time

from atm.core import db_handle
from atm.conf import settings
from atm.core.log import logger

log_transaction=logger("transaction")
def transactions(user_data,amount,tran_type="withdraw",**kwargs):
    action_dict={
        "repay":"还款",
        "withdraw":"提现",
        "transfer":"转账",
        "consume":"消费"
    }
    data=user_data.get("account_data")
    amount = float(amount)
    if tran_type in  settings.TRANSACTION_TYPE:

        interest =  amount * settings.TRANSACTION_TYPE[tran_type]['interest']

        old_balance = data['balance']
        if settings.TRANSACTION_TYPE[tran_type]['action'] == 'plus':
            new_balance = old_balance + amount + interest
        elif settings.TRANSACTION_TYPE[tran_type]['action'] == 'minus':
            new_balance = old_balance - amount - interest
            #check credit
            if  new_balance <0:
                print('''\033[31;1m您的信用额度为[%s]元,您的交易金额为[%s]元,您的剩余金额为[%s]元,交易不成功\033[0m''' %(data['credit'],(amount + interest), old_balance ))
                return
        data['balance'] = new_balance
        db_handle.db_handle("update atm where id=%s" %data['id'],new_data=data)

        bill_dict={
        }
        bill_dict["id"]=str(data['id'])
        bill_dict["tran_type"]=action_dict.get(tran_type)
        bill_dict["amount"]=str(amount)
        bill_dict["interest"]=str(interest)
        bill_dict["action_date"]=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

        db_handle.add_bill(bill_dict)
        log_transaction.info("开号:%s   %s:%s    金额:%s   手续费:%s" %
                          (data['id'],action_dict.get(tran_type), tran_type, amount,interest))
        return user_data
    else:
        print("\033[31;1mTransaction type [%s] is not exist!\033[0m" % tran_type)



