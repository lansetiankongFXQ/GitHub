#!/usr/bin/env python
# encoding: utf-8
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from taodata.spiders.article import article_util
import time
from lxml import etree
import datetime
import traceback
import redis
from taodata.settings import LOCAL_REDIS_HOST, LOCAL_REDIS_PORT, LOCAL_REDIS_PASSWORD
import requests


r = redis.Redis(host=LOCAL_REDIS_HOST, port=LOCAL_REDIS_PORT, password=LOCAL_REDIS_PASSWORD)


# 解析央广网-滚动新闻
def parse_roll(response):
    page_url = response.url
    data = article_util.get_page_setting(page_url)
    try:
        link = LinkExtractor(restrict_xpaths='//div[@class="w650 fl"]/ul/li')
        links = link.extract_links(response)
        for link in links:
            url = link.url
            if url == page_url:
                continue
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
        publish_time_node = tree_node.xpath('//div[@class="contentExtra"]/span[@class="first"]/text()')
        publish_time = publish_time_node[0].replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '')
        if publish_time:
            time_obj = datetime.datetime.strptime(publish_time.strip(), '%Y-%m-%d %H:%M:%S')
            time1 = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            time2 = str(int(time.mktime(time_obj.timetuple())))
            return time1, time2
    except:
        pass

    try:
        publish_time_node = tree_node.xpath('//div[@class="extra mlr20"]/span[@class="fl"]/text()')
        publish_time = publish_time_node[0].replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '')
        if publish_time:
            time_obj = datetime.datetime.strptime(publish_time.strip(), '%Y-%m-%d %H:%M:%S')
            time1 = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            time2 = str(int(time.mktime(time_obj.timetuple())))
            return time1, time2
    except:
        pass

    try:
        publish_time_node = tree_node.xpath('//div[@class="main"]/div[@class="newsMess"]/span/text()')
        publish_time = publish_time_node[0].replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '')
        if publish_time:
            time_obj = datetime.datetime.strptime(publish_time.strip(), '%Y-%m-%d %H:%M:%S')
            time1 = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            time2 = str(int(time.mktime(time_obj.timetuple())))
            return time1, time2
    except:
        pass

    try:
        publish_time_node = tree_node.xpath('//div[@class="video_list_7"][1]/text()')
        publish_time = publish_time_node[0][5:24].replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '')
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
        title = tree_node.xpath('//div[@class="show_text"]/h1[@class="show_wholetitle"]/text()')
        if title and title[0]:
            return title[0].replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '')
    except:
        pass

    try:
        title = tree_node.xpath('//div[@class="show_text fl"]/h1[@class="show_wholetitle"]/text()')
        if title and title[0]:
            return title[0].replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '')
    except:
        pass

    try:
        title = tree_node.xpath('//div[@class="w640 fl"]/h1[@class="mlr20"]/text()')
        if title and title[0]:
            return title[0].replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '')
    except:
        pass

    try:
        title = tree_node.xpath('//div[@class="main"]/h1/text()')
        if title and title[0]:
            return title[0].replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '')
    except:
        pass

    try:
        title = tree_node.xpath('//div[@class="video_box_2"]/h1/text()')
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
        original_source = tree_node.xpath('//div[@class="contentExtra"]/span[2]/a/text()')
        if original_source and original_source[0]:
            result_source = original_source[0]
            if result_source.find("来源：") > -1:
                result_source = result_source[3:]
            return result_source
    except:
        pass

    try:
        original_source = tree_node.xpath('//div[@class="contentExtra"]/span[2]/text()')
        if original_source and original_source[0]:
            result_source = original_source[0]
            if result_source.find("来源：") > -1:
                result_source = result_source[3:]
            return result_source
    except:
        pass
    try:
        original_source = tree_node.xpath('//div[@class="extra mlr20"]/span[2]/a/text()')
        if original_source and original_source[0]:
            result_source = original_source[0]
            if result_source.find("来源：") > -1:
                result_source = result_source[3:]
            return result_source
    except:
        pass
    try:
        original_source = tree_node.xpath('//div[@class="extra mlr20"]/span[2]/text()')
        if original_source and original_source[0]:
            result_source = original_source[0]
            if result_source.find("来源：") > -1:
                result_source = result_source[3:]
            return result_source
    except:
        pass

    try:
        original_source = tree_node.xpath('//div[@class="newsMess"]/span[2]/a/text()')
        if original_source and original_source[0]:
            result_source = original_source[0]
            if result_source.find("来源：") > -1:
                result_source = result_source[3:]
            return result_source
    except:
        pass

    try:
        original_source = tree_node.xpath('//div[@class="newsMess"]/span[2]/text()')
        if original_source and original_source[0]:
            result_source = original_source[0]
            if result_source.find("来源：") > -1:
                result_source = result_source[result_source.find("来源：")+3:]
            return result_source
    except:
        pass

    try:
        original_source = tree_node.xpath('//div[@class="newsMess"]/span[2]/text()')
        if original_source and original_source[0]:
            result_source = original_source[0]
            if result_source.find("来源：") > -1:
                result_source = result_source[result_source.find("来源：")+3:]
            return result_source
    except:
        pass

    try:
        original_source = tree_node.xpath('//div[@class="video_list_7"]/a/text()')
        if original_source and original_source[0]:
            result_source = original_source[0]
            if result_source.find("来源：") > -1:
                result_source = result_source[result_source.find("来源：")+3:]
            return result_source
    except:
        pass

    try:
        original_source = tree_node.xpath('//div[@class="video_list_7"]/text()')
        if original_source and original_source[0]:
            result_source = original_source[0]
            if result_source.find("来源：") > -1:
                result_source = result_source[result_source.find("来源：")+3:]
            return result_source
    except:
        pass
    # 默认返回
    return None


# 解析来源
def parse_article_original_url(tree_node):
    try:
        original_url = tree_node.xpath('//div[@class="contentExtra"]/span[2]/a/@href')
        if original_url and original_url[0]:
            return original_url[0]
    except:
        pass

    try:
        original_url = tree_node.xpath('//div[@class="newsMess"]/span[2]/a/@href')
        if original_url and original_url[0]:
            return original_url[0]
    except:
        pass

    # 默认返回
    return None


# 解析 正文
def parse_article_content(tree_node):
    # 央广网
    content = ''
    try:
        article_data = tree_node.xpath('//div[@class="articleText"]')
        if article_data and article_data[0]:
            p_nodes = article_data[0].xpath('p')
            for node in p_nodes:
                content = content + node.xpath('string(.)').replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '') + '\n'
            return content
    except:
        pass

    try:
        article_data = tree_node.xpath('//div[@class="contentMain"]')
        if article_data and article_data[0]:
            p_nodes = article_data[0].xpath('p')
            for node in p_nodes:
                content = content + node.xpath('string(.)').replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '') + '\n'
            return content
    except:
        pass

    try:
        article_data = tree_node.xpath('//div[@id="cen" and @class="c mlr20"]')
        if article_data and article_data[0]:
            p_nodes = article_data[0].xpath('p')
            for node in p_nodes:
                content = content + node.xpath('string(.)').replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '') + '\n'
            return content
    except:
        pass

    try:
        article_data = tree_node.xpath('//div[@class="des"]')
        if article_data and article_data[0]:
            p_nodes = article_data[0].xpath('p')
            for node in p_nodes:
                content = content + node.xpath('string(.)').replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '') + '\n'
            return content
    except:
        pass

    try:
        article_data = tree_node.xpath('//div[@class="video_list_7ri"]/div')
        if article_data and article_data[0]:
            p_nodes = article_data[0].xpath('p')
            for node in p_nodes:
                content = content + node.xpath('string(.)').replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '') + '\n'
            return content
    except:
        pass
    # 默认返回
    return None


# 解析page_subject
def parse_page_subject(tree_node):
    try:
        page_subject = tree_node.xpath('//div[@class="show_logo clearfix"]/div[@class="fl"][2]/a/text()')
        if page_subject:
            page_subject_str = ''
            for item in page_subject:
                page_subject_str = page_subject_str+" "+item
            return page_subject_str[1:]
    except:
        pass

    try:
        page_subject = tree_node.xpath('//div[@class="logo"]/div[@class="fl"]/a/text()')
        if page_subject:
            page_subject_str = ''
            for item in page_subject:
                page_subject_str = page_subject_str+" "+item
            return page_subject_str[1:]
    except:
        pass

    try:
        page_subject = tree_node.xpath('//div[@class="nav mt10"]/a/text()')
        if page_subject:
            page_subject_str = ''
            for item in page_subject:
                page_subject_str = page_subject_str+" "+item
            return page_subject_str[1:page_subject_str.find(' 正文')]
    except:
        pass

    try:
        page_subject = tree_node.xpath('//div[@class="video_box_1"]/a/text()')
        if page_subject:
            page_subject_str = ''
            for item in page_subject:
                if item:
                    page_subject_str = page_subject_str+" "+item
            return page_subject_str[1:]
    except:
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






