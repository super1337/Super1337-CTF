from django.contrib import admin

from .models import Quiz, SimpleQuestion, MultipleChoiceQuestion, Tag

admin.site.register([Quiz, SimpleQuestion, MultipleChoiceQuestion, Tag])
