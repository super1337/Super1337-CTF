from django.contrib import admin

from .models import Tag, TagAdmin


admin.site.register(Tag, TagAdmin)
