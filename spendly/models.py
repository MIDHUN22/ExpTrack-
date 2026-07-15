from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=12)

    def __str__(self):
        return self.get_full_name()