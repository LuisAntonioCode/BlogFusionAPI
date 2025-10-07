from rest_framework import serializers, pagination # Importamos pagination para el paginador personalizado
from rest_framework.response import Response # Importamos Response para personalizar la respuesta del paginador
from posts.models import Post # Importamos el modelo Post
from categories.models import Category # Importamos el modelo Category
from users.api.serializers import UserInfoSerializer # Importamos el serializador UserInfoSerializer
from categories.api.serializers import CategoryInfoSerializer # Importamos el serializador CategoryInfoSerializer

# # Paginador personalizado para la API de posts.
# Extiende de PageNumberPagination y redefine la estructura de respuesta.
class PaginationSerializer(pagination.PageNumberPagination):
    # Número de elementos por página por defecto
    page_size = 3
    # Permite que el cliente defina el tamaño de página mediante el parámetro "page_size"
    page_size_query_param = 'page_size'
    # Tamaño máximo permitido para "page_size"
    max_page_size = 20
    

    def get_paginated_response(self, data):
        """
        Retorna la respuesta paginada con metadatos adicionales.
        
        - total_posts: cantidad total de posts.
        - total_pages: número total de páginas disponibles.
        - next / previous: enlaces de navegación.
        - posts: lista de posts (en lugar del nombre por defecto 'results').
        """
        total_pages = self.page.paginator.num_pages
        return Response({
            'total_posts': self.page.paginator.count,
            'total_pages': total_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'posts': data   # 👈 Aquí cambias "results" por "posts"
        })

# Serializador principal para el modelo Post.
class PostSerializer(serializers.ModelSerializer):
    # Solo lectura (para mostrar info del usuario)
    user = UserInfoSerializer(read_only=True)
    # Solo lectura (para mostrar info de la categoria)
    category = CategoryInfoSerializer(read_only=True)
    # Este campo representa todos los comentarios relacionados con cada post
    comments = serializers.SerializerMethodField(read_only=True)

    # Solo escritura (acepta ID). 
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),  
        write_only=True, 
        source='category',
        required=False # Necesario para permitir usar slug como alternativa
    )
    #Solo escritura (acepta slug)
    category_slug = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug', 
        write_only=True, 
        source='category',
        required=False # Necesario para permitir usar id como alternativa
    )

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'slug', 'image', 'published', 'created_at', 'user', 'category', 
            'category_id', 'category_slug', 'comments' 
        ]
        # Campos de solo lectura, no pueden ser modificados por el cliente.
        read_only_fields = ('slug', 'created_at', 'user', 'comments')
        # Restricción adicional: la categoría debe estar siempre presente y no puede ser nula.
        extra_kwargs = {
            'category': {'required': True, 'allow_null': False},
        }
    
    def validate(self, data):
        """
        Valida que el cliente proporcione al menos un identificador de categoría
        (category_id o category_slug) al crear un nuevo post.
        """
        if 'category' not in data and not self.instance:
            raise serializers.ValidationError({
                'category': 'Debe proporcionar category_id o category_slug'
            })
        return data

    def get_comments(self, obj):
        """
        Obtiene todos los comentarios relacionados con el post, ordenados por fecha (más recientes primero).
        Se usa importación diferida para evitar dependencias circulares.
        """
        from comments.api.serializers import CommentInfoSerializer  # Import diferido
        comments_qs = obj.comments.order_by('-created_at')  # más recientes primero
        return CommentInfoSerializer(comments_qs, many=True).data # Serializamos los comentarios

# Serializador simplificado para listar en otras partes.
class PostInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug']