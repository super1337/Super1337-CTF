from django.contrib import admin

from .models import Tag, Challenge, ChallengeAdmin

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Tag)
