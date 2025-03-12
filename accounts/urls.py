from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('create/', views.create_post, name='create_post'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('add_comment/<int:post_id>/<int:parent_comment_id>/', views.add_comment, name='add_reply'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('news_feed/', views.news_feed, name='news_feed'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'), 
    path('my_profile/', views.my_profile, name='my_profile'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('search/', views.search, name='search'),
]