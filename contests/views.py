from django.shortcuts import render, get_object_or_404
from .models import Contest


def index(request):
    contests = Contest.objects.all()
    # may be make this client side by filtering state in templates
    yet_to_begin = contests.filter(state=1)
    ongoing = contests.filter(state=2)
    ended = contests.filter(state=3)
    l1 = len(yet_to_begin)
    l2 = len(ongoing)
    l3 = len(ended)
    return render(request, 'contests/index.html', {'yet_to_begin': yet_to_begin, 'ongoing': ongoing, 'ended': ended, 'l1' : l1, 'l2' : l2, 'l3' : l3})


# needs to be improvised
def contest_view(request, name):
    contest = get_object_or_404(Contest, name=name)
    if contest.state == 1:
        return render(request, 'contests/contest_1.html', {'contest': contest})
    elif contest.state == 2:
        pass
    elif contest.state == 3:
        pass
    # check this, return if i return in above region /contest/name does'nt work
    return render(request, 'contests/contest_1.html', {'contest': contest})




# nothing as registration yet to keep things simple
"""
def contest_register(request, name):
    contest = get_object_or_404(Contest, name=name)
    has_registered = check_registered_contests(request, contest)
    if has_registered:
        contest.users_registered += 1
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
"""