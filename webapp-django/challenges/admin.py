from django.contrib import admin

from .models import Tag, Challenge, Document

admin.site.register([Tag, Challenge, Document])
