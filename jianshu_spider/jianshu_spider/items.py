# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JianshuSpiderItem(scrapy.Item):
    nickname = scrapy.Field()
    slug = scrapy.Field()
    head_pic = scrapy.Field()
    gender = scrapy.Field()
    is_contract = scrapy.Field()
    following_num = scrapy.Field()
    followers_num = scrapy.Field()
    articles_num = scrapy.Field()
    words_num = scrapy.Field()
    be_liked_num = scrapy.Field()
