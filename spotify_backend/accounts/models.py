from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    profile_picture = models.URLField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    is_premium = models.BooleanField(default=False)

    # Thêm related_name để tránh xung đột
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Đổi từ 'user_set' thành 'customuser_set'
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Đổi từ 'user_set' thành 'customuser_set'
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username