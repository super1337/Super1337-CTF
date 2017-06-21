from django.contrib import admin

from .models import SimpleQuestion, MultipleChoiceQuestion

admin.site.register([SimpleQuestion, MultipleChoiceQuestion])
