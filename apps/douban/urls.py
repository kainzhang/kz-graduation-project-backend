from rest_framework import routers

from apps.douban.views import MovieViewSet, BookViewSet, CommentViewSet

router = routers.SimpleRouter()
router.register('movie', MovieViewSet)
router.register('book', BookViewSet)
router.register('comment', CommentViewSet)

urlpatterns = router.urls
