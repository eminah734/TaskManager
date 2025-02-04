from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    CATEGORY_CHOICES = [
        ('work', 'Work'),
        ('home', 'Home'),
        ('hobby', 'Hobby'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, related_name="tasks", on_delete=models.CASCADE)
    body = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='medium')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} ({self.created_at:%Y-%m-%d}): {self.body}..."

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

def createProfile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

post_save.connect(createProfile, sender=User)