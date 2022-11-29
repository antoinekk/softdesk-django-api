from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2048)
    TYPES = [
        ('BACKEND', 'BACKEND'),
        ('FRONTEND', 'FRONTEND'),
        ('iOS', 'iOS'),
        ('ANDROID', 'ANDROID')
    ]
    type = models.CharField(choices=TYPES, max_length=8)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Contributor(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    ROLES = [
        ('AUTHOR', 'AUTHOR'),
        ('CONTRIBUTOR', 'CONTRIBUTOR')
    ]
    role = models.CharField(max_length=11, choices=ROLES, default='CONTRIBUTOR')

class Issue(models.Model):
    pass

class Comment(models.Model):
    pass
