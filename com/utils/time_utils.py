# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta


def get_cur_day_time():
    data_str = time.strftime("%Y-%m-%d", time.localtime())
    return data_str+" 00:00:00"

def get_pre_day_time():
    result = datetime.now() + timedelta(-1)
    data_str = result.strftime("%Y-%m-%d")
    return data_str+" 00:00:00"