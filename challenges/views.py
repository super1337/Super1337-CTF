from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect

from .forms import FlagForm
from .models import Challenge, Tag
from results.models import UserResult
from contests.models import Contest


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


def challenge(request, name, **kwargs):
    messages = {'success': [], 'info': [], 'warning': [], 'danger': []}
    chal = Challenge.objects.get(name=name)

    # url_word_list = request.build_absolute_uri().split('/')

    if contest_name in kwargs:
        is_in_contest = True
        try:
            contest = Contest.objects.get(name=contest_name)
        except Contest.DoesNotExist:
            return HttpResponseRedirect('/contests/')
    else:
        is_in_contest = False

    # if url_word_list[4] == 'contests':
    #     is_in_contest = True
    #     contest_name = url_word_list[5]
    #     try:
    #         contest = Contest.objects.get(name=contest_name)
    #     except Contest.DoesNotExist:
    #         return HttpResponseRedirect('/contests/')
    # else:
    #     is_in_contest = False

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
                    if is_in_contest:
                        try:
                            result_object = UserResult.objects.get(user=request.user.pk, contest=contest.pk)
                        except UserResult.DoesNotExist:
                            return HttpResponseRedirect('/contests/'+contest_name+'/register/')
                        finally:
                            if chal not in result_object.solved_challenges.all():
                                result_object.solved_challenges.add(chal)
                                result_object.score += chal.score

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
