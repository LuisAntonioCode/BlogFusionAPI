from django.db import models
from django.db.models import SET_NULL
from posts.models import Post
from users.models import User

# Create your models here.
class Comment(models.Model):
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, blank=False)
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=False)

    def __str__(self):
        return f'Comentario creado por {self.user.username if self.user else "Usuario anonimo"} \
        del post "{self.post.title}"'