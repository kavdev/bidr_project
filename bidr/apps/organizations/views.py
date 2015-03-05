"""
.. module:: bidr.apps.organization.views
   :synopsis: Bidr Silent Auction System Organization Views.

.. moduleauthor:: Jirbert Dilanchian <jirbert@gmail.com>
.. moduleauthor:: Alexander Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from .forms import OrganizationCreateForm
from .models import Organization


class OrganizationListView(TemplateView):
    template_name = "organizations/organizations.html"

    def get_context_data(self, **kwargs):
        context = super(OrganizationListView, self).get_context_data(**kwargs)
        context["owned_list"] = Organization.objects.filter(owner=self.request.user)
        context["managed_list"] = [org for org in Organization.objects.all() if self.request.user in org.managers]
        return context


class OrganizationCreateView(CreateView):
    template_name = "organizations/create_organization.html"
    form_class = OrganizationCreateForm
    model = Organization

    def get_form_kwargs(self):
        kwargs = super(OrganizationCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_success_url(self):
        return reverse_lazy('auctions', kwargs={'slug': self.object.slug})
    
class OrganizationUpdateView(UpdateView):
    template_name = "organizations/update_organization.html"
    model = Organization
    

    def get_success_url(self):
        return reverse_lazy('auctions', kwargs={'slug': self.object.slug})