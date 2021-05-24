from rest_framework import routers

from apps.douban.views import MovieViewSet, BookViewSet, CommentViewSet, ItemAnalysisViewSet

router = routers.DefaultRouter()
router.register(r'movie', MovieViewSet)
router.register(r'book', BookViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'item_analysis', ItemAnalysisViewSet)

urlpatterns = router.urls
