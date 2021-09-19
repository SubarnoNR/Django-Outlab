from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.IntegerField(blank=True,default=0)
    repo_info = models.JSONField(blank=True,null=True)
    time_inof = models.CharField(max_length=200,default="")
    avatar = models.URLField(max_length=200,default="")

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Repository(models.Model):
    name = models.CharField(max_length=150,default="")
    stars = models.IntegerField(default=0)
    user = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
