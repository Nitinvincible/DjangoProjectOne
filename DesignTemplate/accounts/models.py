from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended user model for Social Code Playground"""
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, help_text="Uploaded profile picture")
    avatar_url = models.URLField(blank=True, null=True, help_text="Profile picture URL")
    bio = models.TextField(max_length=500, blank=True, help_text="User biography")
    tech_stack_tags = models.JSONField(default=list, blank=True, help_text="Technologies the user works with")
    github_profile = models.URLField(blank=True, null=True, help_text="GitHub profile URL")
    website = models.URLField(blank=True, null=True, help_text="Personal website")
    
    # Gamification fields
    streak_count = models.IntegerField(default=0, help_text="Current contribution streak")
    total_views = models.IntegerField(default=0, help_text="Total views across all snippets")
    total_likes = models.IntegerField(default=0, help_text="Total likes received")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.username
    
    def get_avatar_display(self):
        """Return the avatar URL, prioritizing uploaded file over URL"""
        if self.avatar:
            return self.avatar.url
        return self.avatar_url or None
    
    def update_stats(self):
        """Update total views and likes from all snippets"""
        snippets = self.snippets.all()
        self.total_views = sum(s.views_count for s in snippets)
        self.total_likes = sum(s.likes_count for s in snippets)
        self.save()


class Activity(models.Model):
    """Track daily user activity for contribution graph (GitHub-style heatmap)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    date = models.DateField(help_text="Date of activity")
    snippet_count = models.IntegerField(default=0, help_text="Snippets created on this day")
    fork_count = models.IntegerField(default=0, help_text="Forks made on this day")
    
    class Meta:
        unique_together = ('user', 'date')
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"
