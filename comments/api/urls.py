from rest_framework.routers import DefaultRouter # Importamos DefaultRouter para crear rutas automáticamente
from .views import CommentApiViewSet # Importamos la vista CommentApiViewSet

# Se crea una instancia del router por defecto de DRF.
router_comments = DefaultRouter()
# Registramos la vista CommentApiViewSet
router_comments.register(r'comments', CommentApiViewSet, 'comments')
# Asignamos las URLs generadas automáticamente por el router a urlpatterns.
urlpatterns = router_comments.urls