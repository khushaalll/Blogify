from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, LoginForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Blog
from .forms import BlogForm
from django.http import HttpResponseForbidden

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def home_view(request):
    blogs = Blog.objects.filter(status='published').order_by('-timestamp')
    return render(request, 'home.html', {'blogs': blogs})


@login_required
def create_blog_view(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Blog created successfully!')
            return redirect('home')
    else:
        form = BlogForm()
    return render(request, 'create_blog.html', {'form': form})


@login_required
def profile_view(request):
    # Get the user's blogs
    blogs = Blog.objects.filter(author=request.user)
    blogs_count = blogs.count()

    return render(request, 'profile.html', {
        'user': request.user,
        'blogs': blogs,
        'blogs_count': blogs_count
    })


@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    # Check if the logged-in user is the author of the blog post
    if blog.author == request.user:
        blog.delete()
        return redirect('profile')
    else:
        return HttpResponseForbidden("You are not allowed to delete this post.")


@login_required
def view_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog/view_blog.html', {'blog': blog})

