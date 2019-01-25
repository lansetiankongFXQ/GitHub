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
from taodata.settings import LOCAL_REDIS_HOST, LOCAL_REDIS_PORT, LOCAL_REDIS_PASSWORD
import requests


r = redis.Redis(host=LOCAL_REDIS_HOST, port=LOCAL_REDIS_PORT, password=LOCAL_REDIS_PASSWORD)


# 解析央广网-国内
def parse_roll_china(response):
    page_url = response.url
    data = article_util.get_page_setting(page_url)
    try:
        link = LinkExtractor(restrict_xpaths='//div[@id="tab-cont-1" and @class="bd clear"]/div[2]/ul/li')
        links = link.extract_links(response)
        for link in links:
            url = link.url
            if url:
                data['link_text'] = link.text
                data['link_url'] = link.url
                data['page_function'] = 'parse_article'
                request = Request(url, dont_filter=True, priority=10, meta=data)
                yield request

        article_util.remove_page_setting(page_url)
    except:
        r.sadd('article:crawl:news:error_page', page_url)


# 解析央广网-国际
def parse_roll_world(response):
    page_url = response.url
    data = article_util.get_page_setting(page_url)
    try:
        link = LinkExtractor(restrict_xpaths='//div[@id="tab-cont-1" and @class="bd clear"]/div[3]/ul/li')
        links = link.extract_links(response)
        for link in links:
            url = link.url
            if url:
                data['link_text'] = link.text
                data['link_url'] = link.url
                data['page_function'] = 'parse_article'
                request = Request(url, dont_filter=True, priority=10, meta=data)
                yield request

        article_util.remove_page_setting(page_url)
    except:
        r.sadd('article:crawl:news:error_page', page_url)


# 解析央广网-军事
def parse_roll_mil(response):
    page_url = response.url
    data = article_util.get_page_setting(page_url)
    try:
        link = LinkExtractor(restrict_xpaths='//div[@id="tab-cont-1" and @class="bd clear"]/div[5]/ul/li')
        links = link.extract_links(response)
        for link in links:
            url = link.url
            if url:
                data['link_text'] = link.text
                data['link_url'] = link.url
                data['page_function'] = 'parse_article'
                request = Request(url, dont_filter=True, priority=10, meta=data)
                yield request

        article_util.remove_page_setting(page_url)
    except:
        r.sadd('article:crawl:news:error_page', page_url)


# 解析央广网-财经
def parse_roll_finance(response):
    page_url = response.url
    data = article_util.get_page_setting(page_url)
    try:
        link = LinkExtractor(restrict_xpaths='//div[@id="tab-cont-1" and @class="bd clear"]/div[6]/ul/li')
        links = link.extract_links(response)
        for link in links:
            url = link.url
            if url:
                data['link_text'] = link.text
                data['link_url'] = link.url
                data['page_function'] = 'parse_article'
                request = Request(url, dont_filter=True, priority=10, meta=data)
                yield request

        article_util.remove_page_setting(page_url)
    except:
        r.sadd('article:crawl:news:error_page', page_url)


# 解析央广网-科技
def parse_roll_tech(response):
    page_url = response.url
    data = article_util.get_page_setting(page_url)
    try:
        link = LinkExtractor(restrict_xpaths='//div[@id="tab-cont-1"]/div[7]/ul/li')
        links = link.extract_links(response)
        for link in links:
            url = link.url
            if url:
                data['link_text'] = link.text
                data['link_url'] = link.url
                data['page_function'] = 'parse_article'
                request = Request(url, dont_filter=True, priority=10, meta=data)
                yield request

        article_util.remove_page_setting(page_url)
    except:
        r.sadd('article:crawl:news:error_page', page_url)


# 解析发布时间
def parse_article_publish_time(tree_node):
    # 央广网
    try:
        publish_time_node = tree_node.xpath('//div[@class="info"]/span[@class="infoA"]/text()')
        publish_time = publish_time_node[0].replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '')
        if publish_time:
            time_obj = datetime.datetime.strptime(publish_time.strip(), '%Y-%m-%d %H:%M:%S')
            time1 = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            time2 = str(int(time.mktime(time_obj.timetuple())))
            return time1, time2
    except:
        pass

    # 默认返回
    return None, None


# 解析主标题
def parse_article_title(tree_node):
    # 央广网
    try:
        title = tree_node.xpath('//h1[@class="articleHead"]/text()')
        if title and title[0]:
            return title[0].replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '')
    except:
        pass

    # 默认返回
    return None


# 解析来源
def parse_article_original_source(tree_node):
    # 央广网
    try:
        temp_original_source = tree_node.xpath('//div[@class="info"]/span[@id="source_baidu"]/text()')
        original_source = temp_original_source[0].split("来源：")
        if original_source and original_source[1]:
            return original_source[1]
    except:
        pass

    # 默认返回
    return None


# 解析来源
def parse_article_original_url(tree_node):
    # 逻辑1
    try:
        original_url = tree_node.xpath('//div[@class="la_tool"]/span[@class="la_t_b"]/a/@href')
        if original_url and original_url[0]:
            return original_url[0]
    except:
        pass

    # 默认返回
    return None


# 解析 正文
def parse_article_content(tree_node):
    # 央广网
    try:
        content = ''
        article_data = tree_node.xpath('//div[@class="articleText"]')
        if article_data and article_data[0]:
            p_nodes = article_data[0].xpath('p')

            for node in p_nodes:
                content = content + node.xpath('string(.)').replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '') + '\n'
        temp_article_data = tree_node.xpath('//div[@class="page"]')
        if temp_article_data and temp_article_data[0]:
            article_data_other_com = temp_article_data[0].xpath('ul[@class="pageUl"]/li')
            del article_data_other_com[0]
            del article_data_other_com[1]
            del article_data_other_com[len(article_data_other_com)-1]
            for cc_item in article_data_other_com:
                response = requests.get(cc_item.xpath('a/@href')[0])
                tree_node_com = etree.HTML(response.text, parser=etree.HTMLParser(encoding='utf-8'))
                article_data_com = tree_node_com.xpath('//div[@class="articleText"]')
                if article_data_com and article_data_com[0]:
                    p_nodes_com = article_data_com[0].xpath('p')
                    for node_com in p_nodes_com:
                        content = content + node_com.xpath('string(.)').replace('\r', '').replace('\u3000','').replace('\t', '').replace('\n', '') + '\n'
        return content

    except:
        pass

    # 默认返回
    return None

# 解析page_name
def parse_page_name(tree_node):

    # 央广网
    try:
        page_name = tree_node.xpath('//div[@class="indexList"]//a/text()')
        if page_name and page_name[1]:
            return page_name[1]
        else:
            pass
    except:
        pass
    return '未知'


# 解析文章
def parse_article(response):
    data = response.meta
    tree_node = etree.HTML(response.text,parser=etree.HTMLParser(encoding='utf-8'))
    try:
        # 新闻分类
        page_name = parse_page_name(tree_node)
        if page_name:
            data['page_name'] = page_name

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
        if original_source:
            data['original_source'] = original_source.strip()
            r.sadd('article:crawl:news:source', original_source.strip())
        # 来源url
        # original_url = parse_article_original_url(tree_node)
        # if original_url:
        #     data['original_url'] = original_url

        # 正文内容
        content = parse_article_content(tree_node)
        if content:
            data['content'] = content

        data['crawl_time'] = str(int(time.time()))

        yield article_util.build_article_item(data)

    except:
        traceback.print_exc()






