from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer
from categories.models import Category

class CategoryApiViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(published =True)
    #
    lookup_field = 'slug'
    #
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'slug', 'id']
 
