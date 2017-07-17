from django import forms

from .models import SimpleQuestion, MCQ


class SimpleQuestionForm(forms.ModelForm):
    class Meta:
        model = SimpleQuestion
        fields = 'answer'


class MCQForm(forms.ModelForm):
    class Meta:
        model = MCQ
        fields = 'correct'
