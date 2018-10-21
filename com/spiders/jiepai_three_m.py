# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup


class JiepaiThreeMSpider(scrapy.Spider):
    name = 'jiepai_three_m'
    allowed_domains = ['www.3ajiepai.com']
    start_urls = ['https://www.3ajiepai.com/article-1274-1.html']

    def parse(self, response):

        bsp = BeautifulSoup(response.body, 'lxml')
        # for br in bsp('br'):
        #     br.extract()
        three_m_content = bsp.select_one(".infoContent")

        #title
        title_item = three_m_content.select_one(".infoTitle > h1")
        title = title_item.text

        three_m_group = three_m_content.select_one("#article_content")
        #第一个图片
        three_m_item = three_m_group.select_one("img")

        while three_m_item:
            three_m_pic_url = three_m_item["src"]

            three_m_next_item = three_m_item.next_sibling
            #图片
            if three_m_next_item.attrs.has_key("src"):
                three_m_item = three_m_next_item


        # for three_m_item in three_m_items:
        #
        #     # 图片
        #     hua_ban_pic_item = hua_ban_item.select_one(".img.x.layer-view.loaded > img")
        #     hua_ban_pic = hua_ban_pic_item["src"]
        #     split_index = hua_ban_pic.index("_")
        #     hua_ban_url = "http:" + hua_ban_pic[0:split_index] + "_fw658"
        #     # hua_ban_url ="http:" + hua_ban_pic
        #
        #     group_content = self.bmob_helper.get_group_content(hua_ban_url, "")
        #     group_url = "https://api2.bmob.cn/1/classes/Beauty"
        #     logging.info("parse_hua_ban_detail group data: " + json.dumps(group_content, ensure_ascii=False))
        #     point_group_id = self.bmob_helper.upload_to_bmob(group_url, group_content)


