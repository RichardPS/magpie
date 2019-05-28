# Django
from django.contrib.auth.models import AbstractUser
from django.db import models

# Local
from .admin_choices import DEPARTMENTS


class User(AbstractUser):

    department = models.CharField(max_length=2, choices=DEPARTMENTS, blank=True)
    is_manager = models.BooleanField(default=False, verbose_name="Is Manager")
    is_director = models.BooleanField(default=False, verbose_name="Is Director")
    is_accounts_admin = models.BooleanField(
        default=False, verbose_name="Is Accounts Administrator"
    )

    @property
    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return self.username
