"""
.. module:: bidr.apps.core.templatetags.currency
    :synopsis: Bidr Silent Auction System Core Template Tags and Filters.

.. moduleauthor:: Alexander Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: Jirbert Dilanchian <jirbert@gmail.com>

"""

from decimal import Decimal

from django import template
register = template.Library()


@register.filter()
def currency(value):
    """ Converts a value into currency notation.

    :param value: The value to convert
    :type value: str
    :returns: A string version of the provided value, in currency notation.

    """

    value = Decimal(value) if value else Decimal(0)

    try:
        if value >= 0:
            return '${amount}'.format(amount=value.quantize(Decimal('0.01')))
        else:
            return '-${amount}'.format(amount=abs(value).quantize(Decimal('0.01')))
    except AttributeError:
        return value
