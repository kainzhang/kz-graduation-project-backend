from django.db import models

import django.utils.timezone as timezone


# Create your models here.
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
        (1, 'Movie'),
        (2, 'Book'),
    )
    id = models.CharField(primary_key=True, max_length=20)  # 豆瓣id
    comment_type = models.IntegerField(choices=COMMENT_TYPE, default=1)  # 评论类型，区分电影评论、图书评论等等
    dad_id = models.CharField(max_length=20, null=False, blank=False)  # 父级id，即评论所属对象的豆瓣id
    author = models.CharField(max_length=50, null=True, blank=True)
    author_url = models.CharField(max_length=200, null=True, blank=True)
    rating_val = models.CharField(max_length=5, null=True, blank=True)
    pub_date = models.DateTimeField(null=True, blank=True)
    content = models.TextField(null=False, blank=False)

    def __str__(self):
        return '<Comment type: %s, id: %s, dad: %s>' % (self.get_comment_type_display(), self.id, self.dad_id)
