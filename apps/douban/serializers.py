import re
from datetime import datetime

from django.db.models import Q
from rest_framework import serializers

from apps.douban.crawl import crawl_item
from apps.douban.models import Movie, Book, Comment, ItemAnalysis


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
        item = ItemAnalysis.objects.create(**validated_data)
        comments = Comment.objects.filter(Q(dad_id__exact=item.dad_id) & Q(comment_type=item.dad_type))

        dict_stars = {'50': 0, '40': 0, '30': 0, '20': 0, '10': 0}  # 评论星级
        dict_senti_year = {}
        li_pos = []  # 正面评论
        li_neu = []  # 中立评论
        li_neg = []  # 负面评论
        li_year = []  # 涉及的年份
        senti_score_sum = 0  # 总情感分数

        for comment in comments:
            # 统计星级
            if comment.rating_val != '-t':
                dict_stars[comment.rating_val] += 1

            senti_score_sum += comment.senti_score

            senti_flag = 0
            # 统计正面、中立、负面分数
            if comment.senti_score > 0.8:
                li_pos.append(comment)
                senti_flag = 1
            elif comment.senti_score < 0.3:
                li_neg.append(comment)
                senti_flag = -1
            else:
                li_neu.append(comment)

            # 每年的三类评论数量
            pub_year = datetime.strftime(comment.pub_date, '%Y')
            if pub_year not in dict_senti_year:
                li_year.append(pub_year)
                dict_senti_year[pub_year] = {'pos': 0, 'neu': 0, 'neg': 0}
            if senti_flag == 1:
                dict_senti_year[pub_year]['pos'] += 1
            elif senti_flag == -1:
                dict_senti_year[pub_year]['neg'] += 1
            else:
                dict_senti_year[pub_year]['neu'] += 1

        item.comment_num = len(comments)  # 评论总数
        item.pos_num = len(li_pos)  # 正面评论总数
        item.neu_num = len(li_neu)  # 中立评论总数
        item.neg_num = len(li_neg)  # 负面评论总数
        item.pos_rate = senti_score_sum / item.comment_num  # 情感正向比率
        item.senti_sum = {'type': ['pos', 'neu', 'neg'], 'val': [item.pos_num, item.neu_num, item.neg_num]}

        # 评分星级分布，柱状图
        item.stars_data = str(dict_stars)

        tmp_pos = []
        tmp_neu = []
        tmp_neg = []
        tmp_sum_pos = []
        tmp_sum_neu = []
        tmp_sum_neg = []
        li_year = sorted(li_year)
        for li in li_year:
            tmp_pos.append(dict_senti_year[li]['pos'])
            if len(tmp_sum_pos) == 0:
                tmp_sum_pos.append(dict_senti_year[li]['pos'])
            else:
                tmp_sum_pos.append(tmp_sum_pos[-1] + dict_senti_year[li]['pos'])

            tmp_neu.append(dict_senti_year[li]['neu'])
            if len(tmp_sum_neu) == 0:
                tmp_sum_neu.append(dict_senti_year[li]['neu'])
            else:
                tmp_sum_neu.append(tmp_sum_neu[-1] + dict_senti_year[li]['neu'])

            tmp_neg.append(dict_senti_year[li]['neg'])
            if len(tmp_sum_neg) == 0:
                tmp_sum_neg.append(dict_senti_year[li]['neg'])
            else:
                tmp_sum_neg.append(tmp_sum_neg[-1] + dict_senti_year[li]['neg'])

        # 每年各类评论发布数量，堆叠条形图
        item.senti_per_year = {'years': li_year, 'pos': tmp_pos, 'neu': tmp_neu, 'neg': tmp_neg}
        # 每年各类评论总数量，基础平滑折线图
        item.senti_sum_year = {'years': li_year, 'pos': tmp_sum_pos, 'neu': tmp_sum_neu, 'neg': tmp_sum_neg}

        print(item.stars_data)
        print(item.neu_num)
        print(item.pos_rate)
        print(item.senti_sum)
        print(item.senti_per_year)
        print(item.senti_sum_year)
        item.save()
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
        item = Movie.objects.filter(id=douban_id).first()
        if item is None:
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
        item = Book.objects.filter(id=douban_id).first()
        if item is None:
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
