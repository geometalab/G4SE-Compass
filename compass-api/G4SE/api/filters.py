from django.db.models import Q
from rest_framework import filters
from rest_framework import serializers
from django.utils.translation import gettext as _

from api import LANGUAGE_CONFIG_MATCH
from api.models import CombinedRecord, record_ids_for_search_query
from api.search_parser import search_query_parser
from api.search_parser.query_parser import SearchSemantics
from db import VectorFieldSearchRank


class RecordSearch(filters.SearchFilter):
    search_param = 'search'
    language_param = 'language'
    # having German as fallback is completely arbitrary
    language = CombinedRecord.GERMAN  # default language

    def get_search_params(self, request):
        """
        Search terms are set by a ?search=... query parameter,
        and may be comma and/or whitespace delimited.
        """
        search_string = request.query_params.get(self.search_param, '')
        language = request.query_params.get(self.language_param, self.language)
        return search_string, language

    def parse_query(self, search_string):
        return search_query_parser.UnknownParser().parse(
            search_string,
            semantics=SearchSemantics(config=LANGUAGE_CONFIG_MATCH[self.language])
        )

    def get_filter_kwargs(self, search_query, search_vector):
        search_query_kwargs = {search_vector: search_query}
        ids_kwargs = {'api_id__in': record_ids_for_search_query(search_query, language=self.language)}
        return Q(**ids_kwargs) | Q(**search_query_kwargs)

    def filter_queryset(self, request, queryset, view):
        search_string, self.language = self.get_search_params(request)
        search_vector = 'search_vector_{}'.format(self.language)
        if not search_string:
            return queryset
        search_query = self.parse_query(search_string)
        filter_condition = self.get_filter_kwargs(search_query, search_vector)
        rank = VectorFieldSearchRank(search_vector, search_query)
        return self.create_query(queryset, filter_condition, rank)

    def create_query(self, queryset, filter_condition, rank=None):
        """
        Parses the passed search_string and returns a query.
        """
        queryset = queryset.filter(filter_condition)
        if rank:
            queryset = queryset.annotate(rank=rank).order_by('-rank')
        return queryset

    def get_fields(self, view):
        return [self.search_param, self.language_param]


class LimitRecordFilter(filters.BaseFilterBackend):
    limit_param = 'limit'

    def filter_queryset(self, request, queryset, view):
        limit_by = request.query_params.get(self.limit_param, '')
        try:
            if limit_by:
                queryset = queryset[:int(limit_by)]
        except:
            raise
        return queryset

    def get_fields(self, view):
        return [self.limit_param]
