from rest_framework.routers import DefaultRouter
from .views import CommentApiViewSet

router_comments = DefaultRouter()
router_comments.register(r'comments', CommentApiViewSet, 'comments')
urlpatterns = router_comments.urls