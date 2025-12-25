from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count
from .models import Snippet, Like, View, Comment
from accounts.models import Activity
import json
from datetime import date


def feed(request):
    """Homepage feed showing latest public snippets"""
    snippets = Snippet.objects.filter(is_public=True).select_related('user')
    
    # Filter by environment if specified
    env = request.GET.get('environment')
    if env in ['2d', '3d']:
        snippets = snippets.filter(environment=env)
    
    # Filter by tags if specified
    tag = request.GET.get('tag')
    if tag:
        snippets = snippets.filter(tags__contains=[tag])
    
    # Get popular tags
    popular_tags = ['navbar', '3d', 'animation', 'card', 'button', 'form', 'landing', 'cyberpunk']
    
    context = {
        'snippets': snippets[:20],  # Limit to 20 for now
        'popular_tags': popular_tags,
    }
    return render(request, 'playground/feed.html', context)


@login_required
def editor(request, slug=None):
    """Code editor page"""
    snippet = None
    if slug:
        snippet = get_object_or_404(Snippet, slug=slug)
        # Check if user owns this snippet
        if snippet.user != request.user:
            # Viewing someone else's snippet in editor = fork
            snippet = None
    
    context = {
        'snippet': snippet,
    }
    return render(request, 'playground/editor.html', context)


def snippet_detail(request, slug):
    """Snippet detail page with code display and comments"""
    snippet = get_object_or_404(Snippet, slug=slug)
    
    # Track view
    if request.user.is_authenticated:
        View.objects.create(
            snippet=snippet,
            user=request.user,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
    snippet.increment_views()
    
    # Check if user liked this snippet
    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(user=request.user, snippet=snippet).exists()
    
    context = {
        'snippet': snippet,
        'user_liked': user_liked,
        'comments': snippet.comments.all().select_related('user'),
    }
    return render(request, 'playground/snippet_detail.html', context)


def snippet_preview(request, slug):
    """Render snippet code in an iframe (for thumbnails)"""
    snippet = get_object_or_404(Snippet, slug=slug)
    
    # Build HTML document
    html_doc = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>{snippet.css_code}</style>
        {'<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>' if snippet.environment == '3d' else ''}
    </head>
    <body>
        {snippet.html_code}
        <script>{snippet.js_code}</script>
    </body>
    </html>
    """
    
    from django.http import HttpResponse
    return HttpResponse(html_doc, content_type='text/html')


@login_required
@require_POST
def save_snippet(request):
    """Save or update a snippet via AJAX"""
    try:
        data = json.loads(request.body)
        
        snippet_id = data.get('id')
        if snippet_id:
            # Update existing snippet
            snippet = get_object_or_404(Snippet, id=snippet_id, user=request.user)
        else:
            # Create new snippet
            snippet = Snippet(user=request.user)
        
        snippet.title = data.get('title', 'Untitled')
        snippet.html_code = data.get('html_code', '')
        snippet.css_code = data.get('css_code', '')
        snippet.js_code = data.get('js_code', '')
        snippet.environment = data.get('environment', '2d')
        snippet.description = data.get('description', '')
        snippet.tags = data.get('tags', [])
        snippet.is_public = data.get('is_public', True)
        snippet.save()
        
        # Track activity
        activity, created = Activity.objects.get_or_create(
            user=request.user,
            date=date.today(),
            defaults={'snippet_count': 0, 'fork_count': 0}
        )
        if created or snippet_id is None:
            activity.snippet_count += 1
            activity.save()
        
        return JsonResponse({
            'success': True,
            'slug': snippet.slug,
            'id': snippet.id,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def fork_snippet(request, slug):
    """Fork a snippet"""
    original = get_object_or_404(Snippet, slug=slug)
    
    # Create a copy
    fork = Snippet.objects.create(
        user=request.user,
        title=f"{original.title} (Fork)",
        html_code=original.html_code,
        css_code=original.css_code,
        js_code=original.js_code,
        environment=original.environment,
        description=original.description,
        tags=original.tags,
        forked_from=original,
    )
    
    # Increment fork count on original
    original.increment_forks()
    
    # Track activity
    activity, created = Activity.objects.get_or_create(
        user=request.user,
        date=date.today(),
        defaults={'snippet_count': 0, 'fork_count': 0}
    )
    activity.fork_count += 1
    activity.save()
    
    return JsonResponse({
        'success': True,
        'slug': fork.slug,
    })


@login_required
@require_POST
def like_snippet(request, slug):
    """Toggle like on a snippet"""
    snippet = get_object_or_404(Snippet, slug=slug)
    
    like, created = Like.objects.get_or_create(user=request.user, snippet=snippet)
    
    if not created:
        # Unlike
        like.delete()
        snippet.likes_count -= 1
        snippet.save()
        return JsonResponse({'success': True, 'liked': False, 'count': snippet.likes_count})
    else:
        # Like
        snippet.likes_count += 1
        snippet.save()
        return JsonResponse({'success': True, 'liked': True, 'count': snippet.likes_count})


@login_required
@require_POST
def add_comment(request, slug):
    """Add a comment to a snippet"""
    snippet = get_object_or_404(Snippet, slug=slug)
    data = json.loads(request.body)
    
    comment = Comment.objects.create(
        user=request.user,
        snippet=snippet,
        text=data.get('text', '')
    )
    
    return JsonResponse({
        'success': True,
        'comment': {
            'username': comment.user.username,
            'text': comment.text,
            'created_at': comment.created_at.isoformat(),
        }
    })


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
