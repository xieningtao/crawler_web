# -*- coding: utf-8 -*-
import scrapy
import logging

import time
from bs4 import BeautifulSoup
from scrapy.loader import ItemLoader

from com.items import BaiduJiePai


class JiepaiBuCouSpider(scrapy.Spider):
    name = 'jiepai_bu_cuo'
    allowed_domains = ["www.bucuo.me"]
    start_urls = ['https://www.bucuo.me/v/news_9229896512998137007']

    def parse(self, response):
        bsp = BeautifulSoup(response.body, 'lxml')
        article_list = bsp.select(".body > p")
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
                baidu_jiepai_img = ItemLoader(item=BaiduJiePai(), selector=response)
                baidu_jiepai_img.add_value('image_urls', img_src)
                time.sleep(3)
                yield baidu_jiepai_img.load_item()


