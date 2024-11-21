from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('create/', views.create_blog_view, name='create_blog'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('delete_blog/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('view_blog/<int:blog_id>/', views.view_blog, name='view_blog'),


]
