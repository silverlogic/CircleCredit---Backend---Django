from django.contrib.auth.models import AbstractUser
from django.db import models
from fcm_django.models import FCMDevice


class User(AbstractUser):
    friends = models.ManyToManyField("self", blank=True, related_name='friends')
    job = models.CharField(max_length=24, blank=True)
    stars = models.IntegerField(blank=True, default=0)
