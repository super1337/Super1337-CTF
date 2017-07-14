from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

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
    except ObjectDoesNotExist:
        return redirect('contests.views.index')
    if contest.state == '1':
        return render(request, 'contests/contest_1.html', {'contest': contest, 'state' : contest.state })
    elif contest.state == '2':
        pass
    elif contest.state == '3':
        pass
    # check this, return if i return in above region /contest/name does'nt work
    return render(request, 'contests/contest_1.html', {'contest': contest, 'state' : contest.state })


# nothing as registration yet to keep things simple

def contest_register(request, name):
    try:
        contest = Contest.objects.get(Contest, name=name)
    except ObjectDoesNotExist:
        return redirect('contests.views.index')
    has_registered = check_registered_contests(request, contest)
    if not has_registered:
        UserResult.create()

    return render(request, 'contests/contest_1.html', {'contest': contest, 'has_registered': has_registered})


def check_registered_contests(request, contest):
    try:
        list_contained_contest = request.user.userprofile.registered_contests.filter(name=contest.name)
        has_registered = True
    except:
        has_registered = False
    finally:
        return has_registered
