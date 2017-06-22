from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    bio = models.TextField(max_length=256, blank=True)
    solved=models.CharField(solved=[],max_length=256)

    def __str__(self):
        return str(self.user.username)


# Method to link the User and UserProfile models
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
