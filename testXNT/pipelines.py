# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import logging
import pymongo

class TestxntPipeline(object):

    def __init__(self):
        logging.info("init object")
        mongo = pymongo.MongoClient('127.0.0.1', 27017)
        self.db = mongo.xnt

    def process_item(self, item, spider):
        logging.info("method->process_item")
        logging.info("title: "+str(item["title"][0].encode('utf-8')))
        logging.info("linkValue: " + str(item["linkValue"][0].encode('utf-8')))
        # logging.info("content: "+str(dict(item)).encode("utf-8"))
        # self.updateAndSave(item)
        return item

    def updateAndSave(self,item):
        # logging.info("result: "+json.dumps(item));
        title=item["title"];
        self.db.col.insert(dict(item))