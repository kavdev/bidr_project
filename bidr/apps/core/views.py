"""
.. module:: bidr.apps.core.views
   :synopsis: Bidr Silent Auction System Core Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from django.shortcuts import redirect

from registration.views import RegistrationView

from .forms import UserRegistrationForm


class IndexView(RegistrationView):
    template_name = "core/index.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("organizations")

    def register(self, request, **cleaned_data):
        """ Handles valid credentials"""

        get_user_model().objects.create_user(name=cleaned_data["name"],
                                             email=cleaned_data["email"],
                                             phone_number=cleaned_data["phone_number"],
                                             password=cleaned_data["password"])


class LoginView(FormView):
    template_name = "core/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("organizations")

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user.is_authenticated():
            auth_login(self.request, user)

        self.success_url = self.request.POST.get('next', self.success_url)

        return super(LoginView, self).form_valid(form)


def logout(request):
    """Logs the current user out."""

    auth_logout(request)
    return redirect("home")


def handler500(request):
    """500 error handler which includes ``request`` in the context."""

    from django.template import RequestContext, loader
    from django.http import HttpResponseServerError

    template = loader.get_template('500.html')

    return HttpResponseServerError(template.render(RequestContext(request)))
