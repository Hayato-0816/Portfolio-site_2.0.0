from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_public']
    list_filter = ['category', 'is_public']
    search_fields = ['title', 'description']