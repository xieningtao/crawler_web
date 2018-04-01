# -*- coding: utf-8 -*-
import scrapy


class BsvideoSpider(scrapy.Spider):
    name = 'bsvideo'
    allowed_domains = ['com.img']
    start_urls = ['http://com.img/']

    def parse(self, response):
        pass
