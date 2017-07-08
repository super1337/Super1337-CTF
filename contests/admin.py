from django.contrib import admin
from .models import Tag, TagAdmin, Contest, ContestAdmin

# Register your models here.

admin.site.register(Tag, TagAdmin)
admin.site.register(Contest, ContestAdmin)
