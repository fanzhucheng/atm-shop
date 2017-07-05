# -*- coding:utf-8 -*-
__author__ = 'shisanjun'

import json
import os,sys

from atm.conf import settings


def get_id(table_name):
    file_name="%s.json" %os.path.join(settings.DATABASE["path"],table_name)
    if os.path.isfile(file_name):
        with open(file_name,'r',encoding="utf-8") as f:
            get_json=json.load(f)
    else:
        with open(file_name,'w',encoding="utf-8") as f:
            get_json={table_name:0}
            json.dump(get_json,f)

    return  get_json[table_name]

def set_id(table_name):
    table_id=int(get_id(table_name))
    table_id=table_id +1
    table_dict={table_name:table_id}
    file_name="%s.json" %os.path.join(settings.DATABASE["path"],table_name)
    with open(file_name,'w',encoding="utf-8") as f:
        json.dump(table_dict,f)

    return table_id

def add(data,table_name="atm"):
    table_id=get_id(table_name)
    data["id"]=table_id
    file_name="%s.json" %os.path.join(settings.DATABASE["path"],table_name,str(table_id))
    with  open(file_name,'w',encoding="utf-8") as f:
        json.dump(data,f)

def db_handle(sql,**kwargs):
    sql_list=sql.split("where")

    if sql_list[0].startswith("select") and len(sql_list)> 1:
        column,table_id = sql_list[1].strip().split("=")
        table_name=  sql_list[0].strip().split("from")[1].strip()

        file_name="%s.json" %os.path.join(settings.DATABASE["path"],table_name,str(table_id))

        if os.path.isfile(file_name):
            with  open(file_name,'r',encoding="utf-8") as f:
                json_record=json.load(f)
                return json_record
        else:
               exit("\033[31;1mAccount [%s] does not exist!\033[0m" % table_id )

    elif  sql_list[0].startswith("update") and len(sql_list)> 1:
            column,table_id = sql_list[1].strip().split("=")
            table_name=  sql_list[0].split()[1]
            file_name="%s.json" %os.path.join(settings.DATABASE["path"],table_name,str(table_id))
            new_record=kwargs["new_data"]

            with  open(file_name,'w' ,encoding="utf-8") as f:
                json_record=json.dump(new_record,f)
                return new_record

def add_bill(bill_dict):
    file_name="%s.json" %os.path.join(settings.DATABASE["path"],"bill")
    f=open(file_name,'a',encoding="utf-8")
    bill_str=json.dumps(bill_dict)
    f.write("%s\n" %bill_str)
    f.flush()
    f.close()

def query_bill(cardid):
    bill_list=[]
    file_name="%s.json" %os.path.join(settings.DATABASE["path"],"bill")
    if os.path.isfile(file_name):
        with open(file_name,'r',encoding="utf-8") as f:
            for line in f:
                bill_dict=json.loads(line.strip())

                if str(cardid)==bill_dict.get("id"):
                    bill_list.append(bill_dict)
    return bill_list


