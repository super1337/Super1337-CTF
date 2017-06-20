from django.shortcuts import render

from .models import Question, MultipleChoiceQuestion


def index(request):
    pass


def questions(request):
    ques = MultipleChoiceQuestion.objects.all() + Question.objects.all()
    questions = []

    p = 0
    for h in que:
        p += 1
        q = 0
        qu = [h['question']]
        ch = []
        for i in h.choices:
            q += 1
            ch += [[q, i]]
        qu += [[ch]]
        questions += [qu]

    return render(request, 'questions.html', {'questions': questions})
