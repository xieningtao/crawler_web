# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup


class JiepaiWeiBoSpider(scrapy.Spider):
    name = 'jiepai_wei_bo'
    allowed_domains = ['www.weibo.com']
    # start_urls = ['http://photo.weibo.com/1304494805/talbum/index#!/mode/2/page/1']
    start_urls = ['https://www.weibo.com/p/1005051304494805/home']

    def __init__(self,name=None, **kwargs):
        super(JiepaiWeiBoSpider, self).__init__(name)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,cookies={'Cookie':'SINAGLOBAL=1618305396374.9795.1496912991585; _s_tentry=-; Apache=3563552099314.0625.1539855770645; ULV=1539855770671:21:2:1:3563552099314.0625.1539855770645:1538997930311; TC-V5-G0=784f6a787212ec9cddcc6f4608a78097; TC-Page-G0=841d8e04c4761f733a87c822f72195f3; TC-Ugrow-G0=e66b2e50a7e7f417f6cc12eec600f517; login_sid_t=370c9fe7d2010bf4a5d5ad1d9870af8f; cross_origin_proto=SSL; WBtopGlobal_register_version=030d061db77a53e5; un=389124248@qq.com; appkey=; SCF=AoH65CzQyP0lsDraBgcU-Jz41EywKxxNqU5AYrvo7hURdNL2fhWy0fCoYndgHHVSexLM3ujuSJpH92tY3z5SzO4.; SUHB=0S7Sk8WUZ1SUtK; un=389124248@qq.com; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9W5AEhE9j_WnEeSIiw5JIqsw5JpV2heR1K2EShzX12WpMC4odcXt; SUB=_2AkMslA7ldcNxrABXnf4TxWvjaI9H-jyfQWcTAn7uJhMyAxh77m8zqSVutBF-XGbS0qmLS7jDZvpsWX5lPZqdmnYo; UOR=www.huangbowen.net,widget.weibo.com,www.google.com.hk; wb_view_log_6655726689=1536*8641.25'})
    def parse(self, response):
        bsp = BeautifulSoup(response.body, 'lxml')
        # pic_group = bsp.select_one(".photoList.clearfix")
        # pic_items = pic_group.select("li")
        count = 0
        title = ""
        cur_group_id=""
        # for pic_item in pic_items:
        #
        #     #pic
        #     img_item = pic_item.select_one("img")
        #     img_url = img_item["src"]
        #     #title
        #     desc_item = pic_item.select_one(".desc > em")
        #     title = desc_item.text
        #
        #     #time
        #
        #     #同一组
        #     if cmp(cur_group_id, title):
        #
        #
        #     else:#一组的开头
        #         cur_group_id = title


