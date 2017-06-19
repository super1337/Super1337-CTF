from django.shortcuts import render
from .models import Question, MultipleChoiceQuestion

def mcq(request):
    questions=MultipleChoiceQuestion.objects.all()
    return render(request,'questionnaire/mcq.html',{'questions':questions})
