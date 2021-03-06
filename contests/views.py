from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Contest
from results.models import ContestResult
from challenges.views import challenge
from questionnaire.views import question


def index(request):
    contests = Contest.objects.all()

    yet_to_begin = contests.filter(state='1')
    ongoing = contests.filter(state='2')
    ended = contests.filter(state='3')
    return render(request, 'contests/index.html', {
        'yet_to_begin': yet_to_begin, 'ongoing': ongoing, 'ended': ended})


def contest_view(request, contest_slug):
    try:
        contest = Contest.objects.get(slug=contest_slug)
    except Contest.DoesNotExist:
        messages.warning(request, 'No contest with slug - {}'.format(contest_slug))
        return redirect('contests.views.index')

    if contest.state == '1':
        has_registered = check_registered_contests(request, contest)
        return render(request, 'contests/contest_1.html', {
            'contest': contest, 'has_registered': has_registered})
    elif contest.state == '2':
        challenges = contest.challenge_set.all()
        return render(request, 'contests/contest_2.html', {
            'contest': contest, 'challenges': challenges})
    elif contest.state == '3':
        challenges = contest.challenge_set.all()
        return render(request, 'contests/contest_3.html', {
            'contest': contest, 'challenges': challenges})


def challenge_solve(request, contest_slug, challenge_slug):
    return challenge(request, challenge_slug, contest_slug)


def question_solve(request, contest_slug, quiz_slug, question_slug):
    return question(request, question_slug, quiz_slug, contest_slug)


def contest_register(request, contest_slug):
    user = request.user

    try:
        contest = Contest.objects.get(slug=contest_slug)
    except Contest.DoesNotExist:
        messages.warning(request, 'No contest with slug - {}'.format(contest_slug))
        return redirect('contests.views.index')
    has_registered = check_registered_contests(request, contest)
    if not has_registered:
        contest_result = ContestResult.create(user, contest)
        contest_result.save()
    return redirect('contests.views.contest_view', contst_slug=contest_slug)


def check_registered_contests(request, contest):
    try:
        ContestResult.objects.get(user=request.user.pk,contest=contest.pk)
        has_registered = True
    except ContestResult.DoesNotExist:
        has_registered = False
    finally:
        return has_registered
