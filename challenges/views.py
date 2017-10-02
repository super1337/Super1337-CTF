from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from results.models import ContestResult
from contests.models import Contest
from tags.models import Tag
from .forms import FlagForm
from .models import Challenge


def index(request):
    tag_name = request.GET.get('tag')
    sort = request.GET.get('sort')

    if sort not in ['name', 'modified', 'created', 'score']:
        sort = 'created'

    if tag_name:
        try:
            tag = Tag.objects.get(name=tag_name)
        except ObjectDoesNotExist:
            messages.info(request, 'Tag {} does not exist! Showing all challenges instead.'.format(tag_name))
            challenges = Challenge.objects.all().filter(hidden=False).order_by(sort)
        else:
            challenges = tag.challenge_set.all().filter(hidden=False).order_by(sort)
    else:
        challenges = Challenge.objects.all().filter(hidden=False).order_by(sort)

    return render(request, 'challenges/index.html', {'challenges': challenges})


def challenge(request, challenge_slug, contest_slug=None):

    # Get contest object if it's given and a valid one. Otherwise continue or redirect to contest.views.index.
    if contest_slug is not None:
        is_in_contest = True
        try:
            contest = Contest.objects.get(slug=contest_slug)
            if contest.state == '1':
                messages.info(request, 'The Contest has not started yet.')
                redirect('contests.views.index')
            if contest.state == '3':
                messages.info(request, 'The Contest has ended go to challenges tab or contest\'s main page')
                redirect('contests.views.index')
        except Contest.DoesNotExist:
            messages.warning(request, 'No contest with slug - {}'.format(contest_slug))
            return redirect('contests.views.index')
    else:
        is_in_contest = False

    # Get challenge or redirect according to in contest or challenge tab.
    try:
        chal = Challenge.objects.get(slug=challenge_slug)
    except Challenge.DoesNotExist:
        if is_in_contest:
            messages.warning(request, 'No challenge with slug - {}'.format(contest_slug))
            return redirect('contests.views.contest_view', contest_slug=contest_slug)
        else:
            messages.warning(request, 'No challenge with slug - {}'.format(challenge_slug))
            return redirect('challenges.views.index')

    # Makes challenge inaccessible out of contest even when user try with url manipulation
    if chal.hidden and (not is_in_contest):
        messages.warning(request, 'No challenge with slug - {}'.format(challenge_slug))
        return redirect('challenges.views.index')

    # If user opens challenges other than the ones in contest through contest tab, redirect them away from getting
    # unnecessary or unintended score
    if is_in_contest:
        if chal not in contest.challenge_set.all():
            messages.warning(request, 'No challenge with slug - {}'.format(challenge_slug))
            return redirect('contests.views.contest_view')

    # Main flag validating code for challenge.
    # Makes necessary changes to user challenge and ContestResult objects
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

                    messages.success(request, 'You did it! You solved the challenge successfully!')
                else:
                    messages.info(request, 'Sorry! You got it wrong. Try harder')
        else:
            messages.danger(request, 'You must be logged in to submit flags')
            form = FlagForm()
        return render(request, 'challenges/challenge.html', {'challenge': chal, 'form': form})

    else:
        form = FlagForm()

    return render(request, 'challenges/challenge.html', {'challenge': chal, 'form': form})
