from rest_framework import serializers # Importación del módulo serializers de Django REST Framework
from categories.models import Category # Importación del modelo Category

# Serializador principal para el modelo Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category # Modelo que se va a serializar
        fields = ['id', 'title', 'slug', 'published', 'created_at'] # Campos que se van a incluir en la serialización 
        read_only_fields = ('created_at',) # Campos de solo lectura

# Serializador para mostrar información básica de la categoría
class CategoryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category # Modelo asociado al serializador
        fields = ['title', 'slug']