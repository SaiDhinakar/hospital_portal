from django.db import models
from django.conf import settings

class Post(models.Model):
    CATEGORY_OPTIONS = [
        ('mental_health', 'Mental Health'),
        ('heart_disease', 'Heart Disease'),
        ('covid19', 'COVID-19'),
        ('immunization', 'Immunization'),
        ('general_health', 'General Health'),
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
    ]
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    category = models.CharField(max_length=100, choices=CATEGORY_OPTIONS)
    summary = models.TextField()
    content = models.TextField()
    is_draft = models.BooleanField(default=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title