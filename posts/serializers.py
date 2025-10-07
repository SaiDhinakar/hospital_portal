from .models import Post
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'image', 'category', 'summary', 'content', 'is_draft', 
                 'author', 'author_name', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']
    
    def get_author_name(self, obj):
        return f"Dr. {obj.author.first_name} {obj.author.last_name}" if obj.author else None