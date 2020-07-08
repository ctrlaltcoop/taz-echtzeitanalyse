from django.utils import timezone

from tazboard.api.queries.common import maybe_add_msid_filter, REFERRER_AGGREGATION_WITH_RANGES, \
    QUERY_FILTER_EXCLUDE_BOTS_IN_INTERVAL
from tazboard.api.queries.constants import KEY_REFERRER_AGGREGATION


def get_referrer_query(min_date, max_date=timezone.now(), msid=None):
    min_date_previous_interval = min_date - (max_date - min_date)
    query = {
        "aggs": {
            KEY_REFERRER_AGGREGATION: REFERRER_AGGREGATION_WITH_RANGES(min_date_previous_interval, min_date, max_date)
        },
        "size": 0,
        "docvalue_fields": [
            {
                "field": "@timestamp",
                "format": "date_time"
            }
        ],
        "query": QUERY_FILTER_EXCLUDE_BOTS_IN_INTERVAL(min_date_previous_interval, max_date)
    }
    query = maybe_add_msid_filter(msid, query)
    return query
