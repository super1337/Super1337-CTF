from django.contrib.auth.models import User
from django.db import models
from challenges.models import Challenge
from questionnaire.models import Quiz, SimpleQuestion, MCQ
from contests.models import Contest


class QuizResult(models.Model):
    user = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz)
    contest = models.ForeignKey(Contest, null=True, blank=True)
    correct_questions = models.ManyToManyField(SimpleQuestion, blank=True)
    score = models.IntegerField(default=0)

    @classmethod
    def create(cls, user, quiz, contest=None):
        if contest is None:
            quiz_result = cls(user=user, quiz=quiz)
        else:
            quiz_result = cls(user=user, quiz=quiz, contest=contest)
        return quiz_result


# User result in this model.py file causes no problem and makes most sense
# Import Error if this class in contests.models.py
# because all other models need each other before compilation causing a loop like condition
class ContestResult(models.Model):
    user = models.ForeignKey(User)
    contest = models.ForeignKey(Contest)
    # code: limit_choices_to=models.Q(contest=contest)
    # most important thing to note is limiting is not necessary as we will add these relation through backed
    # and will keep this model readonly
    # have to make many to many field to challenges limited to the one present in the contest
    # passing query object(model challenge contest pk should be equal to pk of contest here) to limit_choices_to
    solved_challenge = models.ManyToManyField(Challenge, blank=True)
    quiz_results = models.ManyToManyField(QuizResult, blank=True)
    challenge_score = models.IntegerField(default=0)

    @classmethod
    def create(cls, user, contest):
        user_result = cls(user=user, contest=contest)
        return user_result
