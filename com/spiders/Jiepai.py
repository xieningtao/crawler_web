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
    ,'https://www.bucuo.me/app/1583407618504778']


    def __init__(self,name=None, **kwargs):
        super(JiepaiSpider,self).__init__(name)
        self.sina = "http://blog.sina.com.cn/s/articlelist_1340398703_4_1.html"
        self.bucou = "https://www.bucuo.me/app/1583407618504778"

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
            link_title_class = self.get_title_class_by(cur_url)
            link_title = article.select(link_title_class)
            title = link_title[0].string
            link = link_title[0]['href']
            logging.info('jie_pai_group title: ' + title + ' link: ' + link)
            jie_pai_group_loader = ItemLoader(item=HCJiePaiGroup(), selector=response)
            jie_pai_group_loader.add_value('jie_pai_title', title)
            time.sleep(3)
            yield jie_pai_group_loader.load_item()

            yield scrapy.Request(link, meta={"group_title":title,
                                             "cur_url":cur_url},
                                 callback=self.parse_detail)

    def parse_detail(self, response):
        bsp = BeautifulSoup(response.body, 'lxml')
        for br in bsp('br'):
            br.extract()

        title = response.meta["group_title"]
        cur_url = response.meta["cur_url"]
        point_group_id = ""
        jie_pai_details = bsp.select_one('#sina_keyword_ad_area2')
        jie_pai_detail_links = jie_pai_details.select('a')
        is_first = True;
        for jie_pai_detail in jie_pai_detail_links:
            link_content = jie_pai_detail['href']
            if 'photo.blog.sina.com.cn' in link_content:
                jie_pai_detail_img = jie_pai_detail.select('img')

                img_width = 0
                img_height = 0;
                if jie_pai_detail_img[0].attrs.has_key("width"):
                    img_width = int(jie_pai_detail_img[0]['width'])
                if jie_pai_detail_img[0].attrs.has_key("height"):
                    img_height = int(jie_pai_detail_img[0]['height'])

                if img_height > img_width:

                    img_src = jie_pai_detail_img[0]['real_src']
                    img_desc = jie_pai_detail.next_sibling

                    # 第一张图片作为封面
                    if is_first:
                        # 上传group
                        upload_group_content = {}
                        upload_group_content["imgUrl"] = img_src;
                        upload_group_content["imgDesc"] = title;
                        upload_group_content["imgLabel"] = "街拍"
                        url = "https://api2.bmob.cn/1/classes/CardPicGroup"
                        logging.info("upload_group_content data: " + json.dumps(upload_group_content, ensure_ascii=False))
                        # .decode('utf-8').encode('gb2312')
                        point_group_id = self.upload_to_bmob(url, upload_group_content)
                        is_first = False;
                    elif img_desc.strip() != "":
                        upload_detail_content = {}
                        upload_detail_content["imageUrl"] = img_src
                        upload_detail_content["imgDesc"] = img_desc;

                        upload_detail_point = {}
                        upload_detail_point["__type"] = "Pointer";
                        upload_detail_point["className"] = "CardPicGroup";
                        upload_detail_point["objectId"] = point_group_id;

                        upload_detail_content["PicGroupId"] = upload_detail_point
                        url = "https://api2.bmob.cn/1/classes/CardPicBean"
                        logging.info("upload json: " + json.dumps(upload_detail_content))
                        self.upload_to_bmob(url, upload_detail_content)
                    logging.info(
                        'jie_pai_detail img_width: ' + str(img_width) + ' img_height: ' + str(
                            img_height) + ' img_src: ' + img_src + ' img_desc: ' + img_desc)
                else:
                    logging.info("jie_pai_detail img_heigh: " + str(img_height) + " img_width: " + str(img_width))
            else:
                logging.info('jie_pai_detail end')


    def get_article_list_class_by(self,url):
        article_class = ""
        if cmp(url,self.sina) == 0:
            article_class = '.articleCell.SG_j_linedot1'
        elif cmp(url,self.bucou) == 0:
            article_class = ".art-item"

    def get_title_class_by(self,url):
        article_class = ""
        if cmp(url,self.sina) == 0:
            article_class = '.atc_title > a'
        elif cmp(url,self.bucou) == 0:
            article_class = ".art-item > a"

        return article_class
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