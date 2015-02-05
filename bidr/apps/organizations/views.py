"""
.. module:: bidr.apps.Admin.views
   :synopsis: Bidr Silent Auction Admin Views.

.. moduleauthor:: Jirbert Dilanchian <jirbert@gmail.com>

"""
from django.views.generic import ListView
from .models import Organization
from django.db.models import Q


class OrganizationListView(ListView):
    template_name = "organizations/organizations.html"

    def get_queryset(self):
        # return Organization.objects.filter(Q(owner=self.request.user) | Q(managers__in=self.request.user))
        return Organization.objects.filter(owner=self.request.user)
