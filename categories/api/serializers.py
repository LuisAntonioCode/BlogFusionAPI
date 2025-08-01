from rest_framework import serializers
from categories.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'published', 'created_at']
        read_only_fields = ('created_at',)

class CategoryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'slug']