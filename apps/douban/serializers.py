import re

from rest_framework import serializers

from apps.douban.models import Movie, Book, Comment, ItemAnalysis
from apps.douban.crawl import crawl_item

from snownlp import SnowNLP


class ItemAnalysisSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ItemAnalysis
        fields = '__all__'
        extra_kwargs = {
            'comment_num': {'read_only': True},  # 热评样本数量
            'pos_num': {'read_only': True},  # 正面评论数量
            'neg_num': {'read_only': True},  # 负面评论数量
            'stars_data': {'read_only': True},  # 1-5 星评分情况，绘制柱形图
            'pos_neg_sum': {'read_only': True},  # 正负面评论总数，绘制柱形图（横向）
            'pos_neg_per_month': {'read_only': True},  # 各月份的正负面评论数量，绘制柱形图
            'pos_neg_sum_month': {'read_only': True},  # 正负面评论数量走势，绘制折线图
            'emotion_percent': {'read_only': True},  # 喜怒哀乐等情绪占比，饼状图
            'create_date': {'read_only': True}
        }

    def create(self, validated_data):
        ITEM_TYPE = {
            1: 'movie',
            2: 'book'
        }
        item = ItemAnalysis.objects.create(**validated_data)
        item_type = ITEM_TYPE[item.dad_type]
        if item_type == 'movie':
            pass
            # comments = Comment.objects.filter(dad_id__exact=item.dad_id)
            # for comment in comments:
            #     comment.senti_score = SnowNLP(comment.content).sentiments
            #     comment.save()
            # movieitem = Movie.objects.get(id=item.dad_id)
            # item.comment_num = 100
            # item.neg_num = 91
            # item.pos_num = 9
            # item.emotion_percent = movieitem.actor
            # item.pos_neg_sum = movieitem.director
            # item.save()
        elif item_type == 'book':
            pass

        return item


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        extra_kwargs = {
            'name': {'read_only': True},
            'image': {'read_only': True},
            'pub_date': {'read_only': True},
            'duration': {'read_only': True},
            'imdb': {'read_only': True},
            'description': {'read_only': True},
            'rating_val': {'read_only': True},
            'stars5': {'read_only': True},
            'stars4': {'read_only': True},
            'stars3': {'read_only': True},
            'stars2': {'read_only': True},
            'stars1': {'read_only': True},
            'genre': {'read_only': True},
            'director': {'read_only': True},
            'author': {'read_only': True},
            'actor': {'read_only': True},
            'region': {'read_only': True},
            'language': {'read_only': True},
            'alias': {'read_only': True},
            'create_date': {'read_only': True}
        }

    def create(self, validated_data):
        douban_id = re.sub(r'\D', "", validated_data['douban_url'])
        item = Movie.objects.create(
            id=douban_id,
            douban_url=validated_data['douban_url']
        )
        crawl_item('movie', douban_id)
        return item


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {
            'name': {'read_only': True},
            'image': {'read_only': True},
            'pub_date': {'read_only': True},
            'isbn': {'read_only': True},
            'press': {'read_only': True},
            'producer': {'read_only': True},
            'subtitle': {'read_only': True},
            'original_title': {'read_only': True},
            'paginal_num': {'read_only': True},
            'price': {'read_only': True},
            'binding': {'read_only': True},
            'series': {'read_only': True},
            'rating_val': {'read_only': True},
            'stars5': {'read_only': True},
            'stars4': {'read_only': True},
            'stars3': {'read_only': True},
            'stars2': {'read_only': True},
            'stars1': {'read_only': True},
            'author': {'read_only': True},
            'translator': {'read_only': True},
            'create_date': {'read_only': True},
        }

    def create(self, validated_data):
        douban_id = re.sub(r'\D', "", validated_data['douban_url'])
        item = Book.objects.create(
            id=douban_id,
            douban_url=validated_data['douban_url']
        )
        crawl_item('book', douban_id)
        return item


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
