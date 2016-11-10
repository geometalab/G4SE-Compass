from django.db.models import IntegerField
from django.db.models.functions import Cast
from drf_haystack.filters import HaystackFilter
from haystack.inputs import Raw
from rest_framework import filters


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


class IsLatestSearchRecordFilter(HaystackFilter):
    param = 'is_latest'

    def filter_queryset(self, request, queryset, view):
        is_latest = request.query_params.get(self.param, None)
        if is_latest is not None:
            queryset = queryset.exclude(is_latest='false')  # is equal to is_latest__exact='0'
        return queryset

    def get_fields(self, view):
        return [self.param]
