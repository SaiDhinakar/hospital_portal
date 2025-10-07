from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from .models import Post
from .forms import PostForm


@login_required
def post_list_create(request):
    """
    List all published posts for everyone to view
    """
    posts = Post.objects.filter(is_draft=False).order_by('-created_at')
    return render(request, 'dashboard/index.html', {'posts': posts})


@login_required
def post_detail_modify(request, pk):
    """
    View a specific post detail
    """
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})


@login_required
def post_create(request):
    """
    Create a new post - doctors only
    """
    if request.user.user_type != 'doctor':
        messages.error(request, 'Only doctors can create posts.')
        return redirect('post-list-create')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post-detail-modify', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'posts/post_create.html', {'form': form})


@login_required
def post_update(request, pk):
    """
    Update a post - doctors only, and only their own posts
    """
    post = get_object_or_404(Post, pk=pk)
    
    if request.user.user_type != 'doctor':
        messages.error(request, 'Only doctors can update posts.')
        return redirect('post-detail-modify', pk=pk)

    if post.author != request.user:
        messages.error(request, 'You can only update your own posts.')
        return redirect('post-detail-modify', pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post-detail-modify', pk=pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/post_edit.html', {'form': form, 'post': post})


@login_required
def post_delete(request, pk):
    """
    Delete a post - doctors only, and only their own posts
    """
    post = get_object_or_404(Post, pk=pk)
    
    if request.user.user_type != 'doctor':
        messages.error(request, 'Only doctors can delete posts.')
        return redirect('post-detail-modify', pk=pk)

    if post.author != request.user:
        messages.error(request, 'You can only delete your own posts.')
        return redirect('post-detail-modify', pk=pk)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('post-list-create')

    return render(request, 'posts/post_confirm_delete.html', {'post': post})


@login_required
def my_posts(request):
    """
    Show all posts (published and drafts) created by the logged-in doctor
    """
    if request.user.user_type != 'doctor':
        messages.error(request, 'Only doctors can view their posts.')
        return redirect('dashboard')

    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'posts/my_posts.html', {'posts': posts})


@login_required
def drafts(request):
    """
    Show only draft posts created by the logged-in doctor
    """
    if request.user.user_type != 'doctor':
        messages.error(request, 'Only doctors can view drafts.')
        return redirect('dashboard')

    posts = Post.objects.filter(author=request.user, is_draft=True).order_by('-created_at')
    return render(request, 'posts/drafts.html', {'posts': posts})
