from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import admin


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

    STATE_CHOICES = (('1', 'Not Started'), ('2', 'Ongoing'), ('3', 'Ended'))
    state = models.CharField(max_length=15, choices=STATE_CHOICES, default=1)

    def __str__(self):
        return self.name


class ContestAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'modified', 'created', 'state')
    search_fields = ('name', )
    raw_id_fields = ('creators',)
    # readonly_fields = ('state',)
    list_filter = ('tags', 'state', 'created', 'creators')
    ordering = ['name', 'start_time', 'end_time', 'modified', 'created', 'state']


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ['name']
