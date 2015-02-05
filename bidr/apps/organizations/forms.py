"""
.. module:: bidr.apps.organization.forms
   :synopsis: Bidr Silent Auction System Organization Forms.

.. moduleauthor:: Jirbert Dilanchian <jirbert@gmail.com>

"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm

from bidr.apps.organizations.models import Organization


class OrganizationCreateForm(ModelForm):

    def clean_email(self):
        """
        Ensures the email address provided is unique.
        """

        email = self.cleaned_data["email"]
        try:
            get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return email
        raise ValidationError("This email address is already in use.", code='email_not_unique')

    class Meta:
        model = Organization
        fields = ['name', 'email', 'phone_number', 'website']
