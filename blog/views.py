from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Like
from django.contrib.auth.decorators import login_required
from django.http import Http404
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


# Home view
def home_view(request):
    blogs = Blog.objects.filter(status='published').order_by('-timestamp')
    return render(request, 'home.html', {'blogs': blogs})


# Blog detail view
def blog_detail_view(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    user_liked = False

    # Check if the user has liked the blog post
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(blog=blog, user=request.user).exists()

    return render(request, 'blog_detail.html', {
        'blog': blog,
        'user_liked': user_liked,
    })


# Like/unlike a blog
@login_required
def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    user = request.user

    # Check if the user has already liked the blog post
    like_exists = Like.objects.filter(blog=blog, user=user).exists()

    if like_exists:
        # If user has already liked the blog, remove the like
        Like.objects.filter(blog=blog, user=user).delete()
        blog.likes_count -= 1  # Decrease the like count
    else:
        # If user hasn't liked the blog, add the like
        Like.objects.create(blog=blog, user=user)
        blog.likes_count += 1  # Increase the like count

    blog.save()
    return redirect('blog_detail', blog_id=blog.id)  # Redirect to the blog detail page


# Create a new blog post
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


# Edit blog post
@login_required
def edit_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        blog.title = request.POST['title']
        blog.content = request.POST['content']
        blog.save()
        return redirect('blog_detail', blog_id=blog.id)
    return render(request, 'edit_blog.html', {'blog': blog})


# Delete blog post
@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.author == request.user:
        blog.delete()
        return redirect('home')
    else:
        raise Http404("You are not authorized to delete this blog.")


# View a single blog post (this can be redundant if using blog_detail_view)
def view_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})


# Signup view
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


# Login view
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


# Profile view
@login_required
def profile_view(request):
    blogs = Blog.objects.filter(author=request.user)
    blogs_count = blogs.count()

    return render(request, 'profile.html', {
        'user': request.user,
        'blogs': blogs,
        'blogs_count': blogs_count
    })
