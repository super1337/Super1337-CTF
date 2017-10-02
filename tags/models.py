from django.db import models
from django.contrib import admin


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
    description = models.TextField(blank=False)

    def __str__(self):
        return str(self.name)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ['name']
    prepopulated_fields = {'slug' : ('name', 'description')}
