from rest_framework.routers import DefaultRouter
from .views import CategoryApiViewSet

router_categories = DefaultRouter()
router_categories.register(r'categories', CategoryApiViewSet, 'categories')
urlpatterns = router_categories.urls
