from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    USER_TYPES = [
        ('business', 'Business'),
        ('customer', 'Customer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255, default="default")
    file = models.FileField(upload_to='profile_pictures/', null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    working_hours = models.CharField(max_length=50, null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='customer')  # Business or Customer

    email = models.EmailField(unique=True, null=True, blank=True)  # Allow null and blank to avoid migration issues
    created_at = models.DateTimeField( default=timezone.now)  # Set default for migrations

    def __str__(self):
        return self.user.username