"""
.. module:: bidr.apps.core.models
   :synopsis: Bidr Silent Auction System Core Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db.models.fields import CharField, BooleanField, EmailField, DateTimeField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from rest_framework.authtoken.models import Token

from .managers import BidrUserManager


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class BidrUser(AbstractBaseUser, PermissionsMixin):
    """Enterprise Groups Management Tool User Model"""

    name = CharField(max_length=30, verbose_name='Full Name')
    display_name = CharField(max_length=30, blank=True, default="Anonymous", verbose_name='Display Name')
    email = EmailField(unique=True, verbose_name='Email Address')
    phone_number = CharField(max_length=20, verbose_name='Phone Number')
    date_joined = DateTimeField(default=timezone.now)
    ios_device_token = CharField(max_length=64, blank=True, null=True, verbose_name='iOS Device Token')

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

    def get_display_name(self):
        return self.display_name

    def get_short_name(self):
        return self.get_username()

    def email_user(self, subject, message, html_message=None, from_email=None):
        """Sends an email to this user."""

        send_mail(
            subject=subject, message=message, html_message=html_message, from_email=from_email,
            fail_silently=False, recipient_list=[self.email]
        )
