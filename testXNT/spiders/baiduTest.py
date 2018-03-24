# -*- coding: utf-8 -*-
import scrapy
import logging

class BaidutestSpider(scrapy.Spider):
    name = 'baiduTest'
    allowed_domains = ['www.baidu.com','mbd.baidu.com']
    start_urls = ['http://www.meipai.com/medias/hot']

    def parse(self, response):
        # logging.debug("BaidutestSpider-->parse: " + str(response.body))
        return
