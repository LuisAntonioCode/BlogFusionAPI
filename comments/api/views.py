from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from comments.models import Comment
from .serializers import CommentSerializer
from .permissions import IsAuthenticatedOwnerOrReadOnly

class CommentApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOwnerOrReadOnly]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    #
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering = ['-created_at']
    filterset_fields = ['post', 'post__slug']

    #
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
