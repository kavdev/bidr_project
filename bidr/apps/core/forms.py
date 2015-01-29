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
from rest_framework import authentication
from django.contrib.auth.forms import AuthenticationForm


class UserRegistrationForm(ModelForm):
    password_confirm = CharField(max_length=128, widget=PasswordInput, label='confirm password')

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

class LoginForm(AuthenticationForm):
    organization =  CharField(max_length=128, label='Enter your organization')
    