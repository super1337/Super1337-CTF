import os

from django.contrib import admin
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
    file = models.FileField(upload_to='challenges/', blank=True)
    
    score = models.IntegerField()
    tags = models.ManyToManyField(Tag)
    creators = models.ManyToManyField(User)

    hidden = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     '''On save, update timestamps '''
    #
    #     if not self.id:
    #         self.created = timezone.now()
    #     self.modified = timezone.now()
    #     return super(Challenge, self).save(*args, **kwargs)

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return str(self.name)


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('name', 'score', 'modified', 'created')
    search_fields = ('name', 'problem')
    raw_id_fields = ('creators',)
    list_filter = ('tags', 'score', 'modified', 'created', 'creators')
    ordering = ['name', 'score', 'creators', 'modified', 'created']
