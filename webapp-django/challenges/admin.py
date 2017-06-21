from django.contrib import admin

from .models import Tag, Challenge

admin.site.register([Tag, Challenge])
