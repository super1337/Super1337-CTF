from django.contrib import admin

from .models import SimpleQuestion, MultipleChoiceQuestion, Tag

admin.site.register([SimpleQuestion, MultipleChoiceQuestion, Tag])
