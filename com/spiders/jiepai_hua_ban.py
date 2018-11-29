# -*- coding: utf-8 -*-
import json
import logging

import scrapy
import time
from bs4 import BeautifulSoup

from com.utils import time_utils
from com.utils.bmob_upload_helper import BMobUploadHelper


class JiepaiHuaBanSpider(scrapy.Spider):
    name = 'jiepai_hua_ban'
    allowed_domains = ['huaban.com']
    start_urls = ['http://huaban.com/favorite/beauty/']
    # start_urls = ['http://huaban.com/boards/24116838/?md=newbn&beauty=']

    def __init__(self,name=None, **kwargs):
        super(JiepaiHuaBanSpider,self).__init__(name)
        self.bmob_helper = BMobUploadHelper()

    def parse(self, response):
        bsp = BeautifulSoup(response.body, 'lxml')
        hua_ban_group = bsp.select_one("#waterfall")
        hua_ban_items = hua_ban_group.select(".pin.wfc")

        cur_hua_ban_time=time_utils.get_jie_pai_hua_ban_scrapy_time()
        for hua_ban_item in hua_ban_items:

            if hua_ban_item.attrs.has_key("data-created-at"):
                #time
                hua_ban_item_time_stamp = hua_ban_item["data-created-at"]
                timeArray = time.localtime(int(hua_ban_item_time_stamp))
                hua_ban_item_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                logging.info("time: "+hua_ban_item_time)

                if cmp(hua_ban_item_time,cur_hua_ban_time) < 0:
                    logging.info("time is out of date, hua_ban_item_time: "+hua_ban_item_time)
                    break

                #图片
                hua_ban_pic_item = hua_ban_item.select_one(".img.x.layer-view.loaded > img")
                hua_ban_pic = hua_ban_pic_item["src"]
                split_index = hua_ban_pic.index("_")
                hua_ban_url ="http:" + hua_ban_pic[0:split_index]+"_fw658"
                # hua_ban_url ="http:" + hua_ban_pic

                group_content = self.bmob_helper.get_group_content(hua_ban_url, "")
                group_url = "https://api2.bmob.cn/1/classes/Beauty"
                logging.info("parse_hua_ban_detail group data: " + json.dumps(group_content, ensure_ascii=False))
                point_group_id = self.bmob_helper.upload_to_bmob(group_url, group_content)

        time_utils.save_jie_pai_hua_ban_scrapy_time(time_utils.get_next_day_time())