from django.utils import timezone

from tazboard.api.queries.common import get_fingerprint_aggregation_with_ranges, \
    get_interval_filter_exclude_bots
from tazboard.api.queries.constants import KEY_RANGES_AGGREGATION


def get_total_query(min_date, max_date=timezone.now()):
    min_date_previous_interval = min_date - (max_date - min_date)
    query = {
        "aggs": {
            KEY_RANGES_AGGREGATION: get_fingerprint_aggregation_with_ranges(
                min_date_previous_interval, min_date, max_date
            ),
        },
        "size": 0,
        "query": get_interval_filter_exclude_bots(min_date_previous_interval, max_date)
    }
    return query
