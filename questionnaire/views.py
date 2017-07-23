from django.shortcuts import render, redirect

from .models import Quiz, Question
from contests.models import Contest


def index(request):
    messages = {'success': [], 'info': [], 'warning': [], 'danger': []}

    sort = request.GET.get('sort')
    if sort not in ['modified', 'created']:
        if sort is not None:
            messages['info'].append('Cannot sort by {}! Sorting by \'created\' instead.!'.format(sort))
        sort = 'created'

    quizzes = Quiz.objects.all()
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
        quiz = Quiz.objects.get(slug=quiz_slug)
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
            'warning': ['No question with slug - {}'.format(question_slug)]})

    # If user opens challenges other than the ones in contest through contest tab
    # redirect them away from getting unnecessary score
    if is_in_contest:
        if quiz not in contest.quiz_set.all():
            return redirect('contests.views.contest_view', contest_slug=contest_slug, messages={
                'warning': ['No quiz with slug - {}'.format(quiz_slug)]})
        if ques not in quiz.question_set.all():
            return redirect('contests.views.quiz', contest_slug=contest_slug, quiz_slug=quiz_slug, messages={
                'warning': ['No question with slug - {}'.format(quiz_slug)]})

    # main challenge checking code
    # makes necessary changes to user challenge and ContestResult objects
    if request.method == 'POST':
        if request.user.is_authenticated():
            form = Form(request.POST)
            if form.is_valid():
                if form.cleaned_data['flag'] == chal.flag:
                    if chal not in request.user.userprofile.solved_challenges.all():
                        request.user.userprofile.solved_challenges.add(chal)
                        request.user.userprofile.save()
                        chal.solve_count += 1
                        chal.save()
                    if is_in_contest:
                        try:
                            contest_result = ContestResult.objects.get(user=request.user.pk, contest=contest.pk)
                        except ContestResult.DoesNotExist:
                            return redirect('contests.views.contest_register')
                        finally:
                            if chal not in contest_result.solved_challenges.all():
                                contest_result.solved_challenges.add(chal)
                                contest_result.score += chal.score

                    messages['success'].append('You did it! You solved the challenge successfully!')
                else:
                    messages['info'].append('Sorry! You got it wrong. Try harder')
        else:
            messages['danger'].append('You must be logged in to submit flags')
            form = FlagForm()
        return render(request, 'challenges/challenge.html', {'challenge': chal, 'form': form, 'messages': messages})

    else:
        form = FlagForm()

    return render(request, 'challenges/challenge.html', {'challenge': chal, 'form': form, 'messages': messages})
