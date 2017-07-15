from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Contest
from results.models import UserResult
from challenges.views import challenge


def index(request):
    contests = Contest.objects.all()
    # may be make this client side by filtering state in templates
    yet_to_begin = contests.filter(state='1')
    ongoing = contests.filter(state='2')
    ended = contests.filter(state='3')
    return render(request, 'contests/index.html', {'yet_to_begin': yet_to_begin, 'ongoing': ongoing, 'ended': ended})


def contest_view(request, name):
    try:
        contest = Contest.objects.get(name=name)
    except Contest.DoesNotExist:
        return HttpResponseRedirect('/contests/')
    if contest.state == '1':
        has_registered = check_registered_contests(request, contest)
        return render(request, 'contests/contest_1.html', {
            'contest': contest, 'has_registered': has_registered})
    elif contest.state == '2':
        challenges = contest.challenge_set.all()
        return render(request, 'contests/contest_2.html', {'contest': contest, 'challenges': challenges})
    elif contest.state == '3':
        challenges = contest.challenge_set.all()
        return render(request, 'contests/contest_3.html', {'contest': contest, 'challenges': challenges})


def challenge_solve(request,contest_name, challenge_name):
    return challenge(request, challenge_name, contest_name=contest_name)


def contest_register(request, name):
    user = request.user
    try:
        contest = Contest.objects.get(name=name)
    except Contest.DoesNotExist:
        return HttpResponseRedirect('/contests/')
    has_registered = check_registered_contests(request, contest)
    if not has_registered:
        user_result = UserResult.create(user, contest)
        user_result.save()
    return HttpResponseRedirect('/contests/'+name)


def check_registered_contests(request, contest):
    try:
        result_object = UserResult.objects.get(user=request.user.pk,contest=contest.pk)
        has_registered = True
    except UserResult.DoesNotExist:
        has_registered = False
    finally:
        return has_registered
