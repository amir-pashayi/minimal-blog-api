from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from .managers import UserManager


class User(AbstractBaseUser):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]


    phone = models.CharField(
        max_length=11,
        unique=True,
        validators=[
            RegexValidator(regex=r'^09\d{9}$', message="شماره موبایل باید با 09 شروع شده و 11 رقم باشد.")
        ]
    )
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    age = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    gender = models.CharField(choices=GENDER_CHOICES ,max_length=10 ,blank=True ,null=True)
    author = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']


    def __str__(self):
        return f"{self.phone} - {self.full_name or 'کاربر'}"

    @property
    def full_name(self):
        return f"{self.name or ''} {self.last_name or ''}".strip() if self.name or self.last_name else "کاربر"


    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-id']