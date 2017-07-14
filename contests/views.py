from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .models import Contest
from results.models import UserResult


def index(request):
    contests = Contest.objects.all()
    # may be make this client side by filtering state in templates
    yet_to_begin = contests.filter(state='1')
    ongoing = contests.filter(state='2')
    ended = contests.filter(state='3')
    return render(request, 'contests/index.html', {'yet_to_begin': yet_to_begin, 'ongoing': ongoing, 'ended': ended})


# needs to be improvised
def contest_view(request, name):
    try:
        contest = Contest.objects.get(name=name)
    except Contest.DoesNotExist:
        return HttpResponseRedirect('/contests/')
    if contest.state == '1':
        has_registered = check_registered_contests(request, contest)
        return render(request, 'contests/contest_1.html', {
            'contest': contest, 'state' : contest.state, 'has_registered': has_registered
        })
    elif contest.state == '2':
        pass
    elif contest.state == '3':
        pass
    # check this, return if i return in above region /contest/name does'nt work
    return render(request, 'contests/contest_1.html', {'contest': contest, 'state': contest.state})


# nothing as registration yet to keep things simple

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
        list_contained_contest = UserResult.objects.get(user=request.user.pk,contest=contest.pk)
        has_registered = True
    except UserResult.DoesNotExist:
        has_registered = False
    finally:
        return has_registered
