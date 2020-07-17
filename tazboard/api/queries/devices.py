from django.utils import timezone
from tazboard.api.queries.common import maybe_add_msid_filter, get_interval_filter_exclude_bots, get_devices_aggregation
from tazboard.api.queries.constants import KEY_FINGERPRINT_AGGREGATION, KEY_DEVICES_AGGREGATION


def get_devices_query(min_date, max_date=timezone.now(), msid=None):
    query = {
        "aggs": {
            KEY_DEVICES_AGGREGATION: get_devices_aggregation()
        },
        "size": 0,
        "docvalue_fields": [
            {
                "field": "@timestamp",
                "format": "date_time"
            }
        ],
        "query": get_interval_filter_exclude_bots(min_date, max_date)
    }
    query = maybe_add_msid_filter(msid, query)
    return query
