from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import datetime


class Blog(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('post', 'Post'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=100, blank=True)  # Comma-separated tags
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='post')
    cover_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    views_count = models.PositiveIntegerField(default=0)
    comments_allowed = models.BooleanField(default=True)
    likes_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

    # Add additional fields like profile picture

    def __str__(self):
        return self.user.username


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'blog')
