from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from challenges.models import Challenge
from questionnaire.models import Quiz
from contests.models import Contest


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    bio = models.TextField(max_length=256, blank=True)

    solved_challenges = models.ManyToManyField(Challenge, blank=True)
    attempted_quizzes = models.ManyToManyField(Quiz, blank=True)
    score = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return str(self.user.username)

    def calculate_score(self):
        score = 0
        for chal in self.solved_challenges.all():
            score = score + chal.score
        # for ques in self.solved_questions.all():
        #     score = score + ques.score

        return score

    def save(self, *args, **kwargs):
        '''On save, update score '''

        if not self.id:
            self.score = 0
        else:
            self.score = self.calculate_score()

        return super(UserProfile, self).save(*args, **kwargs)


# Method to link the User and UserProfile models
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    try:
        instance.userprofile.save()
    except ObjectDoesNotExist:
        UserProfile.objects.create(user=instance)
        instance.userprofile.save()


# User result in this model.py file causes no problem and makes most sense
# Import Error if this class in contests.models.py
# because all other models need each other before compilation causing a loop like condition
class UserResult(models.Model):
    user = models.ForeignKey(User)
    contest = models.ForeignKey(Contest)
    # most important thing to note is limiting is not necessary as we will add these relation through backed
    # and will keep this model readonly
    # have to make many to many field to challenges limited to the one present in the contest
    # passing query object(model challenge contest pk should be equal to pk of contest here) to limit_choices_to
    solved_challenge = models.ManyToManyField(Challenge, limit_choices_to=models.Q(contest=contest))
    score = models.IntegerField(default=0)