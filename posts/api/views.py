from django_filters.rest_framework import DjangoFilterBackend # Importación del módulo DjangoFilterBackend para filtrado
from rest_framework.viewsets import ModelViewSet # Importación del módulo ModelViewSet para operaciones CRUD
from rest_framework.filters import OrderingFilter # Importación del módulo OrderingFilter para ordenar resultados
from .serializers import PostSerializer, PaginationSerializer # Importación del serializador PostSerializer y PaginationSerializer
from posts.models import Post # Importación del modelo Post
from .permissions import IsAuthenticatedOwnerOrReadOnly # Permiso personalizado: solo el propietario autenticado puede modificar

# Vista para la API de posts
class PostApiViewSet(ModelViewSet):
    # Permisos: solo el autor autenticado puede modificar/eliminar su post,
    # mientras que otros usuarios tienen acceso de solo lectura.
    permission_classes = [IsAuthenticatedOwnerOrReadOnly]

    # Serializador que define la estructura de entrada/salida de los datos.
    serializer_class = PostSerializer
    # Clase de paginación personalizada.
    pagination_class = PaginationSerializer 
    # QuerySet, solo incluye publicaciones que están publicadas.
    queryset = Post.objects.filter(published= True)
    # Configuración de búsqueda. En lugar de usar el campo "id", se utiliza el campo "slug" en las URLs.
    lookup_field = 'slug'
    # Backend de filtrado y ordenamiento habilitados en la API.
    filter_backends = [DjangoFilterBackend, OrderingFilter] 
    # Campos disponibles para aplicar filtros en las peticiones
    filterset_fields = ['category__slug', 'title', 'slug', 'id']
    # Campo por el cual se ordenan los resultados por defecto
    ordering = ['-created_at'] # Ordenar del post mas nuevo al mas antiguo 

    # Solo usuarios autenticados puedan crear sus posts
    # Al crear un post, se asigna automáticamente el usuario autenticado como autor.
    # El campo 'user' no puede ser manipulado directamente desde la petición.
    def perform_create(self, serializer): 
        serializer.save(user=self.request.user)
