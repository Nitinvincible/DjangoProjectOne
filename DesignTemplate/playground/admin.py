from django.contrib import admin
from .models import Snippet, Like, View, Comment


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    """Admin for Snippet model"""
    list_display = ['title', 'user', 'environment', 'is_public', 'views_count', 'likes_count', 'forks_count', 'created_at']
    list_filter = ['environment', 'is_public', 'created_at', 'updated_at']
    search_fields = ['title', 'description', 'user__username']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    readonly_fields = ['id', 'views_count', 'likes_count', 'forks_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'title', 'slug', 'description', 'environment', 'tags')
        }),
        ('Code', {
            'fields': ('html_code', 'css_code', 'js_code')
        }),
        ('Media', {
            'fields': ('thumbnail',)
        }),
        ('Social Stats', {
            'fields': ('views_count', 'likes_count', 'forks_count')
        }),
        ('Fork Lineage', {
            'fields': ('forked_from',)
        }),
        ('Settings', {
            'fields': ('is_public', 'is_pinned')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """Admin for Like model"""
    list_display = ['user', 'snippet', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'snippet__title']
    date_hierarchy = 'created_at'


@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    """Admin for View model"""
    list_display = ['snippet', 'user', 'ip_address', 'created_at']
    list_filter = ['created_at']
    search_fields = ['snippet__title', 'user__username', 'ip_address']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin for Comment model"""
    list_display = ['user', 'snippet', 'text_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'snippet__title', 'text']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    
    def text_preview(self, obj):
        """Show first 50 characters of comment"""
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Comment Preview'
