from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    friends = models.ManyToManyField("self", blank=True)
    description = models.CharField(max_length=24, blank=True)