import string
import random
from django.db import models
from django.db.models import SET_NULL
from django.utils.text import slugify
from users.models import User
from categories.models import Category

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=150, blank=False)
    content = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=False)
    category = models.ForeignKey(Category, on_delete=SET_NULL, null=True, blank=False)

    def generate_unique_slug(self):
        while True:
            base_slug = slugify(self.title[:15])
            unique_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
            slug = f'{base_slug}-{unique_code}'

            if not Post.objects.filter(slug=slug).exists():
                return slug
            
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
