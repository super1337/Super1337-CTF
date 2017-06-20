from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return str(self.name)


class Challenge(models.Model):
    name = models.CharField(max_length=16, unique=True)
    problem = models.CharField(max_length=256)
    hints = models.CharField(max_length=256, blank=True)
    tags = models.ManyToManyField(Tag)
    flag = models.CharField(max_length=256)

    def __str__(self):
        return str(self.problem)
