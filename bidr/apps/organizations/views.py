"""
.. module:: bidr.apps.Admin.views
   :synopsis: Bidr Silent Auction Admin Views.

.. moduleauthor:: Jirbert Dilanchian <jirbert@gmail.com>

"""
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.db.models import Q
from django.core.urlresolvers import reverse_lazy


from .models import Organization
from .forms import OrganizationCreateForm


class OrganizationListView(ListView):
    template_name = "organizations/organizations.html"

    def get_queryset(self):
        # return Organization.objects.filter(Q(owner=self.request.user) | Q(managers__in=self.request.user))
        return Organization.objects.filter(owner=self.request.user)


class OrganizationCreateView(CreateView):
    template_name = "organizations/create.html"
    form_class = OrganizationCreateForm
    model = Organization
#     fields = ['name', 'email', 'phone_number', 'website']
    success_url = reverse_lazy('organizations')

    def form_valid(self, form):
        self.object = form.save()
        return super(OrganizationCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(OrganizationCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs