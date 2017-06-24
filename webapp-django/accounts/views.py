from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User


@login_required(login_url='/accounts/login/')
def index(request):
    return HttpResponseRedirect(redirect_to='/user/{}'.format(request.user.username))


def profile(request, username):
    messages = {'success': [], 'info': [], 'warning': [], 'danger': []}

    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        messages['warning'].append('The user {} does not exist!'.format(username))

    return render(request, 'accounts/profile.html', {'profile': request.user.userprofile, 'messages': messages})


def solved(request, username):
    messages = {'success': [], 'info': [], 'warning': [], 'danger': []}

    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        messages['danger'].append('The user {} does not exist!'.format(username))
        solvedchals = []
    else:
        solvedchals = user.userprofile.solved_challenges.all()

    return render(request, 'accounts/solved.html', {'solvedchals': solvedchals, 'messages': messages})
