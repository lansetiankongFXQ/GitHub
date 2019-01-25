#!/usr/bin/env python
# encoding: utf-8
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from taodata.spiders.article import article_util
import time
from lxml import etree
import datetime
import json
import traceback
import redis
import requests
from taodata.settings import LOCAL_REDIS_HOST, LOCAL_REDIS_PORT, LOCAL_REDIS_PASSWORD


r = redis.Redis(host=LOCAL_REDIS_HOST, port=LOCAL_REDIS_PORT, password=LOCAL_REDIS_PASSWORD)


# 解析滚动新闻
def parse_roll(response):
    page_url = response.url
    data = article_util.get_page_setting(page_url)
    tree_node = etree.HTML(response.text, parser=etree.HTMLParser(encoding='utf-8'))
    c_node = tree_node.xpath('//ul[contains(@class,"fin_newsList") and contains(@class,"cfix")]')
    cc_node = c_node[0].xpath('//li[@class="cfix"]/h2')

    if  cc_node:
        for ccc_node in cc_node:
            cc_url = ccc_node.xpath('a/@href')[0]
            data['link_text'] = ccc_node.xpath('a/text()')[0]
            data['link_url'] = cc_url
            data['page_function'] = 'parse_article'
            yield Request(cc_url, dont_filter=True, priority=10, meta=data)
    else:
        r.sadd('article:crawl:news:error_page', response.url)

    article_util.remove_page_setting(page_url)


# 解析发布时间
def parse_article_publish_time(tree_node):
    # 逻辑1
    try:
        publish_time_node = tree_node.xpath('//div[@id="msgBox"]/p[@class="sourceBox"]/span')
        publish_time = str(publish_time_node[0].text)+str(publish_time_node[1].text)
        if publish_time:
            time_obj = datetime.datetime.strptime(publish_time.strip(), '%Y-%m-%d%H:%M:%S')
            time1 = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            time2 = str(int(time.mktime(time_obj.timetuple())))
            return time1, time2
    except:
        pass

    # 默认返回
    return None, None


# 解析主标题
def parse_article_title(tree_node):
    # 逻辑1
    try:
        title = tree_node.xpath('//div[@class="articleTitle"]/h1/text()')
        if title and title[0]:
            return title[0]
    except:
        pass

    # 默认返回
    return None


# 解析来源
def parse_article_original_source(tree_node):
    # 逻辑1
    try:
        original_source = tree_node.xpath('//div[@id="msgBox"]/p[@class="sourceBox"]/span/text()')
        if original_source and original_source[2]:
            return original_source[2]
    except:
        pass

    # 默认返回
    return None


# 解析来源
def parse_article_original_url(tree_node):
    # 默认返回
    return None


# 解析 正文
def parse_article_content(tree_node):
    # 逻辑1
    try:
        article_data = tree_node.xpath('//div[@id="articleAll"]')
        if article_data and article_data[0]:
            p_nodes = tree_node.xpath('//div[@id="articleAll"]//p')
            t_nodes = tree_node.xpath('//div[@id="articleAll"]//table')
            content = ''
            for node in p_nodes:
                content = content + node.xpath('string(.)').replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '') + '\n'
            for node in t_nodes:
                content = content + node.xpath('string(.)').replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '') + '\n'
            temp_article_data = tree_node.xpath('//ul[@class="pageBox cfix mb28"]')
            if temp_article_data and temp_article_data[0]:
                article_data_other_com = temp_article_data[0].xpath('li')
                del article_data_other_com[0]
                for cc_item in article_data_other_com:
                    href = cc_item.xpath('a/@href')
                    print('http'+href[0])
                    response = requests.get('http:'+href[0])
                    tree_node_com = etree.HTML(response.text, parser=etree.HTMLParser(encoding='utf-8'))
                    article_data_com = tree_node_com.xpath('//div[@id="articleAll"]//p')
                    if not article_data_com:
                        article_data_com = tree_node_com.xpath('//div[@id="articleAll"]//table')
                    for node_com in article_data_com:
                        content = content + node_com.xpath('string(.)').replace('\r', '').replace('\u3000','').replace('\t','').replace('\n', '') + '\n'
            return content
    except:
        pass

    # 默认返回
    return None


# 解析page_name
def parse_page_subject(tree_node):
    # 新闻分类
    page_name = tree_node.xpath('//dl[@class="cfix fLeft"]/dd/a[last()]/text()')
    if page_name and page_name[0]:
        return page_name[0]
    else:
        pass

    return '未知'


# 解析文章
def parse_article(response):
    data = response.meta
    tree_node = etree.HTML(response.text,parser=etree.HTMLParser(encoding='utf-8'))
    try:
        # 新闻分类
        page_subject = parse_page_subject(tree_node)
        if page_subject:
            data['page_subject'] = page_subject

        # 主标题
        title = parse_article_title(tree_node)
        if title:
            data['title'] = title

        # 发布时间
        publish_time_str, publish_time = parse_article_publish_time(tree_node)
        if publish_time_str:
            data['publish_time_str'] = publish_time_str
        if publish_time:
            data['publish_time'] = publish_time

        # 来源
        original_source = parse_article_original_source(tree_node)
        original_url = parse_article_original_url(tree_node)
        if original_source:
            data['original_source'] = original_source.strip()
            r.sadd('article:crawl:news:source', original_source.strip())
        if original_url:
            data['original_url'] = original_url
        # 正文内容
        content = parse_article_content(tree_node)
        if content:
            data['content'] = content

        data['crawl_time'] = str(int(time.time()))

        yield article_util.build_article_item(data)

    except:
        traceback.print_exc()






