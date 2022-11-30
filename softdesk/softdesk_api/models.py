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
    role = models.CharField(choices=ROLES, max_length=11)

class Issue(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2048)
    TAGS =  [
        ('BUG', 'BUG'),
        ('TASK', 'TASK'),
        ('IMPROVMENT', 'IMPROVMENT')
    ]
    tag = models.CharField(choices=TAGS, max_length=10)
    PRIORITIES = [
        ('HIGH', 'HIGH'),
        ('MEDIUM', 'MEDIUM'),
        ('LOW', 'LOW')
    ]
    priority = models.CharField(choices=PRIORITIES, max_length=6)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    STATUSES = [
        ('TODO', 'TODO'),
        ('INPROGRESS', 'INPROGRESS'),
        ('DONE', 'DONE')
    ]
    status = models.CharField(choices=STATUSES, max_length=10)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assigned_user = models.ForeignKey(to=Contributor, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    description = models.TextField(max_length=2048)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


