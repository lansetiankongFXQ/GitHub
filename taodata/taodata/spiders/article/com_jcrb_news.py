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
        link = LinkExtractor(restrict_xpaths='//div[@class="mainContent"]/ul/li')
        links = link.extract_links(response)
        for link in links:
            url = link.url
            if url:
                # if url.find('https://mp.weixin.qq.com') > -1:
                #     continue
                data['link_text'] = link.text
                data['link_url'] = link.url
                data['page_function'] = 'parse_article'
                request = Request(url, dont_filter=True, priority=10, meta=data)
                yield request
    except:
        r.sadd('article:crawl:news:error_page', page_url)

    article_util.remove_page_setting(page_url)


# 解析发布时间
def parse_article_publish_time(tree_node):
    # 央广网
    try:
        publish_time_node = tree_node.xpath('//div[@id="about"]/span[@id="pubtime_baidu"]/text()')
        publish_time = publish_time_node[0][3:]
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
        title = tree_node.xpath('//div[@id="mainLeft"]/h1/text()')
        if title:
            return title[0].replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '')
    except:
        pass


    # 默认返回
    return None


# 解析来源
def parse_article_original_source(tree_node):
    # 央广网

    try:
        original_source = tree_node.xpath('//div[@id="about"]/span[@id="source_baidu"]/text()')
        if original_source and original_source[0]:
            original_source_str = original_source[0].split('来源：')
            if original_source_str:
                return original_source_str[1]
    except:
        pass

    # 默认返回
    return None


# 解析来源
def parse_article_original_url(tree_node):
    # 央广网

    # try:
    #     original_url = tree_node.xpath('//div[@class="la_tool"]/span[@class="la_t_b"]/a/@href')
    #     if original_url and original_url[0]:
    #         return original_url[0]
    # except:
    #     pass

    # 默认返回
    return None


# 解析 正文
def parse_article_content(tree_node):
    # 央广网

    try:
        article_data = tree_node.xpath('//div[@class="Custom_UnionStyle"]')
        if article_data:
            p_nodes = article_data[0].xpath('p')
            content = ''
            for node in p_nodes:
                content = content + node.xpath('string(.)').replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '') + '\n'
            return content
    except:
        pass

    try:
        article_data = tree_node.xpath('//div[@class="TRS_Editor"]')
        if article_data:
            p_nodes = article_data[0].xpath('p')
            content = ''
            for node in p_nodes:
                content = content + node.xpath('string(.)').replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '') + '\n'
            return content
    except:
        pass

    # 默认返回
    return None


# 解析page_subject
def parse_page_subject(tree_node):
    # 央广网

    try:
        page_subjects = tree_node.xpath('//div[@class="curpage"]/a/text()')
        return page_subjects[1]
    except:
        pass
    return None


# 解析文章
def parse_article(response):
    data = response.meta
    tree_node = etree.HTML(response.text,parser=etree.HTMLParser(encoding='utf-8'))
    try:
        # 新闻专题
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






