# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import logging
import pymongo
from testXNT.items import ImgItem,ImgGroup,ImgCover

class TestxntPipeline(object):

    def __init__(self):
        logging.info("init object")
        mongo = pymongo.MongoClient('127.0.0.1', 27017)
        self.db = mongo.xnt

    def process_item(self, item, spider):
        logging.info("method->process_item")
        if "image" in spider.name :
            if type(item) == ImgItem:
                logging.info("imageUrl: "+str(item["img_url"][0].encode('utf-8')))
                logging.info("label: " + str(item["img_label"][0].encode('utf-8')))
                self.updateAndSaveImg(item)
            elif type(item) == ImgGroup:
                logging.info("group_label: " + str(item["group_label"][0].encode('utf-8')))
            elif type(item) == ImgCover:
                self.update_save_img_cover(item)
        elif "dmoz" in spider.name:
            logging.info("title: "+str(item["title"][0].encode('utf-8')))
            logging.info("linkValue: " + str(item["linkValue"][0].encode('utf-8')))
        # logging.info("content: "+str(dict(item)).encode("utf-8"))
            self.updateAndSave(item)
        elif "livideo" in spider.name:
            logging.info("video_title: " + str(item["video_title"][0]))
            logging.info("video_img_url: " + str(item["video_img_url"][0].encode('utf-8')))
            logging.info("video_url: " + str(item["video_url"][0].encode('utf-8')))
            logging.info("video_duration: " + str(item["video_duration"][0]))
            logging.info("video_label: " + str(item["video_label"][0]))
            self.updateAndSaveVideo(item)
        elif "news" in spider.name:
            self.updateAndSaveNews(item)
        return item


    def updateAndSave(self,item):
        # logging.info("result: "+json.dumps(item));
        title=item["title"];
        self.db.col.insert(dict(item))

    def updateAndSaveImg(self,item):
        # self.db.img.insert(dict(item))
        result = self.db.img.find({"img_url":item["img_url"][0]})
        if result.count() == 0:
            self.db.img.insert(dict(item))
        else:
            logging.info("this img is exist url: "+item["img_url"][0])

    def update_save_img_cover(self, item):
        # self.db.img.insert(dict(item))
        result = self.db.img_cover.find({"img_url": item["img_url"][0]})
        if result.count() == 0:
            self.db.img_cover.insert(dict(item))
        else:
            logging.info("this cover_img is exist url: " + item["img_url"][0])

    def updateAndSaveVideo(self, item):
        # self.db.img.insert(dict(item))
        result = self.db.video.find({"video_url": item["video_url"][0]})
        if result.count() == 0:
            self.db.video.insert(dict(item))
        else:
            logging.info("this video is exist url: " + item["video_url"][0])

    def updateAndSaveNews(self,item):
        result = self.db.video.find({"news_title": item["news_title"][0]})
        if result.count() == 0:
            self.db.news.insert(dict(item))
        else:
            logging.info("this new is exist : " + item["news_title"][0])