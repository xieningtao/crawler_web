# -*- coding: utf-8 -*-
import scrapy

from scrapy.contrib.loader import ItemLoader
from bs4 import BeautifulSoup
import logging
from  com.items import LiVideo
import time


class LiVideoSpider(scrapy.Spider):
    name = 'livideo'
    allowed_domains = ['www.pearvideo.com']
    start_urls = ['http://www.pearvideo.com/category_7']

    def parse(self, response):
        bsp = BeautifulSoup(response.body, "lxml")
        latest_label_tag = bsp.select_one(".ctitle-hd.category-new")
        label_str = latest_label_tag.select_one(".ctitle-name").text.encode("utf-8");
        logging.info("label_text: "+label_str)
        latest_video_containers = bsp.select_one(".category-list.clearfix")

        latest_videos = latest_video_containers.select(".categoryem");
        logging.info("video count: "+str(len(latest_videos)))
        i = 0
        for latest_video in latest_videos:
            i = i + 1
            if i == 2:
                break
            video_title = latest_video.select_one(".vervideo-title").text.encode("utf-8")
            logging.info("title: "+video_title)
            video_detail_id = latest_video.select_one(".vervideo-lilink.actplay")["href"]
            logging.info("video_detail_id: "+video_detail_id)
            target_video_detail_url = "http://www.pearvideo.com/"+video_detail_id
            logging.info("target_video_detail_url: "+target_video_detail_url)

            cover_url_style = latest_video.select_one(".img")["style"];
            cover_url = cover_url_style[len("background-image url(")+1:len(cover_url_style)-2]
            logging.info("cover_url: "+cover_url)

            video_duration = latest_video.select_one(".cm-duration").text.encode("utf-8")
            yield scrapy.Request(target_video_detail_url,
                                 meta={"video_title":video_title,
                                       "cover_url":cover_url,
                                       "video_duration":video_duration,
                                       "video_label":label_str},
                                 callback=self.get_all_video_info)

    def get_all_video_info(self,response):
        loader = ItemLoader(item=LiVideo(), response=response)
        video_title = response.meta["video_title"];
        cover_url = response.meta["cover_url"];
        video_duration = response.meta["video_duration"];
        video_label = response.meta["video_label"];

        loader.add_value("video_title",video_title)
        loader.add_value("video_img_url",cover_url)
        loader.add_value("video_duration",video_duration)
        loader.add_value("video_label",video_label)
        # 添加时间戳
        loader.add_value("timestamp",self.get_timestamp())

        # video url地址
        bsp = BeautifulSoup(response.body, "lxml")
        video_container = bsp.select_one(".img.prism-player")
        video_url = video_container.select_one("video")["src"]
        loader.add_value("video_url",video_url)
        logging.info("video_url: "+video_url)
        yield loader.load_item()

    def get_timestamp(self):
        t = time.time()
        return str((int(round(t * 1000))))