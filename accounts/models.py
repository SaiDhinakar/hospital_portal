from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    
    # AbstractUser already provides: username, first_name, last_name, email, password
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='patient')
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    address_line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
