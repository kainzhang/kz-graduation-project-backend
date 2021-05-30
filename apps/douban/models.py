from datetime import datetime

import django.utils.timezone as timezone
from django.db import models


# Create your models here.
class ItemAnalysis(models.Model):
    ITEM_TYPE = (
        (1, 'movie'),
        (2, 'book'),
    )
    dad_id = models.CharField(max_length=20, null=False, blank=False)
    dad_type = models.IntegerField(choices=ITEM_TYPE, default=1)  # 分析对象的类型，区分电影、图书

    # 除分析对象的 id 外，其余数据由系统自动生成
    comment_num = models.IntegerField(null=True, blank=True)  # 热评样本数量
    pos_num = models.IntegerField(null=True, blank=True)  # 正面评论数量
    neu_num = models.IntegerField(null=True, blank=True)  # 中立评论数量
    neg_num = models.IntegerField(null=True, blank=True)  # 负面评论数量
    pos_rate = models.FloatField(null=True, blank=True)  # 正面评论比率

    # figures, 数据库存 json 转字符串
    stars_data = models.TextField(null=True, blank=True)  # 1-5 星评分情况，绘制柱形图
    senti_sum = models.TextField(null=True, blank=True)  # 三种类型评论总数，绘制柱形图（横向）
    senti_per_year = models.TextField(null=True, blank=True)  # 各年份的三种类型评论数量，堆叠条形图
    senti_sum_year = models.TextField(null=True, blank=True)  # 三种类型评论数量走势，绘制折线图
    word_cloud = models.TextField(null=True, blank=True)  # 词云

    # 分析时间
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '<ItemAnalysis: %s, date: %s>' % (
            self.dad_id,
            datetime.strftime(self.create_date, '%Y-%m-%d %H:%M:%S')
        )


class Movie(models.Model):
    id = models.CharField(primary_key=True, max_length=20)  # 豆瓣id
    name = models.CharField(max_length=200, null=False, blank=False)
    image = models.CharField(max_length=200, null=True, blank=True)
    douban_url = models.CharField(max_length=200, null=True, blank=True)
    pub_date = models.CharField(max_length=50, null=True, blank=True)
    duration = models.CharField(max_length=25, null=True, blank=True)
    imdb = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    rating_val = models.CharField(max_length=5, null=True, blank=True)
    stars5 = models.CharField(max_length=5, null=True, blank=True)
    stars4 = models.CharField(max_length=5, null=True, blank=True)
    stars3 = models.CharField(max_length=5, null=True, blank=True)
    stars2 = models.CharField(max_length=5, null=True, blank=True)
    stars1 = models.CharField(max_length=5, null=True, blank=True)

    # 以下各字段将列表转为字符串存储
    genre = models.TextField(null=True, blank=True)
    director = models.TextField(null=True, blank=True)
    author = models.TextField(null=True, blank=True)
    actor = models.TextField(null=True, blank=True)
    region = models.TextField(null=True, blank=True)
    language = models.TextField(null=True, blank=True)
    alias = models.TextField(null=True, blank=True)

    # 创建时间（信息爬取时间）
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '<Movie: %s, id: %s>' % (self.name, self.id)


class Book(models.Model):
    id = models.CharField(primary_key=True, max_length=20)  # 豆瓣id
    name = models.CharField(max_length=200, null=False, blank=False)
    image = models.CharField(max_length=200, null=True, blank=True)
    douban_url = models.CharField(max_length=200, null=True, blank=True)
    pub_date = models.CharField(max_length=50, null=True, blank=True)
    isbn = models.CharField(max_length=20, null=True, blank=True)
    press = models.CharField(max_length=50, null=True, blank=True)
    producer = models.CharField(max_length=50, null=True, blank=True)
    subtitle = models.CharField(max_length=100, null=True, blank=True)
    original_title = models.CharField(max_length=100, null=True, blank=True)
    paginal_num = models.CharField(max_length=10, null=True, blank=True)
    price = models.CharField(max_length=10, null=True, blank=True)
    binding = models.CharField(max_length=20, null=True, blank=True)
    series = models.CharField(max_length=50, null=True, blank=True)

    rating_val = models.CharField(max_length=5, null=True, blank=True)
    stars5 = models.CharField(max_length=5, null=True, blank=True)
    stars4 = models.CharField(max_length=5, null=True, blank=True)
    stars3 = models.CharField(max_length=5, null=True, blank=True)
    stars2 = models.CharField(max_length=5, null=True, blank=True)
    stars1 = models.CharField(max_length=5, null=True, blank=True)

    # 以下各字段将列表转为字符串存储
    author = models.TextField(null=True, blank=True)
    translator = models.TextField(null=True, blank=True)

    # 创建时间（信息爬取时间）
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '<Book: %s, id: %s>' % (self.name, self.id)


class Comment(models.Model):
    COMMENT_TYPE = (
        (1, 'movie'),
        (2, 'book'),
    )
    id = models.CharField(primary_key=True, max_length=20)  # 豆瓣id
    comment_type = models.IntegerField(choices=COMMENT_TYPE, default=1)  # 评论类型，区分电影评论、图书评论等等
    dad_id = models.CharField(max_length=20, null=False, blank=False)  # 父级id，即评论所属对象的豆瓣id
    author = models.CharField(max_length=50, null=True, blank=True)
    author_url = models.CharField(max_length=200, null=True, blank=True)
    rating_val = models.CharField(max_length=5, null=True, blank=True)
    pub_date = models.DateTimeField(null=True, blank=True)
    content = models.TextField(null=False, blank=False)
    senti_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return '<Comment type: %s, id: %s, dad: %s>' % (self.get_comment_type_display(), self.id, self.dad_id)
