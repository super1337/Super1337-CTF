from django.contrib import admin
from .models import Question, SimpleQuestion, MultipleChoiceQuestion


admin.site.register([Question, SimpleQuestion, MultipleChoiceQuestion])
