from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from posts.models import Post

@login_required
def index(request):
    # Get all published posts by doctors (not drafts)
    posts = Post.objects.filter(is_draft=False).order_by('-created_at')[:6]  # Show latest 6 posts
    return render(request, 'dashboard/index.html', {'posts': posts})