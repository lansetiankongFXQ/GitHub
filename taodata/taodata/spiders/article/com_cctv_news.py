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
    # 解析数据
    text1 = response.text
    try:
        json1 = json.loads(text1)
        datas =  json1['data']
    except:
        traceback.print_exc()
        r.sadd('article:crawl:news:error_page', page_url)
        return
    # 处理数据
    if data:
        # 采集新闻详情
        for item in datas:
            date = item['focus_date']
            url = item['url']
            data['link_text'] = item['title']
            data['link_url'] = item['url']
            data['page_function'] = 'parse_article'
            data['page_name'] = parse_page_name(page_url)
            data['title'] = item['title']
            data['original_source'] = item['source']
            data['publish_time_str'] = date
            data['publish_time'] = parse_time(date)
            request = Request(url, dont_filter=True, priority=10, meta=data)
            yield request
    else:
        r.sadd('article:crawl:news:error_page', response.url)

    article_util.remove_page_setting(page_url)


def parse_time(date):
    try:
        time_obj = datetime.datetime.strptime(date.strip(), '%Y年%m月%d日 %H:%M:%S')
        time2 = str(int(time.mktime(time_obj.timetuple())))
        return time2
    except:
        pass
    try:
        time_obj = datetime.datetime.strptime(date.strip(), '%Y年%m月%d日 %H:%M')
        time2 = str(int(time.mktime(time_obj.timetuple())))
        return time2
    except:
        pass
    try:
        time_obj = datetime.datetime.strptime(date.strip(), '%Y-%m-%d %H:%M')
        time2 = str(int(time.mktime(time_obj.timetuple())))
        return time2
    except:
        pass
    try:
        time_obj = datetime.datetime.strptime(date.strip(), '%Y-%m-%d %H:%M:%S')
        time2 = str(int(time.mktime(time_obj.timetuple())))
        return time2
    except:
        pass

    return time2


# 解析发布时间
def parse_article_publish_time(tree_node):
    # 央广网
    try:
        publish_time_node = tree_node.xpath('//div[@class="function"]/span[@class="info"]/i/text()')
        publish_time = publish_time_node[1].replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '')
        if publish_time:
            time_obj = datetime.datetime.strptime(publish_time.strip(), '%Y年%m月%d日 %H:%M')
            time1 = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            time2 = str(int(time.mktime(time_obj.timetuple())))
            return time1, time2
    except:
        pass

    try:
        publish_time_node = tree_node.xpath('//div[@class="function"]/span[@class="info"]/i/text()')
        publish_time = publish_time_node[0][-17:].replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '')
        if publish_time:
            time_obj = datetime.datetime.strptime(publish_time.strip(), '%Y年%m月%d日 %H:%M')
            time1 = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            time2 = str(int(time.mktime(time_obj.timetuple())))
            return time1, time2
    except:
        pass

    try:
        publish_time_node = tree_node.xpath('//div[@class="info"]/p/i/text()')
        publish_time = publish_time_node[1].replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '')
        if publish_time:
            time_obj = datetime.datetime.strptime(publish_time.strip(), '%Y年%m月%d日 %H:%M')
            time1 = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            time2 = str(int(time.mktime(time_obj.timetuple())))
            return time1, time2
    except:
        pass

    try:
        publish_time_node = tree_node.xpath('//div[@class="info"]/p/text()')
        publish_time = publish_time_node[1].replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '')
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
    # 央广网

    try:
        title = tree_node.xpath('//div[@class="col_w660"]/div[@class="cnt_bd"]/h1/text()')
        if title:
            return title[0].replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '')
    except:
        pass

    try:
        title = tree_node.xpath('//div[@class="tj_t_left"]/h3')
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
        original_source = tree_node.xpath('//div[@class="function"]/span[@class="info"]/i/a/text()')
        if original_source and original_source[0]:
            return original_source[0]
    except:
        pass

    try:
        original_source = tree_node.xpath('//div[@class="info"]/p/i/text()')
        if original_source and original_source[0]:
            return original_source[0]
    except:
        pass

    try:
        original_source = tree_node.xpath('//div[@class="function"]/span[@class="info"]/i/text()')
        if original_source and original_source[0]:
            return original_source[0][3:-18]
    except:
        pass
    # 默认返回
    return None


# 解析来源
def parse_article_original_url(tree_node):
    # 央广网

    try:
        original_source = tree_node.xpath('//div[@class="function"]/span[@class="info"]/i/a/@href')
        if original_source and original_source[0]:
            return original_source[0]
    except:
        pass

    # 默认返回
    return None


# 解析 正文
def parse_article_content(tree_node):
    # 央广网

    try:
        article_data = tree_node.xpath('//div[@class="cnt_bd"]')
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
def parse_page_name(url):
    # 央广网
    # 国内
    if url.find('guonei') > -1:
        page_name = '国内'
        return page_name
    # 国际
    if url.find('guoji') > -1:
        page_name = '国际'
        return page_name
    # 娱乐
    if url.find('yule') > -1:
        page_name = '娱乐'
        return page_name
    # 军事
    if url.find('junshi') > -1:
        page_name = '军事'
        return page_name
    # 科技
    if url.find('keji') > -1:
        page_name = '科技'
        return page_name
    # 财经
    if url.find('shehui') > -1:
        page_name = '社会'
        return page_name
    return None


# 解析文章
def parse_article(response):
    data = response.meta
    tree_node = etree.HTML(response.text,parser=etree.HTMLParser(encoding='utf-8'))
    try:
        # 新闻专题
        # page_name = parse_page_name(tree_node)
        # if page_name:
        #     data['page_subject'] = page_name
        # 主标题
        # title = parse_article_title(tree_node)
        # if title:
        #     data['title'] = title

        # 发布时间
        # publish_time_str, publish_time = parse_article_publish_time(tree_node)
        # if publish_time_str:
        #     data['publish_time_str'] = publish_time_str
        # if publish_time:
        #     data['publish_time'] = publish_time

        # 来源
        # original_source = parse_article_original_source(tree_node)
        # if original_source:
        #     data['original_source'] = original_source.strip()
        #     r.sadd('article:crawl:news:source', original_source.strip())
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






