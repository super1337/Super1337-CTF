import os

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return str(self.name)


class Challenge(models.Model):
    name = models.CharField(max_length=16, unique=True)
    problem = models.CharField(max_length=256)
    hints = models.CharField(max_length=256, blank=True)
    flag = models.CharField(max_length=256)
    score = models.IntegerField()
    file = models.FileField(upload_to='challenges/', blank=True)

    tags = models.ManyToManyField(Tag)
    creators = models.ManyToManyField(User)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        '''On save, update timestamps '''

        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Challenge, self).save(*args, **kwargs)

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return str(self.name)