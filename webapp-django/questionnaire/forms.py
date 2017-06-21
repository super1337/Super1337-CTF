from django import forms

from .models import SimpleQuestion, MultipleChoiceQuestion


class SimpleQuestionForm(forms.ModelForm):
    class Meta:
        model = SimpleQuestion
        fields = ('question', 'hints', 'answer')


class MultipleChoiceQuestionForm(forms.ModelForm):
    class Meta:
        model = MultipleChoiceQuestion
        fields = ('question', 'hints', 'answer', 'choices', 'correct')
