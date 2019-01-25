# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class ArticleNewsItem(scrapy.Item):
    _id = Field()    # 标识
    title = Field()  # 标题
    content = Field()  # 内容
    original_source = Field()  # 原来源
    original_url = Field()  # 原链接
    keywords = Field()  # 关键字
    url = Field()  # 链接
    publish_time_str = Field()  # 发布时间
    publish_time = Field()  # 发布时间
    crawl_time = Field()  # 采集时间
    page_id = Field()
    page_name = Field()  # 分类
    page_subject = Field()  # 专题
    app_id = Field()
    app_code = Field()  # 网站编码
    app_name = Field()  # 网站名
    app_type = Field()  # 网站类型
    app_region = Field()  # 网站区域
    job_no = Field()  # 采集编号
    job_seq = Field()  # 采集序号
    dupe_key = Field()
    interval_time = Field()
