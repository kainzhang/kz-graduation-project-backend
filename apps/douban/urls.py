from django.conf.urls import url
from rest_framework import routers

# from apps.douban.views import CommentQuery, ItemAnalysisQuery
from apps.douban.views import MovieViewSet, BookViewSet, CommentViewSet, ItemAnalysisViewSet

router = routers.DefaultRouter()
router.register(r'movie', MovieViewSet)
router.register(r'book', BookViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'item_analysis', ItemAnalysisViewSet)

urlpatterns = router.urls + [
    # url(r'^comment_query/$', CommentQuery.as_view()),
    # url(r'^item_analysis_query/$', ItemAnalysisQuery.as_view()),
]
