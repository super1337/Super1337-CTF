from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from challenges.models import Challenge
from questionnaire.models import Question


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    bio = models.TextField(max_length=256, blank=True)

    solved_challenges = models.ManyToManyField(Challenge, blank=True)
    solved_questions = models.ManyToManyField(Question, blank=True)
    score = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return str(self.user.username)

    def calculate_score(self):
        score = 0
        for chal in self.solved_challenges.all():
            score = score + chal.score
        for ques in self.solved_questions.all():
            score = score + ques.score

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
