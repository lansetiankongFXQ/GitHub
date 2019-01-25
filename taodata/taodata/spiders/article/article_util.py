#!/usr/bin/env python
# encoding: utf-8
import sys
import os
sys.path.append(os.getcwd())
from taodata.settings import LOCAL_REDIS_HOST, LOCAL_REDIS_PORT, LOCAL_REDIS_PASSWORD
from taodata.spiders.article.items import ArticleNewsItem
import redis
import json
import uuid


r = redis.Redis(host=LOCAL_REDIS_HOST, port=LOCAL_REDIS_PORT, password=LOCAL_REDIS_PASSWORD)


def get_page_setting(page_url):
    # 判断页面配置是否存在
    if not r.hexists('article:crawl:news:setting', page_url):
        return None

    page_setting = r.hget('article:crawl:news:setting', page_url).decode('utf-8')
    item = json.loads(page_setting)
    return item


def remove_page_setting(page_url):
    r.hdel('article:crawl:news:setting', page_url)


def build_article_item(data):
    item = ArticleNewsItem()

    # 设置_id
    data['_id'] = str(uuid.uuid1())

    if '_id' in data:
        item['_id'] = data['_id']
    if 'title' in data:
        item['title'] = data['title']
    # page id
    if 'id' in data:
        item['page_id'] = data['id']
    if 'page_name' in data:
        item['page_name'] = data['page_name']
    if 'page_subject' in data:
        item['page_subject'] = data['page_subject']
    if 'app_id' in data:
        item['app_id'] = data['app_id']
    if 'app_code' in data:
        item['app_code'] = data['app_code']
    if 'app_name' in data:
        item['app_name'] = data['app_name']
    if 'publish_time_str' in data:
        item['publish_time_str'] = data['publish_time_str']
    if 'content' in data:
        item['content'] = data['content']
    if 'keywords' in data:
        item['keywords'] = data['keywords']
    if 'link_url' in data:
        item['url'] = data['link_url']
    if 'original_title' in data:
        item['original_title'] = data['original_title']
    if 'original_source' in data:
        item['original_source'] = data['original_source']
    if 'original_url' in data:
        item['original_url'] = data['original_url']
    if 'app_region' in data:
        item['app_region'] = data['app_region']
    if 'app_type' in data:
        item['app_type'] = data['app_type']
    if 'publish_time' in data:
        item['publish_time'] = data['publish_time']
    if 'crawl_time' in data:
        item['crawl_time'] = data['crawl_time']
    if 'job_no' in data:
        item['job_no'] = data['job_no']
    if 'job_seq' in data:
        item['job_seq'] = data['job_seq']
    if 'dupe_key' in data:
        item['dupe_key'] = data['dupe_key']
    if 'crawl_time' in data and 'publish_time' in data:
        item['interval_time'] = str(int(data['crawl_time']) - int(data['publish_time']))

    return item


