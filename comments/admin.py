from django.contrib import admin
from .models import Comment # Importación del modelo Comment

# Registro del modelo Comment en el panel de administración de Django.
# Decorador que asocia el modelo Comment con la clase CommentAdmin
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en el listado de comentarios
    list_display = ['id', 'content',  'post', 'user'] 
    # Campos de solo lectura en el formulario del admin.
    readonly_fields = ('created_at',)