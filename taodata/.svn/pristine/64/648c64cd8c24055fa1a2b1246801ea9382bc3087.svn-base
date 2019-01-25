# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class TaodataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class WeiboUserItem(Item):
    pass


class TweetsItem(Item):
    """ 微博信息 """
    _id = Field()  # 微博id
    weibo_url = Field()  # 微博URL
    created_at = Field()  # 微博发表时间
    like_num = Field()  # 点赞数
    repost_num = Field()  # 转发数
    comment_num = Field()  # 评论数
    content = Field()  # 微博内容
    user_id = Field()  # 发表该微博用户的id
    crawl_time = Field()  # 抓取时间戳


class InformationItem(Item):
    """ 个人信息 """
    _id = Field()  # 用户ID
    nick_name = Field()  # 昵称
    gender = Field()  # 性别
    province = Field()  # 所在省
    city = Field()  # 所在城市
    brief_introduction = Field()  # 简介
    birthday = Field()  # 生日
    tweets_num = Field()  # 微博数
    follows_num = Field()  # 关注数
    fans_num = Field()  # 粉丝数
    sex_orientation = Field()  # 性取向
    sentiment = Field()  # 感情状况
    vip_level = Field()  # 会员等级
    authentication = Field()  # 认证
    person_url = Field()  # 首页链接
    crawl_time = Field()  # 抓取时间戳


class RelationshipsItem(Item):
    """ 用户关系，只保留与关注的关系 """
    _id = Field()
    fan_id = Field()  # 关注者,即粉丝的id
    followed_id = Field()  # 被关注者的id
    crawl_time = Field()  # 抓取时间戳


class CommentItem(Item):
    """
    微博评论信息
    """
    _id = Field()
    comment_user_id = Field()  # 评论用户的id
    content = Field()  # 评论的内容
    weibo_url = Field()  # 评论的微博的url
    created_at = Field()  # 评论发表时间
    crawl_time = Field()  # 抓取时间戳


class WeiboCommentItem(Item):
    """
    微博评论信息
    """
    _id = Field()
    comment_user_id = Field()  # 评论用户的id
    comment_user_nick_name = Field()  # 评论用户昵称
    comment_user_post_num = Field()  # 评论用户微博数
    comment_user_follows_num = Field()  # 评论用户关注数
    comment_user_fans_num = Field()  # 评论用户粉丝数
    comment_user_rank = Field()  # 评论用户等级
    content = Field()  # 评论的内容
    weibo_url = Field()  # 评论的微博的url
    like_num = Field()  # 点赞数
    created_at = Field()  # 评论发表时间
    created_source = Field()  # 评论来源
    crawl_time = Field()  # 抓取时间戳


class WeiboAttitudeItem(Item):
    """
    微博点赞信息
    """
    _id = Field()
    attitude_user_id = Field()  # 点赞用户的id
    attitude_user_nick_name = Field()  # 点赞用户昵称
    attitude_user_post_num = Field()  # 点赞用户微博数
    attitude_user_follows_num = Field()  # 点赞用户关注数
    attitude_user_fans_num = Field()  # 点赞用户粉丝数
    attitude_user_rank = Field()  # 点赞用户等级
    weibo_url = Field()  # 点赞的微博的url
    created_at = Field()  # 点赞发表时间
    crawl_time = Field()  # 抓取时间戳


class WeiboRepostItem(Item):
    """
    微博转发信息
    """
    _id = Field()
    repost_user_id = Field()  # 转发用户的id
    repost_user_nick_name = Field()  # 转发用户昵称
    repost_user_post_num = Field()  # 转发用户微博数
    repost_user_follows_num = Field()  # 转发用户关注数
    repost_user_fans_num = Field()  # 转发用户粉丝数
    repost_user_rank = Field()  # 转发用户等级
    content = Field()  # 转发的内容
    weibo_url = Field()  # 转发的微博的url
    like_num = Field()  # 点赞数
    created_at = Field()  # 转发发表时间
    created_source = Field()  # 转发来源
    crawl_time = Field()  # 抓取时间戳


class WeiboRealtimeItem(Item):
    """ 微博信息 """
    _id = Field()  # ID
    weibo_id = Field()  # 微博ID
    bid = Field() # 微博ID
    weibo_url = Field()  # 微博URL
    weibo_type = Field()  # 微博类型
    created_at = Field()  # 微博发表时间
    created_source = Field()  # 微博来源
    like_num = Field()  # 点赞数
    repost_num = Field()  # 转发数
    comment_num = Field()  # 评论数
    content = Field()  # 微博内容
    user_id = Field()  # 发表该微博用户的id
    user_nick_name = Field()  # 微博用户昵称
    user_post_num = Field()  # 微博用户微博数
    user_follows_num = Field()  # 微博用户关注数
    user_fans_num = Field()  # 微博用户粉丝数
    user_rank = Field()  # 微博用户等级
    original_weibo_id = Field()  # 原创微博ID
    original_bid = Field()  # 原创微博ID
    original_weibo_url =Field()  # 原创微博URL
    original_created_at = Field()  # 原创微博发表时间
    original_created_source = Field()  # 原创微博来源
    original_user_id = Field()  # 原创微博用户的id
    original_user_nick_name = Field()  # 原创微博用户昵称
    original_user_post_num = Field()  # 原创微博用户微博数
    original_user_follows_num = Field()  # 原创微博用户关注数
    original_user_fans_num = Field()  # 原创微博用户粉丝数
    original_user_rank = Field()  # 原创微博用户等级
    original_content = Field()  # 原创微博内容
    original_like_num = Field()  # 原创微博点赞数
    original_repost_num = Field()  # 原创微博转发数
    original_comment_num = Field()  # 原创微博评论数
    crawl_time = Field()  # 抓取时间戳
    req_id = Field()  # 请求ID
    resp_time = Field()  # 响应时间

class WeiboItem(Item):
    """ 微博信息 """
    _id = Field()  # ID
    weibo_id = Field()  # 微博ID
    bid = Field() # 微博ID
    weibo_url = Field()  # 微博URL
    weibo_type = Field()  # 微博类型
    created_at = Field()  # 微博发表时间
    created_source = Field()  # 微博来源
    like_num = Field()  # 点赞数
    repost_num = Field()  # 转发数
    comment_num = Field()  # 评论数
    content = Field()  # 微博内容
    user_id = Field()  # 发表该微博用户的id
    user_nick_name = Field()  # 微博用户昵称
    user_post_num = Field()  # 微博用户微博数
    user_follows_num = Field()  # 微博用户关注数
    user_fans_num = Field()  # 微博用户粉丝数
    user_rank = Field()  # 微博用户等级
    original_weibo_id = Field()  # 原创微博ID
    original_bid = Field()  # 原创微博ID
    original_weibo_url =Field()  # 原创微博URL
    original_created_at = Field()  # 原创微博发表时间
    original_created_source = Field()  # 原创微博来源
    original_user_id = Field()  # 原创微博用户的id
    original_user_nick_name = Field()  # 原创微博用户昵称
    original_user_post_num = Field()  # 原创微博用户微博数
    original_user_follows_num = Field()  # 原创微博用户关注数
    original_user_fans_num = Field()  # 原创微博用户粉丝数
    original_user_rank = Field()  # 原创微博用户等级
    original_content = Field()  # 原创微博内容
    original_like_num = Field()  # 原创微博点赞数
    original_repost_num = Field()  # 原创微博转发数
    original_comment_num = Field()  # 原创微博评论数
    crawl_time = Field()  # 抓取时间戳
    req_id = Field()  # 请求ID
    resp_time = Field()  # 响应时间


class WeiboRelationshipsItem(Item):
    """ 微博用户关系，只保留与关注的关系 """
    _id = Field()  # ID
    fans_id = Field()  # 关注者,即粉丝的id
    followed_id = Field()  # 被关注者的id
    crawl_time = Field()  # 抓取时间戳
    req_id = Field()  # 请求ID
    resp_time = Field()  # 响应时间


class WeiboUserItem(Item):
    """ 微博个人信息 """
    _id = Field()  # ID
    user_id = Field()  # 用户ID
    nick_name = Field()  # 昵称
    gender = Field()  # 性别
    location = Field()  # 地区
    description = Field()  # 简介
    birthday = Field()  # 生日
    post_num = Field()  # 微博数
    follows_num = Field()  # 关注数
    fans_num = Field()  # 粉丝数
    friend_num = Field()  # 相互关注数
    like_num = Field()  # 被点赞数
    member_type = Field()  # 会员类型
    member_rank = Field()  # 会员等级
    user_rank = Field()  # 用户等级
    verified = Field()  # 是否认证
    verified_reason = Field()  # 认证信息
    verified_type = Field()  # 认证类型
    user_type = Field()  # 用户类型
    tags = Field()  # 个人标签
    works = Field()  # 工作经历
    educations = Field()  # 教育情况
    trade = Field()  # 所在行业
    register_date = Field()  # 注册时间
    profile_url = Field()  # 首页链接
    profile_image_url = Field()  # 头像
    crawl_time = Field()  # 抓取时间戳
    req_id = Field()  # 请求ID
    resp_time = Field()  # 响应时间
