"""
.. module:: bidr.apps.core.forms
   :synopsis: Bidr Silent Auction System Core Forms.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from django.forms.fields import CharField
from django.forms.widgets import PasswordInput


class UserRegistrationForm(ModelForm):
    password_confirm = CharField(max_length=128, widget=PasswordInput, label='confirm password')

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

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password' in self.cleaned_data and 'password_confirm' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
                raise ValidationError("The passwords entered do not match.")
        return self.cleaned_data

    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'phone_number', 'password']
