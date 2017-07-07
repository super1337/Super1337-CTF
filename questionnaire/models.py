from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save

from django.contrib.auth.models import User
from django.contrib import admin

from contests.models import Contest, Tag

# signal handlers
from django.dispatch import receiver


class Quiz(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=256, blank=True)
    tags = models.ManyToManyField(Tag)
    score = models.IntegerField(editable=False) # make it dependent on problems contained or some final normalized score

    DIFF_CHOICES = ((1, 'n00b'), (2, 'Easy'), (3, 'Medium'), (4, 'Hard'), (5, '1337'))
    difficulty = models.CharField(max_length=10, choices=DIFF_CHOICES)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, null=True)
    creators = models.ManyToManyField(User)

    hidden = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class Question(models.Model):
    question = models.CharField(max_length=256)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    hints = models.CharField(max_length=256, blank=True)
    answer = models.CharField(max_length=256) # maybe during checking and/or while save compare both small/capitalized texts

    tags = models.ManyToManyField(Tag)
    score = models.IntegerField()

    hidden = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     '''On save, update timestamps '''
    #
    #     if not self.id:
    #         self.created = timezone.now()
    #     self.modified = timezone.now()
    #     return super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.question)


class SimpleQuestion(Question):
    pass


class MCQ(Question):
    choices = models.CharField(choices=[], max_length=256)
    correct = models.IntegerField()

    @classmethod
    def create(cls, question, hints, choices, correct, score):
        CHOICES = [(index, item) for index, item in enumerate(choices)]
        answer = CHOICES[correct][1]
        mcq = cls(question=question, hints=hints, choices=CHOICES, correct=correct, answer=answer, score=score)
        return mcq


# Handles auto update of tags and score of quiz
# @receiver(post_save, sender=SimpleQuestion)
# @receiver(post_save, sender=MCQ)
# def updatequiz(sender, instance, **kwargs):
#     print(instance.tags.all())
#     print(instance.quiz)
#     print(instance.quiz.tags.all())
#     for tag in instance.tags.all():
#         if tag not in instance.quiz.tags.all():
#             instance.quiz.tags.add(tag)
#     print(instance.quiz.tags.all())


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'question', 'score', 'hidden', 'created', 'modified')
    search_fields = ('quiz', 'question')
    list_filter = ('tags', 'score', 'modified', 'created')
    ordering = ['score', 'modified', 'created']


class SimpleQuestionAdmin(QuestionAdmin):
    pass


class MCQAdmin(QuestionAdmin):
    pass


class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'score', 'contest')
    search_fields = ('name', 'description', 'contest')
    raw_id_fields = ('creators',)
    list_filter = ('tags', 'score', 'modified', 'created', 'creators')
    ordering = ['name', 'score', 'creators', 'modified', 'created']
