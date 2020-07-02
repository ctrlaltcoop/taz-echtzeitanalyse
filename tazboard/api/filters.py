from django_filters import FilterSet, filters

from tazboard.api.queries.constants import INTERVAL_10MINUTES


class ClickGraphFilterSet(FilterSet):
    min = filters.CharFilter(default='now-24h')
    max = filters.CharFilter(default='now')
    interval = filters.CharFilter(default=INTERVAL_10MINUTES, required=False)
    msid = filters.NumberFilter(required=False)


class ReferrerFilterSet(FilterSet):
    min = filters.CharFilter(default='now-24h')
    max = filters.CharFilter(default='now')
    msid = filters.NumberFilter(required=False)
