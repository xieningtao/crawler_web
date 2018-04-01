# -*- coding: utf-8 -*-
import scrapy


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['com.img']
    start_urls = ['http://com.img/']

    def parse(self, response):
        pass
