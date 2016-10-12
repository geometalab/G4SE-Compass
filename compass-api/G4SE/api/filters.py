from django.db.models import Q, IntegerField
from django.db.models.functions import Cast
from drf_haystack.filters import HaystackFilter
from rest_framework import filters

from api import LANGUAGE_CONFIG_MATCH
from api.models import record_ids_for_search_query, GeoServiceMetadata
from api.search_parser import search_query_parser
from api.search_parser.query_parser import SearchSemantics
from db import VectorFieldSearchRank


class RecordSearch(filters.SearchFilter):
    search_param = 'search'
    language_param = 'language'
    # having German as fallback is completely arbitrary
    language = GeoServiceMetadata.GERMAN  # default language

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


class DateLimitRecordFilter(filters.BaseFilterBackend):
    year_param = 'year'
    from_param = 'from'
    to_param = 'to'

    def _filter_queryset(self, request, queryset):
        single_year = self._get_year(request)
        if single_year is not None:  # if we have one year defined, just ignore the possible range given
            return queryset.filter(publication_year=single_year)
        return self._get_year_range(request, queryset)

    def _get_year(self, request):
        year = request.query_params.get(self.year_param, '')
        if year.lower() == 'latest':
            return 'latest'
        else:
            return self._to_int_or_None(year)

    def _get_year_range(self, request, queryset):
        from_year = self._to_int_or_None(request.query_params.get(self.from_param, ''))
        to_year = self._to_int_or_None(request.query_params.get(self.to_param, ''))

        if to_year is None and from_year is None:
            return queryset

        # FIXME: ugly hack to only include numbers, because publication_year is not an integer :-(
        queryset = queryset.filter(publication_year__startswith='2')
        queryset = queryset.annotate(publication_year_int=Cast('publication_year', IntegerField()))
        if to_year is not None:
            queryset = queryset.filter(publication_year_int__lte=to_year)
        if from_year is not None:
            queryset = queryset.filter(publication_year_int__gte=from_year)
        return queryset

    def _to_int_or_None(self, value):
        try:
            return int(value)
        except ValueError:
            return None

    def filter_queryset(self, request, queryset, view):
        return self._filter_queryset(request, queryset)

    def get_fields(self, view):
        return [self.year_param, self.from_param, self.to_param]


class LimitRecordFilter(filters.BaseFilterBackend):
    limit_param = 'limit'

    def filter_queryset(self, request, queryset, view):
        limit_by = request.query_params.get(self.limit_param, '')
        if limit_by:
            queryset = queryset[:int(limit_by)]
        return queryset

    def get_fields(self, view):
        return [self.limit_param]


class DateLimitSearchRecordFilter(HaystackFilter):
    from_param = 'from_year'
    to_param = 'to_year'

    def _filter_queryset(self, request, queryset):
        if request.query_params.get(self.from_param, '') == 'latest':
            return queryset.filter(publication_year='latest')
        return self._get_year_range(request, queryset)

    def _get_year_range(self, request, queryset):
        from_year = self._to_int_or_None(request.query_params.get(self.from_param, ''))
        to_year = self._to_int_or_None(request.query_params.get(self.to_param, ''))

        if to_year is None and from_year is None:
            return queryset

        # FIXME: ugly hack to only include numbers, because publication_year is not an integer :-(
        queryset = queryset.filter(publication_year__startswith='2')
        if to_year is not None:
            queryset = queryset.filter(publication_year__lte=to_year)
        if from_year is not None:
            queryset = queryset.filter(publication_year__gte=from_year)
        return queryset

    def _to_int_or_None(self, value):
        try:
            return int(value)
        except ValueError:
            return None

    def filter_queryset(self, request, queryset, view):
        return self._filter_queryset(request, queryset)

    def get_fields(self, view):
        return [self.from_param, self.to_param]
