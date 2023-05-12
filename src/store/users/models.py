from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    dob = models.DateField(null=True, blank=True)

    def get_name(self):
        if not self.get_full_name():
            return self.username
        return self.get_full_name()