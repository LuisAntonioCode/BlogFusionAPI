from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAuthenticatedOwnerOrReadOnly
from .serializers import PostSerializer
from posts.models import Post

class PostApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(published = True)
    lookup_field = 'slug'

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category__slug', 'title', 'slug', 'id']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
