"""
.. module:: bidr.apps.core.models
   :synopsis: Bidr Silent Auction System Core Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core.mail import send_mail
from django.db.models.fields import CharField, BooleanField, EmailField
from django.db.models.signals import post_save
from django.dispatch import receiver


from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class BidrUser(AbstractBaseUser, PermissionsMixin):
    """Enterprise Groups Management Tool User Model"""

    name = CharField(max_length=30, blank=True, verbose_name='Full Name')
    email = EmailField(blank=True, unique=True, verbose_name='Email Address')
    phone_number = PhoneNumberField(verbose_name='Phone Number')

    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        verbose_name = 'Bidr User'
        verbose_name_plural = 'Bidr Users'

    def get_username(self):
        return self.email

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.email

    def email_user(self, subject, message, from_email=None):
        """Sends an email to this user."""

        send_mail(subject, message, from_email, [self.email])

    def __str__(self):
        return self.email
