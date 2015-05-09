"""
.. module:: bidr.apps.organization.forms
   :synopsis: Bidr Silent Auction System Organization Forms.

.. moduleauthor:: Jirbert Dilanchian <jirbert@gmail.com>

"""

from django.forms.models import ModelForm

from .models import Organization


class OrganizationCreateForm(ModelForm):

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(OrganizationCreateForm, self).__init__(*args, **kwargs)

    def clean_owner(self):
        return self.request.user

    class Meta:
        model = Organization
        fields = ['name', 'email', 'phone_number', 'website', 'owner']
