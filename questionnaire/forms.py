from django import forms

from .models import SimpleQuestion, MCQ


class SimpleQuestionForm(forms.ModelForm):
    class Meta:
        model = SimpleQuestion
        fields = ('question', 'hints', 'answer')


class MCQ(forms.ModelForm):
    class Meta:
        model = MCQ
        fields = ('question', 'hints', 'answer', 'choices', 'correct')
