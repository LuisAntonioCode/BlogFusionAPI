from rest_framework import serializers
from posts.models import Post
from categories.models import Category
from users.api.serializers import UserInfoSerializer
from categories.api.serializers import CategoryInfoSerializer

class PostSerializer(serializers.ModelSerializer):
    # Solo lectura (para mostrar info del usuario)
    user = UserInfoSerializer(read_only=True)
    # Solo lectura (para mostrar info de la categoria)
    category = CategoryInfoSerializer(read_only=True)

    # Solo escritura (acepta ID)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),  
        write_only=True, 
        source='category',
        required=False #Necesario para permitir usar slug como alternativa
    )
    #Solo escritura (acepta ID)
    category_slug = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug', 
        write_only=True, 
        source='category',
        required=False #Necesario para permitir usar id como alternativa
    )

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'slug', 'image', 'published', 'created_at', 'user', 'category', 
            'category_id', 'category_slug'
        ]
        read_only_fields = ('slug', 'created_at', 'user')

        extra_kwargs = {
            'category': {'required': True, 'allow_null': False},
        }

    def validate(self, data):
        # Validar que al menos se haya enviado uno de los dos campos "category_id o category_slug"
        if 'category' not in data and not self.instance:
            raise serializers.ValidationError({
                'category': 'Debe proporcionar category_id o category_slug'
            })
        return data

class PostInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug']