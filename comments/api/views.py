from rest_framework.viewsets import ModelViewSet # Importación del módulo ModelViewSet para operaciones CRUD
from rest_framework.filters import OrderingFilter # Importación del módulo OrderingFilter para ordenar resultados
from django_filters.rest_framework import DjangoFilterBackend # Importación del módulo DjangoFilterBackend para filtrado
from .serializers import CommentSerializer # Importación del serializador CommentSerializer
from comments.models import Comment # Modelo Comment, asociado a cada post
from .permissions import IsAuthenticatedOwnerOrReadOnly # Permiso personalizado para gestión de comentarios

# API ViewSet para la gestión de comentarios.
class CommentApiViewSet(ModelViewSet):
    """
    API ViewSet para la gestión de comentarios.

    Funcionalidad:
    - Permite a cualquier usuario leer comentarios (GET).
    - Solo usuarios autenticados pueden crear comentarios (POST).
    - Solo el autor del comentario puede actualizarlo o eliminarlo.
    - El autor del post también puede eliminar comentarios en su propio post.
    """
    # Permisos personalizados para la gestión de comentarios
    permission_classes = [IsAuthenticatedOwnerOrReadOnly] 
    # Serializador que define la estructura de entrada/salida de los datos.
    serializer_class = CommentSerializer
    # QuerySet que incluye todos los comentarios 
    queryset = Comment.objects.all()
    # Configuración de filtros y ordenamiento disponibles en la API.
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    # Ordenar del comentario mas nuevo al mas antiguo
    ordering = ['-created_at'] 
    # Campos disponibles para aplicar filtros en las peticiones
    filterset_fields = ['post', 'post__slug'] 
    
    def perform_create(self, serializer):
        """
        Sobrescribe el método de creación para asignar automáticamente
        el usuario autenticado como autor del comentario.
        """
        serializer.save(user=self.request.user)

