# -*- coding: utf-8 -*-
import scrapy


class JiepaiZhiJiaSpider(scrapy.Spider):
    name = 'jiepai_zhi_jia'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
