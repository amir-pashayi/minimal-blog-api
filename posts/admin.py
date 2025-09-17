from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'created_at', 'updated_at', 'views_count')
    search_fields = ('title', 'description', 'excerpt')
    list_filter = ('status', 'created_at', 'user')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-created_at']