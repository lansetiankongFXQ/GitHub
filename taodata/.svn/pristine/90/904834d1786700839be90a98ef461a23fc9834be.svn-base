# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from pymongo.errors import DuplicateKeyError
import sys
import os
sys.path.append(os.getcwd())
from taodata.spiders.wanfangdata.items import WanfangCategoryItem,WanfangExaminationItem
from taodata.settings import LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, DB_NAME
import redis
from taodata.settings import LOCAL_REDIS_HOST, LOCAL_REDIS_PORT, LOCAL_REDIS_PASSWORD
import json


class WanfangMongoDBPipeline(object):
    r = redis.Redis(host=LOCAL_REDIS_HOST, port=LOCAL_REDIS_PORT, password=LOCAL_REDIS_PASSWORD)

    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        db = client[DB_NAME]
        self.WanfangCategory = db["WanfangCategory"]
        self.WanfangExamination = db["WanfangExamination"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, WanfangCategoryItem):
            self.insert_item(self.WanfangCategory, item)
        if isinstance(item, WanfangExaminationItem):
            self.insert_item(self.WanfangExamination, item)

        return item

    @staticmethod
    def insert_item(collection, item):
        try:
            collection.insert(dict(item))
        except DuplicateKeyError:
            """
            说明有重复数据
            """
            print('重复数据 -->' + item['_id'])
            pass


