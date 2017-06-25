from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# signal handlers
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed, post_delete


class Tag(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return str(self.name)

class Quiz(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=256, blank=True)
    tags = models.ManyToManyField(Tag, blank=True) # autoupdated
    
    def __str__(self):
        return str(self.name)



class Question(models.Model):
    question = models.CharField(max_length=256)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    hints = models.CharField(max_length=256, blank=True)
    answer = models.CharField(max_length=256)
    tags = models.ManyToManyField(Tag)
    score = models.IntegerField(default=0)
    creators = models.ManyToManyField(User)

    created = models.DateTimeField(editable=False,default=timezone.now)
    modified = models.DateTimeField(editable=False,default=timezone.now)

    def save(self, *args, **kwargs):
        '''On save, update timestamps '''

        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Question, self).save(*args, **kwargs)

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

# handles auto update of tags of quiz (basic version (uupdated question can also be handled through this))
@receiver(post_save, sender=SimpleQuestion)
def updatetags_onsave(sender, instance, **kwargs):
    relevent_quiz = instance.quiz
    print(instance.tags.all())
    print(instance.quiz)
    print(instance.quiz.tags.all())
    for tag in instance.tags.all():
        if tag not in relevent_quiz.tags.all():
            relevent_quiz.tags.add(tag)
    print(instance.quiz.tags.all())