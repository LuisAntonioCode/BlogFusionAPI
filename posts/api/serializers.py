from rest_framework import serializers
from posts.models import Post
from users.api.serializers import UserInfoSerializer
from categories.api.serializers import CategoryInfoSerializer

class PostSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()
    category = CategoryInfoSerializer()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'slug', 'image', 'published', 'created_at', 'user', 'category']
        read_only_fields = ('slug', 'created_at', 'user')

        extra_kwargs = {
            'category': {'required': True, 'allow_null': False},
        }  



