#!/usr/bin/env python
# encoding: utf-8
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
from scrapy_redis.spiders import RedisSpider
import sys
import os
sys.path.append(os.getcwd())
from taodata.settings import LOCAL_REDIS_HOST, LOCAL_REDIS_PORT, LOCAL_REDIS_PASSWORD
import redis

from twisted.internet.error import TimeoutError, TCPTimedOutError, ConnectionRefusedError
from twisted.web._newclient import ResponseFailed, ResponseNeverReceived
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.utils.response import response_status_message  # 获取错误代码信息
import importlib
import hashlib
from taodata.spiders.article import article_util
import scrapy.item


class NewsSpider(RedisSpider):
    r = redis.Redis(host=LOCAL_REDIS_HOST, port=LOCAL_REDIS_PORT, password=LOCAL_REDIS_PASSWORD)
    name = "article:crawl:news"
    redis_key = "article:crawl:news:start_urls"

    custom_settings = {
        'CONCURRENT_REQUESTS': 4,
        "DOWNLOAD_DELAY": 0.2,
        'DOWNLOAD_TIMEOUT': 30,
        "SCHEDULER": "scrapy_redis.scheduler.Scheduler",
        "DUPEFILTER_CLASS": "scrapy_redis.dupefilter.RFPDupeFilter",
        "SCHEDULER_PERSIST": True,
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        },
        'HTTPERROR_ALLOWED_CODES': [403],
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
            'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware':None,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
           # 'taodata.middlewares.RetryMiddleware': 550,
           # 'taodata.middlewares.CookieMiddleware': 300,
            #'taodata.middlewares.RedirectMiddleware': 200,
            # 'taodata.middlewares.IPPoolMiddleware': 125,
            #'taodata.middlewares.ProxyMiddleware': 125,
            'taodata.middlewares.NoProxyMiddleware': 125,
        },
        'ITEM_PIPELINES': {
            #'taodata.spiders.article.pipelines.ArticleApiPipeline': 998,
            'taodata.spiders.article.pipelines.ArticleMongoDBPipeline': 999
        },
        'RETRY_TIMES': 50,
        'RETRY_ENABLED': True
    }

    # 默认初始解析函数
    def parse(self, response):
        page_url = response.url

        data = article_util.get_page_setting(page_url)

        # 判断页面配置是否为空
        if not data:
            return None
        print(data['page_module'], data['page_package'],data['page_function'])
        # 动态加载文件
        lib = importlib.import_module('.'+data['page_module'], data['page_package'])

        # 动态执行文件结果
        for item in eval('lib.%s(response)' % data['page_function']):
            # 返回 Request
            if isinstance(item, Request):
                request = item
                data = request.meta
                url = data['link_url']
                main_url = data['page_url']
                dupe_key = main_url + ':' + url
                dupe_key = hashlib.md5(dupe_key.encode('utf-8')).hexdigest()
                # 检查是否已采集
                if self.r.sismember('article:crawl:news:urls', dupe_key) or self.r.sismember('article:crawl:news:error_page', url):
                    print('已采集-->'+url)
                    continue
                # 设为已采集
                request.meta['dupe_key'] = dupe_key
                self.r.sadd('article:crawl:news:urls', dupe_key)
                # 设置request
                request.callback = self.parse_article
                request.errback = self.errback
                yield request

    def parse_article(self, response):
        data = response.meta
        lib = importlib.import_module('.'+data['page_module'], data['page_package'])
        for item in eval('lib.%s(response)' % data['page_function']):
            if isinstance(item, scrapy.Item):
                yield item

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

        self.r.sadd('cues:crawl:errback', request.url)


if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl(NewsSpider)
    process.start()
