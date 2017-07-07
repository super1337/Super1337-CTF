from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Contest(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    creators = models.ManyToManyField(User)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
