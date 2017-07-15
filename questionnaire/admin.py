from django.contrib import admin

from .models import Quiz, SimpleQuestion, MCQ, QuizAdmin, SimpleQuestionAdmin, MCQAdmin

admin.site.register(Quiz, QuizAdmin)
admin.site.register(SimpleQuestion, SimpleQuestionAdmin)
admin.site.register(MCQ, MCQAdmin)

