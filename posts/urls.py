from django.urls import path
from . import views

urlpatterns = [
    # List and create posts
    path('', views.post_list_create, name='post-list-create'),
    path('create/', views.post_create, name='post-create'),
    path('my-posts/', views.my_posts, name='my-posts'),
    path('drafts/', views.drafts, name='drafts'),
    
    # Individual post operations
    path('<int:pk>/', views.post_detail_modify, name='post-detail-modify'),
    path('<int:pk>/update/', views.post_update, name='post-update'),
    path('<int:pk>/delete/', views.post_delete, name='post-delete'),
]
