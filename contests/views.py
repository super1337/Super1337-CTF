from django.shortcuts import render, redirect, get_object_or_404
from .models import Contest

# Create your views here.


def index(request):
    contests = Contest.objects.all()
    yet_to_begin = contests.filter(state=1)
    ongoing = contests.filter(state=2)
    ended = contests.filter(state=3)
    return render(request, 'contests/index.html', {'yet_to_begin': yet_to_begin, 'ongoing': ongoing, 'ended': ended})


# needs to be improvised
def contest_view(request, name):
    contest = get_object_or_404(Contest, name=name)
    print("contest", contest)
    has_registered = check_registered_contests(request, contest)
    print("has_registered", has_registered)
    if contest.state == 1:
        pass
    # check this, return if i return in above region /contest/name does'nt work
    return render(request, 'contests/contest_1.html', {'contest': contest, 'has_registered':has_registered})


def contest_register(request, name):
    contest = get_object_or_404(Contest, name=name)
    has_registered = check_registered_contests(request, contest)
    if has_registered:
        contest.users_registered.add(request.user)
        contest.save()
        request.user.userprofile.registered_contests.add(contest)
        request.user.userprofile.save()
    return render(request, 'contests/contest_1.html', {'contest': contest, 'has_registered':has_registered})


def check_registered_contests(request, contest):
    try:
        list_contained_contest = request.user.userprofile.registered_contests.filter(name=contest.name)
        has_registered = True
    except:
        has_registered = False
    finally:
        return has_registered
