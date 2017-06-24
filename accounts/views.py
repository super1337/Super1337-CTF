from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import UserProfileForm


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


@login_required(login_url='/accounts/login/')
def edit(request, username):
    messages = {'success': [], 'info': [], 'warning': [], 'danger': []}

    if not request.user.username == username:
        messages['danger'].append('You cannot edit the profile of user {}!'.format(username))
        messages['info'].append('Loading your user profile instead.')

    profile = request.user.userprofile
    form = UserProfileForm(request.POST or None, instance=profile)

    if form.is_valid():
        messages['success'].append('You updated your profile successfully!')
        form.save()

    return render(request, 'accounts/edit.html', {'form': form, 'messages': messages})


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
