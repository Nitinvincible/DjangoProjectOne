from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Activity


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Enhanced admin for custom User model"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'streak_count', 'total_views', 'total_likes', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': ('avatar_url', 'bio', 'tech_stack_tags', 'github_profile', 'website')
        }),
        ('Gamification Stats', {
            'fields': ('streak_count', 'total_views', 'total_likes')
        }),
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin for Activity tracking"""
    list_display = ['user', 'date', 'snippet_count', 'fork_count']
    list_filter = ['date', 'user']
    search_fields = ['user__username']
    date_hierarchy = 'date'
