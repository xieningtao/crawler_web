# encoding:UTF-8
# from pipelines import UploadJiePaiPicPipeline
#
# upload = UploadJiePaiPicPipeline()
# url = "https://api2.bmob.cn/2/files/newtest.jpg"
# path = 'C:\\Users\\g8876\\Desktop\\jiepai\\full\\test.jpg'
# upload.uploadImgFile(url,path)

#时间
import json
import os
import time

from datetime import datetime, timedelta

from com.utils import time_utils


def save_scrapy_time(save_file,save_time):
    save_json = {"scrap_time": save_time}
    document = open(save_file, "w+");
    document.write(json.dumps(save_json));

#读取文件
# def get_scrapy_time(save_file):
#     document = open(save_file, "r");
#     saved_json = document.readline();
#     decoded_json = json.loads(saved_json)
#     return decoded_json["scrap_time"]
#
# print "cur path: "+os.getcwd()
# result = datetime.now()
# save_file = ".\\config\\jie_pai_scrapy_time"
# save_time = result.strftime("%Y-%m-%d ")+"00:00:00"
# print "save_time: " +save_time
# time_utils.save_jie_pai_scrapy_time(save_time)
# scrapy_time = time_utils.get_jie_pai_scrapy_time()
# print "jie_pai_scrapy_time: "+scrapy_time



#图片
import urllib

import requests
from io import BytesIO

from PIL import Image

img_file="C:\\Users\\g8876\\Desktop\\craw_img"
# url = "https://ss2.baidu.com/6ONYsjip0QIZ8tyhnq/it/u=2923979759,2371125262&fm=175&app=25&f=JPEG?w=640&h=1138&s=33B5B6AE48A4F6DA593E03A60300706B"
# url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRUdORMzPDvgsGW6qX22IMNWEAQSc_WbZsQCFJlYeSx9AEC9wNHFA"
url = "https://ss1.baidu.com/6ONXsjip0QIZ8tyhnq/it/u=3497976688,645752398&fm=173&app=25&f=JPEG?w=640&h=1138&s=4708FD031EDC3BE9047CB0560300C0F0"
resp = requests.get(url)

img_name = img_file+"\\test.jpg";
with open(img_name, 'wb') as file:  # 以byte形式将图片数据写入
    file.write(resp.content)
    file.flush()
file.close()

# img = Image.open(BytesIO(resp.content))
# img.save(img_file+"\\test.jpg")
#
# # 网络上图片的地址
# img_src = 'http://img.my.csdn.net/uploads/201212/25/1356422284_1112.jpg'

# 将远程数据下载到本地，第二个参数就是要保存到本地的文件名
# urllib.urlretrieve(url,img_file+"\\test.jpg")
