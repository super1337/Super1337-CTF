from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

'''
class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
'''


class Tag(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return str(self.name)


class Challenge(models.Model):
    name = models.CharField(max_length=16, unique=True)
    problem = models.CharField(max_length=256)
    hints = models.CharField(max_length=256, blank=True)
    flag = models.CharField(max_length=256)
    score = models.IntegerField()
    file = models.FilePathField()

    tags = models.ManyToManyField(Tag)
    creators = models.ManyToManyField(User)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        '''On save, update timestamps '''

        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(User, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.problem)
