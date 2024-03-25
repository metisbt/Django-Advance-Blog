from django.contrib import admin
from blog.models import Post, Category

class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'status', 'category', 'image', 'published_date']

admin.site.register(Category)
admin.site.register(Post)