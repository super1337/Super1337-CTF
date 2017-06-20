from django import forms
from .models import Questions

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question','hints','answer' )
