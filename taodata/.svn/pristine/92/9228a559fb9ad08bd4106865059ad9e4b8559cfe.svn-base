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
    if 'items' in json1:
        # 新闻列表
        items = json1['items']
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


# 解析发布时间
def parse_article_publish_time(tree_node):
    # 逻辑1
    try:
        publish_time = tree_node.xpath('//div[@class="box01"]/div[@class="fl"]/text()')
        if publish_time and publish_time[0]:
            time_obj = datetime.datetime.strptime(publish_time[0].replace('：', '').replace('来源', '').replace('&nbsp;', '').strip(), '%Y年%m月%d日%H:%M')
            time1 = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            time2 = str(int(time.mktime(time_obj.timetuple())))
            return time1, time2
    except:
        pass

    try:
        publish_time = tree_node.xpath('//div[@class="p2j_text fl"]/h2/text()')
        if publish_time and publish_time[0]:
            time_obj = datetime.datetime.strptime(publish_time[0].replace('：', '').replace('来源', '').replace('&nbsp;', '').strip(), '%Y年%m月%d日%H:%M')
            time1 = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            time2 = str(int(time.mktime(time_obj.timetuple())))
            return time1, time2
    except:
        pass

    try:
        publish_time = tree_node.xpath('//div[@class="text_c"]/p[@class="sou"]/text()')
        if publish_time and publish_time[0]:
            time_obj = datetime.datetime.strptime(publish_time[0].replace('：', '').replace('来源', '').replace('&nbsp;', '').strip(), '%Y年%m月%d日%H:%M')
            time1 = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            time2 = str(int(time.mktime(time_obj.timetuple())))
            return time1, time2
    except:
        pass

    try:
        publish_time = tree_node.xpath('//div[@class="text width978 clearfix"]/h2/text()')
        if publish_time and publish_time[0]:
            time_obj = datetime.datetime.strptime(publish_time[0].replace('：', '').replace('来源', '').replace('&nbsp;', '').strip(), '%Y年%m月%d日%H:%M')
            time1 = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            time2 = str(int(time.mktime(time_obj.timetuple())))
            return time1, time2
    except:
        pass

    try:
        publish_time = tree_node.xpath('//div[@class="articleCont"]/div[@class="artOri"]/text()')
        if publish_time and publish_time[0]:
            time_obj = datetime.datetime.strptime(publish_time[0].replace('：', '').replace('来源', '').replace('&nbsp;', '').strip(), '%Y年%m月%d日%H:%M')
            time1 = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            time2 = str(int(time.mktime(time_obj.timetuple())))
            return time1, time2
    except:
        pass

    try:
        publish_time = tree_node.xpath('//div[@class="w1000 clearfix tit-ld"]/p/text()')
        if publish_time and publish_time[0]:
            time_obj = datetime.datetime.strptime(publish_time[0].replace('：', '').replace('来源', '').replace('&nbsp;', '').strip(), '%Y年%m月%d日%H:%M')
            time1 = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            time2 = str(int(time.mktime(time_obj.timetuple())))
            return time1, time2
    except:
        pass

    try:
        publish_time = tree_node.xpath('//div[@class="text w1000 clearfix"]/h2/text()')
        if publish_time and publish_time[0]:
            time_obj = datetime.datetime.strptime(publish_time[0].replace('：', '').replace('来源', '').replace('&nbsp;', '').strip(), '%Y年%m月%d日%H:%M')
            time1 = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            time2 = str(int(time.mktime(time_obj.timetuple())))
            return time1, time2
    except:
        pass

    try:
        publish_time = tree_node.xpath('//div[@class="fl"]/div[@class="tool"]h5/text()')
        if publish_time and publish_time[0]:
            time_obj = datetime.datetime.strptime(publish_time[0].replace('：', '').replace('来源', '').replace('&nbsp;', '').strip(), '%Y年%m月%d日%H:%M')
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
        title = tree_node.xpath('//div[@class="clearfix w1000_320 text_title"]/h1/text()')
        if title and title[0]:
            return title[0]
    except:
        pass

    try:
        title = tree_node.xpath('//div[@class="p2j_text fl"]/h1/text()')
        if title and title[0]:
            return title[0]
    except:
        pass

    try:
        title = tree_node.xpath('//div[@class="title"]/h1/text()')
        if title and title[0]:
            return title[0]
    except:
        pass

    try:
        title = tree_node.xpath('//div[@id="jtitle"]/h3/text()')
        if title and title[0]:
            return title[0]
    except:
        pass

    try:
        title = tree_node.xpath('//div[@class="text_c"]/h1/text()')
        if title and title[0]:
            return title[0]
    except:
        pass

    try:
        title = tree_node.xpath('//div[@class="text width978 clearfix"]/h1/text()')
        if title and title[0]:
            return title[0]
    except:
        pass

    try:
        title = tree_node.xpath('//div[@class="articleCont"]/div[@class="title"]')
        if title and title[0]:
            return title[0].xpath("string(.)")
    except:
        pass

    try:
        title = tree_node.xpath('//div[@class="w1000 clearfix tit-ld"]/h2/text()')
        if title and title[0]:
            return title[0]
    except:
        pass

    try:
        title = tree_node.xpath('//div[@class="text w1000 clearfix"]/h1/text()')
        if title and title[0]:
            return title[0]
    except:
        pass

    try:
        title = tree_node.xpath('//div[@class="tit1 fl"]/h2/text()')
        if title and title[0]:
            return title[0]
    except:
        pass

    try:
        title = tree_node.xpath('//div[@class="fl"]/h1/text()')
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
        original_source = tree_node.xpath('//div[@class="box01"]/div[@class="fl"]/a/text()')
        if original_source and original_source[0]:
            return original_source[0]
    except:
        pass

    try:
        original_source = tree_node.xpath('//div[@class="p2j_text fl"]/h2/a/text()')
        if original_source and original_source[0]:
            return original_source[0]
    except:
        pass

    try:
        original_source = tree_node.xpath('//div[@class="text_c"]/p[@class="sou"]/a/text()')
        if original_source and original_source[0]:
            return original_source[0]
    except:
        pass

    try:
        original_source = tree_node.xpath('//div[@class="text width978 clearfix"]/h2/a/text()')
        if original_source and original_source[0]:
            return original_source[0]
    except:
        pass

    try:
        original_source = tree_node.xpath('//div[@class="articleCont"]/div[@class="artOri"]/a/text()')
        if original_source and original_source[0]:
            return original_source[0]
    except:
        pass

    try:
        original_source = tree_node.xpath('//div[@class="w1000 clearfix tit-ld"]/p/a/text()')
        if original_source and original_source[0]:
            return original_source[0]
    except:
        pass

    try:
        original_source = tree_node.xpath('//div[@class="text w1000 clearfix"]/h2/a/text()')
        if original_source and original_source[0]:
            return original_source[0]
    except:
        pass

    try:
        original_source = tree_node.xpath('//div[@class="fl"]/div[@class="tool"]/h5/a/text()')
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
        original_url = tree_node.xpath('//div[@class="box01"]/div[@class="fl"]/a/@href')
        if original_url and original_url[0]:
            return original_url[0]
    except:
        pass

    try:
        original_url = tree_node.xpath('//div[@class="p2j_text fl"]/h2/a/@href')
        if original_url and original_url[0]:
            return original_url[0]
    except:
        pass

    try:
        original_url = tree_node.xpath('//div[@class="text_c"]/p[@class="sou"]/a/@href')
        if original_url and original_url[0]:
            return original_url[0]
    except:
        pass

    try:
        original_url = tree_node.xpath('//div[@class="text width978 clearfix"]/h2/a/@href')
        if original_url and original_url[0]:
            return original_url[0]
    except:
        pass

    try:
        original_url = tree_node.xpath('//div[@class="articleCont"]/div[@class="artOri"]/a/@href')
        if original_url and original_url[0]:
            return original_url[0]
    except:
        pass

    try:
        original_url = tree_node.xpath('//div[@class="w1000 clearfix tit-ld"]/p/a/@href')
        if original_url and original_url[0]:
            return original_url[0]
    except:
        pass

    try:
        original_url = tree_node.xpath('//div[@class="text w1000 clearfix"]/h2/a/@href')
        if original_url and original_url[0]:
            return original_url[0]
    except:
        pass

    try:
        original_url = tree_node.xpath('//div[@class="fl"]/div[@class="tool"]/h5/a/@href')
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
        article_data = tree_node.xpath('//div[@id="rwb_zw"]')
        if article_data and article_data[0]:
            p_nodes = tree_node.xpath('//div[@id="rwb_zw"]//p')
            t_nodes = tree_node.xpath('//div[@id="rwb_zw"]//table')
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
        article_data = tree_node.xpath('//div[@class="p2j_text fl"]/div[@class="gray box_text"]')
        if article_data and article_data[0]:
            p_nodes = tree_node.xpath('//div[@class="p2j_text fl"]/div[@class="gray box_text"]//p')
            t_nodes = tree_node.xpath('//div[@class="p2j_text fl"]/div[@class="gray box_text"]//table')
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
        article_data = tree_node.xpath('//div[@class="content clear clearfix"]')
        if article_data and article_data[0]:
            p_nodes = tree_node.xpath('//div[@class="content clear clearfix"]//p')
            t_nodes = tree_node.xpath('//div[@class="content clear clearfix"]//table')
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
        article_data = tree_node.xpath('//div[@class="text width978 clearfix"]')
        if article_data and article_data[0]:
            p_nodes = tree_node.xpath('//div[@class="text width978 clearfix"]//p')
            t_nodes = tree_node.xpath('//div[@class="text width978 clearfix"]//table')
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
        article_data = tree_node.xpath('//div[@class="show_text"]')
        if article_data and article_data[0]:
            p_nodes = tree_node.xpath('//div[@class="show_text"]//p')
            t_nodes = tree_node.xpath('//div[@class="show_text"]//table')
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
        article_data = tree_node.xpath('//div[@class="articleCont"]/div[@class="artDet"]')
        if article_data and article_data[0]:
            p_nodes = tree_node.xpath('//div[@class="articleCont"]/div[@class="artDet"]//p')
            t_nodes = tree_node.xpath('//div[@class="articleCont"]/div[@class="artDet"]//table')
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
        article_data = tree_node.xpath('//div[@id="picG"]')
        if article_data and article_data[0]:
            p_nodes = tree_node.xpath('//div[@id="picG"]//p')
            t_nodes = tree_node.xpath('//div[@id="picG"]//table')
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


# 解析page_name
def parse_page_name(tree_node):
    try:
        page_name = tree_node.xpath('//span[@id="rwb_navpath"]/a[last()]/text()')
        if page_name and page_name[0]:
            return page_name[0]
    except:
        pass

    try:
        page_name = tree_node.xpath('//div[@class="p2j_text fl"]/h6/a[last()]/text()')
        if page_name and page_name[0]:
            return page_name[0]
    except:
        pass

    try:
        page_name = tree_node.xpath('//div[@class="fl"]/a[last()]/text()')
        if page_name and page_name[0]:
            return page_name[0]
    except:
        pass

    try:
        page_name = tree_node.xpath('//div[@class="subNav"]/a[last()]/text()')
        if page_name and page_name[0]:
            return page_name[0]
    except:
        pass

    try:
        page_name = tree_node.xpath('//div[@class="x_nav clear"]/a[last()]/text()')
        if page_name and page_name[0]:
            return page_name[0]
    except:
        pass

    try:
        page_name = tree_node.xpath('//div[@class="daohang"]/a[last()]/text()')
        if page_name and page_name[0]:
            return page_name[0]
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

        data['crawl_time'] = str(int(time.time()))

        yield article_util.build_article_item(data)

    except:
        traceback.print_exc()






