from django.contrib import admin
from .models import TagCache, CategoryCache, ImageCache, ArticleCache

# Register your models here.
admin.site.register(TagCache)
admin.site.register(CategoryCache)
admin.site.register(ImageCache)
admin.site.register(ArticleCache)
