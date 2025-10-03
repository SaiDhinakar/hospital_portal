from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = [
            "first_name", "last_name", "profile_pic", "username", "email",
            "password1", "password2", "address_line1", "city", "state", "pincode", "user_type"
        ]
