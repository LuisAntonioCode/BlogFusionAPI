from rest_framework import routers # Importacion del modulo routers de Django REST Framework
from .views import CategoryApiViewSet # Importacion del ViewSet de categorias

# Se crea una instancia del enrutador por defecto de DRF.
# Este router genera automáticamente las rutas estándar para operaciones CRUD (list, create, retrieve, update, delete).
router_categories = routers.DefaultRouter()

# Registro del ViewSet CategoryApiViewSet en el router.
# - Primer argumento (r'categories'): prefijo de la URL.
# - Segundo argumento: el ViewSet que gestionará las peticiones.
# - Tercer argumento ('categories'): nombre base para las rutas generadas.
router_categories.register(r'categories', CategoryApiViewSet, 'categories') 

# Asignación de las URLs generadas automáticamente por el router a urlpatterns.
urlpatterns = router_categories.urls 
