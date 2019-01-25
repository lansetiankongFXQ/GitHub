#!/usr/bin/env python
# encoding: utf-8
import json
import requests


# 关注关键词
def start_weibo_monitor_keywords():
    url = 'http://localhost:9090/weibo/monitorKeywordsWeibo'
    request_data = {
        'weibo_keywords': '孟晚舟',
        'system_user': '1'
    }
    headers = {'content-type': 'application/json'}
    print(json.dumps(request_data))
    r = requests.post(url, data=json.dumps(request_data), headers=headers)
    print(r.json())


# 关注用户
def start_monitor_user_weibo():
    url = 'http://localhost:9090/weibo/monitorUserWeibo'
    request_data = {
        'weibo_user': '1298535315',
        'system_user': '1'
    }
    headers = {'content-type': 'application/json'}
    print(json.dumps(request_data))
    r = requests.post(url, data=json.dumps(request_data), headers=headers)
    print(r.json())


# 搜索微博用户
def start_weibo_search_user():
    url = 'http://localhost:9090/weibo/searchUser'
    request_data = {
        'q': '占豪'
    }
    headers = {'content-type': 'application/json'}
    print(json.dumps(request_data))
    r = requests.post(url, data=json.dumps(request_data), headers=headers)
    print(r.json())


# 搜索微博
def start_weibo_search_keywords():
    url = 'http://localhost:9090/weibo/searchUser'
    request_data = {
        'q': '占',
        'user_id': '1'
    }
    headers = {'content-type': 'application/json'}
    print(json.dumps(request_data))
    r = requests.post(url, data=json.dumps(request_data), headers=headers)
    print(r.json())


# 人民网
def start_people():
    url = 'http://192.168.0.8:8080/quartz/startTask'
    job_data = {}
    pages = []
    page_roll = {}
    page_roll['id'] = "20"
    page_roll['page_url'] = 'http://news.people.com.cn/210801/211150/index.js'
    page_roll['page_function'] = 'parse_roll'
    page_roll['page_module'] = 'cn_com_people_news'
    page_roll['page_package'] = 'taodata.spiders.article'
    page_roll['page_name'] = '滚动'
    page_roll['app_id'] = "2"
    page_roll['app_code'] = 'news.people.com.cn'
    page_roll['app_name'] = '人民网'
    page_roll['app_type'] = '新闻网站'
    page_roll['app_region'] = '中国'
    pages.append(page_roll)

    job_data['data'] = pages

    job_data_str = json.dumps(job_data)

    request_data = {
        'job_no': '20181203002',
        'job_name': '20181203002',
        'job_group': 'article',
        'job_description': '20181203002',
        'job_class': 'cn.taodata.datacenter.quartz.ArticleTask',
        'cron_expression': '0 0/1 * * * ?',
        'job_data': job_data_str
    }
    headers = {'content-type': 'application/json'}
    print(json.dumps(request_data))
    r = requests.post(url, data=json.dumps(request_data),headers=headers)
    print(r.json())


# 新浪
def start_sina():
    url = 'http://192.168.0.8:8080/quartz/startTask'
    job_data = {}
    pages = []
    page_roll_china = {}
    page_roll_china['id'] = "1"
    page_roll_china['page_url'] = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2510&k=&num=50&page=1'
    page_roll_china['page_function'] = 'parse_roll'
    page_roll_china['page_module'] = 'cn_com_sina_news'
    page_roll_china['page_package'] = 'taodata.spiders.article'
    page_roll_china['page_name'] = '国内'
    page_roll_china['app_id'] = "1"
    page_roll_china['app_code'] = 'news.sina.com.cn'
    page_roll_china['app_name'] = '新浪'
    page_roll_china['app_type'] = '新闻网站'
    page_roll_china['app_region'] = '中国'
    pages.append(page_roll_china)

    page_roll_word = {}
    page_roll_word['id'] = "2"
    page_roll_word['page_url'] = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2511&k=&num=50&page=1'
    page_roll_word['page_function'] = 'parse_roll'
    page_roll_word['page_module'] = 'cn_com_sina_news'
    page_roll_word['page_package'] = 'taodata.spiders.article'
    page_roll_word['page_name'] = '国际'
    page_roll_word['app_id'] = "1"
    page_roll_word['app_code'] = 'news.sina.com.cn'
    page_roll_word['app_name'] = '新浪'
    page_roll_word['app_type'] = '新闻网站'
    page_roll_word['app_region'] = '中国'
    pages.append(page_roll_word)

    page_roll_society = {}
    page_roll_society['id'] = "3"
    page_roll_society['page_url'] = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2669&k=&num=50&page=1'
    page_roll_society['page_function'] = 'parse_roll'
    page_roll_society['page_module'] = 'cn_com_sina_news'
    page_roll_society['page_package'] = 'taodata.spiders.article'
    page_roll_society['page_name'] = '社会'
    page_roll_society['app_id'] = "1"
    page_roll_society['app_code'] = 'news.sina.com.cn'
    page_roll_society['app_name'] = '新浪'
    page_roll_society['app_type'] = '新闻网站'
    page_roll_society['app_region'] = '中国'
    pages.append(page_roll_society)

    page_roll_sports = {}
    page_roll_sports['id'] = "4"
    page_roll_sports['page_url'] = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2512&k=&num=50&page=1'
    page_roll_sports['page_function'] = 'parse_roll'
    page_roll_sports['page_module'] = 'cn_com_sina_news'
    page_roll_sports['page_package'] = 'taodata.spiders.article'
    page_roll_sports['page_name'] = '体育'
    page_roll_sports['app_id'] = "1"
    page_roll_sports['app_code'] = 'news.sina.com.cn'
    page_roll_sports['app_name'] = '新浪'
    page_roll_sports['app_type'] = '新闻网站'
    page_roll_sports['app_region'] = '中国'
    pages.append(page_roll_sports)

    page_roll_ent = {}
    page_roll_ent['id'] = "5"
    page_roll_ent['page_url'] = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2513&k=&num=50&page=1'
    page_roll_ent['page_function'] = 'parse_roll'
    page_roll_ent['page_module'] = 'cn_com_sina_news'
    page_roll_ent['page_package'] = 'taodata.spiders.article'
    page_roll_ent['page_name'] = '娱乐'
    page_roll_ent['app_id'] = "1"
    page_roll_ent['app_code'] = 'news.sina.com.cn'
    page_roll_ent['app_name'] = '新浪'
    page_roll_ent['app_type'] = '新闻网站'
    page_roll_ent['app_region'] = '中国'
    pages.append(page_roll_ent)

    page_roll_mil = {}
    page_roll_mil['id'] = "6"
    page_roll_mil['page_url'] = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2514&k=&num=50&page=1'
    page_roll_mil['page_function'] = 'parse_roll'
    page_roll_mil['page_module'] = 'cn_com_sina_news'
    page_roll_mil['page_package'] = 'taodata.spiders.article'
    page_roll_mil['page_name'] = '军事'
    page_roll_mil['app_id'] = "1"
    page_roll_mil['app_code'] = 'news.sina.com.cn'
    page_roll_mil['app_name'] = '新浪'
    page_roll_mil['app_type'] = '新闻网站'
    page_roll_mil['app_region'] = '中国'
    pages.append(page_roll_mil)

    page_roll_tech = {}
    page_roll_tech['id'] = "7"
    page_roll_tech['page_url'] = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2515&k=&num=50&page=1'
    page_roll_tech['page_function'] = 'parse_roll'
    page_roll_tech['page_module'] = 'cn_com_sina_news'
    page_roll_tech['page_package'] = 'taodata.spiders.article'
    page_roll_tech['page_name'] = '科技'
    page_roll_tech['app_id'] = "1"
    page_roll_tech['app_code'] = 'news.sina.com.cn'
    page_roll_tech['app_name'] = '新浪'
    page_roll_tech['app_type'] = '新闻网站'
    page_roll_tech['app_region'] = '中国'
    pages.append(page_roll_tech)

    page_roll_finance = {}
    page_roll_finance['id'] = "8"
    page_roll_finance['page_url'] = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2516&k=&num=50&page=1'
    page_roll_finance['page_function'] = 'parse_roll'
    page_roll_finance['page_module'] = 'cn_com_sina_news'
    page_roll_finance['page_package'] = 'taodata.spiders.article'
    page_roll_finance['page_name'] = '财经'
    page_roll_finance['app_id'] = "1"
    page_roll_finance['app_code'] = 'news.sina.com.cn'
    page_roll_finance['app_name'] = '新浪'
    page_roll_finance['app_type'] = '新闻网站'
    page_roll_finance['app_region'] = '中国'
    pages.append(page_roll_finance)

    page_roll_stock = {}
    page_roll_stock['id'] = "9"
    page_roll_stock['page_url'] = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2517&k=&num=50&page=1'
    page_roll_stock['page_function'] = 'parse_roll'
    page_roll_stock['page_module'] = 'cn_com_sina_news'
    page_roll_stock['page_package'] = 'taodata.spiders.article'
    page_roll_stock['page_name'] = '股市'
    page_roll_stock['app_id'] = "1"
    page_roll_stock['app_code'] = 'news.sina.com.cn'
    page_roll_stock['app_name'] = '新浪'
    page_roll_stock['app_type'] = '新闻网站'
    page_roll_stock['app_region'] = '中国'
    pages.append(page_roll_stock)

    page_roll_usstock = {}
    page_roll_usstock['id'] = "10"
    page_roll_usstock['page_url'] = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2518&k=&num=50&page=1'
    page_roll_usstock['page_function'] = 'parse_roll'
    page_roll_usstock['page_module'] = 'cn_com_sina_news'
    page_roll_usstock['page_package'] = 'taodata.spiders.article'
    page_roll_usstock['page_name'] = '美股'
    page_roll_usstock['app_id'] = "1"
    page_roll_usstock['app_code'] = 'news.sina.com.cn'
    page_roll_usstock['app_name'] = '新浪'
    page_roll_usstock['app_type'] = '新闻网站'
    page_roll_usstock['app_region'] = '中国'
    pages.append(page_roll_usstock)


    job_data['data'] = pages

    job_data_str = json.dumps(job_data)

    request_data = {
        'job_no': '20181203001',
        'job_name': '20181203001',
        'job_group': 'article',
        'job_description': '20181203001',
        'job_class': 'cn.taodata.datacenter.quartz.ArticleTask',
        'cron_expression': '0 0/1 * * * ?',
        'job_data': job_data_str
    }
    headers = {'content-type': 'application/json'}
    print(json.dumps(request_data))
    r = requests.post(url, data=json.dumps(request_data), headers=headers)
    print(r.json())


# 关注关键词
def test_api1():
    url = 'http://10.86.11.153:10200/test'
    request_data = {
        'weibo_keywords': '孟晚舟',
        'system_user': '1'
    }
    headers = {'content-type': 'application/json'}
    print(json.dumps(request_data))
    r = requests.post(url, data=json.dumps(request_data), headers=headers)
    print(r.json())


if __name__ == '__main__':
    test_api1()
    #start_weibo_monitor_keywords()
    #start_monitor_user_weibo()
    #start_unmonitor_user_weibo()
    #start_weibo_search_user()
    # start_people()
    # start_sina()
    #test_api_news()


