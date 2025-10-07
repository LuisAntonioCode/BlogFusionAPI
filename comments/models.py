from django.db import models  # Importación de utilidades principales para definir modelos en Django
from django.db.models import SET_NULL  # Estrategia de borrado para claves foráneas
from posts.models import Post  # Importación del modelo Post, al que hace referencia cada comentario
from users.models import User  # Importación del modelo User, autor del comentario

# Modelo que representa un comentario en un post
class Comment(models.Model):
    # Contenido del comentario, no puede estar vacío
    content = models.TextField(blank=False) 
    # Fecha y hora de creación del comentario, se establece automáticamente al crear
    created_at = models.DateTimeField(auto_now_add=True)

    # Relación con el post al que pertenece el comentario.
    # - CASCADE: si se elimina el post, se eliminan también sus comentarios.
    # - related_name='comments': permite acceder a los comentarios desde el post con post.comments.all().
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, blank=False) 

    # Relación con el usuario que creó el comentario.
    # - SET_NULL: si se elimina el usuario, el comentario queda con usuario NULL (se mantiene en la BD).
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=False)
    
    # Muestra quién hizo el comentario y en qué post 
    def __str__(self):
        return (
            f'Comentario creado por {self.user.username if self.user else "Usuario Anónimo"} '
            f'del post "{self.post.title}"'
        ) 