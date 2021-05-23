from rest_framework import routers

from apps.douban.views import MovieViewSet, BookViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'movie', MovieViewSet)
router.register(r'book', BookViewSet)
router.register(r'comment', CommentViewSet)

urlpatterns = router.urls
