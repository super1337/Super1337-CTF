from django import forms
from .models import Questions,SimpleQuestion,MultipleChoiceQuestion

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question','hints','answer' )

class SimpleQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question','hints','answer' )

class MultipleChoiceQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question','hints','answer','choices','correct' )
