from rest_framework import serializers, viewsets

from apps.douban.models import Movie, Book, Comment, ItemAnalysis


# Serializers
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
        item = super().create(validated_data=validated_data)
        item_type = ITEM_TYPE[item.dad_type]
        print('*' * 20 + item_type)
        print('*' * 20 + item.dad_id)
        if item_type == 'movie':
            movieitem = Movie.objects.get(id=item.dad_id)
            item.comment_num = 100
            item.neg_num = 91
            item.pos_num = 9
            item.emotion_percent = movieitem.actor
            item.pos_neg_sum = movieitem.director
            item.save()


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        extra_kwargs = {
            'create_date': {
                'read_only': True,
            }
        }


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {
            'create_date': {
                'read_only': True,
            }
        }


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


# ViewSets
class ItemAnalysisViewSet(viewsets.ModelViewSet):
    queryset = ItemAnalysis.objects.all()
    serializer_class = ItemAnalysisSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
