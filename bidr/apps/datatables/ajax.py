"""
.. module:: bidr.apps.datatables.ajax
   :synopsis: Bidr Silent Auction System Datatable Ajax Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import shlex
import json
import logging
from collections import OrderedDict
from copy import deepcopy

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db.models import Q

from django_datatables_view.base_datatable_view import BaseDatatableView

from .utils import dict_merge

logger = logging.getLogger(__name__)


class BidrDatatablesPopulateView(BaseDatatableView):
    """ The base datatable population view for datatables."""

    table_name = "datatable"
    data_source = None
    max_display_length = 200

    column_definitions = OrderedDict()
    options = {
        "order": [[2, "asc"]],
        "language": {
            "lengthMenu": 'Display <select>' +
                '<option value="10">10</option>' +
                '<option value="25">25</option>' +
                '<option value="50">50</option>' +
                '<option value="100">100</option>' +
                '<option value="-1">All</option>' +
                '</select> items:',
            "search": "Filter items: ",
            "zeroRecords": "No items to display.",
            "processing": """<img src="{loading_gif}" alt=""  /> Processing...""".format(loading_gif=static('img/tiny_loading.gif'))
        },
        "processing": True,
        "serverSide": True,
        "pageLength": 10,
        "pagingType": "full_numbers",
        "lengthChange": True,
        "autoWidth": False,
        "dom": '<lrf><"clear">t<ip><"clear">',
    }

    extra_options = {}

    def initialize(self, *args, **kwargs):
        super(BidrDatatablesPopulateView, self).initialize(*args, **kwargs)

    def get_data_source(self):
        return self.data_source

    def get_table_name(self):
        return self.table_name

    def get_options(self):
        self.options.update({"ajax": str(self.get_data_source())})

        merged = dict_merge(self.options, self.extra_options)

        column_defs = deepcopy(self.column_definitions)
        formatted_column_defs = []

        for column_index, column_key in enumerate(column_defs):
            column_def = column_defs[column_key]
            column_def.update({"targets": [column_index]})
            formatted_column_defs.append(column_def)

        merged.update({"columnDefs": formatted_column_defs})
        return merged

    def get_options_serialized(self):
        return json.dumps(self.get_options())

    def get_columns(self):
        return list(self.column_definitions.keys())

    def _get_columns_by_attribute(self, attribute, default=True, test=True):
        """ Returns a filtered list of columns that have the given attribute.

        :param attribute: The attribute by which to filter
        :type attribute: str
        :param default: The default attribute value
        :param test: If the attribute is equal to this, return it

        """

        columns = []

        for column in self.column_definitions:
            if self.column_definitions[column].get(attribute, default) == test:
                columns.append(column)

        return columns

    def get_order_columns(self):
        """Get searchable columns and handle realated fields."""

        columns = self.get_columns()
        related_columns = self._get_columns_by_attribute("related", default=False)

        for column_name in columns:
            # If the column is related, append the lookup field to the column name
            if column_name in related_columns:
                related_column_name = column_name + "__" + self.column_definitions[column_name]["lookup_field"]
                columns[columns.index(column_name)] = related_column_name

        return columns

    def get_searchable_columns(self):
        """Get searchable columns and handle realated fields."""

        searchable_columns = self._get_columns_by_attribute("searchable")
        related_columns = self._get_columns_by_attribute("related", default=False)

        for column_name in searchable_columns:
            # If the column is related, append the lookup field to the column name
            if column_name in related_columns:
                related_column_name = column_name + "__" + self.column_definitions[column_name]["lookup_field"]
                searchable_columns[searchable_columns.index(column_name)] = related_column_name

        return searchable_columns

    def get_row_id(self, row):
        return None

    def get_row_class(self, row):
        return None

    def get_row_data_attributes(self, row):
        return None

    def prepare_results(self, qs):
        data = []

        for item in qs:
            row = {}
            row_id = self.get_row_id(item)
            row_class = self.get_row_class(item)
            row_data_attributes = self.get_row_data_attributes(item)

            if row_id:
                row.update({"DT_RowId": row_id})

            if row_class:
                row.update({"DT_RowClass": row_class})

            if row_data_attributes:
                row.update({"DT_RowAttr": row_data_attributes})

            for column in self.get_columns():
                row.update({str(self.get_columns().index(column)): self.render_column(item, column)})

            data.append(row)
        return data

    def filter_queryset(self, qs):
        """ Filters the QuerySet by submitted search parameters.

        Made to work with multiple word search queries.
        PHP source: http://datatables.net/forums/discussion/3343/server-side-processing-and-regex-search-filter/p1
        Credit for finding the Q.AND method: http://bradmontgomery.blogspot.com/2009/06/adding-q-objects-in-django.html

        :param qs: The QuerySet to be filtered.
        :type qs: QuerySet
        :returns: If search parameters exist, the filtered QuerySet, otherwise the original QuerySet.

        """

        search_parameters = self.request.GET.get('search[value]', None)
        searchable_columns = self.get_searchable_columns()

        if search_parameters:
            try:
                params = shlex.split(search_parameters)
            except ValueError:
                params = search_parameters.split(" ")
            columnQ = Q()
            paramQ = Q()

            for param in params:
                if param != "":
                    for searchable_column in searchable_columns:
                        columnQ |= Q(**{searchable_column + "__icontains": param})

                    paramQ.add(columnQ, Q.AND)
                    columnQ = Q()
            if paramQ:
                qs = qs.filter(paramQ)

        return qs
