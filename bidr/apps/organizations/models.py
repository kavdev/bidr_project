"""
.. module:: bidr.apps.bids.models
   :synopsis: Bidr Silent Auction System Bid Models.

.. moduleauthor:: Jirbert Dilanchian <Jirbert@gmail.com>

"""

from django.db.models.base import Model
from django.db.models.fields import CharField, EmailField, URLField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.conf import settings

from ..auctions.models import Auction

from phonenumber_field.modelfields import PhoneNumberField

class Organization(Model):
    """An Organization that manages silent auction."""

    name = CharField(max_length=100, verbose_name="Name")
    email = EmailField(blank=True, unique=True, verbose_name='Email Address')
    phone_number = PhoneNumberField(verbose_name='Phone Number')
    website = URLField(verbose_name="Website")
    owner = ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Admin")
    managers = ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Manager")
    auctions = ManyToManyField(Auction)

    def __str__(self):
        return self.name