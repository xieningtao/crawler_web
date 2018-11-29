# -*- coding: utf-8 -*-
from datetime import datetime

import requests
import scrapy
import logging

import time

from PIL import Image
from bs4 import BeautifulSoup
from io import BytesIO
from scrapy.loader import ItemLoader

from com.items import BaiduJiePai
from com.utils.bmob_upload_helper import BMobUploadHelper


class JiepaiBaiDuSpider(scrapy.Spider):
    name = 'jiepai_bai_du'
    allowed_domains = ['mbd.baidu.com',"pic.rmb.bdstatic.com","www.bucuo.me"]
    start_urls = ['https://mbd.baidu.com/newspage/data/landingshare?context=%7B%22nid%22%3A%22news_9092911382839666944%22%2C%22sourceFrom%22%3A%22bjh%22%2C%22url_data%22%3A%22bjhauthor%22%7D']
    # start_urls = ['https://www.bucuo.me/v/news_9229896512998137007']


    def __init__(self,name=None, **kwargs):
        super(JiepaiBaiDuSpider,self).__init__(name)
        self.bmob_helper = BMobUploadHelper()
        self.img_save_path = "C:\\Users\\g8876\\Desktop\\craw_img"

    def parse(self, response):
        bsp = BeautifulSoup(response.body, 'lxml')
        article_list = bsp.select(".contentMedia.contentPadding")
        # article_list = bsp.select(".body > p")
        count = 0
        for article in article_list:
            # count +=1;
            # if count ==2:
            #     break

            img = article.select('img')
            if img:
                img_src = img[0]["src"]
                # img_src = "http://pic.rmb.bdstatic.com/34e6447062a7dc082b37b5044d7c6867.jpeg"
                logging.info('jie_pai_group img_src: ' + img_src )
                self.downloadPic(img_src)
            #文字
            desc = article.next_sibling.select_one(".bjh-p").text
            logging.info("jie_pai_group desc: "+desc)

    def downloadPic(self,url):
        # url = "https://ss2.baidu.com/6ONYsjip0QIZ8tyhnq/it/u=2923979759,2371125262&fm=175&app=25&f=JPEG?w=640&h=1138&s=33B5B6AE48A4F6DA593E03A60300706B"
        resp = requests.get(url)
        img = Image.open(BytesIO(resp.content))
        file_name = datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"_img.jpg"
        img_file_path = self.img_save_path+"\\"+file_name
        logging.info("downloadPic img_file_path: "+img_file_path)
        img.save(img_file_path)


