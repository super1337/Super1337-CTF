from django.contrib import admin

from .models import Challenge, ChallengeAdmin


admin.site.register(Challenge, ChallengeAdmin)
