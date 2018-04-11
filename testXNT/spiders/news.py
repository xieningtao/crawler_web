# -*- coding: utf-8 -*-
import scrapy
import logging
from  testXNT.items import NetNews
import time
import json
import requests

class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['c.3g.163.com']
    start_urls = ['http://c.3g.163.com/recommend/getSubDocPic?tid=T1348647909107&from=toutiao&offset=0&size=10&fn=4&prog=LMA1&passport=xt3aXUI%2F0vKeSBsgPsGx6%2F%2BVl9Iv%2BZonLeLmSMxhclRbSaGBZSsXSVQ7leyYqOgLrqJv2nCCD2QqQsfBWgSZWQ%3D%3D&devId=TN7nkeuf4NIS6%2FhflY3NEA%3D%3D&lat=d5JPmRoeCiDYCTXH9OQy4w%3D%3D&lon=lD7KfiP%2Bz5xD0wz7zZqB9A%3D%3D&version=17.1&net=wifi&ts=1478174409&sign=fUtM1OtsZKU4DT0HVA69pfdCsC2OM4ata14nFxytyb148ErR02zJ6%2FKXOnxX046I&encryption=1&canal=miliao_news&mac=Vs3jgAx3MGdwkSWIle2S%2B7XXhQnPCVyraDgInk6Dmbk%3D']

    def parse(self, response):
        data = json.loads(response.text)
        for key in data.keys():
            dataLenth = len(data[key])
            logging.info("total size: " + str(dataLenth))
            for i in range(1, dataLenth):
                logging.info("curIndex: " + str(i))
                content = {}
                logging.info("title: "+data[key][i]["title"])

                loader = ItemLoader(item=NetNews(), response=response)

                content["title"] = data[key][i]["title"];
                loader.add_value("news_title", content["title"])

                content["digest"] = data[key][i]["digest"]
                loader.add_value("news_digest", content["digest"])
                # print "recSource: "+data[key][i]["recSource"]
                content["label"] = data[key][i]["recSource"];
                loader.add_value("news_label", content["label"])

                content["imageUrl"] = data[key][i]["imgsrc"]
                loader.add_value("news_img_url", content["imageUrl"])

                content["id"] = data[key][i]["id"]
                loader.add_value("news_id", content["id"])

                detail = self.getNewsDetail(content["id"])
                # print "body: "+detail
                if (len(detail) != 0):
                    loader.add_value("news_detail", detail)

                # 添加时间戳
                loader.add_value("timestamp", self.get_timestamp())
                yield loader.load_item()


    def getNewsDetail(self,newsId):
        url = "http://c.m.163.com/nc/article/" + newsId + "/full.html"
        resp = self.doCommanHttpRequest(url);
        logging.info("text: " + resp.text)
        try:
            detailData = json.loads(resp.text)
        except ValueError, e:
            logging.info("exception: " + str(e))
            return ""

        return detailData[newsId]["body"]


    def doCommanHttpRequest(self,url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
        resp = requests.get(url=url, headers=headers)
        return resp

    def get_timestamp(self):
        t = time.time()
        return str((int(round(t * 1000))))