from django_filters.rest_framework import DjangoFilterBackend # Importación del módulo DjangoFilterBackend para filtrado
from rest_framework.viewsets import ModelViewSet # Importación del módulo ModelViewSet para operaciones CRUD
from .serializers import CategorySerializer # Importación del serializador CategorySerializer
from categories.models import Category # Importación del modelo Category
from .permissions import IsAdminOrReadOnly # Permiso personalizado: solo administradores pueden modificar

# Vista para la API de categorías
# Proporciona automáticamente endpoints para listar, crear, actualizar y eliminar categorías.
class CategoryApiViewSet(ModelViewSet): 
    permission_classes = [IsAdminOrReadOnly] # los usuarios anónimos o no administradores solo pueden leer (GET).
    serializer_class = CategorySerializer # Serializador que se va a utilizar
    queryset = Category.objects.filter(published = True) # Conjunto de datos, solo se incluyen categorías publicadas  
    lookup_field = 'slug' # Configuración de búsqueda. En lugar de usar el campo "id", se utiliza el campo "slug" en las URLs.
    filter_backends = [DjangoFilterBackend] # Backend de filtrado habilitados en la API.
    filterset_fields = ['title', 'slug', 'id'] # Campos disponibles para aplicar filtros en las peticiones
 
