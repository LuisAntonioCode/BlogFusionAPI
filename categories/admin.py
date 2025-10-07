from django.contrib import admin
from categories.models import Category # Importación del modelo Category

# Registro del modelo Category en el admin de Django
@admin.register(Category) # Decorador que asocia el modelo Category con la clase CategoryAdmin
class CategoryAdmin(admin.ModelAdmin): 
    # Campos que se mostaran en el listado de categorías
    list_display = ['id', 'title', 'slug', 'published', 'created_at'] 
    # Campos de solo lectura
    readonly_fields = ('created_at',) 
    