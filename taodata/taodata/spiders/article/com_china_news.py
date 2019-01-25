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


r = redis.Redis(host=LOCAL_REDIS_HOST, port=LOCAL_REDIS_PORT, password=LOCAL_REDIS_PASSWORD)


# 解析新闻
def parse_roll(response):
    page_url = response.url
    data = article_util.get_page_setting(page_url)
    try:
        link = LinkExtractor(restrict_xpaths='//div[@class="content_list"]/ul//li')
        links = link.extract_links(response)
        for link in links:
            url = link.url
            if url:
                data['link_text'] = link.text
                data['link_url'] = link.url
                data['page_function'] = 'parse_article'
                data['page_name'] = parse_page_name_url(page_url)
                request = Request(url, dont_filter=True, priority=10, meta=data)
                yield request
    except:
        r.sadd('article:crawl:news:error_page', response.url)

    article_util.remove_page_setting(page_url)


# 解析发布时间
def parse_article_publish_time(tree_node):
    try:
        publish_time_node = tree_node.xpath('//div[@class="left-time"]/div[@class="left-t"]/text()')
        temp_publish_time = publish_time_node[0].split('\u3000')
        publish_time = temp_publish_time[0]
        if publish_time:
            time_obj = datetime.datetime.strptime(publish_time.strip(), '%Y年%m月%d日 %H:%M')
            time1 = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            time2 = str(int(time.mktime(time_obj.timetuple())))
            return time1, time2
    except:
        pass

    try:
        publish_time_node = tree_node.xpath('//div[@class="content_title"]/div[@class="left"]/p/text()')
        publish_time = publish_time_node[0][6:23]
        if publish_time:
            time_obj = datetime.datetime.strptime(publish_time.strip(), '%Y年%m月%d日 %H:%M')
            time1 = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            time2 = str(int(time.mktime(time_obj.timetuple())))
            return time1, time2
    except:
        pass

    # 默认返回
    return None, None


# 解析主标题
def parse_article_title(tree_node):
    # 国内
    try:
        title = tree_node.xpath('//div[@id="cont_1_1_2"]/h1/text()')
        if title and title[0]:
            return title[0].replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '')
    except:
        pass
    # 国际
    try:
        title = tree_node.xpath('//div[@class="content_title"]/div[@class="left"]/h1/text()')
        if title and title[0]:
            return title[0].replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '')
    except:
        pass


    # 默认返回
    return None


# 解析来源
def parse_article_original_source(tree_node):
    # 国内
    try:
        temp_original_source = tree_node.xpath('//div[@class="left-time"]/div[@class="left-t"]/text()')
        original_source = temp_original_source[0].split("来源：")
        if original_source and original_source[1]:
            return original_source[1]
    except:
        pass

    try:
        original_source = tree_node.xpath('//div[@class="left-time"]/div[@class="left-t"]/a/text()')
        if original_source and original_source[0]:
            return original_source[0]
    except:
        pass

    try:
        temp_original_source = tree_node.xpath('//div[@class="content_title"]/div[@class="left"]/p/text()')
        original_source = temp_original_source[0].split("来源：")
        if original_source and original_source[1]:
            return original_source[1].strip()
    except:
        pass
    # 默认返回
    return None


# 解析来源
def parse_article_original_url(tree_node):
    # 逻辑1
    try:
        original_url = tree_node.xpath('//div[@class="box01"]/div[@class="fl"]/a/@href')
        if original_url and original_url[0]:
            return original_url[0]
    except:
        pass

    # 默认返回
    return None


# 解析 正文
def parse_article_content(tree_node):
    # 逻辑1
    try:
        article_data = tree_node.xpath('//div[@class="left_zw"]')
        if article_data and article_data[0]:
            p_nodes = article_data[0].xpath('p')
            content = ''
            for node in p_nodes:
                content = content + node.xpath('string(.)').replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '') + '\n'
            return content
    except:
        pass

    # 默认返回
    return None


# 解析page_name
def parse_page_name_url(url):

    # 国际
    if url.find('world') > -1:
        page_name = '国际'
        return page_name
    # 体育
    if url.find('sports') > -1:
        page_name = '体育'
        return page_name
    # 娱乐
    if url.find('ent') > -1:
        page_name = '娱乐'
        return page_name
    # 军事
    if url.find('mil') > -1:
        page_name = '军事'
        return page_name
    # 科技
    if url.find('tech') > -1:
        page_name = '科技'
        return page_name
    # 财经
    if url.find('fortune') > -1:
        page_name = '财经'
        return page_name
    return '未知'


# 解析page_name
def parse_page_name(tree_node):

    # 国内
    page_name = tree_node.xpath('//div[@id="nav"]/a/text()')
    if page_name and page_name[1]:
        return page_name[1]
    else:
        pass
    return None


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
        original_url = parse_article_original_url(tree_node)
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






