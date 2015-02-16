"""
.. module:: bidr.apps.bids.models
   :synopsis: Bidr Silent Auction System Bid Models.

.. moduleauthor:: Jirbert Dilanchian <Jirbert@gmail.com>

"""

import re

from django.db.models.base import Model
from django.db.models.fields import CharField, EmailField, URLField, SlugField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.utils import IntegrityError
from django.conf import settings
from django.template.defaultfilters import slugify

from ..auctions.models import Auction

from phonenumber_field.modelfields import PhoneNumberField


class Organization(Model):
    """An Organization that manages silent auction."""

    name = CharField(max_length=100, verbose_name="Name")
    slug = SlugField(max_length=120, verbose_name="Slug")
    email = EmailField(unique=True, verbose_name='Email Address')
    phone_number = PhoneNumberField(verbose_name='Phone Number')
    website = URLField(verbose_name="Website")
    owner = ForeignKey(settings.AUTH_USER_MODEL, related_name="owner", verbose_name="Owner")
    managers = ManyToManyField(settings.AUTH_USER_MODEL, related_name="managers", verbose_name="Managers", blank=True)
    auctions = ManyToManyField(Auction, related_name="auctions", verbose_name="Auctions", blank=True)
 
    def save(self):
        """Auto-populate an empty slug field from the MyModel name and
        if it conflicts with an existing slug then append a number and try
        saving again.
        https://djangosnippets.org/snippets/761/
        """
         
        if not self.slug:
            self.slug = slugify(self.name)  # Where self.name is the field used for 'pre-populate from'
  
        while True:
            try:
                super(Organization, self).save()
            # Assuming the IntegrityError is due to a slug fight
            except IntegrityError:
                match_obj = re.match(r'^(.*)-(\d+)$', self.slug)
                if match_obj:
                    next_int = int(match_obj.group(2)) + 1
                    self.slug = match_obj.group(1) + '-' + str(next_int)
                else:
                    self.slug += '-2'
            else:
                break
  
    def __str__(self):
        return self.name
