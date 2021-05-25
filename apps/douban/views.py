from rest_framework import viewsets, filters, generics

from apps.douban.models import ItemAnalysis, Movie, Book, Comment
from apps.douban.serializers import ItemAnalysisSerializer, MovieSerializer, BookSerializer, CommentSerializer


class ItemAnalysisViewSet(viewsets.ModelViewSet):
    queryset = ItemAnalysis.objects.all()
    serializer_class = ItemAnalysisSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['create_date', 'id']
    ordering = ['create_date']


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['create_date', 'id']
    ordering = ['create_date']


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter()
    serializer_class = CommentSerializer


class CommentList(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        dad_id = self.request.query_params.get('dad_id', None)
        return queryset.filter(dad_id__exact=dad_id)
