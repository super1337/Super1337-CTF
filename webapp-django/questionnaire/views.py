from itertools import chain

from django.shortcuts import render

from .models import SimpleQuestion, MultipleChoiceQuestion


def index(request):
    pass


def questions(request):
    questions = list(chain(SimpleQuestion.objects.all(), MultipleChoiceQuestion.objects.all()))
    print(questions)

    return render(request, 'questions.html', {'questions': questions})
