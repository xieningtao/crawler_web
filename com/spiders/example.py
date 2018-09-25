# -*- coding: utf-8 -*-
import scrapy
import logging

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['www.baidu.com']
    start_urls = ['https://www.baidu.com/']

    def parse(self, response):
        logging.debug("parse: "+response)
        pass
