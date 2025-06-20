from django.contrib import admin
from categories.models import Category

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'published', 'created_at']
    readonly_fields = ('created_at',)
    