# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from img import ImgGroup
# class TestxntItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass


class DmozItem(scrapy.Item):
    title = scrapy.Field()
    imgValue = scrapy.Field()
    linkValue = scrapy.Field()
    timeVale = scrapy.Field()
    linkTarget= scrapy.Field()


class ImgItem(scrapy.Item):
    img_label = scrapy.Field()
    img_url = scrapy.Field()
    img_parent_id = scrapy.Field()


class ImgCover(scrapy.Item):
    img_label = scrapy.Field()
    img_url = scrapy.Field()
    timestamp = scrapy.Field()
    img_cover_id = scrapy.Field()


class ImgGroup(scrapy.Item):
    group_label = scrapy.Field()


class LiVideo(scrapy.Item):
    video_title = scrapy.Field()
    video_img_url = scrapy.Field()
    video_url = scrapy.Field()
    video_duration = scrapy.Field()
    video_label = scrapy.Field()
    timestamp = scrapy.Field()