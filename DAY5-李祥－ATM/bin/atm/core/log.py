# -*- coding:utf-8 -*-
__author__ = 'shisanjun'

import logging
import sys,os

from atm.conf import settings

def logger(log_type):

    log_file="%s" %os.path.join(settings.BASE_DIR,"log",settings.LOG_FILE[log_type])

    log_level=settings.LOG_LEVEL


    logger_var=logging.getLogger(log_type)
    logger_var.setLevel(log_level)

    ch=logging.StreamHandler()
    ch.setLevel(log_level)

    fh=logging.FileHandler(log_file,encoding="utf-8")
    fh.setLevel(log_level)

    #fomatter=logging.Formatter('%(asctime)s  %(name)s  %(levelname)s - %(message)s')
    fomatter=logging.Formatter('%(asctime)s  %(levelname)s - %(message)s')
    ch.setFormatter(fomatter)
    fh.setFormatter(fomatter)

    if len(logger_var.handlers)>=1:
        return logger_var

    logger_var.addHandler(ch)
    logger_var.addHandler(fh)

    return logger_var
