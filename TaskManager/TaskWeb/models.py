from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, related_name="tasks", on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(f"{self.user} "
               f"({self.created_at:%Y-%m-%d}): "
               f"{self.body}..."
               )




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self",related_name="followed_by",symmetrical=False,blank=True)

    date_modified = models.DateTimeField(User, auto_now=True)

    def __str__(self):
        return self.user.username
    
def createProfile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

post_save.connect(createProfile, sender=User)