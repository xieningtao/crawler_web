# -*- coding: utf-8 -*-
import json
import logging
import re

import scrapy
import time
from bs4 import BeautifulSoup

from com.utils.bmob_upload_helper import BMobUploadHelper

class JiepaiWeiBoSpider(scrapy.Spider):
    name = 'jiepai_wei_bo'
    allowed_domains = ['weibo.com']
    # start_urls = ['http://photo.weibo.com/1304494805/talbum/index#!/mode/2/page/1']
    start_urls = [
                  'https://weibo.com/u/1304494805?is_all=1',#街拍美
                  'https://weibo.com/u/3757458303?is_all=1',#街拍摄美
                  # 'https://weibo.com/tajiepai?is_all=1'#她街拍
                  ]

    def __init__(self,name=None, **kwargs):
        super(JiepaiWeiBoSpider, self).__init__(name)
        self.bmob_helper = BMobUploadHelper()
        self.key_words=["四年"]

    def hit_key_word(self,word):
        result = False
        for my_word in self.key_words:
            result = my_word in word.encode("utf-8")
            if result:
                return result
        return result

    def parse(self, response):
        bsp = BeautifulSoup(response.body, 'lxml')
        wei_bo_group = bsp.select_one(".WB_feed.WB_feed_v3.WB_feed_v4")
        time.sleep(1)
        wei_bo_items = wei_bo_group.select(".WB_feed_detail.clearfix")
        count = 0
        title = ""
        cur_wei_bo_time = "2018-10-21 00:00"
        cur_group_id=""
        point_group_id=""
        for wei_bo_item in wei_bo_items:

            # time
            wei_bo_time_item = wei_bo_item.select_one(".WB_from.S_txt2 > a")
            wei_bo_time = wei_bo_time_item["title"]

            if cmp(wei_bo_time,cur_wei_bo_time) < 0:
                logging.info("time is out of date, wei_bo_time: "+wei_bo_time)
                continue

            # titile
            wei_bo_title_item = wei_bo_item.select_one(".WB_text.W_f14")
            wei_bo_title = wei_bo_title_item.text
            wei_bo_title = wei_bo_title.replace("\n", "").strip()
            reobj = re.compile("\(.*\)")
            wei_bo_title_result, number = reobj.subn("", wei_bo_title)

            #通过关键字过滤一些微博
            if self.hit_key_word(wei_bo_title):
                logging.info("hit_key_word title: "+wei_bo_title)
                continue
            img_urls=[]
            #pic
            wei_bo_pics = wei_bo_item.select(".WB_pic")
            for wei_bo_pic in wei_bo_pics:
                img_item = wei_bo_pic.select_one("img")
                img_url = img_item["src"]
                final_img_url=""
                if "thumb150" in img_url:
                    final_img_url = "http:"+img_url.replace("thumb150","mw690")
                elif "orj360" in img_url:
                    final_img_url = "http:" + img_url.replace("orj360", "mw690")
                img_urls.append(final_img_url)

            if len(img_urls) > 0:
                #cover
                cover_url = img_urls[0]

                #upload cover
                group_content = self.bmob_helper.get_group_content(cover_url, wei_bo_title_result)
                group_url = "https://api2.bmob.cn/1/classes/CardPicGroup"
                logging.info("parse_wei_bo_detail group data: " + json.dumps(group_content, ensure_ascii=False))
                point_group_id = self.bmob_helper.upload_to_bmob(group_url, group_content)

                #upload sub_pics
                sub_pic_url="https://api2.bmob.cn/1/classes/CardPicBean"
                for index in range(1,len(img_urls)):
                    detail_content=self.bmob_helper.get_detail_content("", img_urls[index], point_group_id)
                    logging.info("upload sub_pics json: " + json.dumps(detail_content,ensure_ascii=False))
                    self.bmob_helper.upload_to_bmob(sub_pic_url, detail_content)





