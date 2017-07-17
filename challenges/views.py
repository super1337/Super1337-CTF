from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from .forms import FlagForm
from .models import Challenge, Tag
from results.models import ContestResult
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
            challenges = tag.challenge_set.all().filter(hidden=False).order_by(sort)
    else:
        challenges = Challenge.objects.all().filter(hidden=False).order_by(sort)

    return render(request, 'challenges/index.html', {'challenges': challenges, 'messages': messages})


def tags(request):
    tags = Tag.objects.all()
    return render(request, 'challenges/tags.html', {'tags': tags})


def challenge(request, challenge_name, contest_name=None, messages=None, **kwargs):
    if messages is not None:
        messages = {'success': [], 'info': [], 'warning': [], 'danger': []}

    # Get contest object or redirect to contests.views.index
    if contest_name is not None:
        is_in_contest = True
        try:
            contest = Contest.objects.get(name=contest_name)
        except Contest.DoesNotExist:
            return redirect('contests.views.index', messages={'warning': ['No contest with name - {}'.format(contest_name)]})
    else:
        is_in_contest = False

    # Get challenge or redirect according to in contest or challenge tab
    try:
        chal = Challenge.objects.get(name=challenge_name)
    except Challenge.DoesNotExist:
        if is_in_contest:
            return redirect('contests.views.contest_view', contest_name=contest_name, messages={
                'warning': ['No challenge with name - {}'.format(challenge_name)]})
        else:
            return redirect('challenges.views.index', messages={
                'warning': ['No challenge with name - {}'.format(challenge_name)]})

    # Makes challenge inaccessible out of contest even when user try with url manipulation
    if chal.hidden and (not is_in_contest):
        return redirect('challenges.views.index', messages={
            'warning': ['No challenge with name - {}'.format(challenge_name)]})

    # If user opens challenges other than the ones in contest through contest tab
    # redirect them away from getting unnecessary score
    if is_in_contest:
        if chal in contest.challenge_set.all():
            return redirect('contests.views.contest_view', contest_name=contest_name, messages={
                'warning': ['No challenge with name - {}'.format(challenge_name)]})

    # main challenge checking code
    # makes necessary changes to user challenge and ContestResult objects
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
                            contest_result = ContestResult.objects.get(user=request.user.pk, contest=contest.pk)
                        except ContestResult.DoesNotExist:
                            return redirect('contests.views.contest_register')
                        finally:
                            if chal not in contest_result.solved_challenges.all():
                                contest_result.solved_challenges.add(chal)
                                contest_result.score += chal.score

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
