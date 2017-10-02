from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class Contest(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=16, unique=True)
    initial_description = models.CharField(max_length=512, blank=False)
    ongoing_description = models.CharField(max_length=512, blank=False)
    tags = models.ManyToManyField(Tag)
    creators = models.ManyToManyField(User)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    STATE_CHOICES = (('1', 'Not Started'), ('2', 'Ongoing'), ('3', 'Ended'))
    state = models.CharField(max_length=16, choices=STATE_CHOICES, default=1)

    def __str__(self):
        return self.name


class ContestAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'modified', 'created', 'state')
    search_fields = ('name', )
    raw_id_fields = ('creators',)
    # readonly_fields = ('state',)
    list_filter = ('tags', 'state', 'created', 'creators')
    ordering = ['name', 'start_time', 'end_time', 'modified', 'created', 'state']
