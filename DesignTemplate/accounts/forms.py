from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form for the custom User model"""
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
