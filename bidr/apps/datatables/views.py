"""
.. module:: bidr.apps.datatables.views
   :synopsis: Bidr Silent Auction System Datatable Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>


"""

from django.core.exceptions import ImproperlyConfigured
from django.views.generic.edit import CreateView

from .ajax import BidrDatatablesPopulateView


class DatatablesView(CreateView):
    populate_class = None

    def __init__(self, **kwargs):
        super(DatatablesView, self).__init__(**kwargs)

        if not issubclass(self.populate_class, BidrDatatablesPopulateView):
            raise ImproperlyConfigured("The populate_class instance variable is either not set or is not a subclass of BidrDatatablesPopulateView.")

    def get_context_data(self, **kwargs):
        context = super(DatatablesView, self).get_context_data(**kwargs)
        context["datatables_class"] = self.populate_class
        return context
