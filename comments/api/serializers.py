from rest_framework import serializers # Utilidades para crear serializadores en DRF
from comments.models import Comment # Importar el modelo Comment
from users.api.serializers import UserInfoSerializer # Importar el serializado simplificado del usuario
from posts.models import Post # Importar el modelo Post

# Serializador principal para el modelo Comment
class CommentSerializer(serializers.ModelSerializer):
    # --- Campos de solo lectura ---
    # Información del usuario que creó el comentario (solo visible en respuesta).
    user = UserInfoSerializer(read_only=True)
    # Información del post al que pertenece el comentario
    post = serializers.SerializerMethodField(read_only=True)

    # --- Campos de escritura ---
    # Permite asociar un comentario a un post usando el ID.
    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), 
        write_only=True,  
        source='post', 
        required=False # Necesario para permitir usar slug como alternativa
    )
    # Permite asociar un comentario a un post usando el slug.
    post_slug = serializers.SlugRelatedField(
        queryset=Post.objects.all(),
        slug_field='slug', 
        write_only=True, 
        source='post',
        required=False # Necesario para permitir usar id como alternativa 
    )

    class Meta:
        model = Comment
        # Campos que se incluirán en el serializador 
        fields = ['id', 'content', 'post', 'user', 'post_id', 'post_slug', 'created_at']
        # Campos de solo lectura, no pueden ser modificados por el cliente.
        read_only_fields = ('created_at', 'user', 'post')

    def validate(self, data):
        """
        Valida que el cliente proporcione al menos un identificador de post
        (post_id o post_slug) al crear un comentario nuevo.
        """
        if 'post' not in data and not self.instance:
            raise serializers.ValidationError({
                'post': 'Debe proporcionar post_id o post_slug'
            })
        return data

    def get_post(self, obj):
        """
        Devuelve una representación simplificada del post asociado utilizando PostInfoSerializer.
        Se usa importación diferida para evitar dependencias circulares.
        """
        from posts.api.serializers import PostInfoSerializer
        return PostInfoSerializer(obj.post).data
    
# Serializador simplificado para listar comentarios
class CommentInfoSerializer(serializers.ModelSerializer):
    # Incluye información básica del usuario que escribió el comentario. 
    user = UserInfoSerializer(read_only=True)

    class Meta:
        model = Comment
        # Campos incluidos en el serializador simplificado
        fields = ['content', 'user', 'created_at']