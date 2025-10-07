from django.contrib import admin
from .models import Post # Importación del modelo Post

# Registro del modelo Post en el panel de administración de Django.
# Decorador que asocia el modelo Post con la clase PostAdmin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en el listado de posts
    list_display = ['id', 'title', 'slug', 'image', 'published', 'created_at', 'user', 'category']

    # Campos de solo lectura en el formulario del admin.
    # 'created_at': porque se genera automáticamente.
    # 'slug': porque se genera de manera automática en el método save().
    readonly_fields = ('created_at', 'slug')