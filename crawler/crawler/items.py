# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from apps.douban import models as douban_models


class DoubanMovieItem(DjangoItem):
    django_model = douban_models.Movie

    # django_model.name = scrapy.Field()
    # django_model.date_published = scrapy.Field()
    # django_model.genre = scrapy.Field()
    # django_model.duration = scrapy.Field()
    # django_model.rating_value = scrapy.Field()
    # django_model.director = scrapy.Field()
    # django_model.author = scrapy.Field()
    # django_model.actor = scrapy.Field()
    # django_model.description = scrapy.Field()
    # django_model.image = scrapy.Field()
    # django_model.url = scrapy.Field()
    #
    # django_model.region = scrapy.Field()
    # django_model.language = scrapy.Field()
    # django_model.alias = scrapy.Field()


class DoubanBookItem(DjangoItem):
    django_model = douban_models.Book

    # name = scrapy.Field()
    # author = scrapy.Field()
    # url = scrapy.Field()
    # isbn = scrapy.Field()
    #
    # # 评分
    # rating_value = scrapy.Field()
    #
    # # 封面图片
    # image = scrapy.Field()
    # # 出版社
    # press = scrapy.Field()
    # # 出品方
    # producer = scrapy.Field()
    # # 副标题
    # subtitle = scrapy.Field()
    # # 原作名
    # original_title = scrapy.Field()
    # # 译者
    # translator = scrapy.Field()
    # # 出版日期
    # pub_date = scrapy.Field()
    # # 页数
    # paginal_num = scrapy.Field()
    # # 定价
    # price = scrapy.Field()
    # # 装帧
    # binding = scrapy.Field()
    # # 丛书
    # series = scrapy.Field()


class DoubanCommentItem(DjangoItem):
    django_model = douban_models.Comment
