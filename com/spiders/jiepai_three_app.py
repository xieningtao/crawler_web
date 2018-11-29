# -*- coding: utf-8 -*-
import logging

import requests
import scrapy
import json

import time

from com.utils.bmob_upload_helper import BMobUploadHelper

from com.utils import time_utils


class JiepaiThreeAppSpider(scrapy.Spider):
    name = 'jiepai_three_app'
    allowed_domains = ['app.3ajiepai.com']
    start_urls = ['http://app.3ajiepai.com/thread/list?fid=170&page=1&pageSize=20']

    def __init__(self,name=None, **kwargs):
        super(JiepaiThreeAppSpider,self).__init__(name)
        self.cur_time = time_utils.get_jie_pai_three_m_scrapy_time()
        self.cookies_jie_pai = {}
        self.bmob_helper = BMobUploadHelper()

    def start_requests(self):
        jsession_id,jie_pai = self.get_login_info()
        self.cookies_jie_pai={
            '__cfduid': 'd038136efebfcd498fc25c12f2a9cbad81539412011',
            'JSESSIONID': jsession_id,
            '3ajiepai': jie_pai
        }
        for url in self.start_urls:
            yield scrapy.Request(url,cookies=self.cookies_jie_pai)

    def get_login_info(self):
        login_url = "http://app.3ajiepai.com/wechat/login?code=onQGp1RAFbnzN6m4y259Qma2vMu4"
        response = requests.get(login_url)
        jsession_id = response.cookies["JSESSIONID"]
        jie_pai = response.cookies["3ajiepai"]
        logging.info("response cookies: "+str(response.cookies))
        return  jsession_id,jie_pai

    def parse(self, response):
        logging.info("jiepai_three_app response: "+response.body)
        json_content = json.loads(response.body)

        data_array = json_content["data"]
        count = 0
        for data_item in data_array:
            # count +=1
            # if count ==2:
            #     break
            #time
            data_date = data_item["dateline"]
            timeArray = time.localtime(int(data_date))
            jie_pai_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            if cmp(jie_pai_time, self.cur_time) < 0:
                logging.info("time is out of date, jie_pai_time: " + jie_pai_time)
                return

            # 封面
            data_thumb = data_item["thumb"]
            # title
            data_subject = data_item["subject"]
            #id
            data_tid = data_item["tid"]

            detial_url = "http://app.3ajiepai.com/thread/"+str(data_tid)

            yield scrapy.Request(detial_url,
                                 meta={
                "data_thumb":data_thumb,
                "data_subject":data_subject,
            },
           cookies= self.cookies_jie_pai,
            callback=self.handle_detail)

        # 所有的事情都办完了
        time_utils.save_jie_pai_three_m_scrapy_time(time_utils.get_next_day_time())


    def handle_detail(self,response):
        data_thumb = response.meta["data_thumb"]
        data_subject = response.meta["data_subject"]
        data_detail = json.loads(response.body)
        photos = data_detail["data"]["photos"]
        point_group_id = ""
        sub_pic_url = "https://api2.bmob.cn/1/classes/CardPicBean"
        first_photo = True;
        for photo in photos:
            img_url = photo["origin"]
            # 第一张：
            if first_photo:
                group_content = self.bmob_helper.get_group_content(img_url, data_subject)
                group_url = "https://api2.bmob.cn/1/classes/CardPicGroup"
                logging.info("parse_wei_bo_detail group data: " + json.dumps(group_content, ensure_ascii=False))
                point_group_id = self.bmob_helper.upload_to_bmob(group_url, group_content)
                first_photo = False
            else:
                detail_content = self.bmob_helper.get_detail_content("", img_url, point_group_id)
                logging.info("upload sub_pics json: " + json.dumps(detail_content, ensure_ascii=False))
                self.bmob_helper.upload_to_bmob(sub_pic_url, detail_content)


