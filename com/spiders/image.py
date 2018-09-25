# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import logging
from testXNT.items import ImgItem,ImgGroup,ImgCover
import time
from scrapy.contrib.loader import ItemLoader


class ImageSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['www.win4000.com']
    start_urls = ['http://www.win4000.com/meitu.html']

    def __init__(self):
        self.img_count = 0

    def parse(self, response):
        bsp = BeautifulSoup(response.body, "lxml")
        columTags = bsp.select(".list_cont.list_cont2.w1180")

        # 第一个标签
        colum_tag = columTags[0];

        # 对标签便利
        # for colum_tag in columTags:
        loader = ItemLoader(item=ImgGroup(), selector=response)
        head_value = colum_tag.select_one("h2")
        loader.add_value("group_label",head_value.text)
        yield loader.load_item()

        logging.info("head_value: "+head_value.text)
        img_list = colum_tag.select("li");
        i = 0;
        # 每一组标签的图片组便利
        for imgItem in img_list:
            i = i + 1
            if i == 5:
                break
            # 每一组图片的小图或者说是封面
            loader_img = ItemLoader(item=ImgCover(), selector=response)
            img_value = imgItem.select_one("img")
            loader_img.add_value("img_url", img_value['data-original'])
            labelValue = imgItem.select_one("p")
            link_value = imgItem.select_one("a")["href"]
            loader_img.add_value("img_label", labelValue.text)
            logging.info("link_value: " + link_value);
            logging.info("img_value: " + img_value['data-original'])
            logging.info("labelValue: " + labelValue.text)

            img_cover_id = str(hash(img_value['data-original']))
            logging.info("img_parent_id: " + img_cover_id)

            loader_img.add_value("img_cover_id",img_cover_id)
            loader_img.add_value("timestamp", self.get_timestamp())

            yield loader_img.load_item()
            # scrapy.Request(link_value, callback=self.get_total_num)


            yield scrapy.Request(link_value,
                                 meta={"origin_link_value":link_value,
                                        "labelText":labelValue.text,
                                        "img_cover_id":img_cover_id
                                       },
                                 callback=self.parse_group_page)

    def parse_group_page(self, response):
        self.get_total_num(response)
        bsp = BeautifulSoup(response.body, "lxml")
        # 第一个页面的数据
        page_img_item_container = bsp.select_one(".pic-meinv")
        page_img_value = page_img_item_container.select_one("img")
        page_link_value = page_img_item_container.select_one("a")["href"]

        logging.info("pageLinkValue: " + page_link_value);
        logging.info("pageImgValue: " + page_img_value['data-original'])

        origin_link_value = response.meta["origin_link_value"];
        label_text = response.meta["labelText"]
        logging.info("origin_link_value: "+origin_link_value)

        origin_link_value_prefix = origin_link_value.rstrip(".html");
        logging.info("origin_link_value_prefix: " + origin_link_value_prefix)

        loader = ItemLoader(item=ImgItem(), response=response)
        img_url = page_img_value['data-original'];


        loader.add_value('img_url', img_url)
        loader.add_value('img_label', label_text)
        img_parent_id = response.meta["img_cover_id"]
        loader.add_value("img_parent_id",img_parent_id)

        yield loader.load_item()
        logging.info("img_count: "+ str(self.img_count))
        for index in range(0, (self.img_count+1)):
            if index != 0:
                next_link_value = origin_link_value.replace(".html", "_" + str((index+1)) + ".html")
            else:
                next_link_value = origin_link_value
            logging.info("next_link_value: " + next_link_value)

            yield scrapy.Request(next_link_value,
                                 meta={"labelText":label_text,
                                       "img_cover_id":img_parent_id},
                                 callback=self.parse_next_page)


    def parse_next_page(self,response):

        bsp = BeautifulSoup(response.body, "lxml")
        # 第后续页面的数据
        page_img_item_container = bsp.select_one(".pic-meinv")
        page_img_value = page_img_item_container.select_one("img")
        page_link_value = page_img_item_container.select_one("a")["href"]

        logging.info("pageLinkValue: " + page_link_value);
        logging.info("pageImgValue: " + page_img_value['data-original'])

        label_text = response.meta["labelText"]
        img_url = page_img_value['data-original'];

        loader = ItemLoader(item=ImgItem(), response=response)
        loader.add_value('img_url', img_url)
        loader.add_value('img_label', label_text)
        img_parent_id = response.meta["img_cover_id"]
        loader.add_value("img_parent_id", img_parent_id)
        return loader.load_item()


    def get_total_num(self,response):
        logging.info("method->get_total_num")
        bsp = BeautifulSoup(response.body, "lxml")
        total_number_container = bsp.select_one(".ptitle")
        em_tag = total_number_container.select_one("em")
        total_number = em_tag.string;
        logging.info("total_number: "+total_number);
        self.img_count = int(total_number)


    def get_timestamp(self):
        t = time.time()
        return str((int(round(t * 1000))))