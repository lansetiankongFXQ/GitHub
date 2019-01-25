#!/usr/bin/env python
# encoding: utf-8
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
from scrapy_redis.spiders import RedisSpider
import sys
import os
sys.path.append(os.getcwd())
from taodata.spiders.wanfangdata.items import WanfangCategoryItem,WanfangExaminationItem
from taodata.settings import LOCAL_REDIS_HOST, LOCAL_REDIS_PORT, LOCAL_REDIS_PASSWORD
import redis
from urllib.parse import urlparse
import urllib

from twisted.internet.error import TimeoutError, TCPTimedOutError, ConnectionRefusedError
from twisted.web._newclient import ResponseFailed, ResponseNeverReceived
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.utils.response import response_status_message  # 获取错误代码信息
from lxml import etree


class WanFangSpider(RedisSpider):
    r = redis.Redis(host=LOCAL_REDIS_HOST, port=LOCAL_REDIS_PORT, password=LOCAL_REDIS_PASSWORD)
    name = "taodata:crawl:wanfang"
    redis_key = "taodata:crawl:wanfang:start_urls"

    custom_settings = {
        'CONCURRENT_REQUESTS': 8,
        "DOWNLOAD_DELAY": 0.5,
        'DOWNLOAD_TIMEOUT': 30,
        "SCHEDULER": "scrapy_redis.scheduler.Scheduler",
        "DUPEFILTER_CLASS": "scrapy_redis.dupefilter.RFPDupeFilter",
        "SCHEDULER_PERSIST": True,
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
            'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware':None,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
            'taodata.middlewares.RetryMiddleware': 550,
            'taodata.middlewares.CookieMiddleware': 300,
            'taodata.middlewares.RedirectMiddleware': 200,
            # 'taodata.middlewares.IPPoolMiddleware': 125,
            'taodata.middlewares.ProxyMiddleware': 125,
            # 'taodata.middlewares.NoProxyMiddleware': 125,
        },
        'ITEM_PIPELINES': {
            'taodata.spiders.wanfangdata.pipelines.WanfangMongoDBPipeline': 999
        },
        'RETRY_TIMES': 50,
        'RETRY_ENABLED': True
    }

    # 默认初始解析函数
    def parse(self, response):
        page_url = response.url
        tree_node = etree.HTML(response.text, parser=etree.HTMLParser(encoding='utf-8'))
        category_list = tree_node.xpath('//div[@class="res-bottom-left"]/div[contains(@class,"res-left-list")]')
        for category in category_list:
            # 目录名
            category_type = category.xpath('./div[contains(@class,"list-all all-title")]/b/text()')
            if category_type:
                links = category.xpath('./div[@class="lists"]/a')
                for link in links:
                    url = link.xpath('./@data-url')[0]
                    text = link.xpath('./text()')[0]
                    url = 'http://lczl.med.wanfangdata.com.cn/' + url
                    q_dict = urllib.parse.parse_qs(urlparse(url).query)
                    category_id = q_dict['categoryId'][0]
                    item = WanfangCategoryItem()
                    item['_id'] = category_id
                    item['category_id'] = category_id
                    item['category_name'] = text
                    item['category_type'] = category_type[0]
                    yield item
                    yield Request(url, callback=self.parse_sub_category, meta={'data': item}, dont_filter=True,priority=10, errback=self.errback)

    def parse_sub_category(self, response):
        data = response.meta['data']
        tree_node = etree.HTML(response.text, parser=etree.HTMLParser(encoding='utf-8'))
        links = tree_node.xpath('//li/a')
        for link in links:
            url = link.xpath('./@href')[0]
            text = link.xpath('./@title')[0]
            url = 'http://lczl.med.wanfangdata.com.cn/' + url
            q_dict = urllib.parse.parse_qs(urlparse(url).query)
            id = q_dict['Id'][0]

            item = WanfangExaminationItem()
            item['_id'] = id
            item['name'] = text
            item['category_id'] = data['category_id']
            item['category_name'] = data['category_name']
            item['category_type'] = data['category_type']

            yield Request(url, callback=self.parse_detail, meta={'data': item}, dont_filter=True, priority=10,
                          errback=self.errback)

    def parse_detail(self,response):
        data = response.meta['data']
        tree_node = etree.HTML(response.text, parser=etree.HTMLParser(encoding='utf-8'))
        item_desc = tree_node.xpath('string(//div[@class="message-boxs"])')
        if item_desc:
            data['description'] = item_desc.replace('\r', '').replace('\u3000', '').replace('\t','').replace('\n', '').strip()

        list = tree_node.xpath('//div[@class="list-label clear"]')
        for temp in list:
            title = temp.xpath('./span/text()')
            name = temp.xpath('string(./div/span)')
            if title:
                title = title[0].strip()
                if name:
                    name = name.strip()
                if title.find('标准名称') != -1 and name:
                    data['name'] = name
                if title.find('别名') != -1 and name:
                    data['alias_name'] = name
                if title.find('英文名称') != -1 and name:
                    data['en_name'] = name
                if title.find('缩写名') != -1 and name:
                    data['ab_name'] = name
        yield data

    def errback(self, failure):
        request = failure.request

        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error(
                'errback <%s> %s , response status:%s' %
                (request.url, failure.value, response_status_message(response.status))
            )
        elif failure.check(ResponseFailed):
            self.logger.error('errback <%s> ResponseFailed' % request.url)

        elif failure.check(ConnectionRefusedError):
            self.logger.error('errback <%s> ConnectionRefusedError' % request.url)

        elif failure.check(ResponseNeverReceived):
            self.logger.error('errback <%s> ResponseNeverReceived' % request.url)

        elif failure.check(TCPTimedOutError, TimeoutError):
            self.logger.error('errback <%s> TimeoutError' % request.url)

        else:
            self.logger.error('errback <%s> OtherError' % request.url)

        self.r.sadd('taodata:crawl:errback', request.url)


if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl(WanFangSpider)
    process.start()
