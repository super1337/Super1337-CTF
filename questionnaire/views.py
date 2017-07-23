from django.shortcuts import render, redirect

from .forms import MCQForm, SimpleQuestionForm
from .models import Quiz, Question
from contests.models import Contest
from results.models import ContestResult, QuizResult


def index(request, messages=None):
    if messages is not None:
        messages = {'success': [], 'info': [], 'warning': [], 'danger': []}

    sort = request.GET.get('sort')
    if sort not in ['modified', 'created']:
        if sort is not None:
            messages['info'].append('Cannot sort by {}! Sorting by \'created\' instead.!'.format(sort))
        sort = 'created'

    quizzes = Quiz.objects.all().order_by(sort)
    return render(request, 'questionnaire/index.html', {'quizzes': quizzes, 'messages': messages})


def quiz(request, quiz_slug, contest_slug, messages=None):
    if messages is not None:
        messages = {'success': [], 'info': [], 'warning': [], 'danger': []}

    # Get contest object or redirect to contests.views.index
    if contest_slug is not None:
        is_in_contest = True
        try:
            contest = Contest.objects.get(slug=contest_slug)
        except Contest.DoesNotExist:
            return redirect('contests.views.index',
                            messages={'warning': ['No contest with slug - {}'.format(contest_slug)]})
    else:
        is_in_contest = False

    sort = request.GET.get('sort')
    if sort not in ['modified', 'created', 'score']:
        if sort is not None:
            messages['info'].append('Cannot sort by {}! Sorting by \'created\' instead.!'.format(sort))
        sort = 'created'

    try:
        quiz = Quiz.objects.get(slug=quiz_slug)
    except Quiz.DoesNotExist:
        messages['danger'].append('The quiz {} does not exist!'.format(quiz_slug))
        questions = []
    else:
        questions = quiz.question_set.all()

    # Makes challenge inaccessible out of contest even when user try with url manipulation
    if quiz.hidden and (not is_in_contest):
        return redirect('questionnaire.views.index', messages={
            'warning': ['No quiz with slug - {}'.format(quiz_slug)]})

    return render(request, 'questionnaire/quiz.html', {'quiz': quiz, 'questions': questions, 'messages': messages})


def question(request, question_slug, quiz_slug, contest_slug=None, messages=None):
    if messages is not None:
        messages = {'success': [], 'info': [], 'warning': [], 'danger': []}

        # Get contest object or redirect to contests.views.index
        if contest_slug is not None:
            is_in_contest = True
            try:
                contest = Contest.objects.get(slug=contest_slug)
            except Contest.DoesNotExist:
                return redirect('contests.views.index',
                                messages={'warning': ['No contest with slug - {}'.format(contest_slug)]})
        else:
            is_in_contest = False

    try:
        ques = Question.objects.get(slug=question_slug)
    except Question.DoesNotExist:
        if is_in_contest:
            return redirect('questionnaire.views.quiz', contest_slug=contest_slug, quiz_slug=quiz_slug, messages={
                'warning': ['No question with slug - {}'.format(question_slug)]})
        else:
            return redirect('questionnaire.views.index', messages={
                'warning': ['No question with slug - {}'.format(question_slug)]})

    # Get challenge or redirect according to in contest or challenge tab
    try:
        quiz_obj = Quiz.objects.get(slug=quiz_slug)
    except Quiz.DoesNotExist:
        if is_in_contest:
            return redirect('contests.views.contest_view', contest_slug=contest_slug, messages={
                'warning': ['No quiz with slug - {}'.format(quiz_slug)]})
        else:
            return redirect('questionnaire.views.index', messages={
                'warning': ['No quiz with slug - {}'.format(quiz_slug)]})

    # Makes challenge inaccessible out of contest even when user try with url manipulation
    if quiz.hidden and (not is_in_contest):
        return redirect('questionnaire.views.index', messages={
            'warning': ['No quiz with slug - {}'.format(quiz_slug)]})

    # If user opens challenges other than the ones in contest through contest tab
    # redirect them away from getting unnecessary score
    if is_in_contest:
        if quiz_obj not in contest.quiz_set.all():
            return redirect('contests.views.contest_view', contest_slug=contest_slug, messages={
                'warning': ['No quiz with slug - {}'.format(quiz_slug)]})
        if ques not in quiz_obj.question_set.all():
            return redirect('contests.views.quiz', contest_slug=contest_slug, quiz_slug=quiz_slug, messages={
                'warning': ['No question with slug - {}'.format(quiz_slug)]})

    # set form
    if ques.is_mcq:
        form = MCQForm(request.POST)
    else:
        form = SimpleQuestionForm(request.POST)

    # main challenge checking code
    # makes necessary changes to user challenge and ContestResult objects
    if request.method == 'POST':
        if request.user.is_authenticated():
            if form.is_valid():
                if str(form.cleaned_data['answer']).lower() == str(ques.answer).lower():
                    quiz_result = quiz_result_get_or_create(request, quiz_obj, contest)
                    if ques not in quiz_result.correct_questions.all():
                        quiz_result.correct_questions.add(ques)
                        quiz_result.score += ques.score
        else:
            messages['danger'].append('You must be logged in to submit flags')
        return render(request, 'challenges/challenge.html', {'question': ques, 'form': form, 'messages': messages})

    else:
        messages['info'].append('You\'re response has been recorded.')

    return render(request, 'challenges/challenge.html', {'question': ques, 'form': form, 'messages': messages})


# gets or create quiz_result on basis of whether quiz_result should be linked with
# contest_result or not auto add quiz_result to mtm field quiz_results of contest_result
def quiz_result_get_or_create(request, quiz_obj, contest_obj=None):
    user = request.user
    try:
        if contest_obj is None:
            quiz_result = QuizResult.objects.get(user=request.user.pk, quiz=quiz_obj.pk)
        else:
            quiz_result = QuizResult.objects.get(user=request.user.pk, quiz=quiz_obj.pk, contest=contest_obj.pk)
    except QuizResult.DoesNotExist:
        if contest_obj is None:
            quiz_result = QuizResult.create(user, quiz_obj)
        else:
            quiz_result = QuizResult.create(user, quiz_obj, contest_obj)
            try:
                contest_result = ContestResult.objects.get(user=request.user.pk, contest=contest_obj.pk)
            except ContestResult.DoesNotExist:
                contest_result = ContestResult.create(user, contest_obj)
            finally:
                if quiz_result not in contest_result.quiz_results.all():
                    contest_result.quiz_results.add(quiz_result)
                    contest_result.save()
        quiz_result.save()
    finally:
        return quiz_result
