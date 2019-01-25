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
from taodata.spiders.article.items import ArticleNewsItem
from taodata.settings import LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, DB_NAME
import redis
from taodata.settings import LOCAL_REDIS_HOST, LOCAL_REDIS_PORT, LOCAL_REDIS_PASSWORD
import json
import requests
from bson import json_util


class ArticleApiPipeline(object):
    r = redis.Redis(host=LOCAL_REDIS_HOST, port=LOCAL_REDIS_PORT, password=LOCAL_REDIS_PASSWORD)

    def __init__(self):
        pass

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, ArticleNewsItem):
            url = 'http://192.168.0.120:18088/api/news?appkey=5dkg44'
            headers = {'content-type': 'application/json'}
            request_data = {}
            data = []
            item_dict = dict(item)
            item_dict['id'] = item_dict['_id']
            del item_dict['_id']
            data.append(item_dict)

            request_data['data'] = data
            print(json.dumps(request_data))
            r = requests.post(url, data=json.dumps(request_data), headers=headers)
            json1 = r.json()
            if 'code' in json1:
                code = json1['code']
                if code != '200':
                    self.r.sadd('article:crawl:news:error_api', item_dict['url'])
        return item


class ArticleMongoDBPipeline(object):
    r = redis.Redis(host=LOCAL_REDIS_HOST, port=LOCAL_REDIS_PORT, password=LOCAL_REDIS_PASSWORD,db=3)

    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        db = client[DB_NAME]
        self.ArticleNews = db["ArticleNews"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, ArticleNewsItem):
            # title为空则不保存
            if 'job_no' in item and item['job_no'] and 'title' in item and item['title']:
                # self.insert_item(self.ArticleNews, item)
                # self.r.hset('article:crawl:news:data',)
                self.insert_item(self.r,item)
                if 'job_no' in item:
                    self.r.zincrby('article:crawl:news:rank_job', item['job_no'], 1)
                if 'original_source' in item:
                    self.r.zincrby('article:crawl:news:rank_source', item['original_source'], 1)
                if 'app_name' in item:
                    self.r.zincrby('article:crawl:news:rank_app', item['app_name'], 1)
                if 'page_name' in item:
                    self.r.zincrby('article:crawl:news:rank_page', item['page_name'], 1)

            else:
                self.r.sadd('article:crawl:news:error_page', item['url'])
                self.r.sadd('article:crawl:news:error_page_detail', item['url']+"::"+"no title")
                self.r.srem('article:crawl:news:urls', item['dupe_key'])
            if 'page_subject' not in item and 'page_name' not in item:
                self.r.sadd('article:crawl:news:error_page_detail',item['url'] + "::" + "no page_name or no page_subject")
            if 'publish_time' not in item:
                self.r.sadd('article:crawl:news:error_page_detail', item['url'] + "::" + "no publish_time")
            if 'original_source' not in item and item['url'].find('pictures') == -1 and item['url'].find('photo') == -1 and item['url'].find('huanqiu.com/gt') == -1 \
                    and item['url'].find('www.thepaper.cn/newsDetail') == -1:
                self.r.sadd('article:crawl:news:error_page_detail', item['url'] + "::" + "no original_source")
            if 'content' not in item and item['url'].find('pictures') == -1 and item['url'].find('photo') == -1 and item['url'].find('huanqiu.com/gt') == -1and item['url'].find('http://www.chinanews.com/gn/') == -1 and item['url'].find('shipin') == -1 \
                    and item['url'].find('www.thepaper.cn/newsDetail') == -1 and item['url'].find('financepic') == -1 and item['url'].find('http://www.xinhuanet.com/mil') == -1 and item['url'].find('http://v.haiwainet.cn/n/') == -1:
                self.r.sadd('article:crawl:news:error_page_detail', item['url'] + "::" + "no content")
        return item

    @staticmethod
    def insert_item(collection, item):
        try:
            collection.hset('article:crawl:news:data',item['_id'],json_util.dumps(item, ensure_ascii=False))
            # print("插入数据"+str(item))
            # collection.insert(dict(item))
        except DuplicateKeyError:
            """
            说明有重复数据
            """
            print('重复数据 -->' + item['_id'])
            pass


