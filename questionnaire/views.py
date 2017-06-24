from itertools import chain

from django.shortcuts import render

from .models import SimpleQuestion, MultipleChoiceQuestion


def index(request):
    return render(request,'questionnaire/index.html',{})

def contest(request):
    return render(request,'questionnaire/contest.html',{})


def questions(request):
    questions = list(chain(SimpleQuestion.objects.all(), MultipleChoiceQuestion.objects.all()))
    print(questions)

    return render(request, 'questionnaire/questions.html', {'questions': questions})
