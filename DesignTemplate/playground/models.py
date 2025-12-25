from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
import uuid


class Snippet(models.Model):
    """User-created code snippets (HTML/CSS/JS)"""
    
    ENVIRONMENT_CHOICES = [
        ('2d', '2D Web'),
        ('3d', '3D (Three.js)'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='snippets'
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField(blank=True, help_text="Brief description of the snippet")
    
    # Code storage
    html_code = models.TextField(blank=True, help_text="HTML code")
    css_code = models.TextField(blank=True, help_text="CSS styles")
    js_code = models.TextField(blank=True, help_text="JavaScript code")
    
    # Metadata
    environment = models.CharField(
        max_length=2, 
        choices=ENVIRONMENT_CHOICES, 
        default='2d',
        help_text="Rendering environment"
    )
    tags = models.JSONField(default=list, blank=True, help_text="Tags for categorization")
    thumbnail = models.ImageField(
        upload_to='thumbnails/', 
        blank=True, 
        null=True,
        help_text="Auto-generated or uploaded thumbnail"
    )
    
    # Social tracking
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    forks_count = models.IntegerField(default=0)
    
    # Fork lineage tracking
    forked_from = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='forks',
        help_text="Original snippet this was forked from"
    )
    
    # Privacy
    is_public = models.BooleanField(default=True, help_text="Public snippets appear in feed")
    is_pinned = models.BooleanField(default=False, help_text="Show on user profile")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['slug']),
        ]
        verbose_name = 'Snippet'
        verbose_name_plural = 'Snippets'
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from title
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Snippet.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} by {self.user.username}"
    
    def get_absolute_url(self):
        return reverse('playground:detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def increment_forks(self):
        """Increment fork count"""
        self.forks_count += 1
        self.save(update_fields=['forks_count'])


class Like(models.Model):
    """Track snippet likes (users can like once per snippet)"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'snippet')
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} likes {self.snippet.title}"


class View(models.Model):
    """Track snippet views for analytics"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        help_text="User who viewed (if authenticated)"
    )
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE, related_name='view_records')
    ip_address = models.GenericIPAddressField(help_text="IP address of viewer")
    user_agent = models.CharField(max_length=500, blank=True, help_text="Browser user agent")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'View'
        verbose_name_plural = 'Views'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"View of {self.snippet.title} at {self.created_at}"


class Comment(models.Model):
    """Snippet comments"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=1000, help_text="Comment text")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.snippet.title}"
