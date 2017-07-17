from django.shortcuts import render, redirect

from .models import Contest
from results.models import ContestResult
from challenges.views import challenge


def index(request, messages=None):
    if messages is not None:
        messages = {'success': [], 'info': [], 'warning': [], 'danger': []}

    contests = Contest.objects.all()
    # may be make this client side by filtering state in templates
    yet_to_begin = contests.filter(state='1')
    ongoing = contests.filter(state='2')
    ended = contests.filter(state='3')
    return render(request, 'contests/index.html', {
        'yet_to_begin': yet_to_begin, 'ongoing': ongoing, 'ended': ended, 'messages': messages})


def contest_view(request, contest_name, messages=None):
    if messages is not None:
        messages = {'success': [], 'info': [], 'warning': [], 'danger': []}

    try:
        contest = Contest.objects.get(name=contest_name)
    except Contest.DoesNotExist:
        return redirect('contests.views.index', messages={
            'warning': ['No contest with name - {}'.format(contest_name)]})

    if contest.state == '1':
        has_registered = check_registered_contests(request, contest)
        return render(request, 'contests/contest_1.html', {
            'contest': contest, 'has_registered': has_registered, 'messages': messages})
    elif contest.state == '2':
        challenges = contest.challenge_set.all()
        return render(request, 'contests/contest_2.html', {
            'contest': contest, 'challenges': challenges, 'messages': messages})
    elif contest.state == '3':
        challenges = contest.challenge_set.all()
        return render(request, 'contests/contest_3.html', {
            'contest': contest, 'challenges': challenges, 'messages':messages})


def challenge_solve(request,contest_name, challenge_name):
    return challenge(request, challenge_name, contest_name)


def contest_register(request, contest_name):
    user = request.user
    try:
        contest = Contest.objects.get(name=contest_name)
    except Contest.DoesNotExist:
        return redirect('contests.views.index', messages={
            'warning': ['No contest with name - {}'.format(contest_name)]})
    has_registered = check_registered_contests(request, contest)
    if not has_registered:
        user_result = ContestResult.create(user, contest)
        user_result.save()
    return redirect('contests.views.contest_view', contest_name=contest_name)


def check_registered_contests(request, contest):
    try:
        result_object = ContestResult.objects.get(user=request.user.pk,contest=contest.pk)
        has_registered = True
    except ContestResult.DoesNotExist:
        has_registered = False
    finally:
        return has_registered
