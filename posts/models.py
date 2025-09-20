from django.db import models
from accounts.models import User
from ckeditor.fields import RichTextField
from django.utils.text import slugify


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('private', 'Private'),
    ]

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='posts/%Y/%m/%d/')
    description = RichTextField()
    reading_time = models.PositiveSmallIntegerField(default=1)
    categories = models.ManyToManyField('Category', related_name='posts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    excerpt = models.CharField(max_length=300, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True ,related_name='user_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PostLike(models.Model):
    VALUE_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.CharField(max_length=10, choices=VALUE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'PostLike'
        verbose_name_plural = 'PostLikes'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post_vote')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.post.title} - {self.value}"