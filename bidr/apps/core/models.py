"""
.. module:: bidr.apps.core.models
   :synopsis: Bidr Silent Auction System Core Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.mail import send_mail
from django.db.models.fields import CharField, BooleanField, EmailField, DateTimeField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token

from ..auctions.models import Auction


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


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


class BidrUser(AbstractBaseUser, PermissionsMixin):
    """Enterprise Groups Management Tool User Model"""

    name = CharField(max_length=30, blank=True, verbose_name='Full Name')
    email = EmailField(unique=True, verbose_name='Email Address')
    phone_number = PhoneNumberField(verbose_name='Phone Number')
    date_joined = DateTimeField(default=timezone.now)

    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']
    objects = BidrUserManager()

    class Meta:
        verbose_name = 'Bidr User'
        verbose_name_plural = 'Bidr Users'

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.get_username()

    def email_user(self, subject, message, from_email=None):
        """Sends an email to this user."""

        send_mail(subject, message, from_email, [self.email])

    def get_auctions_participated_in(self):
        try:
            return self.auction_set.all()
        except AttributeError:
            return Auction.objects.none()
