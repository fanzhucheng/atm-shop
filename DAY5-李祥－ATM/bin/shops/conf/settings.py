# -*- coding:utf-8 -*-
__author__ = 'shisanjun'

import os
import logging

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE={
    "engine":"file_store",
    "name":"shops",
    "path":"%s" %os.path.join(BASE_DIR,"db")
}

#日志等级:DEBUG,INFO,WARNING,ERROR,CRITICAL
LOG_LEVEL=logging.INFO
LOG_FILE="shop.log"



