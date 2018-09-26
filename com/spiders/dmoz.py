# -*- coding: utf-8 -*-
import scrapy

from bs4 import BeautifulSoup
import logging
from com.items import DmozItem
from scrapy.contrib.loader import ItemLoader

class DmozSpider(scrapy.Spider):
    name = 'dmoz'
    allowed_domains = ['id.tudou.com']
    start_urls = [
        "http://id.tudou.com/i/id_91374690",
    ]

    def parse(self, response):
        bsp = BeautifulSoup(response.body,"lxml")

        videoTags = bsp.select(".videos-list .v")
        for videoTag in videoTags:
            l = ItemLoader(item=DmozItem(), selector=videoTag)
            # domzItem = DmozItem()
            # print "videoTag: "+str(videoTag)
            imgTag = videoTag.select(".v-thumb > img")
            # domzItem["imgValue"] = imgTag[0]['src']
            l.add_value("imgValue",imgTag[0]['src'])
            logging.info("img value: "+imgTag[0]['src'])

            linkTag = videoTag.select(".v-link > a")
            # domzItem["linkValue"] = linkTag[0]['href']
            l.add_value("linkValue",linkTag[0]['href'])
            logging.info("link value: " + linkTag[0]['href'])
            linkTargetTag = videoTag.select(".v-link-tagrt .ico-SD")
            # domzItem["linkTarget"] = linkTargetTag[0].string
            if(len(linkTargetTag) > 0):
                l.add_value("linkTarget",linkTargetTag[0].string)
                logging.info("link-tagrt value: " + linkTargetTag[0].string)
            else:
                logging.info("linkTarget is null")
                l.add_value("linkTarget", "")

            timeTag = videoTag.select(".v-link-tagrb .v-time")
            # domzItem["timeVale"]= timeTag[0].string
            l.add_value("timeVale",timeTag[0].string)
            logging.info("time value: " + timeTag[0].string)

            titleTag = videoTag.select(".v-meta-title > a")
            # domzItem["title"] = titleTag[0].string
            l.add_value("title",titleTag[0].string)
            logging.info("title value: " + titleTag[0].string)
            # print "title: "+ str(titleValue.encode('utf-8'))
            # yield domzItem
            yield l.load_item()
        # l.load_item()



