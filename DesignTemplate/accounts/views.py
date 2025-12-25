from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import User, Activity
from .forms import CustomUserCreationForm, UserSettingsForm
from playground.models import Snippet
from datetime import date, timedelta


def signup(request):
    """User registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('playground:feed')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def user_profile(request, username):
    """User profile page with snippets and contribution graph"""
    profile_user = get_object_or_404(User, username=username)
    
    # Get user's public snippets
    snippets = Snippet.objects.filter(user=profile_user, is_public=True).order_by('-created_at')
    pinned_snippets = snippets.filter(is_pinned=True)[:3]
    
    # Get activity data for contribution graph (last 365 days)
    end_date = date.today()
    start_date = end_date - timedelta(days=365)
    activities = Activity.objects.filter(
        user=profile_user,
        date__gte=start_date,
        date__lte=end_date
    ).order_by('date')
    
    # Format activity data for JavaScript
    activity_data = [
        {
            'date': activity.date.isoformat(),
            'count': activity.snippet_count + activity.fork_count,
        }
        for activity in activities
    ]
    
    context = {
        'profile_user': profile_user,
        'snippets': snippets[:12],  # Show latest 12
        'pinned_snippets': pinned_snippets,
        'activity_data': activity_data,
        'is_own_profile': request.user == profile_user,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def user_settings(request):
    """User settings page"""
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile', username=request.user.username)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserSettingsForm(instance=request.user)
    
    return render(request, 'accounts/settings.html', {'form': form})
