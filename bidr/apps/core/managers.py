"""
.. module:: bidr.apps.core.managers
   :synopsis: Bidr Silent Auction System Core Model Managers.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class BidrUserManager(BaseUserManager):

    def _create_user(self, name, email, phone_number, password, is_staff, is_superuser, **extra_fields):
        """Creates and saves a User with the given username, email and password."""

        now = timezone.now()
        if not email:
            raise ValueError('The given email address must be set')
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, phone_number=phone_number, is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, email, phone_number, password, **extra_fields):
        return self._create_user(name, email, phone_number, password, False, False,
                                 **extra_fields)

    def create_superuser(self, name, email, phone_number, password, **extra_fields):
        return self._create_user(name, email, phone_number, password, True, True,
                                 **extra_fields)
