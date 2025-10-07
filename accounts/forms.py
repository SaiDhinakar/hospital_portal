from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    email = forms.EmailField(required=True, label="Email Address")
    profile_pic = forms.ImageField(required=False, label="Profile Picture")
    address_line1 = forms.CharField(max_length=255, required=True, label="Address Line 1")
    city = forms.CharField(max_length=100, required=True, label="City")
    state = forms.CharField(max_length=100, required=True, label="State")
    pincode = forms.CharField(max_length=10, required=True, label="PIN Code")
    user_type = forms.ChoiceField(
        choices=CustomUser.USER_TYPE_CHOICES,
        required=True,
        label="Register as",
        widget=forms.RadioSelect
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'username', 'email',
            'password1', 'password2', 'user_type',
            'profile_pic', 'address_line1', 'city', 'state', 'pincode'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.user_type = self.cleaned_data['user_type']
        user.address_line1 = self.cleaned_data['address_line1']
        user.city = self.cleaned_data['city']
        user.state = self.cleaned_data['state']
        user.pincode = self.cleaned_data['pincode']
        
        if commit:
            user.save()
            if self.cleaned_data.get('profile_pic'):
                user.profile_pic = self.cleaned_data['profile_pic']
                user.save()
        return user