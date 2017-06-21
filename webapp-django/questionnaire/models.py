from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import datetime


class Tag(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return str(self.name)


class Question(models.Model):
    question = models.CharField(max_length=256)
    hints = models.CharField(max_length=256, blank=True)
    answer = models.CharField(max_length=256)
    tags = models.ManyToManyField(Tag)
    score = models.IntegerField(default=0)
    creators = models.ManyToManyField(User)

    created = models.DateTimeField(editable=False,default=datetime.datetime.now().date())
    modified = models.DateTimeField(editable=False,default=datetime.datetime.now().date())

    def save(self, *args, **kwargs):
        '''On save, update timestamps '''

        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(User, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.question)


class SimpleQuestion(Question):
    pass


class MultipleChoiceQuestion(Question):
    choices = models.CharField(choices=[], max_length=256)
    correct = models.IntegerField()

    @classmethod
    def create(cls, question, hints, choices, correct, score):
        CHOICES = [(index, item) for index, item in enumerate(choices)]
        answer = CHOICES[correct][1]
        mcq = cls(question=question, hints=hints, choices=CHOICES, correct=correct, answer=answer, score=score)
        return mcq
