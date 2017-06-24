from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import UserProfile


@login_required(login_url='/accounts/login/')
def index(request):
    return HttpResponseRedirect(redirect_to='/user/{}'.format(request.user.username))


def profile(request, username):
    return render(request, 'accounts/profile.html', {'profile': request.user.userprofile})


def solved(request):
    pass
