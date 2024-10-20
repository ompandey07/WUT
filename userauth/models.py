from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    registration_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
    
class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s post at {self.created_at}"

    class Meta:
        ordering = ['-created_at']