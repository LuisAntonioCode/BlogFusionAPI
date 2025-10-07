from rest_framework.routers import DefaultRouter # Importamos DefaultRouter para crear rutas automáticamente
from .views import PostApiViewSet  # Importamos la vista PostApiViewSet

# Se crea una instancia del router por defecto de DRF.
router_posts = DefaultRouter()
# Registramos la vista PostApiViewSet
router_posts.register(r'posts', PostApiViewSet, 'posts')
# Asignamos las URLs generadas automáticamente por el router a urlpatterns.
urlpatterns = router_posts.urls