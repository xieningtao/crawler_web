# -*- coding: utf-8 -*-
import logging

import requests
from flask import json


class BMobUploadHelper(object):

    def get_detail_content(self, img_desc, img_url, point_group_id):
        logging.info("get_detail_content img_desc: "+img_desc+" img_url: "+img_url+" point_group_id: "+point_group_id)
        upload_detail_content = {}
        upload_detail_content["imageUrl"] = img_url
        upload_detail_content["imgDesc"] = img_desc;
        upload_detail_point = {}
        upload_detail_point["__type"] = "Pointer";
        upload_detail_point["className"] = "CardPicGroup";
        upload_detail_point["objectId"] = point_group_id;
        upload_detail_content["PicGroupId"] = upload_detail_point
        return upload_detail_content

    def get_news_detail_content(self, img_desc, img_url, point_group_id):
        logging.info("get_detail_content img_desc: "+img_desc+" img_url: "+img_url+" point_group_id: "+point_group_id)
        upload_detail_content = {}
        upload_detail_content["imageUrl"] = img_url
        upload_detail_content["imgDesc"] = img_desc;
        upload_detail_point = {}
        upload_detail_point["__type"] = "Pointer";
        upload_detail_point["className"] = "StyleNews";
        upload_detail_point["objectId"] = point_group_id;
        upload_detail_content["NewsId"] = upload_detail_point
        return upload_detail_content

    def get_group_content_with_title(self, img_url,desc, title):
        upload_group_content = {}
        upload_group_content["imgUrl"] = img_url;
        upload_group_content["imgDesc"] = desc;
        upload_group_content["title"] = title;
        upload_group_content["imgLabel"] = "街拍"
        return upload_group_content

    def get_group_content(self, img_url, desc):
        upload_group_content = {}
        upload_group_content["imgUrl"] = img_url;
        upload_group_content["imgDesc"] = desc;
        upload_group_content["imgLabel"] = "街拍"
        return upload_group_content



    def upload_to_bmob(self, url, data):
        headers = {
            'X-Bmob-Application-Id': '55a1a92dd0096e5178ff10be85b06feb',
            'X-Bmob-REST-API-Key': '83c860ec56761949993c558c37a1cc45',
            'Content-Type': 'application/json'
        }  ## headers中添加上content-type这个参数，指定为json格式
        logging.info("upload_to_bmob data: " + json.dumps(data))
        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        logging.info("upload_to_bmob data response content: " + response.content)
        json_content = json.loads(response.content)
        return json_content["objectId"]