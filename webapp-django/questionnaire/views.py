from django.shortcuts import render
from .models import Question, MultipleChoiceQuestion

def mcq(request):
    return render(request,'questionnaire/mcq.html',{})
