from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=512, blank=True)

    def __str__(self):
        return str(self.name)


class Contest(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=False)
    tags = models.ManyToManyField(Tag)
    creators = models.ManyToManyField(User)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    STATE_CHOICES = ((1, 'Not Started'), (2, 'Ongoing'), (3, 'Ended'))
    state = models.CharField(max_length=15, choices=STATE_CHOICES, default=1)
