from django.shortcuts import render

from .models import Quiz


def index(request):
    quizzes = Quiz.objects.all()
    return render(request, 'questionnaire/index.html', {'quizzes': quizzes})


def quiz(request, name):
    messages = {'success': [], 'info': [], 'warning': [], 'danger': []}

    sort = request.GET.get('sort')
    if sort not in ['modified', 'created', 'score']:
        messages['info'].append('Cannot sort by {}! Sorting by \'created\' instead.!'.format(name))
        sort = 'created'

    try:
        quiz = Quiz.objects.get(name=name)
    except Quiz.DoesNotExist:
        messages['danger'].append('The quiz {} does not exist!'.format(name))
        questions = []

    else:
        questions = quiz.question_set.all()

    return render(request, 'challenges/index.html', {'questions': questions, 'messages': messages})
