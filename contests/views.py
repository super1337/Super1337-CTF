from django.shortcuts import render
from .models import Contest

# Create your views here.


def index(request):
    contests = Contest.objects.all()
    yet_to_begin = contests.filter(state=1)
    ongoing = contests.filter(state=2)
    ended = contests.filter(state=3)
    return render(request, 'contests/index.html', {'yet_to_begin': yet_to_begin, 'ongoing': ongoing, 'ended': ended})