from django.utils import timezone

from tazboard.api.queries.common import maybe_add_msid_filter, get_referrer_aggregation_with_ranges, \
    get_interval_filter_exclude_bots
from tazboard.api.queries.constants import KEY_REFERRER_AGGREGATION


def get_referrer_query(min_date, max_date=timezone.now(), msid=None):
    min_date_previous_interval = min_date - (max_date - min_date)
    query = {
        "aggs": {
            KEY_REFERRER_AGGREGATION: get_referrer_aggregation_with_ranges(
                min_date_previous_interval, min_date, max_date
            )
        },
        "size": 0,
        "docvalue_fields": [
            {
                "field": "@timestamp",
                "format": "date_time"
            }
        ],
        "query": get_interval_filter_exclude_bots(min_date_previous_interval, max_date)
    }
    query = maybe_add_msid_filter(msid, query)
    return query
