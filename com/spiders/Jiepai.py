# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import logging
from scrapy.loader import ItemLoader
from com.items import HCJiePaiGroup
import requests
import json
import time

import sys

if sys.getdefaultencoding() != 'gbk':
 reload(sys)
 sys.setdefaultencoding('gbk')


class JiepaiSpider(scrapy.Spider):

    name = 'jiepai'
    allowed_domains = [
        'blog.sina.com.cn'
    ,'www.bucuo.me']

    start_urls = [
        'http://blog.sina.com.cn/s/articlelist_1340398703_4_1.html'
    ,
        'https://www.bucuo.me/app/1583407618504778'
    ]


    def __init__(self,name=None, **kwargs):
        super(JiepaiSpider,self).__init__(name)
        self.sina = "http://blog.sina.com.cn/s/articlelist_1340398703_4_1.html"
        self.bucou = "https://www.bucuo.me/app/1583407618504778"
        self.cur_time = "2018-10-18 00:00:00"

    def parse(self, response):
        bsp = BeautifulSoup(response.body, 'lxml')
        cur_url = response.url
        article_class = self.get_article_list_class_by(cur_url)
        article_list = bsp.select(article_class)
        count = 0
        title =""
        for article in article_list:
            count +=1;
            if count == 2:
                break

            article_time_class = self.get_article_time_class_by(cur_url)
            article_time = article.select(article_time_class)
            if cmp(cur_url,self.sina) == 0:
                scrap_time = article_time[0].string
            else:
                scrap_time = article_time[0]["title"]
            #第一个就不满足，可以立即去除掉
            if cmp(self.cur_time,scrap_time) > 0:
                logging.error("jie_pai_group time is out of date cur_time: "+self.cur_time+" scrap_time: "+scrap_time)
                return
            link_title_class = self.get_title_class_by(cur_url)
            link_title = article.select(link_title_class)
            title = link_title[0].string
            link = link_title[0]['href']
            logging.info('jie_pai_group title: ' + title + ' link: ' + link+" scrap_time: "+scrap_time)
            jie_pai_group_loader = ItemLoader(item=HCJiePaiGroup(), selector=response)
            jie_pai_group_loader.add_value('jie_pai_title', title)
            time.sleep(3)
            yield jie_pai_group_loader.load_item()

            call_back = self.parse_sina_detail
            detail_url = link
            if cmp(cur_url,self.sina)==0:
                call_back = self.parse_sina_detail
                detail_url = link
            else:
                call_back = self.parse_bu_cuo_detail
                detail_url = "https://www.bucuo.me"+link

            yield scrapy.Request(detail_url, meta={"group_title": title},
                                     callback=call_back)
    def parse_bu_cuo_detail(self,response):
        bsp = BeautifulSoup(response.body, 'lxml')
        for br in bsp('br'):
            br.extract()

        title = response.meta["group_title"]
        point_group_id = ""
        jie_pai_details = bsp.select(".body > p")
        is_first = True
        p_count = 0
        img_url = ""
        img_desc = ""
        for jie_pai_detail in jie_pai_details:
            p_count += 1
            img = jie_pai_detail.select('img')
            if img:     #图片
                img_url = ""
                img_url = img[0]["src"]
                continue

            else: #文字
                img_desc = ""
                img_desc = jie_pai_detail.string

            #第一张图片作为封面
            if is_first:
                upload_group_content = self.get_group_content(img_url, title)
                url = "https://api2.bmob.cn/1/classes/CardPicGroup"
                logging.info("parse_bu_cuo_detail group data: " + json.dumps(upload_group_content, ensure_ascii=False))
                # point_group_id = self.upload_to_bmob(url, upload_group_content)
                is_first = False
            else:
                #后续图片作为sub_img
                upload_detail_content = self.get_detail_content(img_desc,img_url,point_group_id)
                url = "https://api2.bmob.cn/1/classes/CardPicBean"
                logging.info("parse_bu_cuo_detail detail data: " + json.dumps(upload_detail_content,ensure_ascii=False))
                # self.upload_to_bmob(url, upload_detail_content)


    def parse_sina_detail(self, response):
        bsp = BeautifulSoup(response.body, 'lxml')
        for br in bsp('br'):
            br.extract()

        title = response.meta["group_title"]
        point_group_id = ""
        jie_pai_details = bsp.select_one('#sina_keyword_ad_area2')
        jie_pai_detail_links = jie_pai_details.select('a')
        is_first = True;
        for jie_pai_detail in jie_pai_detail_links:
            link_content = jie_pai_detail['href']
            if 'photo.blog.sina.com.cn' in link_content:
                result = self.process_detail(is_first, jie_pai_detail, point_group_id, title)
                if result and is_first:
                    is_first = False;
            else:
                logging.info('jie_pai_detail end')

    def process_detail(self, is_first, jie_pai_detail, point_group_id, title):
        jie_pai_detail_img = jie_pai_detail.select('img')
        img_width = 0
        img_height = 0;
        if jie_pai_detail_img[0].attrs.has_key("width"):
            img_width = int(jie_pai_detail_img[0]['width'])
        if jie_pai_detail_img[0].attrs.has_key("height"):
            img_height = int(jie_pai_detail_img[0]['height'])
        if img_height > img_width:

            img_url = jie_pai_detail_img[0]['real_src']
            img_desc = jie_pai_detail.next_sibling

            #另外一种情况获取img_desc
            img_desc = self.get_img_desc_if_needed(img_desc, jie_pai_detail)
            # 第一张图片作为封面
            if is_first:
                # 上传group
                upload_group_content = self.get_group_content(img_url, title)
                url = "https://api2.bmob.cn/1/classes/CardPicGroup"
                logging.info("upload_group_content data: " + json.dumps(upload_group_content, ensure_ascii=False))
                # point_group_id = self.upload_to_bmob(url, upload_group_content)
            elif img_desc.strip() != "":
                upload_detail_content = self.get_detail_content(img_desc, img_url, point_group_id)
                url = "https://api2.bmob.cn/1/classes/CardPicBean"
                logging.info("upload json: " + json.dumps(upload_detail_content))
                # self.upload_to_bmob(url, upload_detail_content)
            logging.info(
                'jie_pai_detail img_width: ' + str(img_width) + ' img_height: ' + str(
                    img_height) + ' img_src: ' + img_url + ' img_desc: ' + img_desc)
            return True
        else:
            logging.info("jie_pai_detail img_heigh: " + str(img_height) + " img_width: " + str(img_width))

        return False

    def get_img_desc_if_needed(self, img_desc, jie_pai_detail):
        while cmp(img_desc, '\n') == 0:
            img_desc = jie_pai_detail.next_sibling
            jie_pai_detail = jie_pai_detail.next_sibling

        # div
        if cmp("div", jie_pai_detail.name) == 0:
            img_desc = jie_pai_detail.text

        return img_desc

    def get_detail_content(self, img_desc, img_url, point_group_id):
        upload_detail_content = {}
        upload_detail_content["imageUrl"] = img_url
        upload_detail_content["imgDesc"] = img_desc;
        upload_detail_point = {}
        upload_detail_point["__type"] = "Pointer";
        upload_detail_point["className"] = "CardPicGroup";
        upload_detail_point["objectId"] = point_group_id;
        upload_detail_content["PicGroupId"] = upload_detail_point
        return upload_detail_content

    def get_group_content(self, img_url, title):
        upload_group_content = {}
        upload_group_content["imgUrl"] = img_url;
        upload_group_content["imgDesc"] = title;
        upload_group_content["imgLabel"] = "街拍"
        return upload_group_content

    def get_article_list_class_by(self,url):
        article_class = ""
        if cmp(url,self.sina) == 0:
            article_class = '.articleCell.SG_j_linedot1'
        elif cmp(url,self.bucou) == 0:
            article_class = ".art-item"

        return article_class

    def get_title_class_by(self,url):
        title_class = ""
        if cmp(url,self.sina) == 0:
            title_class = '.atc_title > a'
        elif cmp(url,self.bucou) == 0:
            title_class = "h2 > a"

        return title_class

    def get_article_time_class_by(self,url):
        article_time_class = ""
        if cmp(url,self.sina) == 0:
            article_time_class = '.atc_tm.SG_txtc'
        elif cmp(url,self.bucou) == 0:
            article_time_class = ".title-info > span"

        return article_time_class


    def get_details_class_by(self,url):
        details_class = ""
        if cmp(url,self.sina) == 0:
            details_class = '#sina_keyword_ad_area2'
        elif cmp(url,self.bucou) == 0:
            details_class = ".art-item > a"

        return details_class


    def upload_to_bmob(self, url, data):
        headers = {
            'X-Bmob-Application-Id': '55a1a92dd0096e5178ff10be85b06feb',
            'X-Bmob-REST-API-Key': '83c860ec56761949993c558c37a1cc45',
            'Content-Type': 'application/json'
        }  ## headers中添加上content-type这个参数，指定为json格式
        logging.info("upload_to_bmob data: " + json.dumps(data))
        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        logging.info("upload_to_bmob data response content: " + response.content)
        json_content = json.loads(response.content)
        return json_content["objectId"]