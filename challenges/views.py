from django.shortcuts import render

from .forms import FlagForm
from .models import Challenge


def index(request):
    challenges = Challenge.objects.all()
    return render(request, 'challenges/index.html', {'challenges': challenges})

def tags(request):
    pass


def challenge(request, name):
    messages = {'success': [], 'info': [], 'warning': [], 'danger': []}
    chal = Challenge.objects.get(name=name)

    if request.method == 'POST':
        if request.user.is_authenticated():
            form = FlagForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['flag'] == chal.flag:
                    request.user.userprofile.solved_challenges.add(chal)
                    request.user.userprofile.save()
                    messages['success'].append('You did it! You solved the challenge successfully!')
                else:
                    messages['info'].append('Sorry! You got it wrong. Try harder')
        else:
            messages['danger'].append('You must be logged in to submit flags')
            form = FlagForm()
        return render(request, 'challenges/challenge.html', {'challenge': chal, 'form': form, 'messages': messages})

    else:
        form = FlagForm()

    return render(request, 'challenges/challenge.html', {'challenge': chal, 'form': form, 'messages': messages})
