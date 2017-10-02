from django.contrib import admin
from .models import Contest, ContestAdmin


admin.site.register(Contest, ContestAdmin)
