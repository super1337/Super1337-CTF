from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .forms import FlagForm
from .models import Challenge, Tag


def index(request):
    messages = {'success': [], 'info': [], 'warning': [], 'danger': []}
    tagname = request.GET.get('tag')

    sort = request.GET.get('sort')
    if sort not in ['name', 'modified', 'created', 'score']:
        sort = 'created'

    if tagname:
        try:
            tag = Tag.objects.get(name=tagname)
        except ObjectDoesNotExist:
            messages['info'].append('Tag {} does not exist! Showing all challenges instead.'.format(tagname))
            challenges = Challenge.objects.all().order_by(sort)
        else:
            challenges = tag.challenge_set.all().order_by(sort)
    else:
        challenges = Challenge.objects.all().order_by(sort)

    return render(request, 'challenges/index.html', {'challenges': challenges, 'messages': messages})


def tags(request):
    tags = Tag.objects.all()
    return render(request, 'challenges/tags.html', {'tags': tags})


def challenge(request, name):
    messages = {'success': [], 'info': [], 'warning': [], 'danger': []}
    chal = Challenge.objects.get(name=name)

    if request.method == 'POST':
        if request.user.is_authenticated():
            form = FlagForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['flag'] == chal.flag:
                    if chal not in request.user.userprofile.solved_challenges.all():
                        request.user.userprofile.solved_challenges.add(chal)
                        request.user.userprofile.save()
                        chal.solve_count += 1
                        chal.save()
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
