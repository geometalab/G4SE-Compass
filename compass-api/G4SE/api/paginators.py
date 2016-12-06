from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


def to_sorted_list(x):
    l = [y for y in set(x) if y is not None]
    l.sort()
    # even though this would be more correct, it breaks
    # django-filter at the moment
    # if None in x:
    #     l.insert(0, None)
    return l


class ChoicesPagination(StandardResultsSetPagination):
    result_choices_fields = None
    _result_choices = None

    def paginate_queryset(self, queryset, request, view=None):
        self.get_result_choices(queryset)
        return super().paginate_queryset(queryset, request, view=None)

    def get_result_choices(self, queryset):
        if self.result_choices_fields is not None:
            queryset_choices = queryset.values_list(*self.result_choices_fields)
            self._result_choices = {
                k: to_sorted_list(v) for k, v in zip(self.result_choices_fields, zip(*queryset_choices))
            }

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('result_choices', self._result_choices),
            ('results', data)
        ]))


class MetadataResultsSetPagination(ChoicesPagination):
    result_choices_fields = [
        'collection',
        'crs',
        'dataset',
        'geodata_type',
        'geography',
        'publication_year',
        'service_type',
        'source',
    ]
