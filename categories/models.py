from django.db import models

# Definición del modelo Category, que representa una categoría dentro del blog.
class Category(models.Model):
    # Título de la categoría
    title = models.CharField(max_length=150)
    # Slug único para la categoría (usado en URLs amigables y legibles)
    slug = models.SlugField(max_length=100, unique=True)
    # Indica si la categoría está o no esta visible/publicada en el blog
    published = models.BooleanField(default=False)
    # Fecha y hora en que se creó la categoría
    created_at = models.DateTimeField(auto_now_add=True)

    # Representación legible del modelo 
    def __str__(self):
        # Devuelve el título de la categoría
        return self.title
    
    class Meta:
        verbose_name = "Categoría" # Nombre legible en singular
        verbose_name_plural = "Categorías" # Nombre legible en plural
        ordering = ['-created_at'] # Ordena las categorías por fecha de creación 
