from drf_haystack.filters import HaystackFilter
from haystack.backends import SQ
from rest_framework import filters

from api.helpers.input import ElasticSearchExtendedAutoQuery


class DateRangeFilterMixin:
    from_param = 'from'
    to_param = 'to'

    def _get_year_range(self, request, queryset):
        from_year = self._to_int_or_None(request.query_params.get(self.from_param, ''))
        to_year = self._to_int_or_None(request.query_params.get(self.to_param, ''))

        if to_year is None and from_year is None:
            return queryset

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
        return self._get_year_range(request, queryset)

    def get_fields(self, view):
        return [self.from_param, self.to_param]


class DateLimitRecordFilter(DateRangeFilterMixin, filters.BaseFilterBackend):
    pass


class LimitRecordFilter(filters.BaseFilterBackend):
    limit_param = 'limit'

    def filter_queryset(self, request, queryset, view):
        limit_by = request.query_params.get(self.limit_param, '')
        if limit_by:
            queryset = queryset[:int(limit_by)]
        return queryset

    def get_fields(self, view):
        return [self.limit_param]


class DateLimitSearchRecordFilter(DateRangeFilterMixin, HaystackFilter):
    from_param = 'from_year'
    to_param = 'to_year'


class IsLatestSearchRecordFilter(HaystackFilter):
    param = 'is_latest'

    def filter_queryset(self, request, queryset, view):
        is_latest = request.query_params.get(self.param, None)
        if is_latest is not None:
            queryset = queryset.exclude(is_latest='false')  # is equal to is_latest__exact='0'
        return queryset

    def get_fields(self, view):
        return [self.param]


class MetadataSearchFilter(HaystackFilter):
    FALLBACK_LANGUAGE = 'en'
    param = 'search'

    def filter_queryset(self, request, queryset, view):
        query_string = request.query_params.get(self.param, None)
        language = request.query_params.get('language', self.FALLBACK_LANGUAGE)

        if query_string is not None and query_string != '':
            cleaned_query_string = ElasticSearchExtendedAutoQuery(query_string)
            keyword_search = {'keywords_{}'.format(language): cleaned_query_string}
            queryset = queryset.filter(
                SQ(content=cleaned_query_string) |
                SQ(text=cleaned_query_string) |
                SQ(abstract=cleaned_query_string) |
                SQ(title=cleaned_query_string) |
                SQ(**keyword_search) |
                SQ(geography=cleaned_query_string) |
                SQ(collection=cleaned_query_string) |
                SQ(dataset=cleaned_query_string)
            )
        return queryset

    def get_fields(self, view):
        return [self.param]


class MetadataSearchOrderingFilter(HaystackFilter):
    param = 'ordering'

    def filter_queryset(self, request, queryset, view):
        ordering = request.query_params.get(self.param, None)

        if ordering is not None and ordering != '':
            queryset = queryset.order_by(ordering)
        return queryset

    def get_fields(self, view):
        return [self.param]
