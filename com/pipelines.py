# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import logging

import pymongo
import requests
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

from items import ImgItem,ImgGroup,ImgCover

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

class BaiduJiepaiImgDownloadPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            # self.default_headers['referer'] = image_url
            logging.info("BaiduJiepaiImgDownloadPipeline imge_url: "+image_url)
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        logging.info("item_completed results: ")
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item


class UploadJiePaiPicPipeline(object):

    def process_item(self, item, spider):
        logging.info("UploadJiePaiPicPipeline-->process_item")

        upload_detail_content = {}
        upload_detail_content[""] = "@C:\\Users\\g8876\\Desktop\\jiepai\\full\\test.jpg"
        upload_detail_content["imgDesc"] = "this is a test";

        upload_detail_point = {}
        upload_detail_point["__type"] = "Pointer";
        upload_detail_point["className"] = "CardPicGroup";
        upload_detail_point["objectId"] = "f8dc9d9169";

        upload_detail_content["PicGroupId"] = upload_detail_point


    def uploadImgFile(self,url,path):
        headers = {
            'X-Bmob-Application-Id': '55a1a92dd0096e5178ff10be85b06feb',
            'X-Bmob-REST-API-Key': '83c860ec56761949993c558c37a1cc45',
            'Content-Type': 'image/jpg'
        }  ## headers中添加上content-type这个参数，指定为json格式
        data = file(path, 'rb').read()
        response = requests.post(url=url, headers=headers, data=data)
        logging.info("uploadImgFile response content: " + response.content)
        json_content = json.loads(response.content)
        logging.info("uploadImgFile json_content: "+str(json_content))
        return json_content["url"]

    def upload_to_bmob(self, url, data):
        headers = {
            'X-Bmob-Application-Id': '55a1a92dd0096e5178ff10be85b06feb',
            'X-Bmob-REST-API-Key': '83c860ec56761949993c558c37a1cc45',
            'Content-Type': 'image/jpg'
        }  ## headers中添加上content-type这个参数，指定为json格式
        logging.info("upload_to_bmob data: " + json.dumps(data))
        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        logging.info("upload_to_bmob data response content: " + response.content)
        json_content = json.loads(response.content)
        return json_content["objectId"]