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
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    excerpt = models.CharField(max_length=300, blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True ,related_name='userـposts')
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