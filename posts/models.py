import string   # Librería estándar para trabajar con cadenas de caracteres
import random   # Librería estándar para generación de valores aleatorios
from django.db import models 
from django.db.models import SET_NULL  # Estrategia de borrado para relaciones foráneas
from django.utils.text import slugify  # Utilidad de Django para convertir texto en slugs
from users.models import User          # Modelo de usuario personalizado
from categories.models import Category # Modelo de categorías

# Modelo que representa un post dentro de la aplicación.
class Post(models.Model):
    # Título del post, obligatorio.
    title = models.CharField(max_length=150, blank=False)
    # Contenido principal del post. Puede estar vacío.
    content = models.TextField(blank=True)
    # Slug único para URLs amigables. Se genera automaticamente.
    slug = models.SlugField(unique=True, blank=True)
    # Imagen asociada al post, almacenada en la carpeta 'posts/images/'.
    # Puede estar vacía o ser nula.
    image = models.ImageField(max_length=100, upload_to='posts/images/', blank=True, null=True)
    # Indica si el post está publicado o no.
    published = models.BooleanField(default=False)
    # Fecha de creación, se asigna automáticamente.
    created_at = models.DateTimeField(auto_now_add=True)
    # Relación con el autor del post. Si el usuario se elimina, el valor pasa a NULL.
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=False)
    # Relación con la categoría del post. Si la categoría se elimina, el valor pasa a NULL.
    category = models.ForeignKey(Category, on_delete=SET_NULL, null=True, blank=False)

    # Método para generar un slug único a partir del título.
    def generate_unique_slug(self):
        while True:
            # Se toma como base el título (máx. 15 caracteres) y se convierte en slug.
            base_slug = slugify(self.title[:15])
            # Se genera un código aleatorio de 5 caracteres para garantizar unicidad.
            unique_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
            # Se combina el slug base con el código único.
            slug = f"{base_slug}-{unique_code}"

            # Se valida que el slug generado no exista ya en la base de datos.
            if not Post.objects.filter(slug=slug).exists():
                # Si es único, se retorna.
                return slug

    # Sobrescritura del método save para garantizar que siempre haya un slug único antes de guardar.
    def save(self, *args, **kwargs):
        # Si no hay slug, se genera uno.
        if not self.slug:
            # Genera y asigna un slug único.
            self.slug = self.generate_unique_slug()
        # Llama al método save original para guardar el objeto.
        super().save(*args, **kwargs)

    # Representación en texto del objeto Post (muy útil en Django Admin).
    def __str__(self):
        return self.title
