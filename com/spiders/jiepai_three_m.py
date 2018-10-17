# -*- coding: utf-8 -*-
import scrapy


class JiepaiThreeMSpider(scrapy.Spider):
    name = 'jiepai_three_m'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
