# -*- coding: utf-8 -*-
import json
import os
import time
from datetime import datetime, timedelta


def get_cur_day_time():
    data_str = time.strftime("%Y-%m-%d", time.localtime())
    return data_str+" 00:00:00"

def get_next_day_time():
    result = datetime.now() + timedelta(1)
    data_str = result.strftime("%Y-%m-%d")
    return data_str + " 00:00:00"

def get_pre_day_time():
    result = datetime.now() + timedelta(-1)
    data_str = result.strftime("%Y-%m-%d")
    return data_str+" 00:00:00"

def save_jie_pai_scrapy_time(save_time):
    print "cur path: " + os.getcwd()+" save_time: "+str(save_time)
    save_file = ".\\config\\jie_pai_scrapy_time"
    save_scrapy_time(save_file, save_time)

def save_jie_pai_three_m_scrapy_time(save_time):
    print "cur path: " + os.getcwd()
    save_file = ".\\config\\jie_pai_three_m_scrapy_time"
    save_scrapy_time(save_file, save_time)

def save_jie_pai_hua_ban_scrapy_time(save_time):
    print "cur path: " + os.getcwd()
    save_file = ".\\config\\jie_pai_hua_ban_scrapy_time"
    save_scrapy_time(save_file, save_time)

def save_jie_pai_weibo_scrapy_time(save_time):
    print "cur path: " + os.getcwd()
    save_file = ".\\config\\jie_pai_weibo_scrapy_time"
    save_scrapy_time(save_file, save_time)


def save_scrapy_time(save_file, save_time):
    save_json = {"scrap_time": save_time}
    document = open(save_file, "w+");
    document.write(json.dumps(save_json));


#读取文件
def get_jie_pai_scrapy_time():
    print "cur path: " + os.getcwd()
    save_file = ".\\config\\jie_pai_scrapy_time"
    return get_scrapy_time(save_file)

def get_jie_pai_three_m_scrapy_time():
    print "cur path: " + os.getcwd()
    save_file = ".\\config\\jie_pai_three_m_scrapy_time"
    return get_scrapy_time(save_file)

def get_jie_pai_hua_ban_scrapy_time():
    print "cur path: " + os.getcwd()
    save_file = ".\\config\\jie_pai_hua_ban_scrapy_time"
    return get_scrapy_time(save_file)

def get_jie_pai_wei_bo_scrapy_time():
    print "cur path: " + os.getcwd()
    save_file = ".\\config\\jie_pai_weibo_scrapy_time"
    return get_scrapy_time(save_file)

def get_scrapy_time(save_file):
    document = open(save_file, "r");
    saved_json = document.readline();
    decoded_json = json.loads(saved_json)
    return decoded_json["scrap_time"]