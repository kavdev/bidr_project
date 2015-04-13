"""
.. module:: bidr.apps.datatables.templatetags
   :synopsis: Bidr Silent Auction System Datatables Template Tags and Filters.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
"""

import logging

from django.template import Context, loader, Library, Node, TemplateSyntaxError
from django.core.exceptions import ImproperlyConfigured
from ..ajax import BidrDatatablesPopulateView

logger = logging.getLogger(__name__)
register = Library()


@register.tag(name="datatables_script")
def do_datatables(parser, token):
    return DatatablesNode()


class DatatablesNode(Node):
    """Renders Datatables Code into a django template. Designed to be thread safe."""

    template_name = 'datatables/datatables_code.html'

    def render(self, context):
        try:
            datatables_class = context["datatables_class"]
        except KeyError:
            raise TemplateSyntaxError("The datatables template tag requires a datatables class to be passed into context. (context['datatables_class'])")

        try:
            kwargs = context["kwargs"]
        except KeyError:
            raise TemplateSyntaxError("The datatables template tag requires kwargs to be passed into context. (context['kwargs'])")

        # Add context
        if datatables_class:
            if not issubclass(datatables_class, BidrDatatablesPopulateView):
                raise ImproperlyConfigured("The populate_class instance variable is either not set or is not a subclass of BidrDatatablesPopulateView.")

            datatables_class_instance = datatables_class(kwargs=kwargs)

            context['datatable_name'] = datatables_class_instance.get_table_name()
            context['datatable_options'] = datatables_class_instance.get_options_serialized()

            template = loader.get_template(self.template_name)

            return template.render(Context(context))
        else:
            return ''
