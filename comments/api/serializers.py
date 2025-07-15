from rest_framework import serializers
from comments.models import Comment
from users.api.serializers import UserInfoSerializer
from posts.models import Post

class CommentSerializer(serializers.ModelSerializer):
    # Solo lectura (para mostrar info del usuario)
    user = UserInfoSerializer(read_only=True)
    # Solo lectura (para mostrar info del post)
    post = serializers.SerializerMethodField(read_only=True)

    # Solo escritura (acepta ID)
    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(),  
        write_only=True, 
        source='post',
        required=False #Necesario para permitir usar slug como alternativa
    )
    #Solo escritura (acepta ID)
    post_slug = serializers.SlugRelatedField(
        queryset=Post.objects.all(),
        slug_field='slug', 
        write_only=True, 
        source='post',
        required=False #Necesario para permitir usar id como alternativa
    )

    class Meta:
        model = Comment
        fields = ['id', 'content', 'post', 'user', 'post_id', 'post_slug', 'created_at']
        read_only_fields = ('created_at', 'user', 'post')

    def validate(self, data):
        # Validar que al menos se haya enviado uno de los dos campos "post_id o post_slug"
        if 'post' not in data and not self.instance:
            raise serializers.ValidationError({
                'post': 'Debe proporcionar post_id o post_slug'
            })
        return data
    
    def get_post(self, obj):
        from posts.api.serializers import PostInfoSerializer
        return PostInfoSerializer(obj.post).data
    
class CommentInfoSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['content', 'user', 'created_at']