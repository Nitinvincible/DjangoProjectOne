from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form for the custom User model"""
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserSettingsForm(forms.ModelForm):
    """Form for user profile settings"""
    
    class Meta:
        model = User
        fields = ['avatar', 'avatar_url', 'bio', 'github_profile', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Tell us about yourself...',
            }),
            'github_profile': forms.URLInput(attrs={
                'placeholder': 'https://github.com/yourusername',
            }),
            'website': forms.URLInput(attrs={
                'placeholder': 'https://yourwebsite.com',
            }),
            'avatar_url': forms.URLInput(attrs={
                'placeholder': 'https://example.com/avatar.jpg',
            }),
            'avatar': forms.FileInput(attrs={
                'accept': 'image/*',
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        avatar = cleaned_data.get('avatar')
        avatar_url = cleaned_data.get('avatar_url')
        
        # Clear avatar_url if a new file is uploaded
        if avatar:
            cleaned_data['avatar_url'] = ''
        
        return cleaned_data
