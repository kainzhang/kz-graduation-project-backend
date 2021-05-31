from django.db.models import Q
from rest_framework import viewsets, filters, generics

from apps.douban.models import ItemAnalysis, Movie, Book, Comment
from apps.douban.serializers import ItemAnalysisSerializer, MovieSerializer, BookSerializer, CommentSerializer


class ItemAnalysisViewSet(viewsets.ModelViewSet):
    queryset = ItemAnalysis.objects.all()
    serializer_class = ItemAnalysisSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['create_date']
    ordering = ['-create_date']
    search_fields = ['=dad_id']


class ItemAnalysisQuery(generics.ListAPIView):
    serializer_class = ItemAnalysisSerializer

    def get_queryset(self):
        dad_id = self.request.query_params.get('dad_id', None)
        douban_type = self.request.query_params.get('douban_type', 0)
        if dad_id is not None and douban_type != 0:
            queryset = ItemAnalysis.objects.filter(Q(dad_id__exact=dad_id) & Q(dad_type__exact=douban_type))
        elif dad_id is None and douban_type == 0:
            queryset = ItemAnalysis.objects.all()
        elif douban_type != 0:
            queryset = ItemAnalysis.objects.filter(dad_type__exact=douban_type)
        else:
            queryset = ItemAnalysis.objects.filter(dad_id__exact=dad_id)

        return queryset.order_by('-create_date')


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['create_date', 'id']
    ordering = ['-create_date']
    search_fields = ['=id', 'name', 'actor', 'director', 'genre']


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['create_date', 'id']
    ordering = ['-create_date']
    search_fields = ['=id', 'name', 'author']


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=dad_id']


class CommentQuery(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        dad_id = self.request.query_params.get('dad_id', None)
        douban_type = self.request.query_params.get('douban_type', 0)

        if dad_id is not None and douban_type != 0:
            queryset = Comment.objects.filter(Q(dad_id__exact=dad_id) & Q(comment_type__exact=douban_type))
        elif dad_id is None and douban_type == 0:
            queryset = Comment.objects.all()
        elif douban_type != 0:
            queryset = Comment.objects.filter(comment_type__exact=douban_type)
        else:
            queryset = Comment.objects.filter(dad_id__exact=dad_id)

        return queryset
