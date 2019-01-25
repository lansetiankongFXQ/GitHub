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


def parse_china(response):
    link = LinkExtractor(restrict_xpaths=['//li'])
    links = link.extract_links(response)
    page_url = response.url
    data = article_util.get_page_setting(page_url)

    # 设置数据
    for link in links:
        url = link.url
        if url.startswith('https://news.sina.com.cn/c'):
            data['link_text'] = link.text
            data['link_url'] = link.url
            data['page_function'] = 'parse_china_article'
            request = Request(url, dont_filter=True, priority=10, meta=data)
            yield request


# 解析滚动新闻
def parse_roll(response):
    page_url = response.url
    data = article_util.get_page_setting(page_url)
    # 解析数据
    text1 = response.text
    try:
        json1 = json.loads(text1)
    except:
        traceback.print_exc()
        r.sadd('article:crawl:news:error_page', response.url)
        return

    # 处理数据
    if 'result' in json1 and 'status' in json1['result'] and 'code' in json1['result']['status'] \
            and json1['result']['status']['code'] == 0:
        if 'data' in json1['result']:
            # 新闻列表
            items = json1['result']['data']
            # 采集新闻详情
            for item in items:
                url = item['url']
                data['link_text'] = item['title']
                data['link_url'] = item['url']
                data['page_function'] = 'parse_article'
                request = Request(url, dont_filter=True, priority=10, meta=data)
                yield request
    else:
        r.sadd('article:crawl:news:error_page', response.url)

    article_util.remove_page_setting(page_url)


# 解析关键字
def parse_article_keywords(tree_node):
    # 逻辑1
    try:
        article_keywords = tree_node.xpath('//p[@class="art_keywords"]/a/text()')
        if article_keywords and article_keywords[0]:
            ret = ''
            for kw in article_keywords:
                ret = ret + kw + ' '
            return ret
    except:
        pass

    # 逻辑2
    try:
        article_keywords = tree_node.xpath('//div[@id="keywords"]/@data-wbkey')
        if article_keywords and article_keywords[0]:
            return article_keywords[0]
    except:
        pass

    return None


# 解析发布时间
def parse_article_publish_time(tree_node):
    # 逻辑1
    try:
        publish_time = tree_node.xpath('//span[@id="pub_date"]/text()')
        if publish_time and publish_time[0]:
            time_obj = datetime.datetime.strptime(publish_time[0].strip(), '%Y年%m月%d日%H:%M')
            time1 = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            time2 = str(int(time.mktime(time_obj.timetuple())))
            return time1, time2
    except:
        pass

    # 逻辑2
    try:
        publish_time = tree_node.xpath('//span[@id="pub_date"]/text()')
        if publish_time and publish_time[0]:
            time_obj = datetime.datetime.strptime(publish_time[0].strip(), '%Y-%m-%d %H:%M:%S')
            time1 = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            time2 = str(int(time.mktime(time_obj.timetuple())))
            return time1, time2
    except:
        pass

    # 逻辑3
    try:
        publish_time = tree_node.xpath('//div[@class="date-source"]/span[@class="date"]/text()')
        if publish_time and publish_time[0]:
            time_obj = datetime.datetime.strptime(publish_time[0], '%Y年%m月%d日 %H:%M')
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
        title = tree_node.xpath('//h1[@id="artibodyTitle"]/text()')
        if title and title[0]:
            return title[0]
    except:
        pass

    # 逻辑2
    try:
        title = tree_node.xpath('//h1[@class="main-title"]/text()')
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
        original_source = tree_node.xpath('//span[@id="media_name"]/a/text()')
        if original_source and original_source[0]:
            return original_source[0]
    except:
        pass

    # 逻辑2
    try:
        original_source = tree_node.xpath('//div[@class="date-source"]/a/text()')
        if original_source and original_source[0]:
            return original_source[0]
    except:
        pass

    # 逻辑3
    try:
        original_source = tree_node.xpath('//div[@class="date-source"]/span[@class="source ent-source"]/text()')
        if original_source and original_source[0]:
            return original_source[0]
    except:
        pass

    # 逻辑4
    try:
        original_source = tree_node.xpath('//div[@class="date-source"]/span[@class="source"]/text()')
        if original_source and original_source[0]:
            return original_source[0]
    except:
        pass


    # 默认返回
    return None

# 解析来源
def parse_article_original_url(tree_node):
    # 逻辑1
    try:
        original_url = tree_node.xpath('//span[@id="media_name"]/a/@href')
        if original_url and original_url[0]:
            return original_url[0]
    except:
        pass

    # 逻辑2
    try:
        original_url = tree_node.xpath('//div[@class="date-source"]/a/@href')
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
        article_data = tree_node.xpath('//div[@id="artibody"]')
        if article_data is not None and len(article_data) > 0:
            p_nodes = tree_node.xpath('//div[@id="artibody"]//p')
            t_nodes = tree_node.xpath('//div[@id="artibody"]//table')
            content = ''
            for node in p_nodes:
                content = content + node.xpath('string(.)').replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '') + '\n'
            for node in t_nodes:
                content = content + node.xpath('string(.)').replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '') + '\n'
            return content
    except:
        pass

    # 逻辑2
    try:
        article_data = tree_node.xpath('//div[@id="article"]')
        if article_data and article_data[0]:
            p_nodes = tree_node.xpath('//div[@id="article"]//p')
            t_nodes = tree_node.xpath('//div[@id="artibody"]//table')
            content = ''
            for node in p_nodes:
                content = content + node.xpath('string(.)').replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '') + '\n'
            for node in t_nodes:
                content = content + node.xpath('string(.)').replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '') + '\n'
            return content
    except:
        pass

    # 默认返回
    return None


# 解析文章
def parse_article(response):
    data = response.meta
    tree_node = etree.HTML(response.text,parser=etree.HTMLParser(encoding='utf-8'))
    try:
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
            data['original_source'] = original_source
            r.sadd('article:crawl:news:source', original_source)
        if original_url:
            data['original_url'] = original_url

        # 正文内容
        content = parse_article_content(tree_node)
        if content:
            data['content'] = content

        # 正文关键字
        keywords = parse_article_keywords(tree_node)
        if keywords:
            data['keywords'] = keywords

        data['crawl_time'] = str(int(time.time()))

        yield article_util.build_article_item(data)

    except:
        traceback.print_exc()






