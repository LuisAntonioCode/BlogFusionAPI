from rest_framework.routers import DefaultRouter
from .views import PostApiViewSet

router_posts = DefaultRouter()
router_posts.register(r'posts', PostApiViewSet, 'posts')
urlpatterns = router_posts.urls