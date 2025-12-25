from django.urls import path
from . import views

app_name = 'playground'

urlpatterns = [
    # Feed/Homepage
    path('', views.feed, name='feed'),
    
    # Editor
    path('editor/', views.editor, name='editor'),
    path('editor/<slug:slug>/', views.editor, name='editor_edit'),
    
    # Snippet views
    path('snippet/<slug:slug>/', views.snippet_detail, name='detail'),
    path('snippet/<slug:slug>/preview/', views.snippet_preview, name='preview'),
    
    # API endpoints (AJAX)
    path('api/save/', views.save_snippet, name='save_snippet'),
    path('api/fork/<slug:slug>/', views.fork_snippet, name='fork_snippet'),
    path('api/like/<slug:slug>/', views.like_snippet, name='like_snippet'),
    path('api/comment/<slug:slug>/', views.add_comment, name='add_comment'),
    path('api/delete/<slug:slug>/', views.delete_snippet, name='delete_snippet'),
]
