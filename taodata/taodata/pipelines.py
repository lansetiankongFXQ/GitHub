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
from taodata.items import RelationshipsItem, TweetsItem, InformationItem, CommentItem
from taodata.items import WeiboRelationshipsItem, WeiboUserItem, WeiboItem, WeiboCommentItem, WeiboAttitudeItem, WeiboRepostItem
from taodata.settings import LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, DB_NAME
import redis
from taodata.settings import LOCAL_REDIS_HOST, LOCAL_REDIS_PORT, LOCAL_REDIS_PASSWORD
import json


class FudanRedisDBPipeline(object):
    def __init__(self):
        self.r = redis.Redis(host=LOCAL_REDIS_HOST, port=LOCAL_REDIS_PORT, password=LOCAL_REDIS_PASSWORD)

    def process_item(self, item, spider):
        if isinstance(item, WeiboRelationshipsItem):
            req_id = item['req_id']
            key = "fudan:crawl:data:%s:relationships" % req_id
            dupekey = "fudan:crawl:data:%s:relationships_dupe" % req_id
            self.r.lpush(key, json.dumps(dict(item)))
            self.r.sadd(dupekey, item['_id'])

        elif isinstance(item, WeiboUserItem):
            req_id = item['req_id']
            key = "fudan:crawl:data:%s:weibo_user" % req_id
            dupekey = "fudan:crawl:data:%s:weibo_user_dupe" % req_id
            self.r.lpush(key, json.dumps(dict(item)))
            self.r.sadd(dupekey, item['_id'])
        elif isinstance(item, WeiboItem):
            req_id = item['req_id']
            key = "fudan:crawl:data:%s:weibo" % req_id
            dupekey = "fudan:crawl:data:%s:weibo_dupe" % req_id
            self.r.lpush(key, json.dumps(dict(item)))
            self.r.sadd(dupekey, item['_id'])
        elif isinstance(item, WeiboCommentItem):
            pass
        elif isinstance(item, WeiboAttitudeItem):
            pass
        elif isinstance(item, WeiboRepostItem):
            pass

        return item


class FudanMongoDBPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        db = client[DB_NAME]
        self.WeiboRelationships = db["FudanWeiboRelationships"]
        self.WeiboUser = db["FudanWeiboUser"]
        self.Weibo = db["FudanWeibo"]
        self.WeiboComment = db["FudanWeiboComment"]
        self.WeiboAttitude = db["FudanWeiboAttitude"]
        self.WeiboRepost = db["FudanWeiboRepost"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item,WeiboRelationshipsItem):
            self.insert_item(self.WeiboRelationships, item)
        elif isinstance(item, WeiboUserItem):
            self.insert_item(self.WeiboUser, item)
        elif isinstance(item,WeiboItem):
            self.insert_item(self.Weibo, item)
        elif isinstance(item,WeiboCommentItem):
            self.insert_item(self.WeiboComment, item)
        elif isinstance(item,WeiboAttitudeItem):
            self.insert_item(self.WeiboAttitude, item)
        elif isinstance(item,WeiboRepostItem):
            self.insert_item(self.WeiboRepost, item)
        return item

    @staticmethod
    def insert_item(collection, item):
        try:
            collection.insert(dict(item))
        except DuplicateKeyError:
            """
            说明有重复数据
            """
            print('重复数据')
            pass


class TaodataRedisRealtimeDBPipeline(object):
    def __init__(self):
        self.r = redis.Redis(host=LOCAL_REDIS_HOST, port=LOCAL_REDIS_PORT, password=LOCAL_REDIS_PASSWORD)

    def process_item(self, item, spider):
        if isinstance(item, WeiboItem):
            req_id = item['req_id']
            key = "taodata:crawl:data:%s:weibo" % req_id
            self.r.lpush(key, json.dumps(dict(item)))

        return item


class TaodataMongoRealtimeDBPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        db = client[DB_NAME]
        self.Weibo = db["TaodataRealtimeWeibo"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, WeiboItem):
            self.insert_item(self.Weibo, item)

        return item

    @staticmethod
    def insert_item(collection, item):
        try:
            collection.insert(dict(item))
        except DuplicateKeyError:
            """
            说明有重复数据
            """
            print('重复数据')
            pass


class TaodataRedisDBPipeline(object):
    def __init__(self):
        self.r = redis.Redis(host=LOCAL_REDIS_HOST, port=LOCAL_REDIS_PORT, password=LOCAL_REDIS_PASSWORD)

    def process_item(self, item, spider):
        if isinstance(item, WeiboRelationshipsItem):
            pass
        elif isinstance(item, WeiboUserItem):
            key = "taodata:crawl:data:weibo_user"
            name = item['user_id']
            self.r.hset(key, name, json.dumps(dict(item)))
        elif isinstance(item, WeiboItem):
            pass
        elif isinstance(item, WeiboCommentItem):
            pass
        elif isinstance(item, WeiboAttitudeItem):
            pass
        elif isinstance(item, WeiboRepostItem):
            pass

        return item


class TaodataMongoDBPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        db = client[DB_NAME]
        self.WeiboRelationships = db["TaodataWeiboRelationships"]
        self.WeiboUser = db["TaodataWeiboUser"]
        self.Weibo = db["TaodataWeibo"]
        self.WeiboComment = db["TaodataWeiboComment"]
        self.WeiboAttitude = db["TaodataWeiboAttitude"]
        self.WeiboRepost = db["TaodataWeiboRepost"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, WeiboRelationshipsItem):
            self.insert_item(self.WeiboRelationships, item)
        elif isinstance(item, WeiboUserItem):
            self.insert_item(self.WeiboUser, item)
        elif isinstance(item, WeiboItem):
            self.insert_item(self.Weibo, item)
        elif isinstance(item,WeiboCommentItem):
            pass
            # self.insert_item(self.WeiboComment, item)
        elif isinstance(item,WeiboAttitudeItem):
            pass
            # self.insert_item(self.WeiboAttitude, item)
        elif isinstance(item,WeiboRepostItem):
            pass
            # self.insert_item(self.WeiboRepost, item)
        return item

    @staticmethod
    def insert_item(collection, item):
        try:
            collection.insert(dict(item))
        except DuplicateKeyError:
            """
            说明有重复数据
            """
            print('重复数据')
            pass


class MongoDBPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        db = client[DB_NAME]
        self.Information = db["Information"]
        self.Tweets = db["Tweets"]
        self.Comments = db["Comments"]
        self.Relationships = db["Relationships"]
        self.WeiboRelationships = db["WeiboRelationships"]
        self.WeiboUser = db["WeiboUser"]
        self.Weibo = db["Weibo"]
        self.WeiboComment = db["WeiboComment"]
        self.WeiboAttitude = db["WeiboAttitude"]
        self.WeiboRepost = db["WeiboRepost"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, RelationshipsItem):
            self.insert_item(self.Relationships, item)
        elif isinstance(item, TweetsItem):
            self.insert_item(self.Tweets, item)
        elif isinstance(item, InformationItem):
            self.insert_item(self.Information, item)
        elif isinstance(item, CommentItem):
            self.insert_item(self.Comments, item)
        elif isinstance(item,WeiboRelationshipsItem):
            self.insert_item(self.WeiboRelationships, item)
        elif isinstance(item, WeiboUserItem):
            self.insert_item(self.WeiboUser, item)
        elif isinstance(item,WeiboItem):
            self.insert_item(self.Weibo, item)
        elif isinstance(item,WeiboCommentItem):
            self.insert_item(self.WeiboComment, item)
        elif isinstance(item,WeiboAttitudeItem):
            self.insert_item(self.WeiboAttitude, item)
        elif isinstance(item,WeiboRepostItem):
            self.insert_item(self.WeiboRepost, item)
        return item

    @staticmethod
    def insert_item(collection, item):
        try:
            collection.insert(dict(item))
        except DuplicateKeyError:
            """
            说明有重复数据
            """
            print('重复数据')
            pass
